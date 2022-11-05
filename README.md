# ICS To CSV exporter

Python script, that can take any ICS url and convert it to CSV format. Adittionally it can count the total time of all events in the ics file.

you can also specify a timeframe with **--start** and **--end**

## to install all requirements do:

```bash
pip install -r requirements.txt
```

## for usage use.

```bash
python3 ics-csv-exporter.py -h
```

```bash
usage: main.py [-h] [-s START] [-e END] [-u URL] [--csv] [--hours]

Tool to analyze ical Calendar from url

options:
  -h, --help            show this help message and exit
  -s START, --start START
                        specify start Date wit the following format: YYYY.MM.DD
  -e END, --end END     specify end Date wit the following format: YYYY.MM.DD
  -u URL, --url URL     specify calendar url
  --csv                 export events to csv file with name hours-{start date}-{end date}.csv
  --hours               print total hours
```