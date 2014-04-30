#!/usr/bin/env python

import urllib2

from sqlalchemy import create_engine, schema, types
from BeautifulSoup import BeautifulSoup
import prettytable
from collections import Counter
import pickle, simplejson
import all_games
import datetime
from os import listdir
from os.path import isfile, join

import create_db

players=['bose','mscurmudgeon','stth','Vodalus','muad']

def get_player_file(player_name):
    '''
    This function will save the associated player_name html file
    into the ./player_html directory.
    '''

    #player_name="zomgreg"

    req_string='http://alt.org/nethack/player-all-xlog.php?player=%s' % (player_name)

    req=urllib2.Request(req_string)
    response=urllib2.urlopen(req)
    html=response.read()
    ##
    f=open('./player_files/%s.html' % player_name,'w')
    f.write(html)
    f.close()

#for p in players:
#    get_player_file(p)

#f=open('./playerdata.html','r')


g=create_db.Games()

metadata=schema.MetaData()
engine=create_engine('sqlite:///nao.db', echo=False)
metadata.bind=engine

def process_player_file(player_file):

    f=open(player_file,'r')
    soup=BeautifulSoup(f)
    all_games=soup.findAll('pre')[0].string.split('\n')
    print "Importing %s games." % (len(all_games))
    f.close()

    game_list=[]
    for i in range(0,len(all_games)-1):
        keys=[t.split('=')[0] for t in all_games[i].split(':')]
        values=[t.split('=')[1] for t in all_games[i].split(':')]
        game=dict(zip(keys,values))
        game_list.append(game)

        if not game['endtime']:
            game['endtime'] = 00000000
        if not game['starttime']:
            game['starttime'] = 00000000

    for game in game_list:
        game_dict=dict(align0=game['align0'], deathlev=game['deathlev'], uid=game['uid'], deaths=game['deaths'],
                       turns=game['turns'], points=game['points'], death=game['death'], realtime=game['realtime'],
                       version=game['version'], role=game['role'], conduct=game['conduct'], gender0=game['gender0'],
                       deathdate=datetime.datetime.strptime(game['deathdate'],"%Y%m%d").date(), hp=game['hp'],
                       achieve=game['achieve'], gamedelta=game['gamedelta'], maxlvl=game['maxlvl'], maxhp=game['maxhp'],
                       endtime=datetime.datetime.fromtimestamp(int(game['endtime'])), nachieves=game['nachieves'],
                       nconducts=game['nconducts'], name=game['name'], gender=game['gender'], align=game['align'],
                       birthdate=datetime.datetime.strptime(game['birthdate'], "%Y%m%d").date(), race=game['race'],
                       flags=game['flags'], starttime=datetime.datetime.fromtimestamp(int(game['starttime'])),
                       deathdnum=game['deathdnum']
        )

        create_db.load_game(game_dict)

game_dir='./player_files'
game_files = [ f for f in listdir(game_dir) if isfile(join(game_dir,f)) ]

for g in game_files:
    player_file=join(game_dir,g)
    process_player_file(player_file)
