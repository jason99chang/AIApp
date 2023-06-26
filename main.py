import requests
import pandas as pd
from bs4 import BeautifulSoup
import time




def scrape_realtor_website(url):

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language' : 'en-US,en;q=0.5',
    'Accept-Encoding' : 'gzip',
    'DNT' : '1', # Do Not Track Request Header
    'Connection' : 'close'
}

    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        print(f"Failed to get the page, status code: {r.status_code}")
        return

    soup = BeautifulSoup(r.content, 'html.parser')

    data_points = ['property_type', 'time_on_realtor', 'price_per_sqft', 'garage', 'year_built', 
                   'lot_size', 'hoa', 'mls', 'status', 'days_on_market', 'bed', 'bath', 'sqft', 'city',
                   'state', 'zip', 'address', 'price', 'nearby_school_ratings', 'neighborhood_ratings']

    class_names = ['property-type-class', 'time-on-realtor-class', 'price-per-sqft-class', 
                   'garage-class', 'year-built-class', 'lot-size-class', 'hoa-class', 'mls-class',
                   'status-class', 'days-on-market-class', 'bed-class', 'bath-class', 'sqft-class',
                   'city-class', 'state-class', 'zip-class', 'address-class', 'price-class', 
                   'nearby-school-ratings-class', 'neighborhood-ratings-class']  # replace with actual classes

    data = {}

    for dp, cn in zip(data_points, class_names):
        element = soup.find('div', class_=cn)
        data[dp] = element.text if element else None

    return data


def scaper_iterator(url):
    #Iterate through the pages of the website so that this function can call the scrape_realtor_website function on each listing.
    # Return a list of dictionaries
    # Create an empty list to store the dictionaries
    data = []
    # Iterate through the pages of the website
    for i in range(1, 10):
        # Get the URL
        url = url + str(i)
        # Call the scrape_realtor_website function
        time.sleep(5)
        data.append(scrape_realtor_website(url))
    # Return the list of dictionaries
    return data

def main_scraper(url):
    #the main function that will make multiple calls to the scaper iterator function and save the data to a csv file
    #the main function should also try to scrape listings from all 50 states. 
    # Return a csv file
    # Create an empty list to store the data
    data = []
    # Iterate through the pages of the website
    for i in range(1, 50):
        # Get the URL
        url = url + str(i)
        # Call the scrape_realtor_website function
        data.append(scaper_iterator(url))
    # Create a dataframe from the list of dictionaries
    df = pd.DataFrame(data)
    # Save the dataframe to a csv file
    df.to_csv('realtor_data.csv', index=False)
    # Return the csv file
    return df


if __name__ == '__main__':
    url = 'https://www.realtor.com/'
    df = main_scraper(url)
    print(df.head())