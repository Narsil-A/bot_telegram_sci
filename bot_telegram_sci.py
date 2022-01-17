import re
from flask import Flask, request
import telegram
from Telebot.credentials import bot_token, bot_user_name,URL


global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
   # retrieve the message in JSON and then transform it to Telegram object
   update = telegram.Update.de_json(request.get_json(force=True), bot)

   chat_id = update.message.chat.id
   msg_id = update.message.message_id

   # Telegram understands UTF-8, so encode text for unicode compatibility
   text = update.message.text.encode('utf-8').decode()
   # for debugging purposes only
   print("got text message :", text)
   # the welcoming message
   if text == "/start":
       # print the welcoming message
       bot_welcome = """
       Welcome to Sciences Dictionary Bot, this bot is using the service from https://sciencenotes.org, to check out a science word in the dictionary and the bot will reply the definition of that word.
       """
       # send the welcoming message
       bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)


   else:
       try:
           # clear the message we got from any non alphabets
           text = re.sub(r"\W", "_", text)
           # api link for the source of definitions 
           url = "https://sciencenotes.org/ph-indicator-chart-colors-and-ranges/".format(text.strip())
           # reply with the definitions 
           # note that you can send photos by url and telegram will fetch it for you
           bot.sendPhoto(chat_id=chat_id, photo=url, reply_to_message_id=msg_id)
       except Exception:
           # if things went wrong
           bot.sendMessage(chat_id=chat_id, text="There was a problem in the name you used, please enter different name", reply_to_message_id=msg_id)

   return 'ok'

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
   s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
   if s:
       return "webhook setup ok"
   else:
       return "webhook setup failed"

@app.route('/')
def index():
   return '.'


if __name__ == '__main__':
   app.run(threaded=True)
