# **Agile development project**
<br />

## **Introduction of the "Yummy Saviour" Website Service**
**Yummy Saviour (YS)** is a fullstack web-based service (prototype). YS is built using flask framework, with python, html, javascript and css for front and back end. The idea behind YS is that, it is a bridge between restaurants and non-profit organizations (npo), to deliver free foods to people in need. Restaurants offer food that otherwise go to waste available for npo, then npo orders food and distribute to people in need.
<br />

## **Features of YS**
YS has pages like "about" and "blog" for all viewers, to read about the company information, and food waste informatics.
YS website includes features such as sign up, log in and logout (for only validated restaurant and non-profit organization users). For restaurant users, features like add, update and delete food items allow users to manage their items. In addition, a unique feature called "insight" is used to show types and amount of food items have been saved by the restaurant, once items have been ordered by npo users. This gives restaurant users a perspective of their food waste so that they can improve the situation. For npo users, YS has features such as view available food items from all restaurants, add desired items to order list, and confirm orders.
<br />

## **Project Structure**
Currently, program files are placed in the "website" directory while test files are in the "tests" directory. Inside website package, sub-directory "static" contains image files, css, javascript files. Sub-directory "templates" contains all the html fiels. Python files and sqlite database are placed within the "website" directory. Directory ".vscode" contains settings and configuration for visual studio based on our program's requirements and specifics. Setup files are used to correctly find program packages.
<br />

## **Installation of YS program**
Make sure you have python3 and visual studio installed on your pc. Download the project repo from our github at: [Github link](https://github.com/chinita226/agile-development-project). Open project folder with visual studio. Under the project directory, activate virtual environment. Once venv has been activated, under the project directory, type "make install". Our makefile command will install all required packages according to the requirements.txt.
<br />

## **Running the YS website**
After you have completed the steps requried above, with venv being activated, type in terminal "make app", this command will run the flask app from main.py. You will be able to see the website address on the terminal, such as :
 * Serving Flask app "website" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Restarting with stat
Created Database!
 * Debugger is active!
 * Debugger PIN: 162-814-031
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

Click on the http link and you will see the YS website and use it. If it is the first time you run the program, a fresh database file will be generated, modifications of data will be recorded in the database file, therefore as long as the file is not deleted, data is saved in the file even you terminate the program.
<br />

## **Running the program tests**
There are two ways to run the program tests.
1. In venv environment under project directory, type in terminal "make unittest". All tests available will run.
2. We added a button to run tests, you should see a bottle like icon named "testing" when hover, on the left side of visual studio's navigation bar, click the button and run all or certain tests of your choice, and view test files.# fullstack-pythonFlask-groupProject
