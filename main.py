import asyncio
import json
from pathlib import Path

from Data_Extractions.extraction import extract_bing_data, extract_google_data, extract_yahoo_data
from api.allAPI import fetchData
from utils.csv_writer import load_config, print_config, write_to_csv
 
# Function to collect data (placeholder for actual implementation)
async def Collect_Data(search_engine, seachData, page_number, AllData):
    """
    Collect data from different search engines based on the provided search parameters.

    Args:
        search_engine (str): The search engine to use ("google", "bing", or "yahoo").
        seachData (str): The search query containing company and keyword.
        page_number (int): The page number to scrape.
        AllData (list): The list to append the extracted data to.
    """
    # Determine the URL and extraction function based on the search engine
    if search_engine == "google":
        data = await fetchData(f"https://www.google.com/search?q={seachData}&tbm=nws&start={(page_number - 1) * 10}")
        extract_google_data(data, AllData, seachData, search_engine, page_number)

    elif search_engine == "bing":
        data = await fetchData(f"https://www.bing.com/news/search?q={seachData}&first={(page_number - 1) * 10 + 1}")
        extract_bing_data(data, AllData, seachData, search_engine, page_number)

    elif search_engine == "yahoo":
        data = await fetchData(f"https://news.search.yahoo.com/search?p={seachData}&b={(page_number - 1) * 10 + 1}")
        extract_yahoo_data(data, AllData, seachData, search_engine, page_number)

    
 

# Function to get user input dynamically and store in comp.json
def get_user_input():
    """
    Get user input for companies, keywords, search engines, and the number of pages to scrape.

    Saves the configuration to a JSON file named "config.json".
    """
    # Get company names
    companies = input("Enter company names (comma-separated): ")
    companies = [c.strip() for c in companies.split(",")]
    # Get keywords
    keywords = input("Enter keywords (comma-separated): ")
    keywords = [k.strip() for k in keywords.split(",")]
    # Get search engines
    engines = input("Enter search engines (comma-separated, e.g., Google, Bing): ")
    engines = [e.strip() for e in engines.split(",")]
    # Get the number of pages to scrape
    pages = int(input("Enter the number of pages to scrape: "))

    # Create the configuration dictionary
    config = {
        "companies": companies,
        "keywords": keywords,
        "engine": engines,
        "pages": pages
    }

    # Save the configuration to a JSON file
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)
    print("Configuration saved to comp.json")
 

# Main function to collect data
async def main():
    """
    Main function to collect data.

    Reads the configuration from the "config.json" file,
    creates a dictionary to store the results,
    and then runs the data collection for each search engine
    using asyncio.gather.
    """
    config = load_config()
    all_results = {engine: [] for engine in config["engine"]}
    tasks = []
 
    # Iterate through each company, keyword, and search engine
    # and create a task for each one
    for company in config["companies"]:
        for keyword in config["keywords"]:
            for search_engine in config["engine"]:
                for page in range(1, config["pages"] + 1):
                    # Print status message
                    print(f"Collecting data for {company} with keyword {keyword} on {search_engine}...")
                    # Create a task to collect data and store it in the results dictionary
                    tasks.append(Collect_Data(search_engine, f"{company} {keyword}", page, all_results[search_engine]))
    
    # Run all tasks concurrently
    await asyncio.gather(*tasks)
 
    # Write separate CSV for each search engine
    for engine, data in all_results.items():
        # Write the data to a CSV file
        write_to_csv(data, engine)
 
# Entry point with a switch-case (Python 3.10+)
def main_menu():
    print("1. Run with existing config")
    print("2. Update config and run")
    print("3. Exit")
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