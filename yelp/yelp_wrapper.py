import os
import time
from pip._vendor import requests
from pip._vendor.requests import HTTPError, RequestException
from nltk import bigrams
import pandas as pd
class Restaurant(object):
    def __init__(self, id, yelp_link, pic_link, name, categories, open, price, location):
        self.id = id
        self.yelp_link = yelp_link
        self.pic_link = pic_link
        self.name = name
        self.categories = categories
        self.open = open
        self.price = price
        self.location = location


class YelpWrapper:
    def __init__(self):
        self.API_KEY = os.getenv("YELP_API")
        self.CLIENT_KEY = os.getenv("YELP_CLIENT")

    def search(self, location: str, categories: str, open_now: bool, price: str, sort_by: str) -> [
        Restaurant]:
        params = {
            "location": location,
            "categories": categories,
            "open_now": open_now,
            "sort_by": sort_by,
            "price": price,
            "limit": 50
        }
        try:
            url = "https://api.yelp.com/v3/businesses/search"
            headers = {"Authorization": f"Bearer {self.API_KEY}"}
            for trial in range(3):
                response = requests.get(url, headers=headers, params=params)
                response.raise_for_status()
                result = response.json()
                res = []
                if result and result.get('businesses'):
                    for bizz in result.get('businesses'):
                        id = bizz['id']
                        name = bizz['name']
                        yelp_link = bizz['url']
                        pic_link = bizz['image_url']
                        open_now = not bool(bizz['is_closed'])
                        cato = []
                        for category in bizz['categories']:
                            cato.append(category['title'])
                        loca = bizz['location']['display_address']
                        p = bizz['price']
                        res.append(Restaurant(id=id, yelp_link=yelp_link, pic_link=pic_link, name=name, categories=cato,
                                              open=open_now, price=p, location=loca))
                    return res
                time.sleep(1)
        except HTTPError as http_err:
            print(f"HTTP error occurred when retrieving last price: {http_err}")
            raise http_err
        except RequestException as r_err:
            print(f"Other request error occurred when retrieving last "
                  f"price: {r_err}")
            raise r_err
        except Exception as err:
            print(f"Other error occurred when retrieving last price: {err}")
            raise err
        else:
            raise ConnectionError

    def get_all_categories(self) -> [str]:
        try:
            url = "https://api.yelp.com/v3/categories"
            headers = {"Authorization": f"Bearer {self.API_KEY}"}
            for trial in range(3):
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                result = response.json()
                res = []
                if result and result.get('categories'):
                    for cato in result.get('categories'):
                        res.append(cato["alias"])
                    return res
                time.sleep(2)
        except HTTPError as http_err:
            print(f"HTTP error occurred when retrieving categories: {http_err}")
            raise http_err
        except RequestException as r_err:
            print(f"Other request error occurred when retrieving categories")
            raise r_err
        except Exception as err:
            print(f"Other error occurred when retrieving categories: {err}")
            raise err
        else:
            raise ConnectionError

    @staticmethod
    def parse(cato):
        curr_grams = bigrams(cato)
        all_df = pd.read_csv("cato.csv")
        all_cato = all_df["categories"]
        #TODO: find the most similar category.
