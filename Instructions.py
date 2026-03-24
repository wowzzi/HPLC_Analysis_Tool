instructions_dict = {
    'Quick start essentials (how to):': "This tool is only for .CSV files from the chromeleon software."
                                        "\nThe options from each menu can be accessed by typing the associated number and hitting enter on the keyboard."
                                        "\nIn certain cases you can enter multiple numbers by separating each with a comma e.g. 0,1,2,3,4"
                                        "\nInputs will ignore any letters, spaces or special characters you type in, it only takes the numbers"
                                        "\nLeaving an input blank will generally select all options, or give you an error to re-enter a number(s)"
                                        "\n"
                                        "\nAdvised Workflow: 1. Import new data, 2. Calibrate your data (to generate a linear standard curve), 3. Export data as CSV, 4. Explore overlaying traces"
                                        "\nExporting data to CSV will generate a file with all the peaks detected for each sample and the calibration results aswell as an image for each trace.",
    'How to import data':   "Select menu option: import new data, by typing in the corresponding number"
                            "\nThis should allow you select the folder containing your .CSV HPLC raw data from the system using the file explorer pop-up"
                            "\nThese data files can include your calibration runs and normal sample runs"
                            "\nThis can be repeated as many times as you like to look at different data-sets",
    'How to generate a calibration curve':  "Before calibration you need to have imported data, inclduing the raw CSVs of your calibration runs"
                                            "\nAfter that, select menu option: calibrate, this will ask you which of your files are the calibration runs"
                                            "\nType in all the numbers of the traces which correspond to your calibration runs, separate each number with a comma"
                                            "\nCalibration requires at least 2 files to be selected"
                                            "\nAfter that it will ask you for the molecular weight in Daltons (e.g. Aldolase = 158000 daltons) of each protein 1 by 1"
                                            "\nOnce that is completed all your data will be automatically interpolated off of the linear standard curve generated"
                                            "\nYou can also view the calibration curve by selecting option: show calibration curve",
    'How to: plot data, including overlays':    "So long as some data is imported the options: show calibration curve, show chromatograms, plot an overlay & plot a normalised overlay all work"
                                                "\nShow calibration curve just pops open your cal curve (if present), close it to continue the program"
                                                "\nShow chromatograms will pop open a graph for each trace you have imported into the tool, again close them all to continue the program"
                                                "\nPlot an overlay and plot a normalised overlay are functionally identical (one is normalised signal and the other is not)"
                                                "\nBoth overlay options give you a choice of which traces to place on the graph by choosing the numbers of the traces you want"
                                                "\nSeparate each number by a comma and press enter, it will then ask you if you want to hide annotations you can press enter to use default settings"
                                                "\nThen it will pop open a single interactive graph with all the selected traces overlayed, utilise the tools at the bottom to zoom and move the graph around",
    'How to export to CSV': "Aslong as some data is imported into the tool select the menu option: export all data to CSV"
                            "\nThis will export peak data from samples and calibrators and the actual calibration curve data to CSV in the current output location"
                            "\nIt will also export an image of each trace"
                            "\nYou can change the output location by selecting option: change data export location (on your pc)"
                            "\nThis will then pop-up a file explorer where you can select a new folder location to export the data"
                            "\nThis is important because the export will over-write any existing files with the same names"
                            "\nso ideally create an empty folder to export to each time you export data",
    'Back to main menu': "done"
}