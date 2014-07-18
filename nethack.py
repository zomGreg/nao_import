#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import string

from sqlalchemy import create_engine, schema, types
from BeautifulSoup import BeautifulSoup
import prettytable
from collections import Counter
import pickle, simplejson
import datetime
from os import listdir
from os.path import isfile, join

import create_db

#players=['bose','mscurmudgeon','stth','Vodalus','muad']
players = ['zomgreg']


def get_player_file(player_name):
    '''
    This function will save the associated player_name html file
    into the ./player_html directory.
    '''

    #player_name="zomgreg"

    req_string = 'http://alt.org/nethack/player-all-xlog.php?player=%s' % (player_name)

    req = urllib2.Request(req_string)
    response = urllib2.urlopen(req)
    html = response.read()
    ##
    f = open('./player_files/%s.html' % player_name, 'w')
    f.write(html)
    f.close()

g = create_db.Games()

metadata = schema.MetaData()
engine = create_engine('sqlite:///players.db', echo=False)
metadata.bind = engine

def process_html_file(player_file):

    f = open(player_file, 'r')
    soup = BeautifulSoup(f)
    all_games = soup.findAll('pre')[0].string.split('\n')
    print "Importing %s games." % (len(all_games))
    f.close()

    game_list = []
    print len(all_games)
    for i in range(0, len(all_games) - 1):
        keys = [t.split('=')[0] for t in all_games[i].split(':')]
        values = [t.split('=')[1] for t in all_games[i].split(':')]
        game = dict(zip(keys, values))
        game_list.append(game)

    for game in game_list:
        game_dict = dict(align0=game.get('align0', 'None'), deathlev=game['deathlev'], uid=game['uid'],
                         deaths=game['deaths'],
                         turns=game.get('turns', 0), points=game['points'], death=game['death'],
                         realtime=game.get('realtime', 0),
                         version=game['version'], role=game['role'], conduct=game.get('conduct', 'None'),
                         gender0=game.get('gender0', 'N/A'),
                         deathdate=datetime.datetime.strptime(game['deathdate'], "%Y%m%d").date(), hp=game['hp'],
                         achieve=game.get('achieve', 0), gamedelta=game.get('gamedelta', 0), maxlvl=game['maxlvl'],
                         maxhp=game['maxhp'],
                         endtime=datetime.datetime.fromtimestamp(int(game.get('endtime', 0))),
                         nachieves=game.get('nachieves', 0),
                         nconducts=game.get('nconducts', 0), name=game['name'], gender=game['gender'],
                         align=game['align'],
                         birthdate=datetime.datetime.strptime(game['birthdate'], "%Y%m%d").date(), race=game['race'],
                         flags=game.get('flags', 0),
                         starttime=datetime.datetime.fromtimestamp(int(game.get('starttime', 0))),
                         deathdnum=game['deathdnum']
        )

        create_db.load_game(game_dict)


def process_player_file(player_file):
    f = open(player_file, 'r')

    for line in f.readlines():
        keys = [t.split('=')[0] for t in line.split(':')]
        values = [filter(lambda x: x in string.printable, t.split('=')[1]) for t in line.split(':')]

        #for v in values:
        #	print v, filter(lambda x: x in string.printable, v),type(v)

        game = dict(zip(keys, values))

        game_dict = dict(align0=game.get('align0', 'None'), deathlev=game['deathlev'], uid=game['uid'],
                         deaths=game['deaths'],
                         turns=game.get('turns', 0), points=game['points'], death=game['death'],
                         realtime=game.get('realtime', 0),
                         version=game['version'], role=game['role'], conduct=game.get('conduct', 'None'),
                         gender0=game.get('gender0', 'N/A'),
                         deathdate=datetime.datetime.strptime(game['deathdate'], "%Y%m%d").date(), hp=game['hp'],
                         achieve=game.get('achieve', 0), gamedelta=game.get('gamedelta', 0), maxlvl=game['maxlvl'],
                         maxhp=game['maxhp'],
                         endtime=datetime.datetime.fromtimestamp(int(game.get('endtime', 0))),
                         nachieves=game.get('nachieves', 0),
                         nconducts=game.get('nconducts', 0), name=game['name'], gender=game['gender'],
                         align=game['align'],
                         birthdate=datetime.datetime.strptime(game['birthdate'], "%Y%m%d").date(), race=game['race'],
                         flags=game.get('flags', 0),
                         starttime=datetime.datetime.fromtimestamp(int(game.get('starttime', 0))),
                         deathdnum=game['deathdnum']
        )

        create_db.load_game(game_dict)


process_html_file('./player_files/stth.html')

#process_player_file('/home/dcm/first10000.txt')
#process_player_file('/home/dcm/xlogfile.full.txt')
#process_player_file('/home/dcm/next.txt')
