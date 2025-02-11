from bs4 import BeautifulSoup
from utils.csv_writer import write_to_csv
 
def extract_bing_data(data, AllData, searchString, searchEngine, page_number):
    soup = BeautifulSoup(data, 'html.parser')
    results = soup.find_all('div', {'class': "news-card newsitem cardcommon"})
 
    for result in results:
        media = result.get('data-author', '')  # Ensure default value
        title = result.get('data-title', '')
        time_span = result.find('span', {'aria-label': True})
        timestamp = time_span.get('aria-label', '') if time_span else ''
        link = result.get('data-url', '')
 
        AllData.append({
            'search_string': searchString,
            'search_engine': searchEngine,
            'title': title,
            'media': media,
            'timestamp': timestamp,
            'link': link,
            'page_number': page_number
        })
 
 
def extract_google_data(data, AllData, searchString, searchEngine, page_number):
    soup = BeautifulSoup(data, 'html.parser')
    sp = soup.find_all('div', {'class': "SoaBEf"})
 
    for s in sp:
        title_tag = s.find('div', {'role': 'heading'})
        title = title_tag.text.strip() if title_tag else ''
 
        link_tag = s.find('a')
        link = link_tag['href'] if link_tag else ''
 
        media_tag = s.find('div', {'class': 'MgUUmf NUnG9d'})
        media = media_tag.text.strip() if media_tag else ''
 
        timestamp_tag = s.find('div', {'class': "OSrXXb rbYSKb LfVVr"})
        timestamp = timestamp_tag.text.strip() if timestamp_tag else ''
 
        AllData.append({
            'search_string': searchString,
            'search_engine': searchEngine,
            'title': title,
            'media': media,
            'timestamp': timestamp,
            'link': link,
            'page_number': page_number
        })
 
 
def extract_yahoo_data(data, AllData, searchString, searchEngine, page_number):
    soup = BeautifulSoup(data, 'html.parser')
    sp = soup.find_all('div', {'class': "dd NewsArticle"})
 
    for s in sp:
        title_tag = s.find('h4', {'class': 's-title fz-20 lh-m fw-500 ls-027 mt-8 mb-2'})
        title = title_tag.text.strip() if title_tag else ''
 
        link_tag = s.find('a')
        link = link_tag['href'] if link_tag else ''
 
        time_tag = s.find('span', {'class': 's-time fz-14 lh-18 fc-dustygray fl-l mr-4'})
        timestamp = time_tag.text.strip() if time_tag else ''
 
        media_tag = s.find('span', {'class': 's-source fw-l'})
        media = media_tag.text.strip() if media_tag else ''
 
        AllData.append({
            'search_string': searchString,
            'search_engine': searchEngine,
            'title': title,
            'media': media,
            'timestamp': timestamp,
            'link': link,
            'page_number': page_number
        })
 