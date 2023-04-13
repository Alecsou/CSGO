import json
from random import choice
with open('./games.json','r') as f:
    data=json.load(f)
depth=15
openings=[]

for _ in data:
    if sorted(_["moves"][:depth]) not in openings:
        openings += [_["moves"][:depth]]

openings = sorted(openings)

def pickOpening():
    return choice(openings)



    


