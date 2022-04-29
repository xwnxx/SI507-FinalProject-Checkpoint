from bs4 import BeautifulSoup
import requests
import requests_cache
import time
import json
import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
#import cache_use 
BASE_URL = 'https://www.boxofficemojo.com'
rank_PATH = '/year/'
path = '/?grossesOption=calendarGrosses'

CACHE_FILE_NAME1 = 'cacheMovie_Scrape.json'
CACHE_DICT1 = {}

CACHE_FILE_NAME2 = 'cacheDetail_Scrape.json'
CACHE_DICT2 = {}

def load_cache(CACHE_FILE_NAME):
    try:
        cache_file = open(CACHE_FILE_NAME, 'r')
        cache_file_contents = cache_file.read()
        cache = json.loads(cache_file_contents)
        cache_file.close()
    except:
        cache = {}
    return cache


def save_cache(cache, CACHE_FILE_NAME):
    cache_file = open(CACHE_FILE_NAME, 'w')
    contents_to_write = json.dumps(cache)
    cache_file.write(contents_to_write)
    cache_file.close()


def make_url_request_using_cache(url, cache, CACHE_FILE_NAME):
    if (url in cache.keys()): # the url is our unique key
        print("Using cache")
        return cache[url]
    else:
        print("Fetching")
        #time.sleep(1)
        response = requests.get(url)
        cache[url] = response.text
        save_cache(cache,CACHE_FILE_NAME)
        return cache[url]

rank_url = BASE_URL + rank_PATH
Genre = []
URL = []
Rank = []
Name = []
Year = []
Length = []
Country = []
Rating = []
Description = []
iTunesURL = []
for i in range(2011,2022):
    index = 0
    url1 = rank_url + str(i) + path

    CACHE_DICT1 = load_cache(CACHE_FILE_NAME1)
    url_text = make_url_request_using_cache(url1, CACHE_DICT1,CACHE_FILE_NAME1)
    response = requests.get(url1)
    soup = BeautifulSoup(response.text, 'html.parser')

    #<td class="a-text-left mojo-field-type-release mojo-cell-wide" style="width: 350px; height: 51px; min-width: 350px; min-height: 51px;"><a class="a-link-normal" href="/release/rl2869659137/?ref_=bo_yld_table_1">Spider-Man: No Way Home</a></td>
    movie_tds = soup.find_all('td', class_='a-text-left mojo-field-type-release mojo-cell-wide')
    rank = 1
    
    for movie_td in movie_tds:
        movie_link_tag = movie_td.find('a', class_="a-link-normal")
        movie_details_path = movie_link_tag['href']
        movie_details_url = BASE_URL + movie_details_path
        URL.append(movie_details_url)
        print(movie_details_url)
        
        #<div class="a-section a-spacing-none"><h1 class="a-size-extra-large">The Eight Hundred<span class="a-size-large a-color-secondary"> (2020)</span></h1><span class="a-size-medium">From the acclaimed filmmaker behind Mr. Six comes a riveting war epic. In 1937, eight hundred Chinese soldiers fight under siege from a warehouse in the middle of the Shanghai battlefield, completely surrounded by the Japanese army.</span></div>
        CACHE_DICT2 = load_cache(CACHE_FILE_NAME2)
        responseDetail = make_url_request_using_cache(movie_details_url, CACHE_DICT2, CACHE_FILE_NAME2)
        soupDetail = BeautifulSoup(responseDetail, 'html.parser')
        
        Rank.append(rank)
        #print('Rank: ', rank)
        rank += 1
        movie_name = soupDetail.find('h1', class_='a-size-extra-large')
        Name.append(movie_name.text)
        #print('Movie name: ',movie_name.text)
        years = i
        Year.append(years)
        #print('Release Year: ', years)
        movie_desc = soupDetail.find('div', class_='a-fixed-left-grid-col a-col-right').find(class_="a-size-medium")
        if movie_desc is None:
            Description.append('None')
            #print('Short Description: None')
        else:
            Description.append(movie_desc.text.strip())
        #<div class="a-section a-spacing-none"><span>Running Time</span><span>2 hr 10 min</span></div>
        #<span>2 hr 10 min</span>
        #<div class="a-section a-spacing-none mojo-summary-values mojo-hidden-from-mobile"><div class="a-section a-spacing-none"><span>Earliest Release Date</span><span>January 15, 2021
            #(China)</span></div><div class="a-section a-spacing-none"><span>Running Time</span><span>2 hr 10 min</span></div><div class="a-section a-spacing-none"><span>Genres</span><span>Drama
    



        #itunesurl = "https://itunes.apple.com/search"
        baseurl = "https://itunes.apple.com/search?term="
        #movie_name.text.replace(" ", "-")
        entity = "&entity=movie"
        parameter_dictionary = {'term':movie_name.text}
        url = baseurl + (movie_name.text.replace(" ", "-")).lower() +entity

        session = requests_cache.CachedSession('iTunesAPI')
        resp = session.get(url)
        Results_Dictionary = resp.json()
 
        if Results_Dictionary['resultCount']>0: 
        
            for re in Results_Dictionary["results"]:

                if 'kind' in re:
                    if re["kind"] == 'feature-movie':

                        if re['primaryGenreName'] !='':
                            Genre.append(re['primaryGenreName'])
                            break
                        else:
                            Genre.append('Unknown')
                            break
                    else:
                        Genre.append('Unknown')
                        break
                else:
                    Genre.append('Unknown')
                    break
                index +=1
        else:
            Genre.append('Unknown')
            
        
        
        if Results_Dictionary['resultCount']>0: 
            
            for re in Results_Dictionary["results"]:

                if 'kind' in re:
                    if re["kind"] == 'feature-movie':
  
                        if "trackTimeMillis" in re:
                            Length.append(round((int(re["trackTimeMillis"])/60000)))
                            break
                        else:
                            Length.append('Unknown')
                            break
                    else:
                        Length.append('Unknown')
                        break
                else:
                    Length.append('Unknown')
                    break
                index +=1
        else:
            Length.append('Unknown')
            
        if Results_Dictionary['resultCount']>0: 
            for re in Results_Dictionary["results"]:
                if 'kind' in re:
                    if re["kind"] == 'feature-movie':
                        if re['contentAdvisoryRating'] !='':
                            Rating.append(re['contentAdvisoryRating'])
                            break
                        else:
                            Rating.append('Unknown')
                            break
                    else:
                        Rating.append('Unknown')
                        break
                else:
                    Rating.append('Unknown')
                    break
                index +=1
        else:
            Rating.append('Unknown')
        
        if Results_Dictionary['resultCount']>0: 
            for re in Results_Dictionary["results"]:
                if 'kind' in re:
                    if re["kind"] == 'feature-movie':
                        if re['trackViewUrl'] !='':
                            iTunesURL.append(re['trackViewUrl'])
                            break
                        else:
                            iTunesURL.append('Unknown')
                            break
                    else:
                        iTunesURL.append('Unknown')
                        break
                else:
                    iTunesURL.append('Unknown')
                    break
                #index +=1
        else:
            iTunesURL.append('Unknown')
        
df = pd.DataFrame({'URL': URL,
                   'Rank': Rank,
                   'Name': Name,
                   'Year': Year,
                   'Length': Length,
                   'Rating': Rating,
                   'Genre': Genre,
                   'Description': Description,
                   'iTunesURL': iTunesURL})     

df = df[df!= 'Unknown']
df = df[df['Rating']!= 'Unrated']
df = df[df['Length']!= 'Unknown']
df["Length"] = pd.to_numeric(df["Length"])
df = df.dropna()
df = df.drop_duplicates(['Name', 'Description', 'iTunesURL'])
df.to_csv('movie_list.csv',index=False)  
