import sys
sys.path.append("/home/maxib/ws/projects/CalSpam47")
print(sys.path)
from src.gmail_cal import GmailCalSender
import datetime as dt
from time import sleep

EVENT_WE =  {'summary': 'Grillen', 'location': 'Wilhelmstraße 29 68799 Reilingen', 'description': 'Grillen bei maxi in Reilingen, wenn es ihm gut geht sonst bei Tim'}

gmaili = GmailCalSender()
att = ["ibakrafal@googlemail.com"]
#att = ["banjio1992@gmail.com"]
start = dt.datetime(2023, 8, 26, 14, 0,0)
end = dt.datetime(2023, 8, 26, 18, 0, 0)

for timedelta in range(0, 5):
        EVENT_WE["summary"] = f"Grillen Part {timedelta}"
        start = start + dt.timedelta(hours=timedelta)
        end = end + dt.timedelta(hours=timedelta)
        gmaili.create_cal_event(EVENT_WE, att, start, end)
        print("Sleeping 5 seconds ....!")
        sleep(5)

