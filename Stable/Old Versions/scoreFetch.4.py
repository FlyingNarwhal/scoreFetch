#/usr/lin/python
###############################################################################
#                            NBA Score Fetch v.0.4
#                            For Linux and Windows
#
#    *NOTE*
# Needed 3rd party modules: pytz and ElementTree if using Windows, note that
# ansi.sys must be enabled.
#
#
#
#
# Things to try out, print out all information to a conky configuration.
###############################################################################

import urllib2
import pytz
import datetime
import time
import json
import os
import platform
import elementtree.ElementTree as ET


if platform.system() == 'Windows':
    from winsound import Beep


url = 'http://scores.nbcsports.msnbc.com/ticker/data/gamesMSNBC.\
js.asp?jsonp=true&sport=%s&period=%d'


def sportsFetch(league, sport):
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
            gameTree = ET.XML(gameStr)
            visitingTree = gameTree.find('visiting-team')
            homeTree = gameTree.find('home-team')
            gamestateTree = gameTree.find('gamestate')
            home = homeTree.get('nickname')
            away = visitingTree.get('nickname')
            homeScore = homeTree.get('score')
            visitScore = visitingTree.get('score')
            per = gamestateTree.get('display_status2')
            clock = gamestateTree.get('display_status1')
            os.environ['TZ'] = 'US/Mountain'
            del os.environ['TZ']
            if sport == 'nba':
                if clock == 'Final':
                    if int(visitScore) > int(homeScore):
                        print 'In ' + away + " at " + home + ', ' + away +\
                        ' win(s) ' + visitScore + ' to ' + homeScore
                    elif int(visitScore) < int(homeScore):
                        print 'In ' + away + " at " + home + ', ' + home +\
                        ' win(s) ' + homeScore + ' to ' + visitScore
                elif visitScore == '' and homeScore == '':
                    print away + ', ' + home + ' at: ' + clock + ' EST'
                else:
                    if clock == 'Half':
                        if int(visitScore) > int(homeScore):
                            print away, visitScore, home, homeScore
                            + ' halftime'
                            print ''
                        elif int(visitScore) < int(homeScore):
                            print home, homeScore, away, visitScore
                            + ' at half'
                            print ''
                        elif int(visitScore) == int(homeScore):
                            print away + ', ' + home + ' tied with '
                            + homeScore +\
                            ' at half'
                    elif clock == 'End':
                        print
                    else:
                        print away, visitScore + ' at'
                        print home, homeScore + ' with ' + clock + ' in ' + per
                        print ''
            if sport == 'nhl':
                if clock == 'Final':
                    if int(visitScore) > int(homeScore):
                        print 'In ' + away + " at " + home + ', ' + away +\
                        ' win(s) ' + visitScore + ' to ' + homeScore
                    elif int(visitScore) < int(homeScore):
                        print 'In ' + away + " at " + home + ', ' + home +\
                        ' win(s) ' + homeScore + ' to ' + visitScore
                elif visitScore == '' and homeScore == '':
                    print away + ', ' + home + ' at: ' + clock + ' EST'
                    print ''
                else:
                    if clock == 'Int':
                        if int(visitScore) > int(homeScore):
                            print away, visitScore, home, homeScore
                            + ' halftime'
                            print ''
                        elif int(visitScore) < int(homeScore):
                            print home, homeScore, away, visitScore
                            + ' at half'
                            print ''
                        elif int(visitScore) == int(homeScore):
                            print away + ', ' + home + ' tied with '
                            + homeScore +\
                            ' at half'
                    elif clock == 'End':
                        print
                    else:
                        print away, visitScore + ' at'
                        print home, homeScore + ' end of ' + clock
                        print ''
    except Exception, e:
        print e


def nbaScoreFetch():
    if __name__ == "__main__":
        while sportsFetch:
            for league in ['NBA']:
                sportsFetch(league, 'nba')
                sleepLength()
                print os.name
                if platform.system() == 'Windows':
                    toNotify()
                os.system('clear')


def nhlScoreFetch():
    if __name__ == "__main__":
        while sportsFetch:
            for league in ['NHL']:
                sportsFetch(league, 'nhl')
                sleepLength()
                if platform.system() == 'Windows':
                    toNotify()
                os.system('clear')


def leagueChoice():
    choice = raw_input('Type \'NBA\' or \'NHL\': ')
    if choice.lower() == 'nba' or choice == str(1):
        return nbaScoreFetch()
    elif choice.lower() == 'nhl'or choice == str(2) or choice == '':
        return nhlScoreFetch()
    elif choice.lower() == 'exit':
        print 'exiting'
    else:
        print 'Check your typing, and it must be either the NHL or NBA. '
        leagueChoice()


def toNotify():
    if notify.lower() == 'y' or notify.lower() == 'yes':
        Beep(1500, 30)
    elif notify.lower() == 'n' or notify.lower() == 'no' or notify == '':
        pass


def sleepLength():
    if str(toSleep) == '':
        time.sleep(3)
    else:
        time.sleep(int(toSleep))


toSleep = raw_input('Refresh time? ')
if platform.system() == 'Windows':
    notify = raw_input('and should I notify you? ')
else:
    leagueChoice()
leagueChoice()
