import pickle
from collections import Counter

# Ascensions

game_list=pickle.load( open("./data/game_list.txt","rb"))

total_games=len(game_list)
ascended_roles=[str(game_list[i]['role']) for i in (range(0,total_games)) if game_list[i]['death']=='ascended']

ascensions=Counter(ascended_roles).most_common()

print "Ascended Roles\n"
for i in ascensions:
    print i[0], i[1], round((float(i[1])/float(len(ascended_roles)))*100,2),'%'

ascensions_dict={}
ascended_games=[(str(game_list[i]['deathdate']),
str(game_list[i]['role']),
str(game_list[i]['race']),
str(game_list[i]['gender']),
str(game_list[i]['align']),
str(game_list[i]['turns']),
str(game_list[i]['points']),
) for i in (range(0,total_games)) if game_list[i]['death']=='ascended']

first_ascension=ascended_games[0]
print "first", first_ascension[0]

for a in ascended_games:
    print a
