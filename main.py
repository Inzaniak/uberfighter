import os
import os.path
import random
import string
import sqlite3

import cherrypy



class Root(object):
    @cherrypy.expose
    def index(self):
        try:
            cherrypy.session['user_logged'] == 1
            return open('html/home.html')
        except KeyError:
            return open('html/login.html')

    @cherrypy.expose
    def register(self, username, email, password, confirm_password, register_submit):
        if password == confirm_password:
            conn = sqlite3.connect('data/db.db')
            conn.execute('insert into Logins (PlayerName,PlayerPassword,PlayerEmail) VALUES (?,?,?)',
                         (username.lower(), password, email))
            conn.commit()
            cherrypy.session['user_logged'] = 1
            cherrypy.session['username'] = username
            raise cherrypy.HTTPRedirect("/index")

    @cherrypy.expose
    def login(self, username, password, login_submit):
        conn = sqlite3.connect('data/db.db')
        user = conn.execute(
            'select * from Logins where PlayerName = ? and PlayerPassword = ?', (username.lower(), password)).fetchone()
        print(user)
        try:
            if len(user) > 0:
                cherrypy.session['user_logged'] = 1
                cherrypy.session['username'] = username
                raise cherrypy.HTTPRedirect("/index")
            else:
                raise cherrypy.HTTPRedirect("/index")
        except TypeError:
            raise cherrypy.HTTPRedirect("/index")

    @cherrypy.expose
    def games(self):
        try:
            cherrypy.session['user_logged'] == 1
            page = open('html/games.html').read()
            template = open('html/templates/gameslist.html').read()
            conn = sqlite3.connect('data/db.db')
            # Get Games
            games = conn.execute(
            'select * from vPlayerByGame where PlayerName = ?', (cherrypy.session['username'].lower(),)).fetchall()
            g_list = []
            for g in games:
                g_list.append(template.format(gamename=g[1],gameid=g[0]))
            # Get Players
            players = conn.execute(
            'select * from Logins order by 2').fetchall()
            p_list = []
            for p in players:
                p_list.append('<option value="{pl}">{pl}</option>'.format(pl=p[1]))
            # Get Expansions
            expansions = conn.execute(
            "select distinct Expansion from Decks where Expansion <> 'Empty' order by Expansion").fetchall()
            e_list = []
            for e in expansions:
                e_list.append('<option value="{ex}">{ex}</option>'.format(ex=e[0]))
            page = page.format(games_list = '\n'.join(g_list),players_list = '\n'.join(p_list),expansions_list = '\n'.join(e_list))
            return page
        except KeyError as e:
            print(e)
            return open('html/login.html')       

    @cherrypy.expose
    def create_game(self,gamename,gameusers,gameexpansions):
        conn = sqlite3.connect('data/db.db')
        conn.execute('insert into Games (GameName,Admin) VALUES (?,?)',(gamename,cherrypy.session['username'].lower()))
        conn.commit()
        g_id = conn.execute('select * from Games where GameName = ? and Admin = ?',(gamename,cherrypy.session['username'].lower())).fetchone()[0]
        if type(gameusers) != type([]):
            gameusers = [gameusers]
        if type(gameexpansions) != type([]):
            gameexpansions = [gameexpansions]
        for p in gameusers:
            pl_id = conn.execute('select PlayerID from Logins where PlayerName = ?',(p.lower(),)).fetchone()[0]
            conn.execute('insert into GamesPlayers (GameID,PlayerID) VALUES (?,?)',(g_id,pl_id))
        for e in gameexpansions:
            print(e)
            conn.execute('insert into GamesExpansions (GameID,ExpansionName) VALUES (?,?)',(g_id,e))
        conn.commit()
        start_pl = conn.execute('''
                        select 
                        *
                        from vPlayerByGame  a
                        where gameID = ?
                        order by random()''',(g_id,)).fetchall()
        for num,p in enumerate(start_pl):
            pl_id = conn.execute('select PlayerID from Logins where PlayerName = ?',(p[2].lower(),)).fetchone()[0]
            conn.execute('insert into GamesTurns (GameID,PlayerID,Turn) VALUES (?,?,?)',(g_id,pl_id,num+1))
        pla_id = conn.execute('select PlayerID from Logins where PlayerName = ?',(start_pl[0][2].lower(),)).fetchone()[0]
        plb_id = conn.execute('select PlayerID from Logins where PlayerName = ?',(start_pl[1][2].lower(),)).fetchone()[0]
        conn.execute('insert into GamesActual (GameID,PlayerA,PlayerB,Phase) VALUES (?,?,?,?)',(g_id,pla_id,plb_id,'Play'))
        # Init Table
        conn.execute('insert into GamesTable (GameID,PlayerId,CardID,Position,[Order]) VALUES (?,?,?,?,?)',(g_id,1,0,'table_c_a',1))
        conn.execute('insert into GamesTable (GameID,PlayerId,CardID,Position,[Order]) VALUES (?,?,?,?,?)',(g_id,1,0,'table_a_aa',2))
        conn.execute('insert into GamesTable (GameID,PlayerId,CardID,Position,[Order]) VALUES (?,?,?,?,?)',(g_id,1,0,'table_a_ab',3))
        conn.execute('insert into GamesTable (GameID,PlayerId,CardID,Position,[Order]) VALUES (?,?,?,?,?)',(g_id,2,0,'table_c_b',4))
        conn.execute('insert into GamesTable (GameID,PlayerId,CardID,Position,[Order]) VALUES (?,?,?,?,?)',(g_id,2,0,'table_a_ba',5))
        conn.execute('insert into GamesTable (GameID,PlayerId,CardID,Position,[Order]) VALUES (?,?,?,?,?)',(g_id,2,0,'table_a_bb',6))
        conn.execute('insert into GamesRemainingCards select ?,CardID,Type from decks d inner join gamesexpansions ge on d.Expansion = ge.ExpansionName and ge.GameID = ?',(g_id,g_id))
        for p in start_pl:
            for i in range(1,4):
                pl_id = conn.execute('select PlayerID from Logins where PlayerName = ?',(p[2].lower(),)).fetchone()[0]
                card = conn.execute("SELECT * FROM GamesRemainingCards where GameID = ? and [Type] = 'Character' ORDER BY RANDOM() LIMIT 1 ",(g_id,)).fetchone()
                conn.execute("delete from GamesRemainingCards where CardID = ? and GameID = ? ",(card[1],g_id))
                conn.execute('insert into GamesHand (GameID,PlayerID,CardID,[Order]) VALUES (?,?,?,?)',(g_id,pl_id,card[1],i))
            for i in range(4,7):
                pl_id = conn.execute('select PlayerID from Logins where PlayerName = ?',(p[2].lower(),)).fetchone()[0]
                card = conn.execute("SELECT * FROM GamesRemainingCards where GameID = ? and [Type] = 'Ability' ORDER BY RANDOM() LIMIT 1 ",(g_id,)).fetchone()
                conn.execute("delete from GamesRemainingCards where CardID = ? and GameID = ? ",(card[1],g_id))
                conn.execute('insert into GamesHand (GameID,PlayerID,CardID,[Order]) VALUES (?,?,?,?)',(g_id,pl_id,card[1],i))
        conn.commit()
        raise cherrypy.HTTPRedirect("/games")

    @cherrypy.expose
    def delete_game(self,gameid):
        conn = sqlite3.connect('data/db.db')
        conn.execute('delete from Games where GameID = ?',(gameid,))
        conn.execute('delete from GamesPlayers where GameID = ?',(gameid,))
        conn.execute('delete from GamesExpansions where GameID = ?',(gameid,))
        conn.execute('delete from GamesActual where GameID = ?',(gameid,))
        conn.execute('delete from GamesHand where GameID = ?',(gameid,))
        conn.execute('delete from GamesLog where GameID = ?',(gameid,))
        conn.execute('delete from GamesRemainingCards where GameID = ?',(gameid,))
        conn.execute('delete from GamesTable where GameID = ?',(gameid,))
        conn.execute('delete from GamesTurns where GameID = ?',(gameid,))
        conn.commit()
        raise cherrypy.HTTPRedirect("/games")

    @cherrypy.expose
    def game(self,game_id):
        page = open('html/game.html').read()
        conn = sqlite3.connect('data/db.db')
        pl_id = conn.execute('select PlayerID from Logins where PlayerName = ?',(cherrypy.session['username'].lower(),)).fetchone()[0]
        table = conn.execute('select * from GamesTable where GameID = ? order by [Order]',(game_id,)).fetchall()
        hand = conn.execute('select * from GamesHand where GameID = ? and PlayerID = ? order by [Order]',(game_id,pl_id)).fetchall()
        print(hand)
        page = page.format(
                table_c_a=conn.execute('select * from Decks where CardID = ?',(table[0][2],)).fetchone()[3]
                ,table_a_aa=conn.execute('select * from Decks where CardID = ?',(table[1][2],)).fetchone()[3]
                ,table_a_ab=conn.execute('select * from Decks where CardID = ?',(table[2][2],)).fetchone()[3]
                ,table_c_b=conn.execute('select * from Decks where CardID = ?',(table[3][2],)).fetchone()[3]
                ,table_a_ba=conn.execute('select * from Decks where CardID = ?',(table[4][2],)).fetchone()[3]
                ,table_a_bb=conn.execute('select * from Decks where CardID = ?',(table[5][2],)).fetchone()[3]
                ,hand_c_a=conn.execute('select * from Decks where CardID = ?',(hand[0][2],)).fetchone()[3]
                ,hand_c_b=conn.execute('select * from Decks where CardID = ?',(hand[1][2],)).fetchone()[3]
                ,hand_c_c=conn.execute('select * from Decks where CardID = ?',(hand[2][2],)).fetchone()[3]
                ,hand_a_a=conn.execute('select * from Decks where CardID = ?',(hand[3][2],)).fetchone()[3]
                ,hand_a_b=conn.execute('select * from Decks where CardID = ?',(hand[4][2],)).fetchone()[3]
                ,hand_a_c=conn.execute('select * from Decks where CardID = ?',(hand[5][2],)).fetchone()[3]
                ,hand_c_a_id=hand[0][2]
                ,hand_c_b_id=hand[1][2]
                ,hand_c_c_id=hand[2][2]
                ,hand_a_a_id=hand[3][2]
                ,hand_a_b_id=hand[4][2]
                ,hand_a_c_id=hand[5][2]
                ,g_id = game_id
                )
        return page

    @cherrypy.expose
    def change_table(self,g_id,c_to_play,a_to_play,pl):
        print(g_id,c_to_play,a_to_play,pl)
        conn = sqlite3.connect('data/db.db')
        if pl == "1":
            conn.execute('update GamesTable set CardID = ? where PlayerID = ? and GameID = ? and [Order] = 1',(c_to_play,1,g_id))
            conn.execute('update GamesTable set CardID = ? where PlayerID = ? and GameID = ? and [Order] = 2',(a_to_play,1,g_id))
            card = conn.execute("SELECT * FROM GamesRemainingCards where GameID = ? and [Type] = 'Ability' ORDER BY RANDOM() LIMIT 1 ",(g_id,)).fetchone()
            conn.execute("delete from GamesRemainingCards where CardID = ? and GameID = ? ",(card[1],g_id))
            conn.execute('update GamesTable set CardID = ? where PlayerID = ? and GameID = ? and [Order] = 3',(card[1],1,g_id))
            conn.commit()
        if pl == "2":
            print('PLAYER2')
            conn.execute('update GamesTable set CardID = ? where PlayerID = ? and GameID = ? and [Order] = 4',(c_to_play,2,g_id))
            conn.execute('update GamesTable set CardID = ? where PlayerID = ? and GameID = ? and [Order] = 5',(a_to_play,2,g_id))
            card = conn.execute("SELECT * FROM GamesRemainingCards where GameID = ? and [Type] = 'Ability' ORDER BY RANDOM() LIMIT 1 ",(g_id,)).fetchone()
            conn.execute("delete from GamesRemainingCards where CardID = ? and GameID = ? ",(card[1],g_id))
            conn.execute('update GamesTable set CardID = ? where PlayerID = ? and GameID = ? and [Order] = 6',(card[1],2,g_id))
            conn.commit()
        for i in range(1,4):
            pl_id = conn.execute('select PlayerID from Logins where PlayerName = ?',(cherrypy.session['username'].lower(),)).fetchone()[0]
            card = conn.execute("SELECT * FROM GamesRemainingCards where GameID = ? and [Type] = 'Character' ORDER BY RANDOM() LIMIT 1 ",(g_id,)).fetchone()
            conn.execute("delete from GamesRemainingCards where CardID = ? and GameID = ? ",(card[1],g_id))
            conn.execute('update GamesHand set CardID = ? where GameID = ? and [Order] = ? and PlayerID = ?',(card[1],g_id,i,pl_id))
        for i in range(4,7):
            pl_id = conn.execute('select PlayerID from Logins where PlayerName = ?',(cherrypy.session['username'].lower(),)).fetchone()[0]
            card = conn.execute("SELECT * FROM GamesRemainingCards where GameID = ? and [Type] = 'Ability' ORDER BY RANDOM() LIMIT 1 ",(g_id,)).fetchone()
            conn.execute("delete from GamesRemainingCards where CardID = ? and GameID = ? ",(card[1],g_id))
            conn.execute('update GamesHand set CardID = ? where GameID = ? and [Order] = ? and PlayerID = ?',(card[1],g_id,i,pl_id))
        conn.commit()
        raise cherrypy.HTTPRedirect("/game?game_id={}".format(g_id))
        


if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }
    cherrypy.config.update({'server.socket_port': 8099})
    cherrypy.quickstart(Root(), '/', conf)
