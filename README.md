# What's for Dinner - Recipe Finder App

**Try out the App Here: [*TBD*]()**

This application allows users to search and save recipes based on a chosen ingredient.  Upon selecting a recipe a picture, ingredient list, and directions are provided. Also with in the recipe details page, registered users are able to leave comments and save their favorite recipes.  For those who choose not to register, access to recipe details are still available.

This project utilizes data from the spoonacular API, under their basic permisions option.  At this time, due to the basic permissions of this API, this application is restricted to 150 calls per day.  

Documentation for Spoonacular can be found [here](https://spoonacular.com/food-api/docs).

## Technologies used:

HTML5 | CSS3 | JavaScript | Python | Git | Visual | Studio Code | JINJA |  *Heroku* | Postgres | Flask | WTForms | SQLAlchemy

## Installation Instructions
1. This application requires an account with Spoonacular to obtain an API key.  [Create an account here](https://spoonacular.com/food-api/console#Dashboard)

1. Clone the repo: https://github.com/DLMedeiro/Recipe_Finder.git

1. Create a virtual environment in the project directory: python3 -m venv venv

1. Start the virtual environment: source venv/bin/activate

1. Install required packages: pip3 install -r requirements.txt

1. After creating a spoonacular acocunt asign your API key to the varilable 'apiKey' within a secrets.py file.  Be sure to include the secrets.py file in your .gitignore file.  

1. Set up a PostgreSQL database for this applicati

1. In the terminal
  1. createdb recipes-app
  1. ipython
    1. run app.py
    1. db.create_all()
  1. flask run
  1. Open web browser and run the app on the port for your server.


#### Improvement Ideas / Notes:
* Change API key in Js file
* Limited to 150 API points per day
* Search results are limited to 6, same results show each time
* Radmon recipe feature based on cuisine
* Multiple ingredient search
* Backup API key
* Consolodate CSS
* Clean routing
* Add testing
* Add features to user profiles
* Change password feature