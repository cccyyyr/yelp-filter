import os
import time
from pip._vendor import requests
from pip._vendor.requests import HTTPError, RequestException
import pandas as pd
import difflib


class Restaurant(object):
    '''
    a class that represent each restaurant.
    '''
    def __init__(self, id, yelp_link, pic_link, name, categories, price, location):
        self.id = id
        self.yelp_link = yelp_link
        self.pic_link = pic_link
        self.name = name
        self.categories = categories
        self.price = price
        self.location = location


class YelpWrapper:
    def __init__(self):
        '''
        initiate a wrapper class by retrieving API keys from .env file
        '''
        self.API_KEY = os.getenv("YELP_API")
        self.CLIENT_KEY = os.getenv("YELP_CLIENT")

    def search(self, location: str, categories: str, open_now: bool, price: str) -> [Restaurant]:
        '''
        :param location: location user input
        :param categories: category information we parsed from user input by our parse method below so we can use a
        category best matched to what the user desires.
        :param open_now: whether user want it to be open now or not
        :param price: price range user put in
        :return: A list of restaurants matching the query.
        Use YelpAPI to retrieve real time list of restaurants that user might be interested in.
        '''
        params = {
            "location": location,
            "categories": categories,
            "open_now": open_now,
            "sort_by": "rating",
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
                        cato = []
                        for category in bizz['categories']:
                            cato.append(category['title'])
                        loca = bizz['location']['display_address']
                        p = bizz['price']
                        res.append(Restaurant(id=id, yelp_link=yelp_link, pic_link=pic_link, name=name, categories=cato,
                                              price=p, location=loca))
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
        """
        :return: a list of all categories.
        Use API key to call all categoriess. This method is used in pre_process.py and used to generate cato.csv.
        """
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
    def parse(input_cate):
        '''
        :param input_cate: the category information user put in
        :return: a parsed cateoory.
        In the event that the input category does not match any one in yelp database, yelp API itself does not do
        anything with it and return a bunch of random categories. Through doing this, we can parse the category and
        return restaurants users are most likely looking for.
        '''
        all_df = pd.read_csv("cato.csv")
        all_cato_lst = all_df["categories"].tolist()
        top10_similiar = difflib.get_close_matches(input_cate, all_cato_lst)
        return top10_similiar[0]



