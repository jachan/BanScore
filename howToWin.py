import requests
import json

file = open("./apiKey.txt", "r")
apiKey = file.read().strip()
file.close()

def main(startingName, k):
    masterPlayerList = getIDs(startingName)

def api(method, url, data):
    r = requests.request(method, url.format(**data), headers = {"X-Riot-Token" : apiKey})
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
        #summonerIDs
        playersFound.add(playerData["playerOrTeamId"])
    return playersFound

def make

main("rebelliousdino")
#getKIDs("Little Pengweng")
