Sometimes I played in [Quizarium](https://quizarium.com/) and often I don't know answer to that questions. So I decided to cheat and write a program that answers to questions and earn points for me. For educational purposes, of course :D (don't cheat for real)  
Such as I didn't find a site with answers for english version of Quizarium, I decided to make my own site with ~~blackjack and hookers~~ answers. I wrote a script that read all questions and surely answers to them and save this information to database. I really don't know how to create a beautiful website with phpmyadmin, databases and etc. so I figured I'd make a dump with my local database and host it in this repo. Everyone can easily download it and update using git pull. I also wrote a script that will do a database dump every day and do a git push to this repository. In my opinion that's make sense

#### What actually do this program?
This program trying to find answers in the database and if found it - sends answer to the specified chat. That can help you to earn some points in the game.  
There are 28932 rows in the database at the moment  

### Installation
0. First check if you have `mysql` installed and make sure that your database management system is configured correctly. You can install and configure it according to [this tutorial](https://dev.mysql.com/doc/mysql-getting-started/en/)
1. Clone this repo: `git clone git@github.com:danillucky1234/quizarium-hack.git`
2. Move to the downloaded directory: `cd quizarium-hack`
3. Enter to mysql command prompt: `mysql -u <your mysql username> -p`  
Then you should type your password and create a new database, such as: `CREATE DATABASE quizarium;`  
4. When you created new database you can exit from mysql prompt by typing `quit` and go to the command line. Let's add all rows to your new database:  
`mysql -u <your mysql username> -p <newly created database name> < quizarium.sql`  
That's fine, from now you have a big dump of database with answers.
5. Next, we need to change the settings in the `config.py` file. But before that we have to write the following command in the terminal `git update-index --assume-unchanged config.py` so that the git knows that this file should not be indexed (this will be useful when we update the database, so it does not cause errors when merge config.py). We need to change api\_id, api\_hash and username. All these values are necessary for [telethon](https://docs.telethon.dev/en/latest/basic/installation.html) to interact correctly with your account. So let's get started.  
  5.1 You need to [log in to your account](https://my.telegram.org/) with your phone number and go to the API Development tools section.  
  5.2 After that create `New application` and fill in `App title` & `Short name`. The other fields are optional and you don't have to fill them in. By the way, you can change these two fields later.  
Click on `Create application` at the end. Remember that your **<ins>API hash is secret</ins>** and Telegram won't let you revoke it. <ins>Don't post it anywhere!</ins>  
  5.3 Copy `api_id` and put it in the right field in the file `config.py`  
  5.4 Copy `api_hash` and paste it into the right field in `config.py` file  
  5.5 Set your username from telegram in the `config.py` file. In my case `username = 'danil'`  
  5.6 Set your username, host, password and database name from mysql in `config.py`  
6. Install python dependencies: `pip3 install -r requirements.txt`.
7. Read the help message, which options are possible `python3 main.py -h`  
7. Run the project `python3 main.py -e` and earn new points in the game!

> **_NOTE_**: When you run the program for the first time, you may see a message that you need to log in, by entering the phone number to which the account is registered, along with sms verification. After you enter all these data, they will be saved in the file \<your username\>.session and you will not need to enter these data again. 

### How to update mysql database?
1. In the working directory type  
`git pull`  
2. And then update existing db:  
`mysql -u <your mysql username> -p <database name> < quizarium.sql`  

#### Possible options
| Key variations | Explanation  |
| :------------- | -----------: |
| -h, --help     | Show the help message and exit |
| -e, --english  | Send answers to english chat |
| -r, --russian  | Send answers to russian chat |
| -er, -re       | Send answers to russian and english chats at the same time | 
