## Collabrators
Yiran Chen & Yuxuan Wang


# Installation Instruction
Open this project in an editor such as PyCharm or Visual Studio Code. First make sure you are running the project under a Django environment. You could run `pip install django` to install Django. 

First-party packages we used:
```
os
time
```

Third-party packages we used:
```
Django
Pandas
Difflib
```

If you run into problems when trying to run the code, try the following installation commands.
```
pip install django
pip install cdifflib
pip install python-dotenv
pip install pandas
```

You could also consult requirements.txt for more detailed documentation on every packages we used.


# How to run?
Enter the command `python manage.py runserver` in your terminal. Open the link given in your browser and you are at the home page of this restaurant app.

The home page will prompt you to begin searching. Once you selected your filters (location, category, price level, currently open or not) and click on "Search", filtered results will be displayed on the page. For each restaurant returned, there is information about it's photo, name, location, price level, and a hyperlink button to direct you to its yelp page.

When the category you entered cannot perfectly match an existing category, we will provide the closest results to what you entered. 

Once a search is completed, you could hit "Return" to begin another search.


# Code Structure
There are three pages to this Yelp App: home.html, search.html, and splash.html. The spalsh page directs users to enter
 search configuration. The search results will be displayed on the home page.

 `urls.py` documents the URLs used. Empty URL directs users to the Splash page. `search/` directs users to the search 
 page. And URLs of the format `search/<location>/<price>/<categories>/<open_now>` directs users to the home page with 
 search results.

 In forms.py, we collect four inputs from the users: location, category, price and hours.

 In yelp_wrapper.py, we have a class `Restaurant` that defines a restaurant object, with several features like name, 
 location, link to picture, link to yelp page, etc.

 Class `YelpWrapper` connects to the provided Yelp API in order to retrieve real-time information. Function `search`
 takes in user-entered information and gives a list of restaurants and also handles possible exceptions. 
 
 However, what if the user-entered information cannot perfectly match with our database? We then implemented a feature 
 to return the closest matches when we couldn't find a perfect match. In order to do that, Function `get_all_categories` 
 gives us a complete list of existing categories to match against and turn the information into a csv file. Since we 
 only need to do it once, the code to do so is in the pre_process.py that you need not to run. 
 And function `parse` returns the closest matches using functions from the difflib package.

 



