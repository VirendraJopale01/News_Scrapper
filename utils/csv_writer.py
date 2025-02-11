import csv,os
import json
import pandas as pd
from pathlib import Path

def write_to_csv(AllData, search_engine):
    if not AllData:
        print(f"No data collected for {search_engine}. Skipping CSV write.")
        return
    
    filename = f"results_{search_engine}.csv"
    
    # Dynamically determine field names
    keys = AllData[0].keys()
    # Update path here for your system
    folder_path = os.path.join(os.getcwd(), 'Data')

    # Ensure the 'markdown' folder exists, create if it doesn't
    os.makedirs(folder_path, exist_ok=True)

    # Complete path of markdown file
    complete_path = os.path.join(folder_path, filename)
    with open(complete_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(AllData)
 
    print(f"Results saved to {filename}")

def read_csv():
    # with open('articles.csv', 'a') as file:
    #     return file.read()
    return pd.read_csv('articles.csv')


def load_config():
    config_path = Path("config.json")
    if not config_path.exists():
        print("Configuration file not found! Creating one...")
    with open(config_path, "r") as f:
        return json.load(f)

def print_config(): 
    config = load_config()
    print("Configuration:")
    for key, value in config.items():
        print(f"{key}: {value}")