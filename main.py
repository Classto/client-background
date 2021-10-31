import asyncio
import webbrowser
from datetime import datetime
import json

import requests

class App:
    def __init__(self, email, pwd):
        user = requests.post("http://localhost:5000/auth/login",json = {"email" : email,"pw" : pwd})
        print(user.json())
        self.session_id = user.json()["session_id"]
        self.current_category = user.json()["current_category"]
        self.meetings = requests.get(f"http://localhost:5000/schedule/{self.session_id}").json()["data"]

    async def enter_zoom(self):
        current_time = datetime.now()
        if current_time.weekday() == 6:
            weekday = "0"
        else:
            weekday = str(current_time.weekday() + 1)

        for meeting in self.meetings[self.current_category]:
            if meeting["time"] == f"{current_time.hour}:{current_time.minute}" and weekday in meeting["repeating-days"]:
                id = meeting["id"]
                pwd = meeting["pw"]
                uname = meeting["nickname"]
                webbrowser.open(f"zoommtg://zoom.us/join?action=join&confno={id}&pwd={pwd}&uname={uname}")

    async def main(self):
        while True:
            await asyncio.sleep(2)
 
            await self.enter_zoom()

print('''
   _____ _               _        
  / ____| |             | |       
 | |    | | __ _ ___ ___| |_ ___  
 | |    | |/ _` / __/ __| __/ _ \ 
 | |____| | (_| \__ \__ \ || (_) |
  \_____|_|\__,_|___/___/\__\___/ 
                                  ''')
email = "sejoon0606@gmail.com" #input("email: ")
pwd = "1234" #input("password: ")
app = App(email=email, pwd=pwd)

loop = asyncio.new_event_loop()
loop.create_task(app.main())
loop.run_forever()
# user = requests.post("http://localhost:5000/auth/login",json = {"email" : email,"pw" : pwd})
# print(user.json()["session_id"])