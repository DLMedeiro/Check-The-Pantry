# Check The Pantry - Recipe Finder App

**Try out the App Here: [Check-The-Pantry](https://check-the-pantry.herokuapp.com/)**

This application allows users to search and save recipes based on a chosen ingredient.  Upon selecting a recipe a picture, ingredient list, and directions are provided. Also with in the recipe details page, registered users are able to leave comments and save their favorite recipes.  For those who choose not to register, access to recipe details are still available.

This project utilizes data from the spoonacular API, under their basic permissions option.  At this time, due to the basic permissions of this API, this application is restricted to 150 calls per day.  

Documentation for Spoonacular can be found [here](https://spoonacular.com/food-api/docs).

## Technologies used:

<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg" height = 50px width=50px/> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg" height = 50px width=50px/> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg" height = 50px width=50px/> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original-wordmark.svg" height = 50px width=50px/> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/flask/flask-original-wordmark.svg" height = 50px width=50px /> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-plain-wordmark.svg" height = 50px width=50px/> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/sqlalchemy/sqlalchemy-original-wordmark.svg" height = 50px width=50px/> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/bootstrap/bootstrap-original.svg" height = 50px width=50px /> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/heroku/heroku-original-wordmark.svg" height = 50px width=50px/>

## Installation Instructions
1. This application requires an account with Spoonacular to obtain an API key.  [Create an account here](https://spoonacular.com/food-api/console#Dashboard)

1. Clone the repo: https://github.com/DLMedeiro/Recipe_Finder.git

1. Create a virtual environment in the project directory: python3 -m venv venv

1. Start the virtual environment: source venv/bin/activate

1. Install required packages: pip3 install -r requirements.txt

1. After creating a spoonacular account assign your API key to the variable 'apiKey' within a secrets.py file.  Be sure to include the secrets.py file in your .gitignore file.  

1. Set up a PostgreSQL database for this application

1. In the terminal

    ``` createdb recipes-app ```
     
    ``` (ipython) run app.py ```
     
    ``` (ipython) db.create_all() ```
    
    ``` (start virtual environment) env\Scripts\activate.bat ```

    ``` (venv) flask run ```