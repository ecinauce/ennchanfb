#Python libraries that we need to import for our bot
import random
from flask import Flask, request
from pymessenger.bot import Bot

application = Flask(__name__)
ACCESS_TOKEN = 'EAAHACooBbO4BAFBrZCdwkWVzYZCqTGOxAuvcfQmAm8vwoMBCj9jILw1nrU7cOZCpmZCzgBCoMPa2vCZCQ8C6ZBjpm66PNchnpOhZAnJVyScUiGUqoPbuBntLllLKWebgjsNbsFOaWq7JfLZAXbw9iRdACJtKXSoHZCp6cYgMwW0vQbAZDZD'
VERIFY_TOKEN = 'mikestesticlesaremassive'
bot = Bot(ACCESS_TOKEN)

#We will receive messages that Facebook sends our bot at this endpoint 
@application.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook.""" 
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    #if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
       output = request.get_json()
       for event in output['entry']:
          messaging = event['messaging']
          for message in messaging:
            if message.get('message'):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    response_sent_text = get_message(message['message']['nlp'])
                    send_message(recipient_id, response_sent_text)
                #if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    response_sent_nontext = get_message()
                    send_message(recipient_id, response_sent_nontext)
    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


#chooses a random message to send to the user
def get_message(entities):
    setEntity = []
    stringEntity = ""
    
    sample_responses = ["You're supposed to be working.", "How are your friends doing?", "Have you dealt with your problems yet?", "Please, do go on. I'm listening."]
    for key, val in entities.items():
      setEntity.append(key)
    for entry in setEntity:
      stringEntity = stringEntity + ", "
    # return selected item to the user
    return random.choice("I think you said something on the lines of "+ stringEntity+ ", or maybe something else. " +sample_responses)

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
  #Deployment script
  application.run(host='0.0.0.0', port=8080)
  #Development script
  #application.run(host='localhost', port=80, debug=True)