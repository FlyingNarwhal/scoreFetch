###############################################################################
#                               Score Fetch v1.0                              #
#                            For the NHL, the NBA                             #
#                              and only on Linux                              #
#                   Added An Entire Graphical User Interface                  #
#   Download podcasts, watch a live feed, and of course, get current scores   #
#                                                                             #
###############################################################################

import urllib2
import pytz
import datetime
import json
import os
import elementtree.ElementTree as ET
from bs4 import BeautifulSoup as bs
import subprocess
import webbrowser
from os.path import isfile as isFile
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.config import Config
from kivy.uix.image import Image
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout

Config.set('graphics', 'width', '600')
Config.set('graphics', 'height', '250')

choice = 'NHL'
teamName = 'Coyotes'


class ScoreFetchGUI(FloatLayout):

    def __init__(self, **kwargs):
        super(ScoreFetchGUI, self).__init__(**kwargs)
        scoreLayout = GridLayout(
            cols=3,
            size_hint=(.7, 1),
            pos=(210, 0))
        self.add_widget(scoreLayout)
        dlPodBtn = Button(
            text='Download Podcast',
            size_hint=(.25, .15),
            pos=(20, 200))
        sfBtn = Button(
            text='ScoreFetch!',
            size_hint=(.25, .15),
            pos=(20, 150))
        feedBtn = Button(
            text='Watch Feed',
            size_hint=(.25, .15),
            pos=(20, 100))
        feedTeamInput = TextInput(
            text='Team',
            size_hint=(.25, .13),
            pos=(20, 15),
            focus=True,
            multiline=False)
        wimg = Image(source='/home/joe/Pictures/sfbanner.png',
                    pos=(0, 0))
        #enterTeamLbl = Label(
            #text='Enter Team Name:',
            #pos=(-215, -70))
        leagueToggleNHL = ToggleButton(
            text='NHL',
            group='league',
            size_hint=(.1, .1),
            pos=(27, 60),
            state='down')
        leagueToggleNBA = ToggleButton(
            text='NBA',
            group='league',
            size_hint=(.1, .1),
            pos=(100, 60))
        dlPodBtn.bind(on_release=whichPodCallback)
        leagueToggleNBA.bind(on_press=choiceCallbackNBA)
        leagueToggleNHL.bind(on_press=choiceCallbackNHL)
        feedTeamInput.bind(text=on_text)
        feedBtn.bind(on_release=showFeedCallback)
        self.add_widget(wimg)
        #self.add_widget(enterTeamLbl)
        self.add_widget(leagueToggleNHL)
        self.add_widget(leagueToggleNBA)
        self.add_widget(dlPodBtn)
        self.add_widget(sfBtn)
        self.add_widget(feedBtn)
        self.add_widget(feedTeamInput)

        url = 'http://scores.nbcsports.msnbc.com/ticker/data/gamesMSNBC.\
js.asp?jsonp=true&sport=%s&period=%d'
        yymmdd = int(datetime.datetime.now(pytz.timezone('US/Mountain'))
        .strftime("%Y%m%d"))
        scoreLayout.clear_widgets()

        def getScores(instance):
            try:
                scoreLayout.clear_widgets()
                f = urllib2.urlopen(url % (choice, yymmdd))
                jsonp = f.read()
                f.close()
                jsonStr = jsonp.replace(
                'shsMSNBCTicker.loadGamesData(', '').replace(');', '')
                jsonParsed = json.loads(jsonStr)
                for gameStr in jsonParsed.get('games', []):
                    gameTree = ET.XML(gameStr)
                    visitingTree = gameTree.find('visiting-team')
                    homeTree = gameTree.find('home-team')
                    gameSTree = gameTree.find('gamestate')
                    home = homeTree.get('nickname')
                    away = visitingTree.get('nickname')
                    homeScore = homeTree.get('score')
                    visitScore = visitingTree.get('score')
                    per = gameSTree.get('display_status2')
                    clock = gameSTree.get('display_status1')
                    os.environ['TZ'] = 'US/Mountain'
                    del os.environ['TZ']
                    playingLabel = Label(valign='top', halign='left',
                        text=visitScore + ' ' + away + ' ' + per + '\n' +
                        homeScore + ' ' + home + ' ' + clock,
                        text_size=(200, None))
                    scoreLayout.add_widget(playingLabel)

            except Exception, e:
                print e
        sfBtn.bind(on_release=getScores)


def on_text(instance, value):
    global teamName
    teamName = value
    print teamName


def choiceCallbackNBA(instance):
    global choice
    choice = 'NBA'
    print 'User selected ', choice
    global teamName
    print teamName


def choiceCallbackNHL(instance):
    global choice
    choice = 'NHL'
    print 'User selected ', choice


def dlPodcast(podcast, startlink, endlink):
    opener = urllib2.build_opener()
    url_opener = opener.open(podcast)
    page = url_opener.read()
    html = str(bs(page))
    startLink = html.find(startlink)
    endLink = html.find(endlink, startLink)
    podcastUrl = html[startLink:endLink]
    print 'Downloading Podcast just wait'
    try:
        mp3file = urllib2.urlopen(podcastUrl)
        fileName = podcastUrl.split('/')[-1]
        if isFile(fileName):
            subprocess.call(['xdg-open ' + fileName], shell=True)
        else:
            output = open(fileName, 'wb')
            output.write(mp3file.read())
            output.close()
            subprocess.call(['xdg-open ' + fileName], shell=True)

    except Exception:
        print 'Error in dlPodcast'


def whichPodCallback(instance):
    global choice

    soupLinkBHS = 'http://feeds.feedburner.com/TheBackhandShelfPodcast'
    soupLinkTBJ = 'http://feeds.feedburner.com/thescore/\
podcasts/thebasketballjones'
    bhsStartLink = 'http://podcastmedia.thescore.com/ooyala-mirror/'
    tbjStartLink = 'http://feedproxy.google.com/~r/thescore/podcasts/\
thebasketballjones/'
    bhsEndLink = '</guid>'
    tbjEndLink = '></media:content>'
    if choice == 'NHL':
        dlPodcast(soupLinkBHS, bhsStartLink, bhsEndLink)
    elif choice == 'NBA':
        dlPodcast(soupLinkTBJ, tbjStartLink, tbjEndLink)
    else:
        print 'Choose a League'


def showFeedCallback(instance):
    print choice
    print teamName
    query = str(teamName.title())
    if choice == 'NHL':
        url = 'http://www.firstrow1.eu/sport/ice-hockey.html'
        opener = urllib2.build_opener()
        url_opener = opener.open(url)
        page = url_opener.read()
        html = str(bs(page))
        startLink = html.find('href="/watch', html.find(query))
        endLink = html.find('.html"', startLink)
        feed = 'http://www.firstrow1.eu' + html[startLink + 6: endLink + 5]
        webbrowser.open_new_tab(feed)
    elif choice == 'NBA':
        url = 'http://www.firstrow1.eu/sport/basketball.html'
        opener = urllib2.build_opener()
        url_opener = opener.open(url)
        page = url_opener.read()
        html = str(bs(page))
        startLink = html.find('href="/watch', html.find(teamName))
        endLink = html.find('.html"', startLink)
        feed = 'http://www.firstrow1.eu' + html[startLink + 6: endLink + 5]
        webbrowser.open_new_tab(feed)


class ScoreFetch(App):

    icon = '/home/joe/scoreFetch/logo/scoreFetch.ico'

    def build(self):
        return ScoreFetchGUI()


if __name__ == '__main__':
    ScoreFetch().run()
