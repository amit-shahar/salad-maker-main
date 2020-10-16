from flask import Flask, render_template, request, redirect, jsonify
import readDB

# global variables
app = Flask(__name__, static_url_path='/static')
veggies_input = []
veggie_content = ""
veggies_names_list = []

# read veggies names from readDB.py once the page is loaded
readDB.create_veggies_dict()

# To upper case, to be able to compare input to database
veggies_names_list_upper = [x.upper() for x in readDB.veggies_dict.keys()]


# this function creates a list of veggies names- for autocomplete option
def create_veggies_names_list():
    for key in readDB.veggies_dict:
        veggies_names_list.append(key)


create_veggies_names_list()


# index page
@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        veggie_content = request.form['content']
        # if the client input is already in the table
        if veggie_content.capitalize() in veggies_input:
            return redirect('/')
        else:
            try:
                # If the client input veggie exist in vegetables database
                if veggie_content.upper() in veggies_names_list_upper:
                    veggies_input.append(veggie_content.capitalize())
                return render_template("index.html", veggies_input=veggies_input)

            except:
                return 'Oops! There was an issue. Try again!'

    # if the method is GET
    else:
        return render_template("index.html", veggies_input=veggies_input)


# Function to delete an unwanted veggie
@app.route('/delete/<string:veg_to_delete>')
def delete(veg_to_delete):
    try:
        veggies_input.remove(veg_to_delete)
        return redirect('/')
    except:
        return 'Oops, cannot delete!'


# Function to send the veggies names list to javascript file- for autocomplete
@app.route('/get_veggies_list', methods=['GET'])
def get_veggies_list():
    return jsonify({"list": veggies_names_list})


# Function to send the whole input
@app.route('/send_veggies_input', methods=['POST'])
def send_veggies_input():
    readDB.veggies_input_from_app = veggies_input
    sorted_relevant_recipes_list_from_readDB = readDB.search_relevant_recipes()
    return render_template("recipes.html", relevant_recipes=sorted_relevant_recipes_list_from_readDB, veggies_input=veggies_input)


# Function to delete all veggies
@app.route('/delete_all_veggies', methods=['POST'])
def delete_all():
    try:
        veggies_input.clear()
        return redirect('/')
    except:
        return 'Oops, cannot delete!'


# start the app
if __name__ == "__main__":
    app.run(debug=True)
