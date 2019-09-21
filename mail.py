#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
File: mail.py
Author: lee
Email: yourname@email.com
Github: https://github.com/yourname
Description:
"""
import os
import smtplib
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

import yaml


class KindleSync:
    """
    Kindle Sync Tool
    """

    def __init__(self, sender, receivers, smtp, password):
        self.sender = sender
        self.receivers = receivers
        self.smtp = smtp
        self.password = password
        self.attaches = []
        self.create_msg()

    def create_msg(self):
        """ create message"""
        self.msg = MIMEMultipart()
        self.msg['From'] = formataddr(["Kindle 管理员", self.sender])
        self.msg['To'] = formataddr(["kindle", self.receivers[0]])
        self.msg['Subject'] = "电子书同步"

    def add_attachs(self, files):
        """添加多个附件"""
        for file in files:
            self.add_attach(file)

    def add_attach(self, filename):
        """ 添加附件"""
        self.attaches.append(filename)
        att = MIMEApplication(open(filename, 'rb').read())
        att.add_header(
            'Content-Disposition',
            'attachment',
            filename=Header(filename, "utf-8").encode())
        self.msg.attach(att)

    def sync(self):
        """ sync """

        if self.attaches == []:
            print("没有附件!")
            return

        title = "\r\n".join(self.attaches)
        self.msg.attach(MIMEText(title, 'plain', 'utf-8'))

        try:
            server = smtplib.SMTP(self.smtp)
            server.login(self.sender, self.password)
            server.sendmail(self.sender, self.receivers, self.msg.as_string())
            print("*邮件* \r\n%s\r\n  发送成功!" % (title))

            for file in self.attaches:
                os.remove(file)
        except smtplib.SMTPException:
            print("Error: 无法发送邮件")


def is_ebooks(filename):
    """is ebook"""
    exts = [".mobi", ".epub", ".pdf", ".jpeg"]
    return any([filename.endswith(ext) for ext in exts])


def main():
    """main"""
    config = yaml.load(open("config.yaml"))

    files = list(filter(is_ebooks, os.listdir()))

    password = open("pwd").readline().strip()

    sync_tool = KindleSync(
        config.get("sender"), 
        config.get("receivers"), 
        config.get("smtp"),
        password)

    sync_tool.add_attachs(files)

    sync_tool.sync()


if __name__ == '__main__':
    main()
