import json
import os
from urllib.request import urlopen

import csv
import pandas as pd

import math

import ssl

from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.shortcuts import choice
from prompt_toolkit.styles import Style
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import input_dialog


# stop the program from trying to verify certificates- my school wifi's firewall wrecks this code so i can't run it at school without doing this
ssl_context = ssl._create_unverified_context()
# pretty sure this is the main thing making the code as slow as it is, so i'd definitely remove it to speed things up, if possible
# (and also it could be like a MASSIVE security issue, for obvious reasons... so there's that too)

BASE_URL = "https://api.openf1.org/v1/"



# functions for aesthetics:

def printProgressBar (iteration, total, suffix = '', decimals = 1, length = 100, fill = '▮', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """

    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '▯' * (length - filledLength)
    print(f'\r |{bar}| {iteration}/{total} {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()


def bettermenu(): # cool CLI interface for program's homepage
    style = Style.from_dict(
    {
        "frame.border": "#ff0000",
        "selected-option": "fg:#ff4444 bold",
    }
    )

    function = choice(
    message=HTML("F1 DATA LOGGER/INTERPRETER | Homepage"),
    options=[
        ("dln", "Download new data"),
        ("ine", "Interpret existing data (WIP)"),
        ("scn", "Scan for existing data (WIP)"),
        ("drv", "Get driver data (WIP)")
    ],
    style=style,
    show_frame=True,
    default="dln",
    )

    if function == "dln":
        print("Downloading new data...")
        getyr2()
    elif function == "ine":
        intexhome()
    elif function == "scn":
        scan()
    elif function == "drv":
        driverdata()



# functions for homepages of other features -- made using a prompt_toolkit interface, so keep that in mind

def intexhome(): # WIP -- interpret existing data into simple .CSVs, which can then be used in Excel
    # print("Interpretation function is yet to be developed. Returning home...")
    # bettermenu()

    style = Style.from_dict(
    {
        "frame.border": "#0022ff",
        "selected-option": "fg:#75b7ff bold",
    }
    )

    function = choice(
    message=HTML("DATA INTERPRETER MENU (beta)"),
    options=[
        ("wins", "Overall top 10 finishes & points"),
        ("fl", "Fastest laps [UNDEVELOPED]")
    ],
    style=style,
    show_frame=True,
    default="dln",
    )

    if function == "fl":
        intfl()
    elif function == "wins":
        intptfin()


def scan(): # WIP -- scan thru existing data
    
    print("Scan function is yet to be developed. Returning home...")
    bettermenu()
    
    
    """
    BASIC IDEA FOR FUNCTION:
    - Scan for calendars
        > If no calendar: let user know, then go back to main menu
        > If yes calendar: pull every meeting key, look for matching folders, subfolders, files, etc. in year's subdirectory *
            - If discrepancies exist between keys in calendar and folders (e.g. if meeting key 1254 doesn't have a subfolder, but is in the calendar):
                > Tell user specific missing keys (e.g. "Subfolder for meeting no. 1254 not found")
                > Count qty. of discrepancies, give final number to user, w. total number of meetings in calendar for reference (e.g. "Found 4 missing subfolders of 16 events for 2025")
                > Go back to main menu
    
    * Check for [session key]_allpos.json, times/summary.json, and [session_key]_info.json -- will need to find race session key to do this
    """


def driverdata(): # WIP -- lookup data on a driver given their number
    # print("Driver data interpreter is yet to be developed. Returning home...")
    

    nm = input_dialog(
        title='Driver lookup (by number)',
        text='Enter number of driver to search:').run()
    
    print(nm)

    url = (f'{BASE_URL}drivers?driver_number={nm}')
    print(url)

    search = urlopen(url, context=ssl_context)
    parsedsearch = json.loads(search.read().decode('utf-8'))

    for i in parsedsearch:
        dispcode = i['name_acronym']
        fullname = i['full_name']

    print(f'{dispcode}, {fullname}, {nm}')

    bettermenu()



# functions for the data-loading part of the program (the main bit):

def timesummary(y, s, m, n): # looks at every driver timesheet and makes a summary of fastest laps for the race
    # variable list:
    # "y": year | "s": session key for race itself | "m": meeting key for entire weekend | "n": driver number
    
    fp = (f'{y}/{m}/times/summary.json') # because 2 characters are easier to type than 33
    fp2 = (f'{y}/{m}/times/{s}_{n}.json') # and because 3 is easier than however many that is
    fp3 = (f'{y}/{m}/{s}_allpos.json') # etc

    with open(fp, 'r') as file:
        search = json.load(file)
        file.close()

    allpurple = [item['fastest'] for item in search]
    allpurple = list(filter(lambda x: x is not None, allpurple))

    racebest = min(allpurple)

    allstroll = [item['slowest'] for item in search]
    allstroll = list(filter(lambda x: x is not None, allstroll))

    raceworst = max(allstroll)

    for item in search:
        if item.get("fastest") == racebest:
            fastestdriver = item.get('driver_number')

        if item.get("slowest") == raceworst:
            slowestdriver = item.get('driver_number')


def drivertimes(y, n, sk, id): ## make laptime jsons for each driver
    
    # talk to the summary json - if the file doesn't exist yet then that's a user error, so idgaf about checking if it's there first
    search = json.loads(open(f'{y}/{id}/{sk}_info.json').read())
    for i in search:
        lapc = i['lap_count'] # number of laps in the race, according to summary JSON
    
    lapnolist = list(range(1,lapc+1)) # make a list ranging from 1 to however many laps there are in the race

    
    if os.path.exists(f'{y}/{id}/times'):
        pass
    else:
        os.mkdir(f'{y}/{id}/times')
    
    filepath = (f'{y}/{id}/times/{sk}_{n}.json')
    fp = (f'{y}/{id}/times/summary.json')

    if os.path.exists(filepath):
        print(f'#{n} lap times already saved')
        with open(filepath) as file:
            data = json.load(file)

    else:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump([], f)
        
        print(f'getting laptimes for #{n}')
        for lap in lapnolist: # get time for every lap
            printProgressBar(lap, lapc)
        
            # talk to the api
            search = urlopen(f'{BASE_URL}laps?session_key={sk}&driver_number={n}&lap_number={lap}', context=ssl_context)
            intsearch = json.loads(search.read().decode('utf-8'))
        
            for i in intsearch:
                with open(filepath, 'r') as file:
                    data = json.load(file)

                # interpret the search- get actual laptimes & make variables
            
                laptimeraw = i['lap_duration'] # from api data

                if laptimeraw != None:
                    mins, sec = divmod(laptimeraw, 60) # find number of minutes and remaining seconds + fractions of a second
                    mins = math.floor(mins) # remove decimal point from isolated minute value
                    sec = round(sec, 3) # round seconds back to 3dp (as they were from the api, there's obv a bug in how Python does math that creates recurring dps out of thin air)
        
                    isosec, subsec = divmod(sec, 1) # find number of whole seconds and remaining part-second
                    subsec = round(subsec, 3) # round back to 3dp again

                    isosec = math.floor(isosec) # remove decimal point from isolated second value

                    ksec = 1000 * subsec # convert part-second (rounded to 3dp) into remaining thousandths of a second
                    ksec = math.floor(ksec) # remove decimal point from thousandths value
        
                    displaptime = (f'{mins}:{sec}') # neatened "m:s.xcm"-format laptime (for display use only)
                else:
                    mins = isosec = sec = ksec = 'N/A'
                    displaptime = "N/A"
                    laptimeraw = None

                entry = {'lap_number': lap, 'raw_time': laptimeraw, 'display_time': displaptime, 'minutes': mins, 'seconds_thousandths': sec, 'seconds_isolated': isosec, 'thousandths': ksec}
                data.append(entry)
                
                with open(filepath, mode='w', encoding='utf-8') as feedsjson:
                    json.dump(data, feedsjson, indent=4)


        
        # python's dumb so now the code needs to read the json it literally just created to find the slowest and fastest laptimes
        # don't ask me why it's doing this, i honestly have no clue
        search = json.loads(open(filepath).read())
        times = [item['raw_time'] for item in search]
        fltrdtimes = list(filter(lambda x: x is not None, times))
        ntimes = len(fltrdtimes)

        try:
            purple = min(fltrdtimes) # fastest lap
            strollin_it=max(fltrdtimes) # take a guess
        except ValueError:
            print("No valid laptimes found")
            purple = None
            strollin_it = None

        with open(filepath) as file:
            data = json.load(file)
        
        summary = {
            'fastest': purple,
            'slowest': strollin_it
        }

        data.append(summary)

        with open(filepath, mode='w', encoding='utf-8') as feedsjson:
            json.dump(data, feedsjson, indent=4)
        
        
        # now write all of that to file again, this time in the summary JSON
        if os.path.exists(fp):
            pass
        else:
            open(fp, 'w', encoding='utf-8').close()
    
        with open(fp) as file:
            try:
                data = json.load(file) # load in whatever's already in the summary
            except json.decoder.JSONDecodeError:
                data = []
                    

        entry = { # make driver entries
            'driver_number': n,
            'fastest': purple,
            'slowest': strollin_it
        }

        data.append(entry)

        with open(fp, mode='w', encoding='utf-8') as feedsjson:
            json.dump(data, feedsjson, indent=4)
        
        print(f"Best lap: {purple}, worst lap: {strollin_it}")
    
    return('complete')


def driverpos2(n, sk): # find position of driver with a given number for the given race, & give them to the function that wanted to know
    search = urlopen(f'{BASE_URL}session_result?session_key={sk}&driver_number={n}', context=ssl_context)
    info = json.loads(search.read().decode('utf-8'))
    for i in info:
        if i['position'] != 'null':
            return i['position']
        else:
            return("DNF/DSQ")
    
    del search
    del info


def alldrivernum(yr, sk, en): # grabbing the numbers for EVERY SINGLE DRIVER in the race and listing them in a JSON file
    print(f'Finding number of every driver to race in {en}')
    search = urlopen(f'{BASE_URL}session_result?session_key={sk}', context=ssl_context)
    info = json.loads(search.read().decode('utf-8'))
    for i in info:
        id = i['meeting_key'] # grab the meeting key again

    if os.path.exists(f'{yr}/{id}/{sk}_allpos.json'):
        print(f'{en} position data already saved')
        
        with open(f'{yr}/{id}/{sk}_allpos.json') as file:
            posdata = json.load(file)

            for i in posdata:
                num = i['driver_number']
                pos = i['position']

                print(f'P{pos} for #{num}')
                status = drivertimes(yr, num, sk, id)

                timesummary(yr, sk, id, num)

    else:
        with open(f'{yr}/{id}/{sk}_allpos.json', 'w', encoding='utf-8') as f:
            json.dump([], f)
        
        for i in info:
            with open(f'{yr}/{id}/{sk}_allpos.json', 'r') as file:
                data = json.load(file)

            num = i['driver_number'] # list of every driver number
            pos = driverpos2(num, sk) # position of every driver number
            print(f"P{pos} for driver with number {num}")

            with open(f'{yr}/{id}/{sk}_allpos.json', mode='w', encoding='utf-8') as feedsjson:
                entry = {'driver_number': num, 'position': pos}
                data.append(entry)
                json.dump(data, feedsjson, indent=4)
            
            status = drivertimes(yr, num, sk, id)

            timesummary(yr, sk, id, num)

    print(status)


def driverpos(sk, pos): # find numbers of the drivers finishing in a given position for the given race, & give them to the function that wanted to know
    print(f"finding driver in P{pos}")
    search = urlopen(f'{BASE_URL}session_result?session_key={sk}&position={pos}', context=ssl_context)
    info = json.loads(search.read().decode('utf-8'))
    for i in info:
        return i['driver_number']
    del search
    del info


def racejsons(yr): # create JSONs for each actual race
    
    calendar=json.loads(open(f'{yr}_calendar.json').read()) # need to load up the calendar AGAIN to get the list of meeting keys into this function
    for i in calendar:
        id=i['meeting_key']
    
        search = urlopen(f'{BASE_URL}sessions?meeting_key={id}', context=ssl_context)
        info = json.loads(search.read().decode('utf-8'))

        evntnm=i['meeting_name']

        # checking through for sessions within each event for marked races
        for i in info:
            if i['session_name'] == "Race": # if a race session IS found (will apply for the vast majority of events)*
                
                print(f"Race session found for {evntnm}")
                sk=i['session_key']
                
                if os.path.isfile(f'{yr}/{id}/{sk}_info.json'): # skips redoing every summary every time the program's run- only does the ones it can't find
                    print(f"Summary JSON already exists for {evntnm}")
                    alldrivernum(yr, sk, evntnm)
                else:
                    tn = lc = p1 = p2 = p3 = p4 = p5 = p6 = p7 = p8 = p9 = p10 = frc = tr = 'unknown' # big ol' definition string for variables that remain unknown as of yet

                    search = urlopen(f'{BASE_URL}sessions?session_key={sk}', context=ssl_context)
                    info = json.loads(search.read().decode('utf-8'))
                    for i in info:
                        tn = i["circuit_short_name"]

                    # find who finished in the top 10, and the number of laps in the race
                    print(f"Downloading top 10 drivers for {evntnm}...")
                    search = urlopen(f'{BASE_URL}session_result?session_key={sk}&position=1', context=ssl_context)
                    info = json.loads(search.read().decode('utf-8'))
                    for i in info:
                        lc = i['number_of_laps']
                    
                        p1 = driverpos(sk, 1)
                        print(f"found driver in P1")
                        p2 = driverpos(sk, 2)
                        print(f"found driver in P2")
                        p3 = driverpos(sk, 3)
                        print(f"found driver in P3")
                        p4 = driverpos(sk, 4)
                        print(f"found driver in P4")
                        p5 = driverpos(sk, 5)
                        print(f"found driver in P5")
                        p6 = driverpos(sk, 6)
                        print(f"found driver in P6")
                        p7 = driverpos(sk, 7)
                        print(f"found driver in P7")
                        p8 = driverpos(sk, 8)
                        print(f"found driver in P8")
                        p9 = driverpos(sk, 9)
                        print(f"found driver in P9")
                        p10 = driverpos(sk, 10)
                        print(f"found driver in P10")

                    print("Creating summary JSON...")
                    details = [{ # dictionary for race session JSON
                        'race_name': evntnm,
                        'track_name': tn,
                        'race_code': sk,
                        'lap_count': lc,
                        'p1': p1,
                        'p2': p2,
                        'p3': p3,
                        'p4': p4,
                        'p5': p5,
                        'p6': p6,
                        'p7': p7,
                        'p8': p8,
                        'p9': p9,
                        'p10': p10,
                        'fastest_race_lap': frc,
                        'track_record': tr
                    }]

                    with open(f'{yr}/{id}/{sk}_info.json', 'w', encoding='utf-8') as f:
                        json.dump(details, f, ensure_ascii=False, indent=4)
                    print(f"Completed summary JSON for {evntnm}.")
        
                    # note: if a race session isn't found, no JSON will be made- it's that simple

                    alldrivernum(yr, sk, evntnm)
    
    bettermenu()


def setupdir(yr): # create directory system for given year
    print(f"Organising folders for {yr}...")
    
    # main year folder- check if one already exists, if not: make one
    if os.path.isfile(yr):
        print(f"{yr} directory already exists")
    else:
        print(f"creating directory for {yr}")
        try:
            os.mkdir(yr)
        except FileExistsError:
            print(f"directory already exists but Python's stupid so it needed me to make that EXTRA clear.")
        print(f"Created {yr} directory successfully.")

    # get event details from calendar JSON
    calendar=json.loads(open(f'{yr}_calendar.json').read())
    for i in calendar:
        
        # location (country)
        where=i['country_name']

        # name of race
        name=i['meeting_name']
        print(name)

        # numerical code assigned to each race
        ident=i['meeting_key']
        
        # make subfolders for above events
        try:
            os.mkdir(f"{yr}/{ident}")
            print(f"Created subfolder for {name}")
        except FileExistsError:
            print(f"Subfolder for {name} already exists.")

    # clear variables that won't be needed anymore
    del name
    del calendar
    del ident

    # move on to next step- race detail JSONs
    racejsons(yr)


def rdyr(year): # pick the year- this is the only one with any user input atm
    # if calendar exists:
    if os.path.isfile(f"{year}_calendar.json"):
        print(f"Calendar for {year} already exists.") 
        calendar=json.loads(open(f'{year}_calendar.json').read())
    
    # if it doesn't:
    else:
        print(f"Can't find {year} calendar, creating one now...")

        # create the calendar JSON
        searchyr = urlopen(f'{BASE_URL}meetings?year={year}', context=ssl_context)
        calendar = json.loads(searchyr.read().decode('utf-8'))
        with open(f'{year}_calendar.json', 'w', encoding='utf-8') as f:
            json.dump(calendar, f, ensure_ascii=False, indent=4)
        
        print(f"Calendar for {year} made.")

        keylist = [item['meeting_key'] for item in calendar]
        numraces = len(keylist)
        print(f"{numraces} races found for year {year}")
        
        # delete variables that aren't needed anymore
        del calendar
        del numraces
        del keylist
        del searchyr

    # onto next step- creating directory
    setupdir(year)


def getyr(): # this version WILL NOT WORK with prompt_toolkit, idk why but the input() function just doesn't work at all with it lol
    year=input("Step 1: Enter year: ")
    print(f"Loading for {year}")
    rdyr(year)


def getyr2():
    year=prompt("Step 1: Enter year: ")
    print(f"Loading for {year}")
    rdyr(year)



# functions for interpreting existing data

def intptfin(): # first function to make a CSV tally of top 10 finishes by each driver for given season
    year = input_dialog(
        title='Top 10 results analyser',
        text='Enter year to compile data from:').run()

    # if calendar exists:
    if os.path.isfile(f"{year}_calendar.json"):
        print(f"Found {year} calendar.") 
        calendar=json.loads(open(f'{year}_calendar.json').read())

        meetid = [item['meeting_key'] for item in calendar]
        numraces = len(meetid)
        print(f"{numraces} races found in {year} calendar, reading their info now...")

        # check if season CSV tally already exists, delete it if it does:
        tCSVfp = (f'{year}/points_tally.csv')
        if os.path.isfile(tCSVfp):
            os.remove(tCSVfp)
        else:
            pass

        # create tally CSV
        header = ['dn', 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 'pts'] # header
        wdc = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] # reigning champion

        with open(tCSVfp, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)

            # write the rows
            writer.writerow(header)
            writer.writerow(wdc)

    
        for i in calendar:
            meetid = i['meeting_key']
            search = urlopen(f'{BASE_URL}sessions?meeting_key={meetid}', context=ssl_context) # talk to the api to grab session keys
            info = json.loads(search.read().decode('utf-8'))

            evntnm=i['meeting_name']

            # checking through for sessions within each event for marked races (excludes pre-season testing, which is technically "free practice")
            for i in info:
                if i['session_name'] == "Race":
                    sk=i['session_key']
                    
                    sumfp = (f'{year}/{meetid}/{sk}_info.json')
                    rcinfo = json.loads(open(sumfp).read()) # look at info JSONs for every race
                    for i in rcinfo:
                        p1 = i['p1']
                        p2 = i['p2']
                        p3 = i['p3']
                        p4 = i['p4']
                        p5 = i['p5']
                        p6 = i['p6']
                        p7 = i['p7']
                        p8 = i['p8']
                        p9 = i['p9']
                        p10 = i['p10']
                
                    print(f"For {year} {evntnm}, top 10 drivers were: #{p1} in 1st, #{p2} in 2nd, #{p3} in 3rd, #{p4} in 4th, #{p5} in 5th, #{p6} in 6th, #{p7} in 7th, #{p8} in 8th, #{p9} in 9th, and #{p10} in 10th")

                    CSVdict(p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,year,sk,sumfp, tCSVfp) # second function used to make things a little more organised
        
        print("Complete!")
                    
    # if there's no matching calendar:
    else:
        print(f"Can't find calendar for {year}- are you sure you already have that data?")
        print("Returning to homepage...")
    
    bettermenu()
    
    
def CSVdict(p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,yr,sk,path,csvp): # write new rows to CSV
    p1r = CSVupdate(p1, 1, 25, csvp)
    p2r = CSVupdate(p2, 2, 18, csvp)
    p3r = CSVupdate(p3, 3, 15, csvp)
    p4r = CSVupdate(p4, 4, 12, csvp)
    p5r = CSVupdate(p5, 5, 10, csvp)
    p6r = CSVupdate(p6, 6, 8, csvp)
    p7r = CSVupdate(p7, 7, 6, csvp)
    p8r = CSVupdate(p8, 8, 4, csvp)
    p9r = CSVupdate(p9, 9, 2, csvp)
    p10r = CSVupdate(p10, 10, 1, csvp)

    with open(csvp, 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)

            # write the rows
            writer.writerow(p1r)
            writer.writerow(p2r)
            writer.writerow(p3r)
            writer.writerow(p4r)
            writer.writerow(p5r)
            writer.writerow(p6r)
            writer.writerow(p7r)
            writer.writerow(p8r)
            writer.writerow(p9r)
            writer.writerow(p10r)


def CSVupdate(num,pos,pts,csvp): # make amended CSV rows  
    df = pd.read_csv(csvp) # load the CSV
    
    # check if given driver number is somewhere in the list
    count = df['dn'].value_counts().get(num, 0) # count how many times the driver number shows up in the CSV
    # print(f"Occurrences of {num}: {count}")

    if count == 0: # if it never shows up then there mustn't be a matching column, and vice versa
        p1 = p2 = p3 = p4 = p5 = p6 = p7 = p8 = p9 = p10 = 0
        
    else:
        # read data from CSV row, convert them to integers
        p1 = int(df.loc[df['dn'] == num, '1'].values[0])
        p2 = int(df.loc[df['dn'] == num, '2'].values[0])
        p3 = int(df.loc[df['dn'] == num, '3'].values[0])
        p4 = int(df.loc[df['dn'] == num, '4'].values[0])
        p5 = int(df.loc[df['dn'] == num, '5'].values[0])
        p6 = int(df.loc[df['dn'] == num, '6'].values[0])
        p7 = int(df.loc[df['dn'] == num, '7'].values[0])
        p8 = int(df.loc[df['dn'] == num, '8'].values[0])
        p9 = int(df.loc[df['dn'] == num, '9'].values[0])
        p10 = int(df.loc[df['dn'] == num, '10'].values[0])
        expts = int(df.loc[df['dn'] == num, 'pts'].values[0])
        pts = expts + pts # add gained points to existing points
        
        # delete old row from the CSV so that it can be replaced with the new one later
        df = df.drop(df[df['dn'] == num].index)
        df.to_csv(csvp, index=False)

    # add 1 to the cell for whichever position was achieved
    if pos == 1:
        p1 = p1 + 1
    elif pos == 2:
        p2 = p2 + 1
    elif pos == 3:
        p3 = p3 + 1
    elif pos == 4:
        p4 = p4 + 1
    elif pos == 5:
        p5 = p5 + 1
    elif pos == 6:
        p6 = p6 + 1
    elif pos == 7:
        p7 = p7 + 1
    elif pos == 8:       
        p8 = p8 + 1
    elif pos == 9:
        p9 = p9 + 1
    elif pos == 10:
        p10 = p10 + 1
        
    newcol = [num, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, pts]
    return newcol


def intfl(): # WIP
    print("This section is incomplete. Returning home...")
    bettermenu()



# onto the main section of code...

print("F1 DATA LOGGER AND INTERPRETER") # this is all totally unnecessary, just some "opening credits" per se
print("Powered by OpenF1 API (www.openf1.org)")
print("Sam Matthews, 2025")
print("Version 1.0")

bettermenu()