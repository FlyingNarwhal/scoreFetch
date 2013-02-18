###############################################################################
#                               Score Fetch v0.6                              #
#                                   For Linux,                                #
#                              and soon, Android!                             #
#                Improved Score display, following the KISS philosophy        #
#                                                                             #
###############################################################################

import urllib2
import pytz
import datetime
import time
import json
import os
import elementtree.ElementTree as ET
from colorama import Fore


url = 'http://scores.nbcsports.msnbc.com/ticker/data/gamesMSNBC.\
js.asp?jsonp=true&sport=%s&period=%d'


def sportsFetch(league):
    yymmdd = int(datetime.datetime.now(pytz.timezone('US/Mountain'))
    .strftime("%Y%m%d"))

    try:
        f = urllib2.urlopen(url % (league, yymmdd))
        jsonp = f.read()
        f.close()
        jsonStr = jsonp.replace(
        'shsMSNBCTicker.loadGamesData(', '').replace(');', '')
        jsonParsed = json.loads(jsonStr)
        #print jsonStr
        for gameStr in jsonParsed.get('games', []):
            rows, columns = os.popen('stty size', 'r').read().split()
            gameTree = ET.XML(gameStr)
            visitingTree = gameTree.find('visiting-team')
            homeTree = gameTree.find('home-team')
            gameSTree = gameTree.find('gamestate')
            home = Fore.MAGENTA + homeTree.get('nickname') + Fore.RESET
            away = Fore.YELLOW + visitingTree.get('nickname') + Fore.RESET
            homeScore = Fore.CYAN + homeTree.get('score') + Fore.RESET
            visitScore = Fore.CYAN + visitingTree.get('score') + Fore.RESET
            per = Fore.GREEN + gameSTree.get('display_status2') + Fore.RESET
            clock = Fore.GREEN + gameSTree.get('display_status1') + Fore.RESET
            os.environ['TZ'] = 'US/Mountain'
            del os.environ['TZ']
            # Print out scores
            lineLenV = 6 - len(away)
            lineLenH = 6 - len(home)
            #lineLenVP =
            #lineLenHP =
            print per, away.rjust(lineLenV), visitScore
            print clock, home.rjust(lineLenH), homeScore
    except Exception, e:
        print e


def nbaScoreFetch():
    if __name__ == "__main__":
        while sportsFetch:
            for league in ['NBA']:
                sportsFetch(league)
                sleepLength()
                os.system('clear')


def nhlScoreFetch():
    if __name__ == "__main__":
        while sportsFetch:
            for league in ['NHL']:
                sportsFetch(league)
                sleepLength()
            os.system('clear')


def leagueChoice():
    if choice.lower() == 'nba' or choice == str(1):
        return nbaScoreFetch()
    elif choice.lower() == 'nhl'or choice == str(2) or choice == '':
        return nhlScoreFetch()
    elif choice.lower() == 'exit':
        print 'exiting'
    else:
        print 'Check your typing, and it must be either the NHL or NBA. '
        leagueChoice()


def sleepLength():
    if str(toSleep) == '':
        time.sleep(30)
    else:
        time.sleep(int(toSleep))


choice = raw_input(Fore.CYAN + 'Type \'NBA\' or \'NHL\': ' + Fore.RESET)
toSleep = raw_input(Fore.CYAN + 'Refresh Time? ' + Fore.RESET)
leagueChoice()
