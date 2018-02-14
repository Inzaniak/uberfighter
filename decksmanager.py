import json
import sqlite3

def import_deck(path):
    deck = json.loads(open(path,'r',encoding='utf-8').read())
    conn = sqlite3.connect('data/db.db')
    conn.execute('delete from Decks where Expansion = ?',(deck['Expansion'],))
    for c in deck['Cards']:
        print(c)
        conn.execute('insert into Decks (Expansion,Type,Description) VALUES (?,?,?)',(deck['Expansion'],c['Type'],c['Description']))
    conn.commit()
    print('Deck Added')

import_deck('data/decks/meme.json')