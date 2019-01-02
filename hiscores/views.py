from django.shortcuts import render
from django.utils import timezone

from .models import Player

import datetime
import requests
from bs4 import BeautifulSoup

usernames = [
    "ChaoTea",
    "A1Shoe",
    "joegrenda",
    "ANC00",
    "albertfuxgoats"
]

def index(request):

    table_dict = {
        "column_names": ["Doge", "Rank", "Wins", "Losses", "Total"],
        "rows": []
    }

    for username in usernames:
        get_stats(username)
        latest = Player.objects.filter(name=username).latest("datetime")
        if latest.datetime < (timezone.now() - datetime.timedelta(days=1)):
            get_stats(username)
            latest = Player.objects.filter(name=username).latest("datetime")

        table_dict["rows"].append([latest.name, latest.rank, latest.wins, latest.losses, latest.total])

    context = {
        "hiscores": table_dict,
    }

    return render(request, "index.html", context)

def get_stats(username):
    try:
        page = requests.get(f"http://na.op.gg/summoner/userName={username}")
        html = BeautifulSoup(page.text, "html.parser")

        summoner_rating_medium = html.find("div", attrs={"class": "SummonerRatingMedium"})

        rank = summoner_rating_medium.find("span", attrs={"class": "tierRank"}).text.strip()
        if rank == "Unranked":
            wins = 0
            losses = 0
            total = 0
        else:
            wins = int(summoner_rating_medium.find("span", attrs={"class": "wins"}).text.strip().rstrip("W"))
            losses = int(summoner_rating_medium.find("span", attrs={"class": "losses"}).text.strip().rstrip("L"))
            total = wins + losses

        new_player = Player.objects.create(name=username, rank=rank, wins=wins, losses=losses, total=total)
    except:
        return
