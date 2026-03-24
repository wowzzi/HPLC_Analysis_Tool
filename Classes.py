import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
from scipy.stats import linregress as lregress
import Utils as u
import settings as sett
#from hplc.quant import Chromatogram

class raw_file:
    def __init__(self, input_df, input_name = "", file_path = r""):
        self.path = file_path
        self.name = input_name
        # initialising data structures - dataframe cleaning & calculations
        self.df = input_df
        self.df = self.df.drop(['Step (s)'], axis=1)
        self.min = self.df['Value (mAU)'].min()
        if self.min < 2 and self.min > -2:
            self.df['Value (mAU)'] = self.df['Value (mAU)'] - self.min # adjust points up if they are negative
        
        self.x = self.df['Time (min)']
        self.y = self.df['Value (mAU)']

        # normalisation params
        self.max_y = self.df['Value (mAU)'].max()
        self.norm_y = self.df['Value (mAU)'] / self.max_y
        self.max_uv_ret_time = self.df[(self.df['Value (mAU)'] == self.max_y)]
        self.max_uv_ret_time.index = [self.name]
        self.interpolated_mw = []

        # dy/dx
        self.df['dx'] = self.df['Time (min)'].diff(periods = 10)
        self.df['dy'] = self.df['Value (mAU)'].diff(periods = 10)
        self.df['dy/dx'] = self.df['dy'] / self.df['dx']
        self.df['smoothed slope'] = self.df['dy/dx'].rolling(window = 100, center = True).mean()
        # slope of slope
        self.df['diff slope'] = self.df['smoothed slope'].diff(periods = 10)
        self.df['slope of slope'] = self.df['diff slope'] / self.df['dx']
        self.df['smoothed slope of slope'] = self.df['slope of slope'].rolling(window = 100, center = True).mean()
        # calculate local min & max across the signal
        self.df['slope local maxis'] = self.df['smoothed slope'].rolling(window = 50, center = True).max()
        self.df['slope local min'] = self.df['smoothed slope'].rolling(window = 50, center = True).min()

        # DETECT PEAKS
        self.troughs = []
        self.trough_heights = []
        self.areas = []
        self.relative_areas = []
        self.detect_peaks()

    def detect_peaks(self):
        self.areas.clear()
        if hasattr(self, 'peaks'):
            delattr(self, 'peaks')
        # settings
        height_setting = sett.settings_dict['minimum peak height']
        distance_setting = sett.settings_dict['minimum indices between peaks']
        prominence_setting = sett.settings_dict['minimum peak prominence']
        #scipy find_peaks() func
        self.peaks, _ = find_peaks(self.y, height=height_setting, distance=distance_setting, prominence=prominence_setting)   # peaks = a numpy ndarray
        self.peak_windows = self.define_peaks() # my own integration windows method
        for p in self.peak_windows: # p = the index of the peak
            start = p[0]
            end = p[1]
            area = np.trapezoid(self.y[start:end], self.x[start:end]) # calculates AUC
            self.areas.append(area)
        # Relative areas
        total_area = np.sum(self.areas)
        self.relative_areas = self.areas / total_area

    def __str__(self):
        return self.name

    def plot(self):
        self.fig, self.axs = plt.subplots()
        self.fig.set_size_inches(12,8)
        self.axs.plot(self.x, self.y, label="HPLC UV Signal")
        self.axs.plot(self.x, np.zeros(len(self.x)), ls = '--', alpha = 0.35, label = "y = 0")
        self.axs.set_xlabel("Retention Time (min)")
        self.axs.set_ylabel("A280 (mAU)")
        self.fig.suptitle(f'{self.name}') 
        self.axs.plot(self.x[self.peaks], self.y[self.peaks], "rx", label="Detected Peaks")
        for i, p in enumerate(self.peaks):
            plt.annotate(f"{self.relative_areas[i] * 100:.1f}%",
                            (self.x[p], self.y[p]),
                            textcoords="offset points",
                            xytext=(0, 8),
                            ha='center')
        for i, p in enumerate(self.peak_windows):
            x_vals = self.x[p[0]:p[1]]
            y1_vals = np.zeros(len(x_vals))
            y2_vals = self.y[p[0]:p[1]]
            self.axs.fill_between(x_vals, y1_vals, y2_vals, alpha = 0.5, label = f"peak {i+1}")        
        self.axs.legend()

    def print_peaks(self):
        for peak in self.peaks:
            print(peak)

    def output_data(self):
        peak_dict = {}
        for n, peak in enumerate(self.peaks):
            try:
                iterpolated = self.interpolated_mw[n]
            except:
                iterpolated = np.nan
            peak_dict[f"peak {n+1} Retention Time (min)"] = self.x[peak]
            peak_dict[f"peak {n+1} Peak Height (mAU)"] = self.y[peak]
            peak_dict[f"peak {n+1} Interpolated Molecular Weight (KDa)"] = iterpolated
            peak_dict[f"peak {n+1} Peak Area"] = self.areas[n]
            peak_dict[f"peak {n+1} Relative Area (%)"] = (self.relative_areas[n])*100
        return peak_dict
    
    def define_peaks(self):
        peak_windows = []
        #settings
        peak_slope_factor = sett.settings_dict['integration window factor']
        peak_slope_floor = sett.settings_dict['slope end cut-off value (mAU/min)']
        join_peaks_dist = sett.settings_dict['connect peaks distance']
        for peak in self.peaks:
            #start of peak logic
            reversed_df = self.df[peak:0:-1]
            stage = 1
            start_index = np.nan
            end_index = np.nan
            for row in reversed_df.iterrows():
                if stage == 1:
                    if row[1]['smoothed slope of slope'] >= 0:
                        slope_apex = row[1]['slope local maxis']
                        stage = 2
                if stage == 2:
                    if row[1]['smoothed slope'] < min(peak_slope_factor*slope_apex, peak_slope_floor):
                        start_index = row[0]
                        break

            #End of peak logic
            truncated_df = self.df[peak:len(self.df)]
            max_index = len(self.df)-1
            stage = 1
            for row in truncated_df.iterrows():
                if row[0] == max_index:
                    end_index = row[0]
                    break
                if stage == 1:
                    if row[1]['smoothed slope of slope'] >= 0:
                        slope_min = row[1]['slope local min']
                        stage = 2
                if stage == 2:
                    if row[1]['smoothed slope'] > max(peak_slope_factor*slope_min, -1*(peak_slope_floor)):
                        end_index = row[0]
                        break
            peak_windows.append([start_index, end_index])
        # checking that the end of one peak doesn't overlap with the start of the next peak
        for n, item in enumerate(peak_windows): 
            if n != 0:
                #not first iteration
                current_start = item[0]
                if current_start < previous[1] or abs(current_start - previous[1]) < join_peaks_dist:
                    #take average
                    mid_point = int(round((current_start + previous[1])/2))
                    #modify current start
                    item[0] = mid_point
                    #modify previous
                    previous[1] = mid_point
                    
            previous = item
        return peak_windows


class calibration_data:
    def __init__(self, data_input = []):
        self.recalibrate(data_input = data_input)
        self.name = "Calibration Curve"

    def recalibrate(self, data_input = []):
        self.data_sets = u.select_item_from_list(input_list = data_input, instruction = "Select the files which make up YOUR calibration curve" \
        "\nselect multiple by typing each number separated by a sigular comma, e.g. 1,2,3") # these are class objects from raw data
        data_frames = [raw_data.max_uv_ret_time.copy() for raw_data in self.data_sets]
        self.df = pd.concat(data_frames)
        for row in self.df.iterrows():
            while True:
                user_input = input(f"Enter the molecular weight in Daltons for {row[0]}: ").strip()
                user_input = u.numeric_only(user_input)
                try:
                    self.df.at[row[0], 'molecular weight'] = float(user_input)
                    break
                except:
                    print("error: type a valid number, don't leave blank")
                    continue
        
        self.df['log molecular weight'] = np.log10(self.df['molecular weight'])
        self.df = self.df.sort_values(by=['log molecular weight'], ascending=False)
        self.x = self.df['Time (min)']
        self.y = self.df['log molecular weight']
        self.equation = lregress(self.x, self.y)


    def plot(self):
        self.fig, self.axs = plt.subplots()
        self.fig.set_size_inches(12,8)
        self.axs.plot(self.x, self.y, 'o', label="Calibration Proteins")
        self.axs.plot(self.x, self.equation.intercept + self.equation.slope * self.x, label = "Linear line of best fit")
        self.axs.set_xlabel("Retention Time (min)")
        self.axs.set_ylabel("Log(MW)")
        self.fig.suptitle("Calibration Curve") 
        self.axs.legend()

    
    def interpolate(self, x_input = 0):
        self.fx = np.poly1d([self.equation.slope, self.equation.intercept])
        return (10 ** self.fx(x_input))/1000
    
    
    def report(self):
        print(f"Equation of the line: y = {self.equation.slope:.3f}x + {self.equation.intercept:.3f} \n R2 = {self.equation.rvalue:.3f}")
