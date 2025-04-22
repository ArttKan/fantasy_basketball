# Fantasy Basketball
## Functionality
A "Fantasy Basketball" application that allows users to simulate basketball games in a basketball league.
Functionalities include:
- user login and registration (the default dataset includes an admin user with password 'admin')
- adding teams, players in teams and games between teams
- tracking statistics of players and records of teams
- editing and deleting players and teams
- display of teams, players and games
 ## Testing with Large Datasets
 In the repository there is a seed.py script that generates a large amount of all data items. The application remains functional but slow and impractical. Loading the main page takes around 15 seconds with the generated dataset. Paging or indexing is not found in this application so no comparison times with more efficient solutions is available.
 ## Installing the Application
 Clone the repository to your directory of choice.  
 Install `flask` with:
 ```
 pip install flask
 ```
Install the virtual environment with:  
 ```
python3 -m venv venv
 ```
 Initialise the database with:  
  ```
sqlite3 database.db < schema.sql
python3 -m init_seed
 ```
 Enter the virtual environment with:  
 ```
 source venv/bin/activate
 ```
 Run the application with:  
  ```
flask run
 ```
 You can find the app running in your browser at 127.0.0.1  
