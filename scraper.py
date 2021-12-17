import requests
from lxml import html
import json


headers = {
	'Connection': 'keep-alive',
	'Cache-Control': 'max-age=0',
	'Upgrade-Insecure-Requests': '1',
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
	'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
}

def getPage(url,jsonr=False):
	if jsonr == True:
		page = requests.post('https://ipfs.infura.io:5001/api/v0/block/get',params=(('arg', 'QmWejQxAdtrDS1dZJ7KSVTrAgVJaufzY7JfFmp3b2mbkN7/{}'.format(url)),))
		page = json.loads(page.text.strip()[7:-3].rstrip("ý").lstrip("ý"))
		return(page)
	data = requests.get(url, headers=headers)
	page = html.fromstring(data.text)
	return page



lineups = getPage("https://www.rotowire.com/football/lineups.php")


games = lineups.xpath("//div[@class='lineup is-nfl']")

db = {}
for game in games:
	visitTeam = game.xpath(".//div[@class='lineup__team is-visit']")[0].xpath(".//div[@class='lineup__abbr']//text()")[0]
	homeTeam = game.xpath(".//div[@class='lineup__team is-home']")[0].xpath(".//div[@class='lineup__abbr']//text()")[0]
	db[visitTeam] = {}
	db[homeTeam] = {}
	
	db[visitTeam]["name"] = game.xpath(".//div[@class='lineup__mteam is-visit']//text()")[0].strip()
	db[homeTeam]["name"] = game.xpath(".//div[@class='lineup__mteam is-home']//text()")[0].strip()

	vistLineup = game.xpath(".//ul[@class='lineup__list is-visit']")
	homeLineup = game.xpath(".//ul[@class='lineup__list is-home']")

	db[visitTeam]["lineup"] = {}
	db[homeTeam]["lineup"] = {}

	for player in vistLineup[0].xpath(".//li[@class='lineup__player']"):
		pos = player.xpath(".//div[@class='lineup__pos']//text()")[0]
		if pos in db[visitTeam]["lineup"]:
			db[visitTeam]["lineup"][pos] = "{}, {}".format(db[visitTeam]["lineup"][pos],player.xpath(".//a/@title")[0])
			continue
		db[visitTeam]["lineup"][pos] = player.xpath(".//a/@title")[0]
	for player in homeLineup[0].xpath(".//li[@class='lineup__player']"):
		pos = player.xpath(".//div[@class='lineup__pos']//text()")[0]
		if pos in db[homeTeam]["lineup"]:
			db[homeTeam]["lineup"][pos] = "{}, {}".format(db[homeTeam]["lineup"][pos],player.xpath(".//a/@title")[0])
			continue
		db[homeTeam]["lineup"][pos] = player.xpath(".//a/@title")[0]
		
db["OAK"] = db["LV"]

def search(team,pos):
	return(db[team]["lineup"][pos])
	
def cardlookup(sbId):
	card = {}
	cardData = getPage(sbId,jsonr=True)["attributes"]
	for player in cardData:
		card[player['trait_type']] = player["value"]
	return([card,sbId])

def cardPlayers(card):
	card = cardlookup(card)
	for player in card[0]:
		if player == "LEVEL":
			continue
		if player[:-1] == "DST":
			print("{}({}): {}".format(card[0][player],db[card[0][player]]["name"],player))
			continue
		name = search(card[0][player],player[:-1])
		print("{}({}): {} - {}".format(card[0][player],db[card[0][player]]["name"],player,name))


while True:
	cardPlayers(input("Input Card ID: "))

