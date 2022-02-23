import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd

baseurl = "https://www.manomano.fr/perceuse-1146"

#initiate data storage
ProductUrl = []
Title = []
Brand = []
Price = []
Ratings = []
NumberofRatings = []

#Go through the first three pages
for page in range(1,4):
    results = requests.get(f'https://www.manomano.fr/perceuse-1146?page={page}')
    soup = BeautifulSoup(results.content, "html.parser")
    drill_div = soup.find_all('div', {'class':'ProductsLayout_root__X32CA Products_root__bnqZC ListingLayout_products__B_vFj'})
    
#Find the content Needed for each drill
    for container in drill_div:
        #Fetch the url of the product
        for link in container.find_all('a', href=True):
            #Fetch every link that is a product link
            if link['href'][:3] != '/p/':
                continue
            print(baseurl + link['href'])
            ProductUrl.append(baseurl+ link['href'])    
               
        #Fetch the title of the product
            productname = link.find('div', class_='root_7414a3e6').text if link.find('div', class_='root_7414a3e6') else '-'
            print(productname)
            Title.append(productname)
            
        #Fetch the brand of the product
            brandname = link.find('img', class_='brand_a2b14580')['alt'] if link.find('img', class_='brand_a2b14580') else 'Unknown'
            brandname = brandname.split('"')[1::2][0] if brandname != 'Unknown' else brandname
            print("Brand " +brandname)
            Brand.append(brandname)
            
        #Fetch the price of the product
            price = link.find('span', class_='root_e38b4538 euro_e38b4538 root_03dd2260 main_56d2c1d7').text
            price = "€" + price.replace("€", ".")
            print("price " +price)              
            Price.append(price)
            
        #Fetch the ratings of the product
            ratingscore = link.find('span', class_='stars_00ec077c')['aria-label'] if link.find('span', class_='stars_00ec077c') else 'No Ratings'
            print("rating " +ratingscore)
            Ratings.append(ratingscore)
            
        #Fetch the number of ratings
            numofratings = "0"
            numofratings_div = link.find_all('div', class_='root_130921a2 small_130921a2 regular_130921a2 primaryDark_130921a2')
            if numofratings_div and numofratings_div[-1].text.isnumeric():
                numofratings = numofratings_div[-1].text
            
            print("numofrating " +numofratings)
            NumberofRatings.append(numofratings)
    
#Create pandas dataframe        
drills = pd.DataFrame({
'ProductUrl': ProductUrl,
'ProductName': Title,
'Brand': Brand,
'Price': Price,
'Ratings': Ratings,
'NumberofRatings': NumberofRatings,
})

#Add dataframe to csv file named
drills.to_csv('drills.csv')
print("all done!!")
