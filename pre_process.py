from django.conf import settings

from yelp.yelp_wrapper import YelpWrapper
import pandas as pd


def process_category():
    settings.configure()
    yelp = YelpWrapper()
    all_cato= yelp.get_all_categories()
    cato_dict = {"categories": all_cato}
    cato_df = pd.DataFrame(cato_dict)
    cato_df.to_csv('cato.csv')

process_category()
