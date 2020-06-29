import pandas as pd
import numpy as np
from random import choices, choice
import datetime
from termcolor import colored

# get the name of the file to search through
file_name = input('Please enter the name of the current tracker excel file: ')
# get the date to search from
date = input('Please enter the date to search back from in form Month/Day/Year: ')
posdate = datetime.datetime.strptime(date, '%m/%d/%Y')
# get who got sick
sickPerson = input('Who tested positive? ')
# get how many days back to check
riskPeriod = input('How Many Days back do you want to check? ')
riskPeriod = int(riskPeriod)

# read in the file
data = pd.read_excel(file_name)


# convert the date into datetime
data['Date'] = pd.to_datetime(data['Date'])
try:
    # get rid of the reduntant indexes if there
    data = data.drop('Unnamed: 0', axis=1)
except:
    pass

# extract what shift everyone is on, its easier to just cache this knowledge
shifts = dict(data.loc[0])

# filter the data down to what we want
danger_time = data[data['Date'] > posdate - datetime.timedelta(days=riskPeriod)]
# flip the data because thats how it becomes useful
danger_time = danger_time.T

# shifts are 'A', 'M', and 'P'
# 'M' puts both at high risk, othewise thers a high med low pattern:
# shift risks has key of sick persons shift, value of risks to other shifts
shift_risks = {'A': {'A': 'red', 'M': 'yellow', 'P': 'green'},
               'M': {'A': 'red', 'M': 'red', 'P': 'red'},
               'P': {'A': 'green', 'M': 'yellow', 'P': 'green'}}

# danger_shift is a dict of key shift value risk color
danger_shift = shift_risks[shifts[sickPerson]]
# generate a list of all contacts
contacts = []
for day in danger_time:
    # risk is the name of the school the sick person was at
    risk = danger_time.loc[sickPerson][day]
    # filter danger time for the list of people who were there
    risky_contact = danger_time[danger_time[day] == risk].index.values
    # save those to a list
    contacts.append(list(risky_contact))

# flatten those contacts into a set so no repeated names
dangers = set()
for day in contacts:
    for contact in day:
        dangers.add((contact, danger_shift[shifts[contact]]))


def prRed(skk):
    print("\033[91m {}\033[00m" .format(skk))


def prGreen(skk):
    print("\033[92m {}\033[00m" .format(skk))


def prYellow(skk):
    print("\033[93m {}\033[00m" .format(skk))


colors = {'red': prRed, 'green': prGreen, 'yellow': prYellow}
for danger in dangers:
    pr = colors[danger[1]]
    pr(danger[0])
