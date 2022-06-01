# Libs
import os, sys
from datetime import datetime, date, timedelta
from dateutil.relativedelta import *

def getIncrementalStrategy(full="False"):
    lastExecutionDate = '{{ ti.get_previous_start_date(state="success").in_timezone("America/Sao_Paulo").strftime("%Y-%m-%d %H:%M:%S") if (ti.get_previous_start_date(state="success") and params.full == "False") else "1900-01-01 00:00:00" }}'
    return lastExecutionDate

def readFile(path):
    with open(path) as f: content = f.read()
    return content