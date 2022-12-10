import json

def test():
    file = open('users.json','r')
    r = json.load(file)

    for i in r['users']:
        print(i)
    # Random.choice(r)

test()