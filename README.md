Project Proposal:

    1. What goal will your website be designed to achieve?

        A: This website will allow users to search and save recipes based on category and/or ingredients.
    
    2. What kind of users will visit your site? In other words, what is the demographic of your users?

        A: The demographic of the site includes those who are looking for recipe inspiration or fresh ideas based on ingredients they have.

    3. What data do you plan on using? You may have not picked your actual API yet, which is fine, just outline what kind of data you would like it to contain.

        A: This site will use the BigOven API (https://api2.bigoven.com/).  Through this API users will have access to recipe ingredients and instructions.

    4. In brief, outline your approach to creating your project (knowing that you may not know everything in advance and that these details might change later). Answer questions like the ones below, but feel free to add more information:
        a. What does your database schema look like?
            
            A1: Users: ID, email, username, password
                Connected to: favorite_recipes, comments
            A3: Comments: ID, text, timestamp, user_id
            A4: Favorite_recipes: ID, user_id, recipe_id
            
            *Recipe IDs user to request ingredients and instructions from API

        b. What kinds of issues might you run into with your API?

            A: Ensuring user categories align with API categories - creating a drop down list of options for users to select

        c. Is there any sensitive information you need to secure?

            A1: User password information
            A2: Only logged in users will be able to create a favorites list
            A3: Only logged in users will be able to create (and possible view) comments

        d. What functionality will your app include?

            A1: Log in / Registration of users
            A2: Recipe search by category or ingredient
            A3: Users can save recipes to a favorites list
            A4: Users can add comments to recipes

        e. What will the user flow look like?

            A1: Homepage:
                - Access for user / non user
                - Search reciepies by category and ingredient
                - Page will list some recipes which will link to more details.  Clicking on recipes will navigate to details page for recipe.
                - Non logged in users navbar:
                    - Login link on navbar directs to Login page
                - Logged in users navbar:
                    - Logout option - logs out user and directs back to homepage
                    - Favorites
                    - Profile
            A2: Login:
                - Login form with username and password. Directs back to homepage on completion
                - Register Link directing to a register form
            A3: Register:
                - Form including username, email, and password sign up
                - Directs back to homepage on completion
            A4: Favories:
                - Lists user's saved recipes.  Clicking on recipes will navigate to details page for recipe.
                - Remove from favorites option
            A5: Details Page:
                - Recipe details: Img, Ingredients, Instructions
                - Non logged in user:
                    - No additional information
                - Logged in user:
                    - View comments.  Delete / edit option for user comments only
                    - Favorites status: Add to favorites / Remove from favorites based on current state. Does not redirect
                    - Add comment. Directs to comment form.
            A6a: Add Comment:
                - Form including: text, submit, cancel.  Directs back to detail page of recipe on completion or cancel.
                A6b: Edit Comment:
                A6c: Delete Comment:
            A8: Profile:
                - Lists user information.
                - Edit profile - directs to edit profile form
                - Delete Account - deletes account record and directs to homepage
            A9: Edit Profile:
                - Update user information form
                - Save changes - redirects to Profile page
                - Delete Account - deletes account record / comments / favorites and directs to homepage

        f. What features make your site more than CRUD? Do you have any stretch
        goals?

            A1: More than CRUD: User log in / authentication.  Access restriction based on user session status.
            A2: Stretch goal: Search based on multuple ingredients and categories
