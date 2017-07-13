#League Ban List
#john.chan@utdallas.edu

#requests allows python to make a post request
import requests
#BeautifulSoup allows us to parse HTML
from bs4 import BeautifulSoup
#allows us to use regexes
import re
#allows us to print out today's date and compare it to other dates
from datetime import date
#allows us to make relative filepaths
import os

#used for scaling banRate
lastUpdate = date(2017,7,12)

#function returns a string with the current date
def todayStr():
    today = date.today()
    return str(today.month) + "-" + str(today.day) + "-" + str(today.year)

#function used to turn win percentage and number of games from strings to ints
def grabNum(in_):
    in_ = re.sub("[^0-9.]","",in_)
    return float(in_)

#function takes in individual champion data and calculates a win metric
def metric(dict):
    patchLength = date.today() - lastUpdate
    patchLength = patchLength.days
    #designed to be 0.5 as meta is new, then 1 when meta is 2 weeks old
    scaleFactor = patchLength*0.036+0.5
    if scaleFactor > 1:
        scaleFactor = 1
    return dict["winRate"] + dict["banRate"]*scaleFactor

#function that takes as input the formData and outputs the banlist
def generateBans(options):
    print("Generating bans for " + options["league"] + " using " + options["period"] + " data from OP.GG")
    #BeautifulSoup setup: first downloads html from op.gg, then parses it with bSoup
    responseC = requests.post("https://na.op.gg/statistics/ajax2/champion/", data = options)
    soupC = BeautifulSoup(responseC.text, "html.parser")
    #responseB is the ban page, responseC is the champion page
    responseB = requests.post("https://na.op.gg/champion/statistics")
    soupB = BeautifulSoup(responseB.text, "html.parser")
    data =  list()

    #uses BeautifulSoup to extract champion data
    for row in soupC.find_all("tr")[1:]:
        champ = row.find_all("td")[2].text.strip()
        winRate = row.find_all("td")[3].text.strip()
        n_games = row.find_all("td")[4].text.strip()

        #these check the ban page to get banrate data
        if champ.lower()=='wukong':
            banRate = soupB.select("a[href=/champion/monkeyking/statistics]")[0].find("b").string
        else:
            champString = soupB.select("a[href=/champion/" + re.sub("[.,\' ]","",champ).lower() + "/statistics]")
            #if the webpage cannot be found for the champion (cough cough kayn update)
            if not champString:
                print("Error loading data for " + champ)
            #grabs the banrate for the champ from the HTML
            else:
                banRate = champString[0].find("b").string
        data.append(dict(
            champ = champ,
            winRate = grabNum(winRate),
            n_games = grabNum(n_games),
            banRate = grabNum(banRate)
        ))

    #sorts the champion data by win metric (high to low)
    data.sort(key=metric, reverse = True)

    #opens a file for printing
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, "banlists/" + options["league"].title() + " " + todayStr() + ".txt")
    file = open(filename,"w")

    #prints out the champions with the highest win metric
    lineNum = 1
    file.write("Who to ban in " + options["league"].title() + " on " + todayStr() + "\n\n   Champ" + 12*" " + "BanScore" + 5* " " + "Ban Rate" + 5*" " + "Win Rate\n")
    for record in data:
        frontString = str(lineNum) + ": " + record["champ"]
        metricString = str(metric(record))[:5]
        banString = str(record["banRate"])[:5]
        winrateString = str(record["winRate"])[:5]
        firstSpacer = " " * (20 - len(frontString))
        secondSpacer = " " * (13 - len(metricString))
        thirdSpacer = " " * (13 - len(banString))
        file.write(frontString + firstSpacer + metricString + secondSpacer + banString + thirdSpacer + winrateString + "\n")
        lineNum = lineNum + 1
    file.write("\nGenerated with data from " + options["period"] + " using (winrate+(banrate*patchLength)) on " + todayStr())
    file.close()


#specifies the form options for op.gg post request necessary
formData = dict(
    type='win',
    league='bronze',
    period='today',
    mapId='1',
    queue='ranked',
)

#actually using the function to generate banlists
generateBans(formData)

formData["league"] = 'silver'
generateBans(formData)

formData["league"] = 'gold'
generateBans(formData)

formData["league"] = 'platinum'
generateBans(formData)

formData["league"] = 'diamond'
generateBans(formData)
