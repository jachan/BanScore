import datetime
import requests

file = open("./apiKey.txt", "r")
apiKey = file.read().strip()
file.close()

patch_date = datetime.datetime(2017, 7, 12, 0, 0, 0)
epoch = datetime.datetime(1970, 1, 1)

def main(startingName, k):
    masterPlayerList = getIDs(startingName)

def api(method, path, data):
    url = 'https://na1.api.riotgames.com' + path
    print(url.format(**data))
    r = requests.request(method, url.format(**data), headers = {"X-Riot-Token" : apiKey})
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
        #summonerIDs
        playersFound.add(playerData["playerOrTeamId"])
    return playersFound

def get_matches(accountId):
    # https://developer.riotgames.com/api-methods/#match-v3/GET_getMatchlist
    beginTime = int((patch_date - epoch).total_seconds() * 1e3)
    url = '/lol/match/v3/matchlists/by-account/{accountId}?beginTime={beginTime}'
    matchlist = api('get', url, locals())
    return matchlist['matches']

def get_summoner(summonerId):
    # https://developer.riotgames.com/api-methods/#summoner-v3/GET_getBySummonerId
    url = '/lol/summoner/v3/summoners/{summonerId}'
    summoner = api('get', url, locals())
    return summoner

#main("rebelliousdino")
#getKIDs("Little Pengweng")
print(get_summoner(42776211))
import random
print('\n'.join(map(str, random.sample(get_matches(205328703), 10))))
