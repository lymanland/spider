from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

PASSWORD = 'mndbotrtnlqmdddh'
FROM_ADDR = '***********@qq.com'
ADDR = input('Email: ')
SMTP_SERVER = 'smtp.qq.com'

class Email:
    def __init__(self):
        self._smtp_server = SMTP_SERVER
        self._addr = ADDR
        self._password = PASSWORD
        # Exception has occurred: smtplib.SMTPSenderRefused
        # (501, b'mail from address must be same as authorization user', '944589610@qq.com')
        self._from_addr = ADDR##FROM_ADDR
    def smtp_connect(self):
        try:
            self.sendemail = smtplib.SMTP_SSL(self._smtp_server, 465)
            self.sendemail.login(self._addr, self._password)
        except Exception as e:
            print('发送邮件登录失败') 
            print('Error:', e)
            exit()
    def send_email(self):
        self.smtp_connect()
        msg = MIMEText('')
        msg['Subject'] = '设置完毕'
        msg['From'] = self._from_addr
        msg['To'] = self._addr
        self.sendemail.sendmail(self._from_addr, self._addr, msg.as_string()) 
        self.sendemail.close()


# def check_shutdown(self):
#        submsg_list = self.receive_email().split()
#        print('最新邮件主题:', ' '.join(submsg_list))
#        sd_type = submsg_list[0]
#        if sd_type == '延时关机':
#            sd_time = '60'
#            if len(submsg_list) > 1:
#                    sd_time = submsg_list[1]
#            command = 'shutdown -s -t ' + sd_time
#        elif sd_type == '定时关机':
#            sd_time = '00:00'
#            if len(submsg_list) > 1:
#                    sd_time = submsg_list[1]
#            command = 'schtasks /create /TN %s /ST %s /sc DAILY /TR "shutdown /s"' %(sd_type, sd_time) 
#        if '关机' in sd_type:
#            os.system(command)
#            print('执行命令:', command)
#            self.reademail.quit()
#            return True
#        else:
#            return False

def main():
    mail = Email()
    mail.send_email()
#    while True:
#        time.sleep(5)
#         print('等待关机信号.....') 
#         if mail.check_shutdown(): 
#             mail.send_email()

main()