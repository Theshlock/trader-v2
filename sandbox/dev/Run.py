from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
from timeframe import timeframe

periods = {
"1_Year": relativedelta(years=+1),
"1_Month": relativedelta(months=+1), 
"1_Week": relativedelta(days=+7), 
"1_Day": relativedelta(days=+1), 
"1_Hour": relativedelta(hours=+1)
} # periods contain datetimes and instructions on when they start


print(datetime.now().strftime("%w"))
for p in periods:
    t = timeframe(datetime.now()+relativedelta(days=+1), periods[p], 10000)
    print(t.__dict__)
