#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr

import poplib

# import email
# 错误写法from email.message_from_string import message_from_string
from email import message_from_string
 

# 输入邮件地址, 口令和POP3服务器地址:
email = input('Email: ')
# password = input('Password: ')
# pop3_server = input('POP3 server: ')
password = 'mndbotrtnlqmdddh'
pop3_server = 'pop.qq.com'

def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset

#邮件的Subject或者Email中包含的名字都是经过编码后的str，要正常显示，就必须decode：
def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value

def print_info(msg, indent=0):
    if indent == 0:
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header=='Subject':
                    value = decode_str(value)
                else:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
            print('%s%s: %s' % ('  ' * indent, header, value))
    if (msg.is_multipart()):
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            print('%spart %s' % ('  ' * indent, n))
            print('%s--------------------' % ('  ' * indent))
            print_info(part, indent + 1)
    else:
        content_type = msg.get_content_type()
        if content_type=='text/plain' or content_type=='text/html':
            content = msg.get_payload(decode=True)
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
            print('%sText: %s' % ('  ' * indent, content + '...'))
        else:
            print('%sAttachment: %s' % ('  ' * indent, content_type))

# 连接到POP3服务器:
# server = poplib.POP3(pop3_server)
# Error: b'-ERR Login fail. A secure connection is requiered(such as ssl). More information at http://service.mail.qq.com/cgi-bin/help?id=28'
server = poplib.POP3_SSL(pop3_server)
# 可以打开或关闭调试信息:
server.set_debuglevel(1)
# 可选:打印POP3服务器的欢迎文字:
print(server.getwelcome().decode('utf-8'))

def server_stat(server):
    # stat()返回邮件数量和占用空间:
    print('Messages: %s. Size: %s' % server.stat())
    # list()返回所有邮件的编号:
    resp, mails, octets = server.list()
    # 可以查看返回的列表类似[b'1 82923', b'2 2184', ...]
    print('mails>>',mails)

    # 获取最新一封邮件, 注意索引号从1开始:
    index = len(mails)#新邮件？？？？？？？？
    print('index>>',index)
    resp, lines, octets = server.retr(index)
    # lines存储了邮件的原始文本的每一行,
    # 可以获得整个邮件的原始文本:
    msg_content = b'\r\n'.join(lines).decode('utf-8')

    # 稍后解析出邮件:
    #！！！！Message对象本身可能是一个MIMEMultipart对象，即包含嵌套的其他MIMEBase对象，嵌套可能还不止一层
    msg = Parser().parsestr(msg_content)
    print_info(msg)

    # 可以根据邮件索引号直接从服务器删除邮件:
    # server.dele(index)

def email_message(server):
    # stat()返回邮件数量和占用空间:
    allemail = server.stat()
    print('Messages: %s. Size: %s' % allemail)

    # 参考https://blog.csdn.net/yatere/article/details/6654647  实际代码
    # 取出信件头部。注意：top指定的行数是以信件头为基数的，也就是说当取0行，
    # 其实是返回头部信息，取1行其实是返回头部信息之外再多1行。
    topemail = server.top(allemail[0], 0)
    emaillist = []


    # 参考https://blog.csdn.net/guogaoan/article/details/37034473
    # 提取当前收件箱中最新的一封邮件，由于邮件数据是经过编码的，这里我们依次尝试utf8、gbk、big5三种编码格 式进行解码，并提取邮件标题部分数据
 

    '''
    type=messageString.get_content_charset()
    #if type=='gb2312':
    #   unicode(messageString.get_payload(),'gb2312')
    #if type=='shift_jis':
    #   unicode(messageString.get_payload(),'shift_jis')
    #if type=='None':
    #   unicode(messageString.get_payload(),'utf-8')
    '''
    for item in topemail[1]:
        try:
            emaillist.append(item.decode('utf8'))
        except Exception as e:
            try:
                emaillist.append(item.decode('gbk'))
            except Exception as e:
                emaillist.append(item.decode('big5'))
    emailmsg = message_from_string('\n'.join(emaillist))
    emailsub = decode_header(emailmsg['subject'])
    # 其中emailsub通常包括两个信息，一个是编码后的标题文本数据，另一个 是其编码格式，所以我们还需要再进行一次解码，这时获得的才是真正可用的标题文本数据。
    if emailsub[0][1]:
        submsg = emailsub[0][0].decode(emailsub[0][1])
    else:
        submsg = emailsub[0][0]
    return submsg

try:
    # 身份认证:
    server.user(email)
    server.pass_(password)
except Exception as e:
    print('Error:', e)
    # 幸好打印错误码，不然一脸懵逼
    # 参考https://blog.csdn.net/qq_41104478/article/details/78581400
    print('读取邮件登录失败') 
    # exit()
else:
    # 如果没有错误发生，可以在except语句块后面加一个else
    # server_stat(server)
    submsg = email_message(server)
    print('submsg>>\n',submsg)

    # 关闭连接:
    server.quit()
    print('server.quit')
finally:
    # except执行后，都会执行，
    # 执行完except后，如果有finally语句块，则执行finally语句块
    print('finally...')


# def pop_connect(self):
#    try:
#        self.reademail = poplib.POP3_SSL(self._pop_server)
#        self.reademail.user(self._addr)
#        self.reademail.pass_(self._password)
#        self.allemail = self.reademail.stat()
# except: print('读取邮件登录失败') exit()

# def receive_email(self):
#    self.pop_connect()
#    topemail = self.reademail.top(self.allemail[0], 0)
#    emaillist = []
#    for item in topemail[1]:
#        try:
#            emaillist.append(item.decode('utf8'))
#     except: try:
#                 emaillist.append(item.decode('gbk'))
#             except:
#                 emaillist.append(item.decode('big5'))
#     emailmsg = email.message_from_string('\n'.join(emaillist))
#     emailsub = email.header.decode_header(emailmsg['subject'])
#     if emailsub[0][1]:
#         submsg = emailsub[0][0].decode(emailsub[0][1])
#     else:
#         submsg = emailsub[0][0]
#     return submsg



