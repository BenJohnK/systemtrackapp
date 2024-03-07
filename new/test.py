import codecs
from contextlib import redirect_stderr
import os
import sys
import time
import traceback
import win32con
import win32evtlog
import win32evtlogutil
import winerror
from pyuac import main_requires_admin
import schedule
from pathlib import Path
from SMWinservice import SMWinservice
import servicemanager
import win32serviceutil
from datetime import datetime

#----------------------------------------------------------------------
def getAllEvents(server, logtypes, basePath):
    """
    """
    if not server:
        serverName = "localhost"
    else: 
        serverName = server
    for logtype in logtypes:
        path = os.path.join(basePath, "%s_%s_log.log" % (serverName, logtype))
        getEventLogs(server, logtype, path)
#----------------------------------------------------------------------
def getEventLogs(server, logtype, logPath):
    """
    Get the event logs from the specified machine according to the
    logtype (Example: Application) and save it to the appropriately
    named log file
    """
    log = codecs.open(logPath, encoding='utf-8', mode='w')
    hand = win32evtlog.OpenEventLog(server,logtype)
    total = win32evtlog.GetNumberOfEventLogRecords(hand)
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ
    count = 0
    DIR = "G:\\new\\log.txt"
    try:
        events=1
        while events:
            events=win32evtlog.ReadEventLog(hand,flags,0)
            for ev_obj in events:
                count+=1
                the_time = ev_obj.TimeGenerated.Format() #'12/23/99 15:54:09'
                if ev_obj.EventID == 4648:
                    with open(DIR, "a+") as file:
                        file.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
                        file.write(the_time + "\n")
                    events = 0
                    break
    except:
        pass

@main_requires_admin
def main():
    server = None  # None = local machine
    logTypes = ["Security"]
    getAllEvents(server, logTypes, "C:\downloads")

def run_scheduler():
    time.sleep(15)
    schedule.every(5).seconds.do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)


class PythonCornerExample(SMWinservice):
    _svc_name_ = "Background Login Log Service"
    _svc_display_name_ = "Log Login Time"
    _svc_description_ = "That's a great winservice! :)"

    def start(self):
        self.isrunning = True

    def stop(self):
        self.isrunning = False

    def main(self):
        run_scheduler()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(PythonCornerExample)
        servicemanager.StartServiceCtrlDispatcher()
        x=input()
    else:
        PythonCornerExample.parse_command_line()