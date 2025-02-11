

from urllib.parse import quote
import aiohttp


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.3"

 

def get_search_url(searchEngine, seachData, page):
    
    if searchEngine == "google":
        return f"https://www.google.com/search?q={seachData}&tbm=nws&start={(page - 1) * 10}"
    elif searchEngine == "bing":
        return f"https://www.bing.com/news/search?q={seachData}&first={(page - 1) * 10 + 1}"
    elif searchEngine == "yahoo":
        return f"https://news.search.yahoo.com/search?p={seachData}&b={(page - 1) * 10 + 1}"
    
 
 
#  fetching the url
async def fetchData(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers={"User-Agent": USER_AGENT},timeout=25) as response:
            dat=await response.text()
            # print(dat)
            return dat
              
