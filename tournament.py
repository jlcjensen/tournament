#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    # Connect to the PostgreSQL database.  Returns a database connection.
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    # Remove all the match records from the database.
    DB = connect()

    cursor = DB.cursor()

    cursor.execute('TRUNCATE TABLE Matches;')

    DB.commit()

    DB.close()


def deletePlayers():
    # Remove all the player records from the database.
    DB = connect()

    cursor = DB.cursor()

    cursor.execute('TRUNCATE TABLE Players CASCADE;')

    DB.commit()

    DB.close()


def countPlayers():
    # Returns the number of players currently registered.
    DB = connect()

    cursor = DB.cursor()

    query = 'SELECT COUNT(PID) FROM Players;'

    cursor.execute(query)

    player_count = cursor.fetchall()

    DB.close()

    return player_count[0][0]


def registerPlayer(name):
    # Adds a player to the tournament database.

    # The database assigns a unique serial id number for the player.  (This
    # should be handled by your SQL database schema, not in your Python code.)

    # Args:
    #  name: the player's full name (need not be unique).

    DB = connect()

    cursor = DB.cursor()

    query = 'INSERT INTO Players (NAME) values (%s);'
    param = (name,)

    cursor.execute(query, param)

    DB.commit()

    DB.close()


def playerStandings():
    # Returns a list of the players and their win records, sorted by wins.

    # The first entry in the list should be the player in first place, or a
    # player tied for first place if there is currently a tie.

    # Returns:
    #  A list of tuples, each of which contains (id, name, wins, matches):
    #    id: the player's unique id (assigned by the database)
    #    name: the player's full name (as registered)
    #    wins: the number of matches the player has won
    #    matches: the number of matches the player has played
    DB = connect()

    cursor = DB.cursor()

    query = """SELECT PID, NAME, TOTALWINS, (TOTALWINS + TOTALLOSSES)
                AS MATCHES FROM Totals ORDER BY TOTALWINS DESC;"""

    cursor.execute(query)

    playersarray = cursor.fetchall()

    DB.close()

    return playersarray


def reportMatch(winner, loser):
    # Records the outcome of a single match between two players.

    # Args:
    #  winner:  the id number of the player who won
    #  loser:  the id number of the player who lost
    DB = connect()

    cursor = DB.cursor()

    query = 'INSERT INTO Matches (WinnerID, LoserID) values (%s,%s);'
    param = (winner, loser,)

    cursor.execute(query, param)

    DB.commit()

    DB.close()


def swissPairings():
    # Returns a list of pairs of players for the next round of a match.

    # Assuming that there are an even number of players registered, each player
    # appears exactly once in the pairings.  Each player is paired with another
    # player with an equal or nearly-equal win record, that is, a player
    # adjacent to him or her in the standings.

    # Returns:
    #  A list of tuples, each of which contains (id1, name1, id2, name2)
    #    id1: the first player's unique id
    #    name1: the first player's name
    #    id2: the second player's unique id
    #    name2: the second player's name

    DB = connect()

    cursor = DB.cursor()

    # get all the players, in standings order
    query = 'SELECT PID,NAME FROM Totals ORDER BY TOTALWINS DESC'

    cursor.execute(query)

    playersarray = cursor.fetchall()

    DB.close()

    i = 0

    matches = []

    while i < len(playersarray):
        pid_a = playersarray[i][0]
        name_a = playersarray[i][1]

        pid_b = playersarray[i+1][0]
        name_b = playersarray[i+1][1]

        matches.append([pid_a, name_a, pid_b, name_b])

        i += 2

    return matches
