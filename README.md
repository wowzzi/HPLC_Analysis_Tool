# HPLC Analysis Tool
A Python tool for visualising and analysing Chromeleon HPLC CSV export data.

# Description
This tool loads CSV data exported from Thermo Chromeleon HPLC software
and generates chromatogram visualisations with basic analysis features.

It was created to make quick inspection of HPLC runs easier without
opening the full Chromeleon software suite.

# Features
- Load Chromeleon CSV exports
- Plot chromatograms
- Peak detection and integration
- Interpolate protein molecular weight for SEC data via in-built calibration loop
- Export data to CSV

# Installation
git clone https://github.com/wowzzi/HPLC_Analysis_Tool.git \n
cd HPLC_Analysis_Tool \n
pip install -r requirements.txt

# Dependencies
 - pandas
 - matplotlib
 - scipy
 - numpy

# How to use
python main.py
1. Launch program
2. Type 0 to select a folder containing .CSV files from a chromeleon HPLC run.
3. Type the various numbers from the menu to analyse/visualize/export the data.
<img width="821" height="351" alt="Main_menu" src="https://github.com/user-attachments/assets/02b06348-8a08-4059-b2de-73061b1d8540" />

Example data import

<img width="355" height="382" alt="Data_import" src="https://github.com/user-attachments/assets/db18dfbc-8a34-4cc1-8a68-8976e442bfd2" />



# Example outputs
<img width="1559" height="811" alt="Ferritin_chromatogram" src="https://github.com/user-attachments/assets/017a34aa-1ef7-4616-b337-6b552477698a" />
Size-exclusion chromatography calibration
<img width="916" height="641" alt="Linear_Calibration" src="https://github.com/user-attachments/assets/32f338ed-0768-46d4-9abc-6a7b7ac87e7c" />
Chromatogram overlay
<img width="1556" height="803" alt="Overlay" src="https://github.com/user-attachments/assets/f8a13e41-53fd-485d-a08f-775afe0e8268" />
Data output to CSV and PNG
<img width="1471" height="711" alt="CSV_output_example" src="https://github.com/user-attachments/assets/f8129b8a-7320-4279-8be1-9660f74cb37b" />
<img width="939" height="431" alt="Data_output" src="https://github.com/user-attachments/assets/63cb1639-f941-4821-9daf-dc57e921a14d" />


