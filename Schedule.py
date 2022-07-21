from schedule import every, run_pending
from time import sleep

#毎日4:00実行する
def check_record():

    return

every().day.at("4:00").do(check_record())

while True:
    run_pending()
    sleep(1)
