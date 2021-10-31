import asyncio
import webbrowser
from datetime import datetime
import json

import requests

class App:
    def __init__(self, user):
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

email = ""
pwd = ""
with open('config.json') as config:
    data = json.load(config)
    email = data["email"]
    pwd = data["pwd"]

user = requests.post("http://localhost:5000/auth/login",json = {"email" : email,"pw" : pwd})
if not user.status_code == 200:
    print("error: user not found")
app = App(user)

loop = asyncio.new_event_loop()
loop.create_task(app.main())
loop.run_forever()
