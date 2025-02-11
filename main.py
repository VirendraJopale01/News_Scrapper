import asyncio
import json
from pathlib import Path

from Data_Extractions.extraction import extract_bing_data, extract_google_data, extract_yahoo_data
from api.allAPI import fetchData
from utils.csv_writer import load_config, print_config, write_to_csv
 
# Function to collect data (placeholder for actual implementation)
async def Collect_Data(search_engine, seachData, page_number, AllData):
    # Simulating data collection
    if search_engine == "google":
        data=await fetchData(f"https://www.google.com/search?q={seachData}&tbm=nws&start={(page_number - 1) * 10}")
        extracted_data = extract_google_data(data,AllData, seachData, search_engine, page_number)
        
    elif search_engine == "bing":
        data=await fetchData(f"https://www.bing.com/news/search?q={seachData}&first={(page_number - 1) * 10 + 1}")
        extracted_data = extract_bing_data(data,AllData, seachData, search_engine, page_number)
    elif search_engine == "yahoo":
        data=await fetchData(f"https://news.search.yahoo.com/search?p={seachData}&b={(page_number - 1) * 10 + 1}")
        extracted_data = extract_yahoo_data(data,AllData, seachData, search_engine, page_number)
   
    if isinstance(extracted_data, dict):
        AllData.append(extracted_data)
    
    
    await asyncio.sleep(1)
 

# Function to get user input dynamically and store in comp.json
def get_user_input():
    companies = input("Enter company names (comma-separated): ").split(",")
    keywords = input("Enter keywords (comma-separated): ").split(",")
    engines = input("Enter search engines (comma-separated, e.g., Google, Bing): ").split(",")
    pages = int(input("Enter the number of pages to scrape: "))
 
    config = {
        "companies": [c.strip() for c in companies],
        "keywords": [k.strip() for k in keywords],
        "engine": [e.strip() for e in engines],
        "pages": pages
    }
 
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)
    print("Configuration saved to comp.json")
 

# Main function to collect data
async def main():
    config = load_config()
    all_results = {engine: [] for engine in config["engine"]}
    tasks = []
 
    for company in config["companies"]:
        for keyword in config["keywords"]:
            for search_engine in config["engine"]:
                for page in range(1, config["pages"] + 1):
                    print(f"Collecting data for {company} with keyword {keyword} on {search_engine}...")
                    tasks.append(Collect_Data(search_engine, f"{company} {keyword}", page, all_results[search_engine]))
 
    await asyncio.gather(*tasks)
 
    # Write separate CSV for each search engine
    for engine, data in all_results.items():
        write_to_csv(data, engine)
 
# Entry point with a switch-case (Python 3.10+)
def main_menu():
    print("1. Run with existing config")
    print("2. Update config and run")
    choice = input("Choose an option (1/2): ")
 
    match choice:
        case "1":
            print_config()
            key=int(input("Press 1 agiain to continue : "))
            if key==1:
                asyncio.run(main())
            
        case "2":
            get_user_input()
            asyncio.run(main())
        case _:
            print("Invalid choice. Exiting.")
            
# Run the script
if __name__ == "__main__":
    main_menu()