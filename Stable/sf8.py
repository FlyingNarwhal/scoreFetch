###############################################################################
#                               Score Fetch v0.8                              #
#                                   For Linux,                                #
#                              and soon, Android!                             #
#            Improved Score display, following the KISS philosophy,           #
#                   downloads Podcasts, and plays live feeds!                 #
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
import termios
import sys
import webbrowser


url = 'http://scores.nbcsports.msnbc.com/ticker/data/gamesMSNBC.\
js.asp?jsonp=true&sport=%s&period=%d'
TERMIOS = termios
isPlaying = []


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
        global isPlaying
        for gameStr in jsonParsed.get('games', []):
            gameTree = ET.XML(gameStr)
            visitingTree = gameTree.find('visiting-team')
            homeTree = gameTree.find('home-team')
            gameSTree = gameTree.find('gamestate')
            home = Fore.MAGENTA + homeTree.get('nickname') + Fore.RESET
            away = Fore.YELLOW + visitingTree.get('nickname') + Fore.RESET
            isPlaying.append(str(homeTree.get('nickname')))
            isPlaying.append(str(visitingTree.get('nickname')))
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
            teams = open('team.txt', 'r').read()
            favList = teams.split('\n')
            for common in favList:
                if common in isPlaying and 'wasrun' not in isPlaying:
                        print 'Watch your teams live feed?'
                        playFeed = getkey()
                        if playFeed == 'y':
                            showFeed(common)
                            isPlaying = ['wasrun']
                            global runCount
                        elif playFeed == 'n':
                            isPlaying = ['wasrun']
            else:
                pass

    except Exception, e:
        print e


def nbaScoreFetch():
    try:
        if __name__ == "__main__":
            while sportsFetch:
                for league in ['NBA']:
                    sportsFetch(league)
                    sleepLength()
                os.system('clear')
    except KeyboardInterrupt:
        print '\nGame over; go home'


def nhlScoreFetch():
    try:
        if __name__ == "__main__":
            while sportsFetch:
                for league in ['NHL']:
                    sportsFetch(league)
                    sleepLength()
                os.system('clear')
    except KeyboardInterrupt:
        print '\nGame over; go home'


def leagueChoice():
    if choice == 'b':
        return nbaScoreFetch()
    elif choice == 'h':
        return nhlScoreFetch()
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
        print Fore.MAGENTA + 'downloading...'
        output.write(mp3file.read())
        output.close()
        print 'opening' + Fore.RESET
        subprocess.call(['xdg-open ' + fileName], shell=True)

    except Exception:
        print 'No podcasts for today'


def showFeed(common):
    if choice == 'h':
        url = 'http://www.firstrow1.eu/sport/ice-hockey.html'
        opener = urllib2.build_opener()
        url_opener = opener.open(url)
        page = url_opener.read()
        html = str(bs(page))
        startLink = html.find('href="/watch', html.find(common))
        endLink = html.find('.html"', startLink)
        feed = 'http://www.firstrow1.eu' + html[startLink + 6: endLink + 5]
        webbrowser.open_new_tab(feed)
    elif choice == 'b':
        url = 'http://www.firstrow1.eu/sport/basketball.html'
        opener = urllib2.build_opener()
        url_opener = opener.open(url)
        page = url_opener.read()
        html = str(bs(page))
        startLink = html.find('href="/watch', html.find(common))
        endLink = html.find('.html"', startLink)
        feed = 'http://www.firstrow1.eu' + html[startLink + 6: endLink + 5]
        webbrowser.open_new_tab(feed)


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
    print Fore.YELLOW + '\'b\'' + Fore.CYAN + 'The Backhand Shelf\n\
' + Fore.YELLOW + '\'j\'' + Fore.CYAN + 'The Basketball Jones' + Fore.RESET
    podChoice = getkey()
    if podChoice == 'b':
        dlPodcast(soupLinkBHS, bhsStartLink, bhsEndLink)
        nhlScoreFetch()
    if podChoice == 'j':
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


def getkey():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] = new[3] & ~TERMIOS.ICANON & ~TERMIOS.ECHO
    new[6][TERMIOS.VMIN] = 1
    new[6][TERMIOS.VTIME] = 0
    termios.tcsetattr(fd, TERMIOS.TCSANOW, new)
    c = None
    try:
        c = os.read(fd, 1)
    finally:
        termios.tcsetattr(fd, TERMIOS.TCSAFLUSH, old)
    return c


print Fore.YELLOW + "'d' " + Fore.CYAN + 'Download and\
 listen to a podcast?\n' + Fore.YELLOW + "'s' " + Fore.CYAN + 'Get cur\
rent scores?\n' + Fore.YELLOW + "'f' " + Fore.CYAN + 'Make a te\
am your favorite?' + Fore.RESET
dlsf = getkey()


if dlsf.lower() == 'd':
    print 'download podcast'
    whichPod()

elif dlsf.lower() == 'f':
    global favList
    teams = open('team.txt', 'w')
    addTeam = raw_input('Enter Team\n>>> ')
    addTeam = addTeam.title()
    teams.write(addTeam)
    teams.close()
    teams = open('team.txt', 'r').read()
    favList = teams.split('\n')
    toSleep = ''
    print Fore.YELLOW + '\'h\'' + Fore.CYAN + 'NHL\n' + Fore.YELLOW + '\'b\'\
' + Fore.CYAN + 'NBA' + Fore.RESET
    choice = getkey()
    if choice == 'h':
        print 'NHL'
    elif choice == 'b':
        print 'NBA'
    leagueChoice()

else:
    print 'ScoreFetch!\n==========='
    print Fore.YELLOW + '\'h\' ' + Fore.CYAN + 'NHL\n' + Fore.YELLOW + '\'b\' \
' + Fore.CYAN + 'NBA' + Fore.RESET
    choice = getkey()
    if choice == 'h':
        print 'NHL'
    elif choice == 'b':
        print 'NBA'
    toSleep = raw_input(Fore.CYAN + 'Refresh wait time?\n>>> ' + Fore.RESET)
    leagueChoice()

favList = []
