import smtplib
server = smtplib.SMTP(email_server_ip)
msg = 'Eat more spam and eggs!'
server.sendmail('from@me.com', 'to@you.com', msg)
server.quit()
