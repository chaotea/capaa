from django.shortcuts import render
from django.utils import timezone

from .models import Player


def index(request):

    table_dict = {
        "rows": []
    }

    usernames = set(Player.objects.values_list("name", flat=True))

    for username in usernames:
        latest = Player.objects.filter(name=username).latest("datetime")
        table_dict["rows"].append([latest.name, latest.rank, latest.wins, latest.losses, latest.total])

    def sort_ranks(element):
        rank = element[1]
        if rank.startswith("Iron"):
            rank_value = 10
        elif rank.startswith("Bronze"):
            rank_value = 20
        elif rank.startswith("Silver"):
            rank_value = 30
        elif rank.startswith("Gold"):
            rank_value = 40
        elif rank.startswith("Plat"):
            rank_value = 50
        elif rank.startswith("Diamond"):
            rank_value = 60
        elif rank.startswith("Master"):
            rank_value = 70
        elif rank.startswith("Grandmaster"):
            rank_value = 80
        elif rank.startswith("Challenger"):
            rank_value = 90
        else:
            rank_value = 0
        if rank.endswith("5"):
            rank_value += 1
        elif rank.endswith("4"):
            rank_value += 2
        elif rank.endswith("3"):
            rank_value += 3
        elif rank.endswith("2"):
            rank_value += 4
        elif rank.endswith("1"):
            rank_value += 5
        else:
            rank_value += 0
        return rank_value

    table_dict["rows"].sort(key=sort_ranks, reverse=True)

    context = {
        "hiscores": table_dict,
    }

    return render(request, "index.html", context)

def get_stats(username):
    import requests
    from bs4 import BeautifulSoup
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
