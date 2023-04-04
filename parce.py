import json
from random import choice
with open('./games.json','r') as f:
    data=json.load(f)

# print(data)

openings=[]

for _ in data:
    if sorted(_["moves"][:6]) not in openings:
        openings += [_["moves"][:6]]

openings = sorted(openings)

def pickOpening():
    return choice(openings)



    


