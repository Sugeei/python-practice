# coding=utf8

from os.path import basename
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import base64
from config import logger


class MailInformer(object):
    def __init__(self, mail_source, mail_target=None):
        # mail_source = json.loads(mail_source_str, 'utf-8')
        # mail_target = json.loads(mail_target_str, 'utf-8')
        self.host = mail_source['host']
        self.port = mail_source['port']
        self.source = mail_source['source']
        self.username = mail_source['username']
        self.password = mail_source['password']
        self.target = mail_source['target']
        # self.target = mail_target['target']
        # self.target = mail_target['target']
        self.subject = mail_source['subject']
        self.msg = None

    def send_simple_email(self, content, type):

        self.msg = MIMEText(content, type, 'utf-8')
        self.__send_email()

    def send_appendix_email(self, content, type, files):
        # Use Jinjia2 template to format the messages.
        body = MIMEText(content, type, 'utf-8')
        self.msg = MIMEMultipart()
        self.msg.attach(body)
        #
        # appendix = MIMEBase('application', 'octet-stream')
        # appendix.set_payload(open(packmsg, 'rb').read())
        # Encoders.encode_base64(appendix)
        # self.msg.attach(appendix)
        for f in files:
            try:
                with open(f.encode('utf-8'), "rb") as fi:
                    part = MIMEApplication(fi.read(), Name=basename(f))
                    part[
                        'Content-Disposition'] = 'attachment; filename="%s"' % basename(
                        f)
                    part["Content-Type"] = 'application/octet-stream'
                    part.add_header('Content-Disposition', 'attachment',
                                    filename='=?utf-8?b?' + base64.b64encode(
                                        f.encode('UTF-8')) + '?=')
                    # Encoders.encode_base64(part)
                    self.msg.attach(part)
            except Exception:
                with open(f, "rb") as fi:
                    part = MIMEApplication(fi.read(), Name=basename(f))
                    part[
                        'Content-Disposition'] = 'attachment; filename="%s"' % basename(
                        f)
                    part["Content-Type"] = 'application/octet-stream'
                    part.add_header('Content-Disposition', 'attachment',
                                    filename='=?utf-8?b?' + base64.b64encode(
                                        f.encode('UTF-8')) + '?=')
                    # Encoders.encode_base64(part)
                    self.msg.attach(part)

        self.__send_email()

    def __send_email(self):
        self.msg['From'] = ";".join(self.source)
        self.msg['To'] = self.target
        # self.msg['To'] = ";".join(self.target)
        self.msg['subject'] = self.subject
        try:
            server = smtplib.SMTP(self.host, self.port)
            server.ehlo()
            server.starttls()
            server.login(self.username, self.password)
            # sendmail()方法就是发邮件，由于可以一次发给多个人，所以传入一个list，邮件正文是一个str，as_string()把MIMEText对象变成str
            server.sendmail(self.source, self.target, self.msg.as_string())
            logger.info(u"邮件发送成功!")
            server.quit()
        except smtplib.SMTPException:
            logger.exception(u"Error: 无法发送邮件")


if __name__ == "__main__":
    mail_source = {"host": "idccellopoint.datayes.com", "port": 587,
                   "username": "svc-pipeline", "password": "Wmcl0ud@2018",
                   "source": "svc-pipeline@datayes.com"}
    mail_target = {"subject": "test", "target": ["xi.cheng@datayes.com"]}

    mail_informer = MailInformer(mail_source, mail_target)
    mail_informer.send_simple_email("hhhh", 'html')
    pass
