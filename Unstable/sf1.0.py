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
import json
import os
import elementtree.ElementTree as ET
import kivy
kivy.require('1.5.1')
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.uix.button import Button
#from kivy.core.text import LabelBase as lb


url = 'http://scores.nbcsports.msnbc.com/ticker/data/gamesMSNBC.\
js.asp?jsonp=true&sport=%s&period=%d'


class ScoreFetchApp(App):

	def nhlCallback(instance):
		if __name__ == '__main__':
			for league in ['NHL']:
				return ScoreFetchApp.sportsFetch(league)

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
				vTree = gameTree.find('visiting-team')
				homeTree = gameTree.find('home-team')
				gSTREE = gameTree.find('gamestate')
				home = homeTree.get('nickname')
				away = + vTree.get('nickname')
				hScore = homeTree.get('score')
				aScore = vTree.get('score')
				per = gSTREE.get('display_status2')
				clock = gSTREE.get('display_status1')
				os.environ['TZ'] = 'US/Mountain'
				del os.environ['TZ']
				line1 = per + away + aScore
				line2 = clock + home + hScore
				return line1, line2
		except Exception, e:
			print e

	def build(self):
		#NHLScore = lb(ScoreFetchApp.nhlScoreFetch())
		NHLBtn = Button(text='NHL', border=(3, 3, 3, 3))
		layout = BoxLayout(orientation='vertical')
		NHLBtn.bind(on_press=ScoreFetchApp.nhlCallback())
		layout.add_widget(NHLBtn)
		return layout


if __name__ == '__main__':
	ScoreFetchApp().run()
