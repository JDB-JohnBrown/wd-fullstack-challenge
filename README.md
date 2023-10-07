**W&D Lead Fullstack Engineering Challenge**

Welcome to our Lead Fullstack Engineering Challenge repository. This document will guide you through the challenge. Please fork this repo before you begin, as we will evaluate the code on your fork.

**Challenge Overview:**

Design and implement a system that allows users to manage their personal property list. Users should be able to sign up, log in, and then add or remove properties to/from their property list.

**Requirements:**

1. **User Authentication**:
    - Implement a basic login and sign-up page.

2. **Database Design and Implementation**: 
    - We recommend using SQLite for the sake of simplicity, but feel free to choose another database if you have a specific preference. Justify your choice.
    - Initiate the database using the data from the provided Excel file. Automation is not necessary. 

3. **Backend Development**:
    - Develop a backend in Python to interact with the database.
    - Choose a suitable Python framework (e.g., Flask, Django, FastAPI, Falcon) and justify your choice.

4. **Frontend Development**:
    - Implement the frontend using Vue.js.
    - Once logged in, users should see their property list.
    - Each property in the list should display:
        - Full Address
        - Class Description
        - Estimated Market Value
    - Users should be able to search for properties from the database and add them to their property list.
        - Users should be able to search on the following values:
            - Full Address
            - Class
            - Estimated_Market_Value
            - BLDG_USE
            - BUILDING_SQ_FT
    - Properties on the users list should have an option to be removed.

5. **Security**:
    - Implement basic security practices for the backend API and user authentication.

6. **Documentation**:
    - Provide a brief README detailing how to set up and run your application.
  
7. **Bonus**:
    - **Optimization**: Propose at least one optimization that can help the application perform better under increased data loads.
    - **Additional Feature**: Propose a feature you believe would enhance the user's experience while managing their property list.


# Development Notes
I wanted to explain my thought process here as I go, since the point of the exercise is to get an understanding for how I think and operate. 

1. **Breakdown Requirments into smaller chunks**
    - Create database (Recc: sqlite, _awesome I'm working on a personal project right now using sqlite_)
    - Create database tables. _What do I need?_
    - Load property table from xlsx file
    - How do I build an app with python backend and vue.js frontend?
    - Authentication & api calls
    - Design front-end

2. **Create database**
    - I have "DB Browser for SQLite" on my machine, quickly create a new DB fille, name it _wd-fsc.db_ (Walker Dunlop - Fullstack Challenge Database)
3. **Create database tables**
    - _What do I need?_
        - Definitely need a _property_ table.
            - Let's take the xlsx file, and copy all the columns. I don't think we need everything _now_ but if we build on it in the future I don't want to reload everything
            - Make sure we have an id column, so I can quickly identify property rows later
            - Make it the "primary key", in SQLite3, it will auto-increment if I pass "NULL" on inserts
        - We need a _user_ table
            - What does _user_ need?
                - Definitely needs *user_id*
                - *username*
                - *password* - password seems like a reserved keyword in sqlite, lets call it *passw*
        - Let's make *user_property_link*
            - Simple table that has foreign keys on both *user* and *property* so we can tell what properties each user has added
        - *user_session*
            - We need to know if a user is logged in before we let them access the DB
            - What do we need?
                - Not sure, been awhile since I've created one, let's wait till I do step 5 and circle back
4. **Load property table from .xlsx file**
    - I already have the "property" table from Step 3
    - Let's pass the whole file to a simple converter to get me insert statements. 
    - Ignore inserting property_id, since if I don't pass a value, it'll auto-increment
    - Make sure I commit hah
5. **How do I build an app with python backend and vue.js frontend?**
    - Neither is my first choice of language
    - _Let's google it!_
        - Wow, basically the first link is exactly what I need. Let's lean on that
        - https://medium.com/@andrelbaldo/register-login-and-logout-boilerplate-written-in-vue-js-and-python-as-api-5ce57e33774b
            - Let's read through the whole thing and see what decisions they made. 
            - Looks pretty good overall. Couple of changes I'm going to make. 
                - They're using a hosted MSSQL database. I'm going to use sqlite. Minor change overall
                - They're using something called *werkzeug* for password hashing. I'm more comfortable with *passLib* as it's commonly suggested in my other searches. 
                - I don't like camel case in my databases, I'm going to change everything to snake-case
                - Need to tweak some date logic. SQLite doesn't have a datetime datatype, I'm going to use integers and store unix time
                - I want better password requirments than what they're using
        - Now I know what *user_session* table needs to look like. Use their example, tweaking names and datatypes.
