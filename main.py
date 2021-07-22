# Get arguments from user
import sys

# Get current time
import datetime

# For connect to the mysql server
import mysql.connector  

# For sleep function
import time

# For randomrange()
import random

# Log errors
import logging

# Settings
import config

# Make connection with telegram
from telethon import TelegramClient, events


##################### LOGGING ##############
# Write all errors to the log file
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y/%m/%d %I:%M:%S %p', filename='errors.log', encoding='utf-8', level=logging.ERROR)


#####################  MYSQL  ##############
# establishing the connection
mydb = mysql.connector.connect(
    host=config.HOST,
    user=config.USER,
    password=config.PASSWORD,
    database=config.DATABASE
)

# creating a cursor object using the cursor() method
cur = mydb.cursor(buffered=True)


##################### TELETHON ################

client = TelegramClient(config.username, config.api_id, config.api_hash) 

async def handler(event):
    msg = str(event.message)
    msg_dict = msg.split('\\n')
    question = ""
    try:
        question = msg_dict[1]
    except:
        logging.warning('In this message was error:')
        logging.error(msg_dict)
                
    # Remove double quotes and single quotes because they can cause error in sql syntax
    question = question.replace('"', '').replace('\'', '')
    query = 'SELECT answer FROM ' + config.TABLE + ' WHERE question = ' + '\"' + question + '\"' + ';'
    cur.execute(query)
    row = cur.fetchone() 
    if row is None:
        # There is no such question in the database
        pass
    else:
        # Send the message
        time.sleep(random.randrange(config.offset, 2 * config.offset))
        await event.respond(row[0])
        with open(config.log_file, "a") as file:
            now = datetime.datetime.now()
            currentTime = now.strftime('%Y-%m-%d %H:%M:%S') 
            file.write(currentTime + "\nq: " + question + "\na: " + row[0] + "\n\n") 

def printHelpMessage():
    print("Usage: python3 main.py [--options]")
    print("Possible options:")
    print("\t-h, --help\t\tCall this function and exit")
    print("\t-e, --english\t\tSend answers to english chat")
    print("\t-r, --russian\t\tSend answers to russian chat")
    print("\nFor example:")
    print("python3 main.py -er\t- send answers to russian and english chats at the same time")
    print("python3 main.py -e\t- send answers only to the english chat")

def main():
    # By default - all chats are untracked
    trackedChat_en      = 'quizarium_en'
    trackedPattern_en   = '.*QUESTION.*'
    trackedChat_ru      = 'Quizarium'
    trackedPattern_ru   = '.*ВОПРОС.*'
    en_chat             = False
    ru_chat             = False

    # Get arguments from shell
    arguments = sys.argv
    if '-h' in arguments or '--help' in arguments:
        printHelpMessage()
        quit()

    if '-e' in arguments or '--english' in arguments:
        en_chat = True

    if '-r' in arguments or '--russian' in arguments:
        ru_chat = True

    if '-re' in arguments or '-er' in arguments:
        ru_chat = True
        en_chat = True
    
    if ru_chat == False and en_chat == False:
        print("Please specify whether you want to use English or Russian chat. Use:")
        print("python3 main.py -h")
        sys.exit("Incorrect usage")

    if ru_chat == True:
        @client.on(events.NewMessage(chats=trackedChat_ru,pattern=trackedPattern_ru))
        async def callHandler(event):
            await handler(event)

    if en_chat == True:
        @client.on(events.NewMessage(chats=trackedChat_en,pattern=trackedPattern_en))
        async def callHandler(event):
            await handler(event)

    client.start()
    client.run_until_disconnected()


if __name__ == "__main__":
    main()
