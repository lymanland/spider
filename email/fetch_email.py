#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr

import poplib

# 输入邮件地址, 口令和POP3服务器地址:
# email = input('Email: ')
# password = input('Password: ')
# pop3_server = input('POP3 server: ')

email = '3180541807@qq.com'
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

# try:
#     # 身份认证:
#     server.user(email)
#     server.pass_(password)
# except: 
#     print('读取邮件登录失败') 
#     exit()

try:
    # 身份认证:
    server.user(email)
    server.pass_(password)
except Exception as e:
    print('Error:', e)
    # 幸好打印错误码，不然一脸懵逼
    # 参考https://blog.csdn.net/qq_41104478/article/details/78581400
else:
    # 如果没有错误发生，可以在except语句块后面加一个else
    server_stat(server)
    # 关闭连接:
    server.quit()
    print('server.quit')
finally:
    # except执行后，都会执行，
    # 执行完except后，如果有finally语句块，则执行finally语句块
    print('finally...')



