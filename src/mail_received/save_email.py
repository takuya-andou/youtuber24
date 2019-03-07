import sqlite3
import poplib
import email
from email.header import decode_header
from email.utils import parsedate_to_datetime

import os


def get_header(msg, name):
    header = ''
    if msg[name]:
        for tup in decode_header(str(msg[name])):
            if type(tup[0]) is bytes:
                charset = tup[1]
                if charset:
                    header += tup[0].decode(tup[1])
                else:
                    header += tup[0].decode()
            elif type(tup[0]) is str:
                header += tup[0]
    return header


# msg から本文を取得
def get_content(msg):
    charset = msg.get_content_charset()
    payload = msg.get_payload(decode=True)
    try:
        if payload:
            if charset:
                return payload.decode(charset)
            else:
                return payload.decode()
        else:
            return ""
    except:
        return payload


def fetchmail(cli, msg_no):
    content = cli.retr(msg_no)[1]
    uidl = cli.uidl(msg_no).decode().split(' ')[-1]
    msg = email.message_from_bytes(b'\r\n'.join(content))
    from_ = get_header(msg, 'From')
    date_hdr = get_header(msg, 'Date')
    if date_hdr:
        date = parsedate_to_datetime(date_hdr)
    else:
        date = None
    subject = get_header(msg, 'Subject')
    content = get_content(msg)
    return (uidl, subject, content, from_, date)


def find_newmail(cli, db):
    uidl = cli.uidl()[1]
    remote_uidl = list(map(lambda elm: elm.decode().split(' '), cli.uidl()[1]))
    c = db.cursor()
    res = c.execute('SELECT uidl FROM mail').fetchall()
    local_uidl = map(lambda tup: tup[0], res)
    # サーバ上のUIDL番号のセットと、受信済みメールのUIDL番号のセットとの差集合をとる
    new_uidl = set(map(lambda elm: elm[-1], remote_uidl)) - set(local_uidl)
    return list(filter(lambda elm: elm[1] in new_uidl, remote_uidl))


def receive_all(cli, db):
    newmail = find_newmail(cli, db)
    count = len(newmail)
    c = db.cursor()
    for mail in newmail:
        msg = fetchmail(cli, mail[0])
        c.execute("""
            INSERT INTO mail (uidl, subject, content, sender, sent_at)
            VALUES (?, ?, ?, ?, ?)
            """, msg)
        print('Date: %s, From: %s, Subject: %s' % (msg[4], msg[3], msg[1]))
        db.commit()
    c.close()


def setup(db):
    c = db.cursor()
    c.execute('CREATE TABLE mail (uidl text, subject text, content text, sender text, sent_at timestamp,read_flg int default 0, created_at default current_timestamp)')
    db.commit()
    c.close()

db = sqlite3.connect('mail.db')

# exec at first time only
# setup(db)

cli = poplib.POP3(os.environ["pop3server"])
print('connected.')

# 認証
cli.user(os.environ["mailaddress"])
cli.pass_(os.environ["mailpass"])

receive_all(cli, db)
cli.quit()
