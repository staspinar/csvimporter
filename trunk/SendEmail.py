# import smtplib from std library
import smtplib
# connect to your email server
server = smtplib.SMTP(email_server_ip)
# your message
msg = 'Eat more spam and eggs!'
# send the email
server.sendmail('from@me.com', 'to@you.com', msg)
# terminate the session and quit
server.quit()
