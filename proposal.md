# Project Proposal:

What goal will your website be designed to achieve?

  >This website will allow users to search and save recipes based on ingredients.
----

What kind of users will visit your site? In other words, what is the demographic of your users?

  >The demographic of the site includes those who are looking for recipe inspiration or fresh ideas based on ingredients they have.
----
What data do you plan on using? You may have not picked your actual API yet, which is fine, just outline what kind of data you would like it to contain.

  >This site will use the Spoonacular API (https://spoonacular.com/food-api/docs).  Through this API users will have access to recipe ingredients and instructions.
----

In brief, outline your approach to creating your project (knowing that you may not know everything in advance and that these details might change later). Answer questions like the ones below, but feel free to add more information:
1. What does your database schema look like?
            
 >Database Schema:

    ![Schmema Design.](/images/schema.PNG "Schema Design.")

   | Users          | Favorites  | Comment_recipe |
   | -------------  |----------  |-------------   |
   | id             | id         |id              |
   | email          | recipe_id  |comment_text    |
   | username       | user_id    |recipe_id       |
   | password       | user*      |user_id         |
   | favorites*     |            |user*           |
   | user_comments* |            |                |       
   
 *Recipe IDs used to request ingredients and instructions from API |

2. What kinds of issues might you run into with your API?

  >(Stretch goal) Ensuring user categories align with API categories - creating a drop down list of options for users to select
  > API key access and a restriction on the number of calls available in a day

3. Is there any sensitive information you need to secure?
  >1. User password information
  >1. Only logged in users will be able to create a favorites list
  >1. Only logged in users will be able to create and view comments

4. What functionality will your app include?
  >1. Log in / Registration of users
  >1. Recipe search by ingredient
  >1. Users can save recipes to a favorites list
  >1. Users can add comments to recipes

5. What will the user flow look like?

            Homepage:
                - Access for user / non user
                    - Search recipes by category and ingredient
                    - Page will list some recipes which will link to more details.  Clicking on recipes will navigate to details page for recipe.
                - Non logged in users navbar:
                    - Login link on navbar directs to Login page
                - Logged in users navbar:
                    - Logout option - logs out user and directs back to homepage
                    - Favorites
                    - Profile
            Login:
                - Login form with username and password. Directs back to homepage on completion
                - Register Link directing to a register form
            Register:
                - Form including username, email, and password sign up
                - Directs back to homepage on completion
            Favorites:
                - Lists user's saved recipes.  Clicking on recipes will navigate to details page for recipe.
                - Remove from favorites option
            Details Page:
                - Recipe details: Img, Ingredients, Instructions
                - Non logged in user:
                    - No additional information
                - Logged in user:
                    - View comments.  Delete / edit option for user's comments only
                    - Favorites status: Add to favorites / Remove from favorites based on current state. Does not redirect
                    - Add comment. Directs to comment form.
            Profile:
                - Lists user information.
                - Edit profile - directs to edit profile form
                - Delete Account - deletes account record and directs to homepage
            Edit Profile:
                - Update user information form
                - Save changes - redirects to Profile page
                - Delete Account - deletes account record / comments / favorites and directs to homepage
            Add Comment:
                - Form including: text, submit, cancel.  Directs back to detail page of recipe on completion or cancel.
            Edit/ Delete Comment
                - Form including: Form to edit or delete existing comment.  Directs back to detail page of recipe on completion or cancel.

----
6. What features make your site more than CRUD? Do you have any stretch goals?

  > 1. More than CRUD: User log in / authentication.  Access restriction based on user session status.
  > 1. Stretch goal: Search based on multiple categories along with ingredients.
