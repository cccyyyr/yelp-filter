from django.conf import settings

from yelp.yelp_wrapper import YelpWrapper
import pandas as pd


def process_category():
    '''
    :return: None
    A pre_processing method that will get all categories from YELP and parse them into a csv file.
    '''
    settings.configure()
    yelp = YelpWrapper()
    all_cato= yelp.get_all_categories()
    cato_dict = {"categories": all_cato}
    cato_df = pd.DataFrame(cato_dict)
    cato_df.to_csv('cato.csv')

'''
The following method is called once and no need to call it again. You can if you want.
'''
process_category()
