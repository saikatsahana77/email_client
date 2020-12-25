import smtplib
import speech_recognition as sr
import pyttsx3
from email.message import EmailMessage
import ntpath
import sqlite3

listener = sr.Recognizer()
engine = pyttsx3.init()


def talk(text):
    engine.say(text)
    engine.runAndWait()


def get_info():
    try:
        with sr.Microphone() as source:
            print('listening...')
            voice = listener.listen(source,timeout=0.8,phrase_time_limit=10)
            info = listener.recognize_google(voice)
            print(info)
            return info.lower()
    except:
        pass


def send_email(receiver, subject, message, sender, cc, bcc, attachs):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    conn = sqlite3.connect('emails.db')
    c = conn.cursor()
    c.execute("SELECT password FROM emails where email=:email",{
        "email":sender
    })
    a = c.fetchone()
    psd = a[0]
    conn.commit()
    conn.close()
    # Make sure to give app access in your Google account
    try:
        server.login(sender, psd)
        email = EmailMessage()
        email['From'] = sender
        email['To'] = receiver
        if (subject!=""):
            email['Subject'] = subject
        if (cc!=""):
            email['Cc'] = cc
        if (bcc!=""):
            email["Bcc"] = bcc
        email.set_content(message)
        if (attachs !=[]):
            for attach in attachs:
                with open (attach,"rb") as f:
                    file_data=f.read()
                    file_name=ntpath.basename(f.name)
                email.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)
        server.send_message(email)
        return True
    except:
        return False




def get_email_info():
    talk('To Whom you want to send email')
    receiver = get_info()
    talk('What is the subject of your email?')
    subject = get_info()
    talk('Tell me the text in your email')
    message = get_info()
    talk('Tell me CC Persons if any')
    cc = get_info()
    talk('Tell me BCC Persons if any')
    bcc = get_info()
    return[receiver, subject, message, cc, bcc]


