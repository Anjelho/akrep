import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
'''
This script will scrap all sub-categories from trustpilot and will
order the TOP-Magazines for each category by filtering on
500+ reviews rating & under 18 Months

'''

url= "https://uk.trustpilot.com/categories"
mainurl= "https://uk.trustpilot.com"
file = 'resources/import.csv'

r = requests.get(url)
f = open(file, 'w', encoding="utf-8")

soup = BeautifulSoup(r.content, "html.parser")
cats = [x.h3.text for x in soup.findAll('div', {"class":"subCategory___BRUDy" })]
subcats = [x.a.span.text for x in soup.findAll('div', {"class":"subCategoryItem___3ksKz" })]
subcatlinks = [x.a.get('href') for x in soup.findAll('div', {"class":"subCategoryItem___3ksKz" })]
shops = {}
for i in soup.findAll('div', {"class":"subCategory___BRUDy" }):
    for item in i.findAll("div",{"class":"subCategoryItem___3ksKz"}):
        subcat = item.a.span.text
        #print(subcat)
        links = item.a.get('href')
        burl = mainurl+links+'?numberofreviews=500&timeperiod=18'
        content = requests.get(burl)
        soup2 = BeautifulSoup(content.content,'html.parser')
        reviewlinks = soup2.findAll("div",{"class":"businessUnitCardsContainer___1Ez9Z"})
        for link in reviewlinks:
            revlink = mainurl+link.a.get('href')
            creview = requests.get(revlink)
            soup3 = BeautifulSoup(creview.content,'html.parser')
            content = soup3.find("script", type='application/ld+json').text.strip()
            stripstart = content.find('[')+1
            stripend = content.find('\"review\"')-1
            jsondata = content[stripstart:stripend]+'}'
            dat = json.loads(jsondata)
           #print(dat)
            print('---------------------')
            print('Main Category : '+i.h3.text)
            print('Sub Category :'+subcat)
            if 'name' in dat.keys():
                print('Shop-Name :'+dat['name'])
            else:
                dat['name'] = ''
            if 'email' in dat.keys():
                print('email :'+dat['email'])
            else:
                dat['email'] = ''
            if 'telephone' in dat.keys():
                print('telephone : '+dat['telephone'])
            else:
                dat['telephone'] = ''
            if '@type' in dat.keys():
                print('Address Type : '+dat['@type'])
            else:
                dat['@type'] = ''
            if 'streetAddress' in dat['address']:
                print('Address : '+dat['address']['streetAddress'])
            else:
                dat['address']['streetAddress'] = ''
            if 'addressLocality' in dat['address']:
                print('Address Locality :'+dat['address']['addressLocality'])
            else:
                dat['address']['addressLocality'] = ''
            if 'postalCode' in dat['address']:
                print('Postal Code : '+dat['address']['postalCode'])
            else:
                dat['address']['postalCode'] = ''
            if 'addressCountry' in dat['address']:
                print('Address Country : '+dat['address']['addressCountry'])
            else:
                dat['address']['addressCountry'] = ''
            print('---------------------')
            shops['MainCategory'] = i.h3.text
            shops['Sub Category'] = subcat
            shops['Shop-Name'] = dat['name']
            shops['email'] = dat['email']
            shops['telephone'] = dat['telephone']
            shops['AddressType'] = dat['@type']
            shops['Address'] = dat['address']['streetAddress']
            shops['AddressLocality'] = dat['address']['addressLocality']
            shops['PostalCode'] = dat['address']['postalCode']
            shops['AddressCountry'] = dat['address']['addressCountry']

            f.write(str(shops)+'|')
