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
git clone https://github.com/wowzzi/HPLC_Analysis_Tool.git
cd HPLC_Analysis_Tool
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


# Example outputs
