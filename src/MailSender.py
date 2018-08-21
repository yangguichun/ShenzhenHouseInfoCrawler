import smtplib
from email.mime.text import MIMEText
from email.header import Header
from src.utils import utils
import configparser
import sys, os

class MailSender:
    @classmethod
    def __read_mailer_sender_info(cls):
        mail_info = {}
        config = configparser.ConfigParser()
        try:
            read_ok = config.read('{}\config.ini'.format(sys.path[0]), encoding='utf-8-sig')
            print(str(read_ok))
            section = 'mail'
            mail_info['host'] = config.get(section, 'host')
            mail_info['user'] = config.get(section, 'user')
            mail_info['pass'] = config.get(section, 'pass')
            mail_info['sender'] = config.get(section, 'sender')
            mail_info['receivers'] = config.get(section, 'receivers')
            if mail_info['host']== '' or mail_info['user']==''  or mail_info['pass']=='' or mail_info['sender']=='' or mail_info['receivers']=='':
                utils.print('读取邮件配置信息失败: 配置内容为: {}'.format(str(mail_info)))
                return None
            return mail_info

        except Exception as e:
            print(' 读取配置文件出错.')
            print(e)
            return None


    @classmethod
    def send_alarm_message(cls, title, msg):
        mail_info = cls.__read_mailer_sender_info()
        if mail_info is None:
            return

        mail_host = mail_info['host']
        mail_user = mail_info['user']
        mail_pass = mail_info['pass']
        sender = mail_info['sender']
        receivers = mail_info['receivers'].split(',')  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

        try:
            message = MIMEText(msg, 'plain', 'utf-8')
            message['From'] = Header("系统监视进程", 'utf-8')
            message['To'] = Header("接收人", 'utf-8')
            message['Subject'] = Header(title, 'utf-8')
            smtpObj = smtplib.SMTP()
            smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
            smtpObj.login(mail_user, mail_pass)
            smtpObj.sendmail(sender, receivers, message.as_string())
            print("邮件发送成功")
            return True
        except smtplib.SMTPException as e:
            print("Error: 无法发送邮件")
            print(e)
            return False
        except Exception as e:
            print("Error: 无法发送邮件")
            print(e)
            return False
