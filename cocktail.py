import itertools
import json
import streamlit as st
import requests
import os

api = (os.environ.get('api_key'))
st.set_page_config(page_title='Drink Recommender', page_icon="https://raw.githubusercontent.com/Githubaments/Images/main/favicon.ico")

def all_combinations(any_list):
    return itertools.chain.from_iterable(
        itertools.combinations(any_list, i + 1)
        for i in range(len(any_list)))

@st.cache(suppress_st_warning=True, show_spinner=False, allow_output_mutation=True)
def all_ingredients(x):
    my_combinations = list(all_combinations(x))

    cocktails = []
    for item in my_combinations:
        all_ingredients = ','.join(map(str, item))
        f = f"https://www.thecocktaildb.com/api/json/v2/{api}/filter.php?i=" + all_ingredients
        data = json.loads(requests.get(f).text)

        for item in (data["drinks"]):
            try:
                drink = item["idDrink"]
                cocktails.append(drink)
            except Exception:
                pass

    return (list(set(cocktails)))


def strict_ingredients(x):

    user_ingredients = ','.join(map(str, x))

    f = f"https://www.thecocktaildb.com/api/json/v2/{api}/filter.php?i=" + user_ingredients
    data = json.loads(requests.get(f).text)

    cocktails = []
    for item in (data["drinks"]):
        try:
            drink = item["idDrink"]
            cocktails.append(drink)
        except Exception:
            pass

    return (cocktails)


def get_drinks(cocktails):
    for item in cocktails:
        f_cocktails = f"https://www.thecocktaildb.com/api/json/v2/{api}/lookup.php?i=" + item
        r_cocktails = json.loads(requests.get(f_cocktails).text)

        st.image(r_cocktails['drinks'][0]['strDrinkThumb'], width=700, use_column_width=True)
        st.subheader(r_cocktails['drinks'][0]['strDrink'])

        for item in (range(1, 15)):
            a = 'strMeasure' + str(item)
            b = 'strIngredient' + str(item)
            a = r_cocktails['drinks'][0][a]
            b = r_cocktails['drinks'][0][b]

            if a != None and b != None:
                try:
                    st.write(a + " " + b)
                except:
                    st.write(b)
            else:
                break

        st.write("\n")
        st.subheader('Instructions:')
        st.write(r_cocktails['drinks'][0]['strInstructions'])
        st.write("\n")

        glass = r_cocktails['drinks'][0]['strGlass']
        Serve = f"**Serve: **{glass}"

        st.write(Serve)
        st.write("\n")
        st.write("\n")
        st.write("\n")

    return


@st.cache(suppress_st_warning=True, show_spinner=False, allow_output_mutation=True)
def filter_alcholic(cocktails):
    f = f"https://www.thecocktaildb.com/api/json/v2/{api}/filter.php?a=Non_Alcoholic"
    data = json.loads(requests.get(f).text)

    non_al = []

    for index,item in enumerate(data["drinks"]):
        non_al.append(data["drinks"][index]['idDrink'])

    cocktails = [x for x in cocktails if x in non_al]

    return cocktails


@st.cache(suppress_st_warning=True, show_spinner=False, allow_output_mutation=True)
def get_ingredient_list():
    f = f"https://www.thecocktaildb.com/api/json/v2/{api}/list.php?i=list"
    st.write(f)
    data = requests.get(f)
    data = json.loads(data.text)

    ingredients = []
    for item in (data["drinks"]):
        try:
            ing = item["strIngredient1"]
            ingredients.append(ing)
        except Exception:
            pass
    a = ingredients.index("Whiskey")
    b = ingredients.index("Scotch")
    ingredients[b] = 'Whiskey'
    ingredients[a] = 'Scotch'
    ingredients[5:] = sorted(ingredients[5:])

    return ingredients

def name_search(user_text):
    f = f"https://www.thecocktaildb.com/api/json/v2/{api}/search.php?s=" + str(user_text)
    data = json.loads(requests.get(f).text)

    cocktails = []

    if data["drinks"] == None:
        st.write("Sorry we can't find a cocktail with these ingredients.")
        st.stop()

    for item in (data["drinks"]):
        cocktails.append(item['idDrink'])

    return cocktails

@st.cache(suppress_st_warning=True, show_spinner=False, allow_output_mutation=True)
def whiskey(user_choice):
    whiskeys = ['Irish Whiskey',
                'Scotch',
                'Blended Scotch',
                'Blended Whiskey',
                'Bourbon',
                'Canadian Whisky',
                'Islay single malt Scotch',
                'Rye Whiskey',
                'Tennessee whiskey',
                'Whisky',
                'Whiskey',
                'Cinnamon Whisky'
                ]

    if 'Whiskey' in user_choice:
        user_choice.extend(whiskeys)

    return user_choice

@st.cache(suppress_st_warning=True, show_spinner=False, allow_output_mutation=True)
def whiskey_strict(user_choice):
    whiskeys = ['Irish Whiskey',
                'Scotch',
                'Blended Scotch',
                'Blended Whiskey',
                'Bourbon',
                'Canadian Whisky',
                'Islay single malt Scotch',
                'Rye Whiskey',
                'Tennessee whiskey',
                'Whisky',
                'Whiskey',
                'Cinnamon Whisky'
                ]
    cocktails = []
    if 'Whiskey' in user_choice:
        user_choice.remove('Whiskey')
        for item in whiskeys:
            temp_list = user_choice.copy()
            temp_list.append(item)
            cocktails.extend(strict_ingredients(temp_list))

    else:
        cocktails = strict_ingredients(user_choice)

    cocktails = list(set(cocktails))

    return cocktails


def popular():
    f = f"https://www.thecocktaildb.com/api/json/v2/{api}/popular.php"
    data = json.loads(requests.get(f).text)

    cocktails = []

    for item in (data["drinks"]):
        cocktails.append(item['idDrink'])

    return cocktails


def new_drinks():
    f = f"https://www.thecocktaildb.com/api/json/v2/{api}/latest.php"
    data = json.loads(requests.get(f).text)

    cocktails = []

    for item in (data["drinks"]):
        cocktails.append(item['idDrink'])

    return cocktails


st.header("Shane’s Drink Recommender")

ingredients = get_ingredient_list()

radio = st.radio('', (
'Search by Ingredients', 'Search by Cocktail Name', 'Newest Cocktails', 'Just Show Me Some Popular Cocktails'))

if radio == 'Search by Cocktail Name':
    user_text = st.text_input('Cocktail Search', value='', max_chars=None, key=None, type='default')
    if len(user_text) != 0:
        cocktails = name_search(user_text)
        get_drinks(cocktails)

elif radio == 'Search by Ingredients':
    user_choice = st.multiselect('Choose your ingredients:', ingredients, [])

    my_expander = st.beta_expander('Options')
    mode = my_expander.radio('Search Mode', (
    'Drink must contain all ingredients', 'Return drinks with any combination of ingredients (slower)'))
    non_alcoholic = my_expander.radio('Non-Alcoholic Only', ('Yes', 'No'), index=1)

    if len(user_choice) != 0:
        if mode == 'Drink must contain all ingredients':
            cocktails = whiskey_strict(user_choice)

        else:
            user_choice = whiskey(user_choice)
            cocktails = all_ingredients(user_choice)

        if non_alcoholic == 'Yes':
            cocktails = filter_alcholic(cocktails)
            if len(cocktails) == 0:
                st.write("Sorry we can't find a non-alcholic cocktail with these ingredients.")
                st.stop()

        if cocktails == 'None Found':
            st.write("Sorry we can't find a cocktail with these ingredients.")
            st.stop()

        get_drinks(cocktails)

elif radio == 'Newest Cocktails':
    cocktails = new_drinks()
    get_drinks(cocktails)

else:
    cocktails = popular()
    get_drinks(cocktails)
