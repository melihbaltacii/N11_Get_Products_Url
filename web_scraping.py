from bs4 import BeautifulSoup as bs
import requests
import json
from time import sleep


data={}
brandUrls=[]


def html(categoryUrl):
  for attempt in range(10):
    try:
      headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}
      #proxies = {'http': 'http://10.10.1.10:3128','https': 'http://10.10.1.10:1080'}
      r=requests.get(categoryUrl,headers = headers)#,proxies=proxies
      if r.status_code==200:
        getHtml=bs(r.content,"lxml") 
        return getHtml
    except:
      sleep(60) 
      continue
  
    
    
    
    
    
  
    



def brand(soup,categoryUrl):
  try:
    brandsInput=soup.find_all("input", attrs={"data-is":"m"})
    for brandName in brandsInput:
      brandUrlDiv=brandName.parent
            
      if brandUrlDiv.find("a"):
        brandUrl=brandUrlDiv.find("a")["href"]
        brandUrls.append(brandUrl)
                
      else:
        brandUrl=brandName.get("data-iv")
        brandUrl=categoryUrl+"?m="+brandUrl
        brandUrls.append(brandUrl)
        
  except:
    print("Not Found Page in Brand")
    return " "
        
    
    
        
def productCount(soup):
  countDiv=soup.find("div", attrs={"class":"resultText"})
  count=countDiv.find("strong").string
  count = count.replace(',', '')
  count = count.replace('.', '')      
        
       
  pageMod=int(count)%28     
  if pageMod==0:
    return (int(count)//28)+1  
  else:
    return (int(count)//28)+2
        
     
    
    


def productsList(categoryUrl,soup,categoryName):
  productsAll=soup.find("div",attrs={'id':'view'})
  products=productsAll.find_all("div", attrs={"class":"pro"})
    
  for productsUrl in products:
    productsUrl=productsUrl.find("a")["href"]
    print(productsUrl)
    data[categoryUrl].append({'products': productsUrl, })
    with open(categoryName+'.json', 'w', encoding='utf-8') as f:
      json.dump(data, f, ensure_ascii=False)


categoryUrl=input("Please enter Category Url= ")
categoryUrlSplint=categoryUrl.split("/")
ArrayCount=len(categoryUrlSplint)
categoryName=categoryUrlSplint[ArrayCount-1]


soup=html(categoryUrl)
brandReturn=brand(soup,categoryUrl)

if brandReturn==" ":
  with open("NoBrandUrls.txt", "a") as file_object:
    file_object.write(categoryUrl)
    file_object.write("\n")
    
else:
  data[categoryUrl] = []
  
  for url in brandUrls:
    soup=html(url)
    pageCount=productCount(soup)
            
            
    for page in range(1,pageCount):
      pageSoup=html(url+("&pg=")+str(page))
      productsUrl=productsList(categoryUrl,pageSoup,categoryName)
      sleep(10)



