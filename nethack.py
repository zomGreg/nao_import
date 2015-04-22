#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
import datetime

def process_player_file(player_file):
    f = open(player_file, 'r')

    for line in f.readlines():
        keys = [t.split('=')[0] for t in line.split(':')]
        values = [filter(lambda x: x in string.printable, t.split('=')[1]) for t in line.split(':')]

        game = dict(zip(keys, values))

        if game.get('conduct') is not None:
            conduct = int(game['conduct'], 0)
        else:
            conduct = 0

        if game.get('achieve') is not None:
            achieve = int(game['achieve'], 0)
        else:
            achieve = 0

        if game.get('flags') is not None:
            flags = int(game['flags'], 0)
        else:
            flags = 0

        if game.get('align0') is not None:
            align0 = game['align0'].rstrip()
        else:
            align0 = game.get('align0')

        game_dict = dict(align0=align0, deathlev=game['deathlev'], uid=game['uid'],
                         deaths=game['deaths'],
                         turns=game.get('turns', 0), points=int(game['points']), death=game['death'],
                         realtime=game.get('realtime', 0),
                         version=game['version'], role=game['role'], conduct=conduct,
                         gender0=game.get('gender0', 'N/A'),
                         deathdate=datetime.datetime.strptime(game['deathdate'], "%Y%m%d").date(), hp=game['hp'],
                         achieve=achieve, gamedelta=game.get('gamedelta', 0), maxlvl=game['maxlvl'],
                         maxhp=game['maxhp'],
                         endtime=datetime.datetime.fromtimestamp(int(game.get('endtime', 0))),
                         nachieves=game.get('nachieves', 0),
                         nconducts=game.get('nconducts', 0), name=game['name'], gender=game['gender'],
                         align=game['align'],
                         birthdate=datetime.datetime.strptime(game['birthdate'], "%Y%m%d").date(), race=game['race'],
                         flags=flags,
                         starttime=datetime.datetime.fromtimestamp(int(game.get('starttime', 0))),
                         deathdnum=game['deathdnum']
                         )

        nao_game = models.Game(align0=game_dict['align0'],
                               deathlev=game_dict['deathlev'],
                               uid=game_dict['uid'],
                               deaths=game_dict['deaths'],
                               turns=game_dict['turns'],
                               realtime=game_dict['realtime'],
                               points=game_dict['points'],
                               death=game_dict['death'],
                               version=game_dict['version'],
                               role=game_dict['role'],
                               conduct=game_dict['conduct'],
                               gender0=game_dict['gender0'],
                               deathdate=game_dict['deathdate'],
                               hp=game_dict['hp'],
                               achieve=game_dict['achieve'],
                               gamedelta=game_dict['gamedelta'],
                               maxlvl=game_dict['maxlvl'],
                               maxhp=game_dict['maxhp'],
                               endtime=game_dict['endtime'],
                               nachieves=game_dict['nachieves'],
                               nconducts=game_dict['nconducts'],
                               name=game_dict['name'],
                               gender=game_dict['gender'],
                               align=game_dict['align'],
                               birthdate=game_dict['birthdate'],
                               race=game_dict['race'],
                               flags=game_dict['flags'],
                               starttime=game_dict['starttime'],
                               deathdnum=game_dict['deathdnum']
                               )
        # print nao_game.align0
        db.session.add(nao_game)
        db.session.commit()
        # keys = [k for k in game_dict.iterkeys()]
        # print len(keys)
        # print game_dict
        # time.sleep(1)


# process_player_file('/Users/gmoselle/xlogfile.full.txt.new.new.new')
process_player_file('/Users/gmoselle/xlogfile.full.txt')
