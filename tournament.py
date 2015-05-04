#!/usr/bin/env python
# tournament.py -- implementation of a Swiss-system tournament
#

import math
import psycopg2
import random


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    cursor = db.cursor()
    query = "DELETE FROM matches"
    cursor.execute(query)
    db.commit()
    db.close()


def deletePlayers():
    """Remove all the player records from the database."""¨{}
    db = connect()
    cursor = db.cursor()
    query = "DELETE FROM players"
    cursor.execute(query)
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    cursor = db.cursor()
    query = "SELECT count(*) FROM players"
    cursor.execute(query)
    result = cursor.fetchall()
    db.close()
    return result[0][0]


def registerPlayer(name):
    """Adds a player to the tournament database.

    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    cursor = db.cursor()
    cursor.execute("INSERT INTO players (name) VALUES (%s)", (name,))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins."""
    db = connect()
    cursor = db.cursor()
    cursor.execute("SELECT * from scores")
    result = cursor.fetchall()
    db.close()
    return result


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players."""
    db = connect()
    cursor = db.cursor()
    query = "INSERT INTO matches (winner, loser) VALUES (%s, %s)",\
        (winner, loser)
    cursor.execute(query)
    db.commit()
    db.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match."""
    num_players = countPlayers()
    pairs = []
    db = connect()
    cursor = db.cursor()
    for i in range(0, num_players, 2):
        query = "SELECT id, name FROM scores LIMIT 2 OFFSET (%d)" % (i,)
        cursor.execute(query)
        result = cursor.fetchall()
        pairs.append(result[0] + result[1])
    db.close()
    return pairs


def simulation():
    """ Runs a tournament simulation """

    # list with the players
    players = ['Twilight Sparkle', 'Fluttershy', 'Applejack', 'Pinkie Pie',
               'Andrew Parson', 'Emily Everett', 'Peter Power', 'Lewis Lame',
               'Sue', 'Michael O.', 'Frankie', 'Obb', 'Zack', 'Maria',
               'Sophie Smith', 'Hooray']

    # clean tables
    deleteMatches()
    deletePlayers()

    # register players
    for player in players:
        registerPlayer(player)

    opt = [0, 2]
    num_players = countPlayers()
    num_matches = int(math.log(num_players, 2))

    # simulate tournament
    for i in range(num_matches):
        pairs = swissPairings()
        for pair in pairs:
            random.shuffle(opt)
            reportMatch(pair[opt[0]], pair[opt[1]])


# Run simulation:
simulation()
