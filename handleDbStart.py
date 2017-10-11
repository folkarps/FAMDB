from Crypto import Random
from Crypto.Cipher import AES

import utils


def initDb():
    c = utils.getCursor()

    # Create table
    c.execute('''CREATE TABLE if not exists missions
                 (id integer primary key,
                  missionName text,
                  lastPlayed text,
                   missionAuthor text,
                  missionModified text,
                  framework text,
                   isBroken integer default 0,
                  needsRevision integer default 0,
                   missionPlayers int,
                   missionType text,
                   missionMap text,
                    playedCounter int default 0,
                    missionDesc text,
                    missionNotes text,
                    status varchar(24) default 'WIP')''')

    c.execute('''CREATE TABLE if not exists users
                 (id integer primary key, login text, email text, password text, createDate text, lastLogin text, permissionLevel integer, sessionKey text)''')
    # Create table
    c.execute('''CREATE TABLE if not exists versions
                 (id integer primary key, missionId integer, existsOnMM integer default 1, existsOnMain integer default 0, name text, createDate text, toBeArchivedMM integer default 0, toBeDeletedMM integer default 0, toBeDeletedMain integer default 0, toBeArchivedMain default 0)''')

    c.execute('''CREATE TABLE if not exists comments
                 (id integer primary key, contents text, user text, createDate text, missionId integer)''')

    c.execute('''CREATE TABLE if not exists sessions
                 (id integer primary key, missionNames text, date text, host text, name text, players integer)''')

    c.execute("select * from users where sessionKey is null")

    try:
        c.execute('''ALTER TABLE users add resetPwLink text''')
    except:
        pass
    usersWithout = c.fetchall()

    for user in usersWithout:
        sessionKey = Random.new().read(AES.block_size)
        c.execute("update users set sessionKey = ? where id = ?", [sessionKey, user['id']])

    # Save (commit) the changes
    c.connection.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    c.connection.close()
