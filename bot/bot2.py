import os
import psycopg2
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# datbase information
DATABASE_NAME = "movies"
DB_USER = "preetham"
DB_PASSWORD = "password"
DB_HOST = "o.tcp.in.ngrok.io"
DB_PORT = "16544"

# postsql database
DATABASE_URL = f"dbname={DATABASE_NAME} user={DB_USER} password={DB_PASSWORD} host={DB_HOST} port={DB_PORT}"
conn = psycopg2.connect(DATABASE_URL, sslmode='require')

# telegram bot section
BOT_TOKEN = "6775951160:AAGQ3mnH1Nmae1WLQeskIM6TUDBj43sE5Js"
updater = Updater(BOT_TOKEN, use_context=True)

# response section
def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Welcome! Please send me the name of the file you're looking for.")

# search  main function
def search_file(update, context):
    file_name = update.message.text
    file_name = update.message.text.lower()   #coverts input into lower case
    result = search_in_database(file_name)    # calls the function with search algorithm
    if result:
        context.bot.send_message(chat_id=update.message.chat_id, text=f"File found! Here is the link: {result}")
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text="File not found.")

# function with search algorithm
def search_in_database(file_name):
    
    try:
        cursor = conn.cursor()

        # Use ILIKE for case-insensitive partial string matching
        query = "SELECT file_link FROM files_table WHERE file_name ILIKE %s LIMIT 1;"
        cursor.execute(query, ('%' + file_name + '%',))

        result = cursor.fetchone()

        if result:
            return result[0]  # Return the file link if found
        else:
            return None

    except psycopg2.Error as e:
        print("Error connecting to PostgreSQL database:", e)
        return None

    finally:
        if cursor:
            cursor.close()

# main function
def main():
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, search_file))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
