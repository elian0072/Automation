#! python

import smtplib
from email.message import EmailMessage
import os
import requests
import json
import logging
import datetime

######## INITIALIZATION ###########

logging.basicConfig(filename='logs.txt', level=logging.INFO,
 format='%(asctime)s -- %(levelname)s : %(message)s')

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
myFile = os.path.join(THIS_FOLDER, r'Data/configs.json')

EMAIL_ADDRESS = os.environ.get('GMAIL_USER')
EMAIL_PASSWORD = os.environ.get('GMAIL_PSWD')
MAIL_SUBJECT = 'Weather Report [Pyhton Script]'
MAIL_SMTP = 'smtp.gmail.com'

logging.info(EMAIL_ADDRESS)
logging.info(EMAIL_PASSWORD)

with open(myFile) as config_json:
    config = json.load(config_json)


######## FUNCTIONS ###########

def makeRequest():
    payload = {'token':config['parameters']['secretKey'], 'insee': config['parameters']['location']}
    r = requests.get(config['parameters']['endpoint'], params=payload)
    data = json.loads(r.text)['forecast']
    logging.info('Request done')
    return data

def formatMailMessage(data):
    weather = config['weather'][str(data['weather'])]
    maxTemp = data['tmax']
    minTemp = data['tmin']
    probarain = data['probarain']

    message = "Prévision météo du jour:\n\nPrévision: "+str(weather)+\
    "\nTempérature minimal: "+ str(minTemp) + " degrés"+ \
    "\nTempérature maximal: "+ str(maxTemp) +" degrés"+\
    "\nProbabilité de pluie: "+ str(probarain)+"%"+\
    "\nRapport généré le " + datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    logging.info('Message formatted')
    return message

def sendMailReport(message):
    msg = EmailMessage()
    msg['Subject'] = MAIL_SUBJECT
    msg['From']= EMAIL_ADDRESS
    msg['To']= ['Jaime <jaime.balbuena@me.com>']
    msg.set_content(message)

    try:
        with smtplib.SMTP_SSL(MAIL_SMTP, 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        logging.info('Mail sent')
    except Exception:
        logging.exception('Something went wrong with sending the email')

def main():
    logging.info('Start Main')
    data = makeRequest()
    message = formatMailMessage(data)
    sendMailReport(message)
    logging.info('End Main')


######## MAIN ###########

main()
