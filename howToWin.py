import datetime
import requests
import json
import datetime
import time

#grabs api key from local text file
#if you're reading this, then I'm glad I kept the apikey local ;)
file = open("./apiKey.txt", "r")
apiKey = file.read().strip()
file.close()

patch_date = datetime.datetime(2017, 7, 12, 0, 0, 0)
epoch = datetime.datetime(1970, 1, 1)

#starts from a starting name, then grabs all players in that league and examines their games
#it then looks for summoners they have played with, and gets the summoner ids, account ids, and summoner names of those players
#the account ids of players are used to look up their games
def main(startingName, k):
    #idSet holds all the summonerIDs processed
    idSet = set()
    #master player list contains a series of dicts that have summoner ids, account ids, and summoner names
    masterPlayerList = []

    newIDs = getIDs(startingName)
    idSet.update(newIDs)
    while len(masterPlayerList) < k:
        print("analyzing new batch of players")
        newPlayers = makeRecords(newIDs)
        masterPlayerList.extend(newPlayers)
        newIDs, games = getMatches(newPlayers)
        newIDs = newIDs - idSet
        idSet.update(newIDs)

def api(method, path, data):
    url = 'https://na1.api.riotgames.com' + path
    r = requests.request(method, url.format(**data), headers = {"X-Riot-Token" : apiKey})
    #remember the last time a request was made, and wait to make another request
    #riot rate limit: 20/sec, 100/2min
    time.sleep(0.75)
    return r.json()

def getIDs(startingName):
    nameLookupStub = '/lol/summoner/v3/summoners/by-name/{startingName}'
    nameRequest = api("get", nameLookupStub, dict(startingName=startingName))
    summonerID = nameRequest["id"]
    accountID = nameRequest["accountId"]

    divLookupStub = "/lol/league/v3/leagues/by-summoner/{startingID}"
    divRequest = api("get", divLookupStub, dict(startingID=summonerID))
    playersFound = set()
    for leagueData in divRequest:
        if leagueData["queue"] == "RANKED_SOLO_5x5":
            entries = leagueData["entries"]
    for playerData in entries:
        #adds summonerIDs to the master list of players found
        playersFound.add(playerData["playerOrTeamId"])
    return playersFound

def get_matches(accountId):
    # https://developer.riotgames.com/api-methods/#match-v3/GET_getMatchlist
    beginTime = int((patch_date - epoch).total_seconds() * 1e3)
    url = '/lol/match/v3/matchlists/by-account/{accountId}?beginTime={beginTime}'
    matchlist = api('get', url, locals())
    games = []
    for match in matchlist['matches']:
        games.append(match['gameId'])
    return games

counter = 0;
def makeRecords(summonerIDs):
    global counter
    playerList = []
    for summonerID in summonerIDs:
        sumLookupStub = '/lol/summoner/v3/summoners/{summonerID}'
        sumRequest = api("get", sumLookupStub, dict(summonerID=summonerID))
        playerInfo = dict(name = sumRequest["name"], summonerID = sumRequest["id"], accountID = sumRequest["accountId"])
        playerList.append(playerInfo)
        if counter%50:
            print("players analyzed: " + counter)
        counter+=1
    return playerList

#main("rebelliousdino", 1000)
r = api('get', '/lol/summoner/v3/summoners/by-name/{summonerName}', dict(summonerName='rebelliousdino'))
accountId = r['accountId']
print(get_matches(accountId))
