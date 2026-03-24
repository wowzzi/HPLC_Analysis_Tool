import pandas as pd
import glob
import tkinter as tk
from tkinter import filedialog
import Classes as cla
import sys
from pathlib import Path
import numpy as np
import settings as sett


def get_base_dir():
    if getattr(sys, "frozen", False):
        #running as exe
        BASE_DIR = Path(sys.executable).resolve().parent
    else:
        #running as script
        BASE_DIR = Path(__file__).resolve().parent
    return BASE_DIR


def convert_dict_to_df(input_dict = {}):
    return pd.DataFrame.from_dict(input_dict, orient = 'index')


def get_binary_input(question = ""):
    output = False
    print(question)
    user_input = input("type 0 for no, type 1 for yes: ")
    if user_input == "1":
        output = True
    return output


 # mostly front-end interface logic/functions
def extract_data(path = None):
    if path is None:
        print("returned none")
        return []
    try:
        csv_path_list = glob.glob(path) # returns list of paths
    except:
        print("returned none - except statment")
        return []
    number_of_files = len(csv_path_list)
    print(f"we found {number_of_files} suitable files.")
    if number_of_files == 0:
        return []
    new_data = []
    i = 0
    errors = []
    for path in csv_path_list:
        i += 1
        file_name = path.split("\\")[-1] # take the last bit of the path
        print(f"processing {file_name} file {i}/{number_of_files}.")
        file_name = file_name.rsplit(".", 1)[0] # get rid of the file extension
        try:
            new_data.append(cla.raw_file(input_df = pd.read_csv(path, skiprows=42), input_name = file_name, file_path = path)) # read csv into a dataframe & save as raw_file object
        except:
            errors.append(str(path))
    if len(errors) > 0:
        print("\nThe following files could not be processed:")
        for error in errors:
            print(error)
    return new_data


def select_directory_gui():
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    directory = filedialog.askdirectory(title="select a folder")
    root.destroy()
    return directory


def load_data_from_path(path = ""):
    path_with_extension = path + r"/*.csv"
    data_dict = extract_data(path = path_with_extension)
    return data_dict


def numeric_only(input_string = ""):
    return "".join([char for char in input_string if char.isnumeric()])


def select_a_dict_key(input_dict = {}, show_key_values = False):
    while True:
        temp_dict = {}
        for n, key in enumerate(input_dict.keys()):
            if show_key_values:
                print(f"{n}: {key} = {input_dict[key]}")
            else:
                print(f"{n}: {key}")
            temp_dict[str(n)] = key
        
        user_selection = input("select an item from the list: ").strip()
        user_selection = numeric_only(input_string = user_selection)
        try:
            converted_key = temp_dict[user_selection]
        except:
            print("key error, make sure you type one of the numbers")
            continue
        break
    return converted_key


def select_item_from_list(input_list = [], instruction = ""):
    print("-"*100)
    print(instruction)
    for n, item in enumerate(input_list):
        print(f"{n}: {item}")
    user_input = input("type the desired number(s) from the list: ").strip()
    user_input = user_input.split(",")
    user_input = [numeric_only(item) for item in user_input]
    if len(user_input) ==1 and user_input[0] == '':
        user_input = list(range(len(input_list)))
    output = []
    error = []
    for n in user_input:
        try:
            output.append(input_list[int(n)])
        except:
            error.append(f"your input: {n} failed, make sure its one of the numbers from the list")
    if len(error) > 0:
        for each_error in error:
            print(each_error)
    return output


data_types = ['str', 'int', 'float', 'tuple', 'set', 'list', 'dict']
def get_data_type(input_data):
    for data_type in data_types:
        if data_type in str(type(input_data)):
            return data_type
    return


def update_settings():
    settings_changed = False
    while True:
        print("\n", "-"*100, "\nSettings menu...")
        setting_key = select_a_dict_key(input_dict = sett.settings_dict, show_key_values = True)
        if setting_key == 'back to main menu':
            return settings_changed
        current_value = sett.settings_dict[setting_key]
        current_type = get_data_type(input_data = current_value)
        print("")
        print(sett.setting_explained[setting_key])
        print(f"current value of {setting_key} = {current_value}")
        while True:
            new_value = input("input your new value: ").strip()
            if new_value == "":
                break
            if current_type == "int":
                try:
                    new_value = int(new_value)
                except:
                    print("error make sure you input an integer value (no decimals)")
                    print("")
                    continue
            elif current_type == "float":
                try:
                    new_value = float(new_value)
                except:
                    print("error make sure you input a numeric value")
                    print("")
                    continue
            sett.settings_dict[setting_key] = new_value
            settings_changed = True
            print("")
            break