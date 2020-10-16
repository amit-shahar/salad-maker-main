import os

# Global variable
name = ''


# Function that creates 'photos' folder if not exist
def create_photos_folder():
    if not os.path.exists('static/photos'):
        os.makedirs('static/photos')


# Function that creates an image for each recipe
def create_image_file(recipe_name, data):
    name = 'static/photos/' + recipe_name + '.png'
    name = name.replace(" ","_")

    # if the image of this recipe is not exist
    if not os.path.exists(name):
        # create image for this recipe
        with open(name, 'wb') as f:
            f.write(data)

