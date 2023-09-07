import requests
from bs4 import BeautifulSoup
import re
from prettytable import PrettyTable

epl = 'https://www.sports.ru/epl/table/'
laliga = 'https://www.sports.ru/la-liga/table/'
url = epl

response = requests.get(url)
bs = BeautifulSoup(response.text, features='lxml')

head = bs.find('thead')
team_stats = bs.find('tbody')

cols = ['Место', head.find('td', 'name-td alLeft bordR').text]

cols.extend(re.findall(r'title="([А-я ]+)">', head.__str__()))

team_data = team_stats.__str__()
main_table = [[a for a in i.split('\n') if a] for i in team_stats.text.split('\n\n\n')]


class Team:
    def __init__(self, place, name, matches, wins, draws, loses, scored, conceded, points):
        self.place = place
        self.name = name
        self.matches = matches
        self.wins = wins
        self.draws = draws
        self.loses = loses
        self.scored = scored
        self.conceded = conceded
        self.points = points


comands = []
for team in main_table:
    comands.append(Team(team[0], team[1], team[2], team[3], team[4], team[5], team[6], team[7], team[8]))

table = PrettyTable()
table.field_names = cols

for el in comands:
    table.add_row([el.place, el.name, el.matches, el.wins, el.draws, el.loses, el.scored, el.conceded, el.points])

print(table)
