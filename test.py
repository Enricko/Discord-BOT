import json

def test():
    file = open('monster.json','r')
    r = json.load(file)

    for i in r['data']['forest']:
        print(i['1']['min_damage'])
    # Random.choice(r)

test()