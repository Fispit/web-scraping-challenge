#Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
# Set up Splinter

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit visitcostarica.herokuapp.com
    url = "https://redplanetscience.com/"
    browser.visit(url)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    #finding the data
    article_title = soup.find('div', class_='content_title').text
    article_desc = soup.find('div', class_='article_teaser_body').text    
    #visint the url for mars image
    url = "https://spaceimages-mars.com/"
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")
    imageloc=soup.find('img',class_="headerimage")
    relative_image_path =imageloc["src"]
    featured_image_url = url + relative_image_path

    url="http://galaxyfacts-mars.com"
    marstable=pd.read_html(url)[1]
    marstable=pd.DataFrame(marstable)
    marstable=marstable.rename(columns={0:"Property",1:"Value"})
    marstable=marstable.set_index("Property")
    marstable.to_html("marstable.html")
    marstable_html=marstable.to_html("marstable.html")

    url = "https://marshemispheres.com/"
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")

    urllist=[]
    hemisphere_text=[]
    hemisphere_desc = soup.find_all('div', class_='description')

    for x in range(0,4):
        name=hemisphere_desc[x].find("h3").text.split(" ")
        listname=name[0]+" "+name[1]
        if x==2 or x==3:
            listname=name[0]+" "+name[1]+" "+name[2]
        hemisphere_text.append(listname)
        relative=hemisphere_desc[x].find("a")["href"]
        imagepage=url+relative
        urllist.append(imagepage)
        

    fullimageurls=[]
    for imgurl in urllist:
        browser.visit(imgurl)
        html = browser.html
        soup = bs(html, "html.parser")
        relative= soup.find_all('div', class_='downloads')[0].find_all("li")[1].find("a")["href"]
        totalurl=url+relative
        fullimageurls.append(totalurl)

    hemisphere_image_urls=[] 
    for x in range(0,len(hemisphere_text)):
        hemisphere_image_urls.append({"title":hemisphere_text[x],"img_url":fullimageurls[x]})
        
    returndict={
        "news":{"title":article_title,"description":article_desc},
        "spaceimg":featured_image_url,
        "marsdata":marstable_html,
        "hemispheres":hemisphere_image_urls
    }
    browser.quit()

    return returndict

