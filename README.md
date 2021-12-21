# High Mi-stakes by TheMistakes
TheMistakes - Alif Abdullah, Daniel Sooknanan, Jesse Xie, Raymond Yeung  
Softdev  
P01 -- ArRESTed Development  

## Roster + Roles
Jesse (PM): Manage backend development of database, facilitate interactions with python  
Alif: Manage development of python code, establish interactions between flask and python  
Daniel: Manage front end development, create easy to use interface  
Raymond: Manage API data retrieval, ensure proper utilization of APIs  

## Project Summary  
Our web application allows users to create an account and earn points / items through playing blackjack. Points, which are earned from winning games of blackjack, may be used to purchase items from the shop that are available to the user. These solely cosmetic items that will decorate their profile and ranking on the leaderboard, including but not limited to name color and profile picture. The player will be randomly awarded some of these cosmetics as they win a game of blackjack. The leaderboard will rank and display all players based on the number of wins they have.

## Install and Launch Instructions
Clone the repository in your desired destination:  
`$ git clone git@github.com:JesseStuy20/TheMistakes.git`  

Create a virtual environment:  
`$ python3 -m venv venv`  

Activate the virtual environment:
- On Mac/Linux: `$ source venv/bin/activate`  
- On Windows: `$ source venv/Scripts/activate` 

Change your directory to the cloned repository:  
`$ cd TheMistakes/`  

Install required modules/packages:  
`$ pip install -r requirements.txt` 

Change your directory to the app folder:  
`$ cd app/`  

Start the flask app:  
`$ python3 __init__.py` 

Navigate to the website:  
Copy and paste this link into the search bar: `http://127.0.0.1:5000/` 
