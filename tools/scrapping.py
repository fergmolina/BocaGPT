import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

def get_players(url, second_team = False):
    """Scrap information about the available (not sanctioned neither injured) players of the team from Transfermarkt
    Args:
        url: String with the url of the team site of Transfermarket 
        second_team: Boolean flag to define if we are scrapping the second squad or the first squad
    Returns: A list of available players to use in the next match
    """

    headers = {'User-Agent': 
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    page = url
    pageTree = requests.get(page, headers=headers)
    pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

    players = pageSoup.find("table", {"class": "items"})

    players_list = list()

    for player in players.findAll("tr", class_=["odd","even"]):
        player_row = {
            'name': '',
            'position': '',
            'extra_data': ''
        }
        for column in player.findAll("td"):
            class_column = column.get('class')

            # Name
            if class_column != None and 'hide' in class_column: 
                    player_row['name'] = column.text

            # Position
            if class_column == None: 
                player_row['position'] = column.text
            
            # Injury or Red Card
            if class_column != None and 'hauptlink' in class_column and len(class_column) == 1:
                for extra_data in column.findAll("span"):
                    data = extra_data.get('title')
                    if data != None:
                        player_row['extra_data'] = data
        
        # Avoid the players that can't play 
        if player_row['extra_data'] != '' or player_row['extra_data'] == 'Team Captain':
            continue

        # Second Team
        if second_team == True:
            if player_row['extra_data'] == '':
                player_row['extra_data'] = 'Second Team'
            else:
                player_row['extra_data'] = player_row['extra_data']  + ' - Second Team '


        players_list.append(player_row)
    return (players_list)

def get_players_full_roster():
    """Function to create a unified list of available players including the first and second squad
    Args:-
    Returns: A list of available players of the first and second team to use in the next match
    """

    players = []
    load_dotenv()

    first_team_url = os.getenv("FIRST_TEAM_ROSTER")
    players = get_players(first_team_url,second_team=False)

    second_team_url = os.getenv("SECOND_TEAM_ROSTER")
    players = players + get_players(second_team_url,second_team=True)

    return players


def get_matches():
    """Scrap information about the past and following matches from FBREF
    Args:-
    Returns: A list of matches objects with information of them
    """
    headers = {'User-Agent': 
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    load_dotenv()

    page = os.getenv("MATCHES")
    pageTree = requests.get(page, headers=headers)
    pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

    matches = pageSoup.find("table", {"id": "matchlogs_for"})

    matches_list = list()

    for match in matches.findAll("tr"):

        match_row = {
            'date': '',
            'start_time': '',
            'comp': '',
            'round': '',
            'dayofweek': '',
            'venue': '',
            'result': '',
            'goals_for': '',
            'goals_against': '',
            'opponent': ''
        }
        
        # Date
        for column in match.find('th'):
            match_row['date'] = column.text
        
        # Other attributes
        for column in match.findAll("td"):
            class_col = column.get('data-stat')
            try:
                if class_col not in ['match_report', 'notes', 'referee', 'formation', 'captain', 'attendance','possession', 'xg_against', 'xg_for']:
                    match_row[class_col] = column.text
            except:
                continue
        
        if match_row['date'] != 'Date':
            matches_list.append(match_row)

    return(matches_list)

def get_last_match():
    """Scrap information about the last match from Transfermarkt
    Args:-
    Returns: string with information about the last match played
    """
    headers = {'User-Agent': 
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
    load_dotenv()

    page = os.getenv("FIRST_TEAM_ROSTER")
    pageTree = requests.get(page, headers=headers)
    pageSoup = BeautifulSoup(pageTree.content, 'html.parser')

    last_match = pageSoup.find("div", {"class": "formation_begegnung"})

    return last_match.text

