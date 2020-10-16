import sqlite3
import imageLoad

# Activating Veggies Database
veg_db = sqlite3.connect('veggies.db')
cveg = veg_db.cursor()

# Activating Recipes Database
recipes_db = sqlite3.connect('recipes.db', check_same_thread=False)
crec = recipes_db.cursor()

# Global variables
veggies_dict = {}
veggies_input_from_app = []
relevant_recipes_dict = {}


# creates a dictionary of veggies names and points
def create_veggies_dict():
    cveg.execute('SELECT * FROM veggies')
    veggies_data = cveg.fetchall()
    for row in veggies_data:
        veggies_dict.update({row[0]: row[1]})


# Function to bring only relevant recipes
def search_relevant_recipes():
    relevant_recipes_dict= {}
    # open photos folder if not exist
    imageLoad.create_photos_folder()
    # Loop through the client's veggies input
    for veg in veggies_input_from_app:
        sql_query = "SELECT * FROM recipes WHERE veggies LIKE '%, {this_veg},%'".format(this_veg=veg)
        crec.execute(sql_query)
        recipes_data = crec.fetchall()
        # Loop through the veggies lists in the recipes database
        for row in recipes_data:
            # if a veggie is found - update the recipes dictionary accordingly (sum the points of the recipe)
            if row[0] not in relevant_recipes_dict.keys():
                relevant_recipes_dict.update({row[0]: [0, row[1], row[2], row[3], row[4]]})
                imageLoad.create_image_file(row[1], row[4])
            relevant_recipes_dict[row[0]][0] += veggies_dict[veg]
    # lambda sorting by dictionary value (by recipe total points)
    sorted_relevant_recipes_list = sorted(relevant_recipes_dict.items(), key=lambda e: e[1][0], reverse=True)
    return sorted_relevant_recipes_list




