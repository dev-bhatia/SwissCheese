# Generic Python
import os
import sys
import json
import logging
from datetime import datetime

import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

class MattMAIL:
        """
        Create, Format, & Send Email with Plots/Images/Message.
        """
        def __init__(self, log):
            self._log = log
            self._log.debug('Attempting to create Email Object...')
            try:
                with open('email_credentials.json', 'r') as f:
                    self._creds = json.load(f)
                    self._log.info('Email Object Created')
            except FileNotFoundError:
                self._log.warning('Credentials JSON file not found.')
                self._log.critical('Terminating Program...')
                sys.exit(1)

        def snail_mail(self, developer_mode):
            """
            Gather Plots, and send Email
            """
            self._log.debug('FORMATTING EMAIL...')
            date = datetime.now().strftime('%Y-%m-%d')
            if (developer_mode == "team"):
                self._log.info("Emailing Team...")
                recipiants = self._creds['recipiants']
            else:
                self._log.info("Developer Mode ONLY, Emailing Dev...")
                recipiants = self._creds['beta']
            # Create the root message and fill in the from, to, and subject headers
            msgRoot = MIMEMultipart('related')
            msgRoot['Subject'] = "{} - Mouse Behavior Plots".format(date)
            msgRoot['To'] = " ,".join(recipiants)
            msgRoot['From'] = self._creds['sender']
            msgRoot.preamble = 'This is a multi-part message in MIME format.'

            # Encapsulate the plain and HTML versions of the message body in an
            # 'alternative' part, so message agents can decide which they want to display.
            msgAlternative = MIMEMultipart('alternative')
            msgRoot.attach(msgAlternative)
            # msgText = MIMEText('Alternate Message Error...Inform Dev if this happens.')
            # msgAlternative.attach(msgText)

            # # We reference the image in the IMG SRC attribute by the ID we give it below
            email_msg = ""
            msgText = MIMEText(email_msg, 'html')
            msgAlternative.attach(msgText)

            # Attach Banner
            email_msg += """
                            <font face="courier" size="4">
                            <b>Team,</b><br><br>
                            <font size="2"><b>Updates...</b><br>
                                           1. Error Correction: plan is to integrate slack to "message" our database (hopefully!).<br>
                                           2. ABS Bias Value Correction: Working on counting # of Left Licks<br>
                            </font>
                            <font size="2"><br><b>Please do not hesitate to recommend additional features or bring up issues!</b><br></font><br>
                            </font>
                            <font face="courier" size="3"></b>
                            <b>-- Dev</b><br>
                            <font size="2">Phase 0: BLACK  Phase 1: <font color='red'>RED</font>  Phase 2: <font color='blue'>BLUE</font>  Phase 3: <font color='green'>GREEN</font>  Phase 4: <font color='purple'>PURPLE</font><br><br></font>
                            </font></b>
                         """
            # Attach Plots
            img_count = 2
            for plot in os.listdir("plots"):
                    email_msg += """<img src="cid:image{}"><br>""".format(img_count)
                    img = "plots/{}".format(plot)
                    fp = open(img, 'rb')
                    msgImage = MIMEImage(fp.read())
                    fp.close()
                    tmp = '<image{}>'.format(img_count)
                    msgImage.add_header('Content-ID', tmp)
                    img_count += 1
                    msgRoot.attach(msgImage)
            msgText = MIMEText(email_msg, 'html')
            msgAlternative.attach(msgText)
            s = smtplib.SMTP('smtp.gmail.com:587')
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(self._creds['sender'].split('@')[0], self._creds['password'])
            s.sendmail(self._creds['sender'], recipiants, msgRoot.as_string())
            s.quit()
