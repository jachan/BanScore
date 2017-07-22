import requests
import json
import datetime

file = open("./apiKey.txt", "r")
apiKey = file.read().strip()
file.close()

def main(startingName, k):
    idSet = set()
    masterPlayerList = []

    newIDs = getIDs(startingName)
    idSet.update(newIDs)
    while len(masterPlayerList) < k:
        newPlayers = makeRecords(newIDs)
        masterPlayerList.extend(newPlayers)
        newIDs, games = getMatches(newPlayers)
        idSet.update(newIDs)

def api(method, url, data):
    r = requests.request(method, url.format(**data), headers = {"X-Riot-Token" : apiKey})
    #remember the last time a request was made, and wait to make another request
    #riot rate limit: 20/sec, 100/2min
    time.sleep(0.75)
    return r.json()

def getIDs(startingName):
    nameLookupStub = 'https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/{startingName}'
    nameRequest = api("get", nameLookupStub, dict(startingName=startingName))
    summonerID = nameRequest["id"]
    accountID = nameRequest["accountId"]

    divLookupStub = "https://na1.api.riotgames.com/lol/league/v3/leagues/by-summoner/{startingID}"
    divRequest = api("get", divLookupStub, dict(startingID=summonerID))
    playersFound = set()
    for leagueData in divRequest:
        if leagueData["queue"] == "RANKED_SOLO_5x5":
            entries = leagueData["entries"]
    for playerData in entries:
        #adds summonerIDs to the master list of players found
        playersFound.add(playerData["playerOrTeamId"])
    return playersFound

counter = 0;
def makeRecords(summonerIDs):
    playerList = []
    for summonerID in summonerIDs:
        sumLookupStub = 'https://na1.api.riotgames.com/lol/summoner/v3/summoners/{summonerID}'
        sumRequest = api("get", nameLookupStub, dict(summonerID=summonerID))
        playerInfo = ict(name = sumRequest["name"], summonerID = sumRequest["id"], accountID = sumRequest["accountId"])
        playerList.append(playerInfo)
        if counter%50:
            print(counter)
        counter+=1
    return playerList

main("rebelliousdino", 1000)
