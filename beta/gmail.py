#** apricot.R = 0 **#
def gmail(toby, sub, txt):
    pass

#** apricot.R = 1 **#
def gmail(toby, sub, txt):
    password = getpass.getpass()
    print "Sending... Please wait for a while."
    to = "{}@gmail.com".format(toby)
    by = "{}@gmail.com".format(toby)
    #txt = "This mail was sent by apricotPie."
    host, port = 'smtp.gmail.com', 465
    msg = MIMEText(txt)
    msg['Subject'] = sub
    msg['From'] = by
    msg['To'] = to

    smtp = smtplib.SMTP_SSL(host, port)
    smtp.ehlo()
    smtp.login(by, password)
    smtp.mail(by)
    smtp.rcpt(to)
    smtp.data(msg.as_string())
    smtp.quit()
