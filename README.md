# How to get started
Instructions will be based on a Windows machine, but should be largely followable on other systems.
1. Ensure Python3 is installed.
    - Go to https://www.python.org/downloads/
    - Ensure pip is installed. (Should come with Python3)
        - Run "pip" and make sure it works.
        - Otherwise, google installing it
2. Ensure Node.js Is installed 
    - go to https://nodejs.org/ and follow the instructions to install it on your platform, please set the node into the path so you can use node from windows command prompt.
    - Ensure npm is installed
        - Run "npm" and make sure it works
        - Otherwise, google installing it
3. Ensure yarn is installed. 
    - Try the command "yarn"
    - If it doesnt work run: "npm install yarn -g"
4. Install Vue.js client
    - "npm install -g @vue/cli"
5. Download code from this package
    - "git clone https://github.com/JDB-JohnBrown/wd-fullstack-challenge.git"
6. Run "install.bat" 
    - or follow the commands inside of it step by step
7. Run "start-backend.bat"
8. Run "start-backend.bat"
   - If it closes immediately, something may have gone wrong with yarn install. Open the frontend folder, and run "yarn install" in a command line


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
6. **Let's create a virtual environment for our build, hoping to reduce the amount of setup needed to run my project**
    - Apparently kind of a pain on Windows
    - cd backend
    - pip install virtualenv
    - python -m virtualenv venv
    - .\venv\Scripts\activate.bat
    - where.exe python 
        - \wd-fullstack-challenge\backend\venv\Scripts\python.exe    #OKAY GOOD!
    - Let's make sure VSCode is _also_ using our venv for the interpretter. 
        - Open Command Pallete
        - Search for Python  Interpretter, set it to venv\Scripts\python.exe
7. **Borrow the code from that reference little by litte**
    - I want to make sure I understand every piece going into my codebase
    - I've also made a few stylistic choices that I want to try to be consistent with
        - Honestly, this is kindof intentional so I MAKE myself understand everyline
        - Needing to make sure everything is going to work my my db, and moving a few things around, requires every line to be combed over
8. **Start on the frontend**
    - Need node.js, NPM, Vue js client installed
        - I'm a node guy, so I have the first two
        - *cd ..*  (I was in the backend folder)
        - *npm install -g @vue/cli*
        - *vue create frontend*
        - Wow, lot's of options, let's follow my tutorial to the best of my ability
        - Manually select features: Babel, PWA, Router, Vuex, Linter
        - Version: 3 *tutorial didnt have this question, So I'm guessing they were on v2. Let's do v3 and if we hit bugs, well figure them out!*
        - History Mode-> Yes, linter/formatter config? -> Basic, -> Lint on Save, -> Dedicated config files, -> No, don't save this as a preset, -> Let's use Yarn as the package manager
        - cd frontend
        - yarn serve
        - goto http://localhost:8080/, wow pretty. We're movin now
        - close, commit
        - vue add vuetify
            - darn, vuetify doesn't work with v3 of vue 
            - cd ..; rm ./frontend -r -force
            - redo installing vue, but swap to v2
9. **Get login and registration working**      
    - FOllowing the tutorial this was a breeze
    - Added more constraints to password and username creation
    - Changed out using "emails" for raw usernames
10. **Now we're logged in, do the resy**
    - This is where it should get easy. I aleady have some basic API calls for logging in, etc...
    - Start with viewing properties. I can add some test values straight to the database. 
    - First lets build the python bit, then the front end bit
    - Pull user ID from the headers we have from logging in. 
    - Use Flask to enforce active logins are the only people who can access my new listing api router
    - Honestly flew through that
    - Pretty easy to have a dynamic data table in vue.js with vuetify
11. **Add delete API call**
    - I don't want to do search yet, so let's work on the easier requirment of being able to delete
    - Add a delete button to the ui
    - Add delete js functions
    - Add python delete user listing router 
    - Add logic to do the delete on the database
12. **Search**
    - Search, hmmm... let;s add some text boxes to the ui
    - SQL has a "like" function, let's use that for these, nice and easy
    - Follow the same strategy as above
    - Google how to paginate v-data-tables
    - Add the "add" logic to a button per row
        - why, why, why can't I make these buttons smaller?




