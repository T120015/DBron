from email.mime.text import MIMEText
from smtplib import SMTP
print('Hello Python World!!!')


# 送受信先
from_email = "zen.aku_movie@outlook.com"
to_BCC = ["t120008@ed.sus.ac.jp", "t120015@ed.sus.ac.jp"]
# MIMETextを作成
body = "昨日の記録が未登録です.\n早急に健康記録を登録してください."
msg = MIMEText(body, "html")
msg["Subject"] = "昨日の健康記録が未登録です"
msg["From"] = from_email
msg["Bcc"] = ";".join(to_BCC)

# サーバを指定する
server = SMTP("smtp.office365.com", 587)
server.ehlo()
server.starttls()
server.ehlo()
# メールを送信する
server.login(from_email, "ZenAkuMovie5963")
server.send_message(msg)
# debug for email
# server.set_debuglevel(True)
# 閉じる
server.quit()
