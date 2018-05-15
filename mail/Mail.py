import smtplib
import argparse
import time
from email.mime.text import MIMEText
from Logger import Logger

class Mail:

    def __init__(self):
        self.log = Logger()
        self.log.info('Initialized custom email class')

    def send_email(self,email_list,email_sub,email_body):
        '''    
            This method can be used to send email to the recipients specified
            arg1 - List of email recipients separated by commas in a list. Example [user1@cisco.com,user2@cisco.com]
            arg2 - Subject for email
            arg3 - Email Body to be sent out
        '''    
        flag = 0 
        counter = 10
        recipients = email_list
        email_list = email_list.split(',')
        while counter>0:
            try:
                self._construct_email(email_list,email_sub,email_body)

                self.log.info('\n********************************************************')
                self.log.info('Email will be sent to: ' + str(recipients) + '\n')
                self.log.info('Email subject: ' + str(email_sub) + '\n')
                self.log.info('Email body: \n\n' + str(email_body) + '\n\n\n' + 'Please contact nraamanu@cisco.com if you have any questions')
                self.log.info('********************************************************\n')

                flag = 1 
                counter = 0 
            except:
                time.sleep(1)
                counter -= 1
                continue

        if flag == 1:
            self.log.info("\nEmail was sent successfully!\n")
            return True
        else:
            self.log.info("\nEmail sending Failed. Please check!\n")
            return False

    def _construct_email(self,to,sub,body):

        msg = MIMEText(body)

        me = 'avs-admin@cisco.com'
        msg['Subject'] = sub
        msg['From'] = me
        msg['To'] = ','.join(entry.strip() for entry in to)

        server = smtplib.SMTP('email.cisco.com')
        server.sendmail(me, to, msg.as_string())
        server.quit()
