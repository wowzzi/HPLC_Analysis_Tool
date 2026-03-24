import matplotlib.pyplot as plt
import Utils as u
import Classes as cla
import Instructions as ins


data = []
current_calibration = None
output_directory = u.get_base_dir()

def print_files():
    for item in data:
        print(item.path)
    input("press enter to continue")


def end_script():
    quit()


def read_instructions():
    while True:
        print("\n", "~"*100)
        key = u.select_a_dict_key(input_dict = ins.instructions_dict)
        if key == "Back to main menu":
            break
        print("\n", "~"*100)
        print(ins.instructions_dict[key])
        input("press enter to continue")


def change_output_dir():
    global output_directory
    new_dir = u.select_directory_gui()
    if new_dir is None or new_dir == "":
        return
    else:
        output_directory = new_dir


def plot_raw_data():
    for data_object in data:
        data_object.plot()
    plt.show()


def plot_normalised():
    plot_overlay(normalised = True)


def plot_overlay(normalised = False):
    chromatograms = u.select_item_from_list(input_list = data, instruction="" \
                                            "Type the numbers corresponding to the chromatograms you want to overlay" \
                                            "\nSeparate each number with a comma" \
                                            "\nLeaving blank will overlay everything")
    dont_annotate_peaks = u.get_binary_input(question = "do you want to hide peak annotations?")
    if len(chromatograms) < 1:
        print("import data first")
        return
    max_vals = [item.max_y for item in chromatograms]
    overall_max = max(max_vals)
    for data_obj in chromatograms:
        x = data_obj.x
        if normalised:
            y = (data_obj.norm_y)*overall_max
        else:
            y = data_obj.y
        plt.plot(x, y, label = data_obj.name)
        plt.plot(x[data_obj.peaks], y[data_obj.peaks], "rx")
        if not dont_annotate_peaks:
            for n, peak in enumerate(data_obj.peaks):
                if current_calibration is not None:
                    plt.annotate(f"{data_obj.interpolated_mw[n]:.1f}KDa",
                                (x[peak], y[peak]),
                                textcoords="offset points",
                                xytext=(0, 8),
                                ha='center')
                else:
                    plt.annotate(f"{x[peak]:.1f}min",
                    (x[peak], y[peak]),
                    textcoords="offset points",
                    xytext=(0, 8),
                    ha='center')
    plt.legend()
    plt.xlabel("Retention Time (min)")
    if normalised:
        plt.ylabel("Normalised signal")
    else:
        plt.ylabel("A280 (mAU)")
    plt.show()


def export_data():
    if len(data) < 1:
        print("no data to export")
        return
    all_peak_data = {}
    for data_obj in data:
        all_peak_data[data_obj.name] = data_obj.output_data()
        data_obj.plot()
        png_output = rf"{output_directory}/{data_obj.name}.png"
        data_obj.fig.savefig(fname = png_output)
    png_output = rf"{output_directory}/Calibration curve.png"
    if current_calibration is not None:
        current_calibration.plot()
        current_calibration.fig.savefig(fname = png_output)
    plt.close(fig = 'all')
    temp_df = u.convert_dict_to_df(all_peak_data)
    file_output = rf"{output_directory}/HPLC tool output.csv"
    temp_df.to_csv(file_output, float_format = "%.4f")
    if current_calibration is not None:
        with open(file_output, "a") as f:
            f.write("\nCalibration values")
        current_calibration.df.to_csv(file_output, float_format = "%.4f", mode = 'a')
        with open(file_output, "a") as f:
            f.write("\n,slope,intercept")
            f.write(f"\nLOBF equation:, {current_calibration.equation.slope:.6f},{current_calibration.equation.intercept:.6f}")
    print(f"Success! CSV raw data exported to: {output_directory}\nReturning to main")
    input("press enter to continue")


def run_calibration(data_input = data):
    global current_calibration
    if len(data) < 2:
        print("need more files to establish calibration curve, try the import data option first!")
        return
    if current_calibration is None:
        current_calibration = cla.calibration_data(data_input)
    else:
        current_calibration.recalibrate(data_input)
    #interpolate off of the new calibration curve
    for data_object in data:
        data_object.interpolated_mw.clear()
        for peak in data_object.peaks:
            peak_x = data_object.x[peak]
            data_object.interpolated_mw.append(current_calibration.interpolate(x_input = peak_x))


def show_cal_curve():
    if current_calibration is None:
        print("calibration curve not yet established!")
        return
    current_calibration.report()
    current_calibration.plot()
    plt.show()


def import_new_data(): # this takes the spectra dict as parameter and mutates it to take new data.
    folder_directory = u.select_directory_gui()
    data.clear() # clear the old directory spectra out
    new_data = u.load_data_from_path(path = folder_directory) # load new data
    data.extend(new_data) # mutate the data list to contain the new data.
    if current_calibration is not None:
        for data_object in data:
            data_object.interpolated_mw.clear()
            for peak in data_object.peaks:
                peak_x = data_object.x[peak]
                data_object.interpolated_mw.append(current_calibration.interpolate(x_input = peak_x))


def change_settings():
    if u.update_settings():
        for data_object in data:
            data_object.detect_peaks()
        print("peaks and integration windows have been re-calculated with your updated settings")
        input("press enter to continue")


 # menu options in terminal, prints upon running script
main_menu_dict = {
    'import new data': import_new_data,
    'calibrate': run_calibration,
    'show calibration curve': show_cal_curve,
    'show chromatograms': plot_raw_data,
    'plot an overlay': plot_overlay,
    'plot a normalised overlay': plot_normalised,
    'change data export location (on your pc)': change_output_dir,
    'export all data to CSV': export_data,
    'what files am I currently working with?': print_files,
    'instructions': read_instructions,
    'settings': change_settings,
    'quit': end_script
}


def menu_loop():
    while True:
        print("\n")
        print("*"*100)
        print("Main Menu - type a number to select an option!")
        print(f"raw data will currently be output to {output_directory}")
        chosen_action = u.select_a_dict_key(main_menu_dict)
        function_call = main_menu_dict[chosen_action]
        function_call()


if __name__ == '__main__':
    menu_loop()