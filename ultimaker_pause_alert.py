#!/usr/bin/python3
### BEGIN INIT INFO
# Provides:          pause_alert.py
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start daemon at boot time
# Description:       Enable service provided by daemon.
### END INIT INFO

import systemd.journal
import socket
from time import sleep
import smtplib
import email
from smtplib import SMTP
from email.message import EmailMessage
import datetime


def main():
  j = systemd.journal.Reader()
  j.seek_tail()
  j.get_previous()
  while True:
    event = j.wait(1000000)
    if event == systemd.journal.APPEND:
      for entry in j:
         print (entry['MESSAGE'] + " " + str(datetime.datetime.now()))
         alertmail(entry['MESSAGE'])

def alertmail(logEntry):
    # returns first occurrence of Substring
    trigger_text = 'pause'
    result = logEntry.find(trigger_text)
    if (logEntry.find(trigger_text) != -1):
        print ("Contains '" + trigger_text + "' at index:", result)
        msg = EmailMessage()
        msg.set_content(str(datetime.datetime.now()) + " \n " + logEntry)
        msg['Subject'] = ' '.join(logEntry[24:].split())
        msg['From'] = "ultimaker@mail.bellariastrasse.com"
        msg['To'] = "adriano.aguzzi@usz.ch"

        smtp = smtplib.SMTP('mail.bellariastrasse.com', port='587')
        smtp.ehlo()  # send the extended hello to our server
        smtp.starttls()  # tell server we want to communicate with TLS encryption
        smtp.login('ultimaker@mail.bellariastrasse.com', 'scrap10')  # login to our email server

        # send our email message 'msg' to our boss
        smtp.send_message(msg)
        smtp.quit()  # finally, don't forget to close the connection
    else:
        print ("Doesn't contain substring '" + trigger_text +"'")

if __name__ == '__main__':
    main()