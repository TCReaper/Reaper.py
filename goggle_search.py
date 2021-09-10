import urllib.request
from bs4 import BeautifulSoup as BS

def goggle_search(url):
    req = urllib.request.Request(
        url,
        data=None, 
        headers={
        
        # HEADERS USED TO MASK 'BOT' IDENTITY --> ALLOWS WEB SCRAPING

            'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393'
        }
    )
    r = urllib.request.urlopen(req)
    text = r.read().decode('utf-8')

    # WRITE TO TEXTFILE searchResults FOR DEBUGGING
    file = open('searchResults.txt','w')
    text2 = text.encode('utf-8')
    file.write(url+'\n\n\n'+str(text2))
    file.close()

    return text



def goggle_search_2(url):
    html = urllib.urlopen(URL).read()

    soup = BS(html)
    
    file = open('searchResults.txt','w')
    
    file.write(url+'\n\n\n'+str(soup.findAll(tag_name).get_text()))
    
    file.close()
    
