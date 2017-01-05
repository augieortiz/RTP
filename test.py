import smtplib

sender = 'research@test.research.me'
receivers = ['augie@devao.me']

message = """From: Research Request <research@test.research.me>
Subject: Access Request

This is a request from the test environment for a new user account.  Below is the information submitted.

Name: %s
Email: %s


Request statuses is completely up to the discretion the research team.

Thanks,
researchDevAO
"""

email = "augieortiz@me.com"
name = "Agustin Ortiz"

try:
   smtpObj = smtplib.SMTP('localhost')
   smtpObj.sendmail(sender, receivers, message % (name, email))         
   print "Successfully sent email"
except SMTPException:
   print "Error: unable to send email"