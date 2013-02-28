###############################################################################
#                               Score Fetch v0.7                              #
#                                   For Linux,                                #
#                              and soon, Android!                             #
#                Improved Score display, following the KISS philosophy        #
#                           And downloads Podcasts too!                       #
#                                                                             #
###############################################################################

import urllib2
import pytz
import datetime
import time
import json
import os
import elementtree.ElementTree as ET
from bs4 import BeautifulSoup as bs
from colorama import Fore
import subprocess


url = 'http://scores.nbcsports.msnbc.com/ticker/data/gamesMSNBC.\
js.asp?jsonp=true&sport=%s&period=%d'


def sportsFetch(league):
    yymmdd = int(datetime.datetime.now(pytz.timezone('US/Mountain'))
    .strftime("%Y%m%d"))
    Fore.RESET

    try:
        Fore.RESET
        f = urllib2.urlopen(url % (league, yymmdd))
        jsonp = f.read()
        f.close()
        jsonStr = jsonp.replace(
        'shsMSNBCTicker.loadGamesData(', '').replace(');', '')
        jsonParsed = json.loads(jsonStr)
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
            lineLenV = 6 - len(away)
            lineLenH = 6 - len(home)
            print per, away.rjust(lineLenV), visitScore
            print clock, home.rjust(lineLenH), homeScore
            Fore.RESET
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
    if choice.lower() == 'nba' or choice == str(2):
        return nbaScoreFetch()
    elif choice.lower() == 'nhl'or choice == str(1) or choice == '':
        return nhlScoreFetch()
    elif choice.lower() == 'exit':
        print 'exiting'
    else:
        print 'Check your typing, and it must be either the NHL or NBA. '
        leagueChoice()


def dlPodcast(podcast, startlink, endlink):
    opener = urllib2.build_opener()
    url_opener = opener.open(podcast)
    page = url_opener.read()
    html = str(bs(page))
    startLink = html.find(startlink)
    endLink = html.find(endlink, startLink)
    podcastUrl = html[startLink:endLink]
    try:
        mp3file = urllib2.urlopen(podcastUrl)
        fileName = podcastUrl.split('/')[-1]
        output = open(fileName, 'wb')
        print Fore.MAGENTA + 'downloading... Then opening' + Fore.RESET
        output.write(mp3file.read())
        output.close()
        subprocess.call(['xdg-open ' + fileName], shell=True)

    except Exception:
        print 'No podcasts for today'


def whichPod():
    soupLinkBHS = 'http://feeds.feedburner.com/TheBackhandShelfPodcast'
    soupLinkTBJ = 'http://feeds.feedburner.com/thescore/\
podcasts/thebasketballjones'
    bhsStartLink = 'http://podcastmedia.thescore.com/ooyala-mirror/'
    tbjStartLink = 'http://feedproxy.google.com/~r/thescore/podcasts/\
thebasketballjones/'
    bhsEndLink = '</guid>'
    tbjEndLink = '></media:content>'
    print '==========================='
    podChoice = raw_input(Fore.CYAN + '\'b\' for The Backhand Shelf\n\'j\' \
for The Basketball Jones\n>>> ' + Fore.RESET)
    if podChoice.lower() == 'b' or podChoice == str(1):
        dlPodcast(soupLinkBHS, bhsStartLink, bhsEndLink)
        nhlScoreFetch()
    if podChoice.lower() == 'j' or podChoice == str(2):
        dlPodcast(soupLinkTBJ, tbjStartLink, tbjEndLink)
        nbaScoreFetch()
    else:
        print'type \'b\' or \'j\''
        whichPod()


def sleepLength():
    try:
        if str(toSleep) == '':
            time.sleep(30)
        else:
            time.sleep(int(toSleep))
    except Exception:
        time.sleep(30)


dlsf = raw_input(Fore.CYAN + 'Download and listen to a podcast?\
 Or get current scores?:\n' +
    'Type ' + Fore.YELLOW + "'d'" + Fore.CYAN + 'to download, or ' +
    Fore.YELLOW + "'sf'" + Fore.CYAN + ' to Score Fetch\n>>> ' + Fore.RESET)
if dlsf.lower() == 'd' or dlsf == str(1) or dlsf == '':
    whichPod()
else:
    choice = raw_input(Fore.CYAN + '\'NHL\' or \'NBA\'\n>>> ' + Fore.RESET)
    toSleep = raw_input(Fore.CYAN + 'Refresh wait time?\n>>> ' + Fore.RESET)
    leagueChoice()
