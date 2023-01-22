from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import re
from datetime import date,datetime
import smtplib
from email.message import EmailMessage
import ssl
import os


url = "https://tadkirati.chan2022.dz/fr/events/search"
filename = "result.txt"



def sendMail(date_match,remaing_day,title):
    sender = 'technology.watching.dz@gmail.com'
    sender_password = os.getenv("GMAIL_PSSWD")

    subject ="NOTIFIER"
    receiver = 'issiakhem.mohamedramzi@gmail.com'
    body = "Il reste " + str(remaing_day) + " jours avant le Match " + title
    try:
        em = EmailMessage()
        em['To']  = receiver
        em['From'] = sender
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(sender,sender_password)
            smtp.sendmail(sender,receiver, em.as_string())
            print("Successfully sent email")
            writeDate(date.today())
    except:
        return False

def writeDate(date):
    f = open(filename,'w+')
    datetim = datetime.combine(date, datetime.min.time())
    datetim = datetim.strftime("%Y-%m-%d")
    f.write(datetim)
    f.close()

def calculate_time(date_match):
    date_today = date.today()
    date_file = date_today
    go = False

    try:
        with open(filename,"r") as f:
            line = f.readline()
            date_f =  datetime.strptime(line,"%Y-%m-%d")
            date_file = date_f.date()
            f.close()
    except IOError:
        writeDate(date_today)
        go = True
    
    if (date_today != date_file) or go:
        print(date_file)
        print(date_today)
        # difference between dates in timedelta
        delta = date_match - date_today
        if (delta.days == 0):
            return [date_match,delta.days]
        if (delta.days <= 3):
            return [date_match,delta.days]
    else:
        return []          






opts = Options()
opts.add_argument(' — headless')
driver = webdriver.Chrome('chromedriver', options=opts)

driver.get(url)
driver.implicitly_wait(220)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight,)")
time.sleep(2)

soup = BeautifulSoup(driver.page_source, 'html.parser')
list_match_div= list(soup.findAll('div',class_='MuiBox-root ltrmui-1puescb'))

for match_div in list_match_div:
        

    title = match_div.find("p",class_="MuiTypography-root MuiTypography-body1 ltrmui-pib2jw")
    title = title.text
    title = title.lower()
    
    if (re.search("niger|algérie|algerie",title)):
        day_timestamp = match_div.find('time')                                                                                                                                                                                                                                                                                          
        day_timestamp = day_timestamp["datetime"]
        day_timestamp = float(day_timestamp[:-3])
        match_date = date.fromtimestamp(day_timestamp)
        
        state = calculate_time(match_date)
        
        if state != []:
            try:
                sendMail(state[0],state[1],title)    
            except:
                exit(0)
        else:
            exit(0)   
    