import selenium.webdriver as webdriver
import asyncio
from datetime import datetime
from json import loads

options = webdriver.ChromeOptions()
# options.add_argument("headless")

browser = webdriver.Chrome(executable_path="chromedriver", options=options)
browser.get("https://classto-beta.loca.lt/")

class App:
    async def enter_zoom(self) -> None:
        current_time = datetime.now()
        if current_time.weekday() == 6:
            weekday = "0"
        else:
            weekday = str(current_time.weekday() + 1)

        # print(weekday)
        # print(f"{current_time.hour}:{current_time.minute}")

        for meeting in self.meetings[self.current_category]:
            if meeting.time == f"{current_time.hour}:{current_time.minute}" and weekday in meeting["repeating-days"]:
                print('oh')

    async def main(self):
        while True:
            self.meetings = loads(browser.execute_script('return localStorage.getItem("meetings")'))
            self.current_category = browser.execute_script('return localStorage.getItem("recent_editor")')
            await asyncio.sleep(2)
 
            await self.enter_zoom()

app = App()

loop = asyncio.new_event_loop()
loop.create_task(app.main())
loop.run_forever()
