import imaplib
import email

from config import MAIL_PASSWORD

def run():
    mail_pass = MAIL_PASSWORD
    username = "kibyakov98@mail.ru"
    imap_server = "imap.mail.ru"
    imap = imaplib.IMAP4_SSL(imap_server)
    imap.login(username, mail_pass)
    imap.select("INBOX")
    msg_list = list(reversed(imap.uid('search', 'ALL')[1][0].decode('utf-8').split(' ')))

    for msg_uid in msg_list:
        res, msg = imap.uid('fetch', msg_uid, '(RFC822)')
        msg = email.message_from_bytes(msg[0][1])
        if msg["Return-path"] == '<no-reply@br-analytics.ru>':
            for part in msg.walk():
                if part.get_content_disposition() == 'attachment':
                    with open('report.xlsx', 'wb') as file:
                        file.write(part.get_payload(decode=True))
                        print('\nReport downloaded\n')
            break
