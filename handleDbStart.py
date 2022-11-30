from Crypto import Random
from Crypto.Cipher import AES

import json
import utils


def initDb():
    c = utils.getCursor()

    db_initial_create(c)
    db_migrate_add_users_resetpwlink(c)
    db_migrate_ensure_users_sessionkeys(c)
    db_migrate_add_missions_cdlcflag(c)
    db_migrate_reencode_session_missionnames_as_json(c)
    db_migrate_set_null_framework_to_unknown(c)
    db_migrate_framework_prefix_old_f3(c)
    db_migrate_add_tags_tables(c)

    # Save (commit) the changes
    c.connection.commit()

    db_populate_valid_tags(c)

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    c.connection.close()


def db_populate_valid_tags(c):
    valid_tags = [
        '3ifb',
        'aaf',
        'ai_friends',
        'assassination',
        'boats',
        'bundeswehr',
        'cache_hunt',
        'cdf',
        'chdkz',
        'cls',
        'csat',
        'csla',
        'ctrg',
        'custom_faction',
        'day',
        'defense',
        'demolition',
        'denmark',
        'escape',
        'escort',
        'fia',
        'gendarmerie',
        'helicopters',
        'hostages',
        'item_retrieval',
        'jets',
        'jungle',
        'large',
        'ldf',
        'long',
        'mechanised',
        'mines',
        'motorised',
        'nato',
        'night',
        'no_markers',
        'no_reinforcements',
        'npr',
        'nva',
        'paradrop',
        'parameters',
        'poland',
        'radio',
        'randomised',
        'scripted_gimmick',
        'seasonal',
        'short',
        'silly',
        'small',
        'special_forces',
        'spetsnaz',
        'symmetric_fireteams',
        'syndikat',
        'takistan',
        'tanks',
        'towing',
        'toys',
        'urban',
        'us'
    ]

    c.execute('''begin exclusive transaction''')
    c.execute('''delete from valid_tags''')
    c.executemany('''insert into valid_tags (tag) values (?)''', [(tag,) for tag in valid_tags])
    c.execute('''commit transaction''')


def db_migrate_add_tags_tables(c):
    c.execute('''create table if not exists mission_tags
                     (tag text, missionId int, primary key(tag, missionId)) without rowid''')

    c.execute('''create table if not exists valid_tags
                     (tag text primary key) without rowid''')


def db_migrate_framework_prefix_old_f3(c):
    # Some older missions has both 'x.x.x' and 'F3 x.x.x' entries in database. Clean-up by adding prefix to former
    c.execute('''update missions set framework = 'F3 '||framework where framework in (
        '3.1.x or older',
        '3.2.0',
        '3.2.1',
        '3.2.2',
        '3.3.0',
        '3.3.x or older',
        '3.4.0',
        '3.4.1'
    )''')


def db_migrate_set_null_framework_to_unknown(c):
    c.execute("update missions set framework = 'Unknown' where framework is NULL")


def db_migrate_reencode_session_missionnames_as_json(c):
    # Find any session with missionNames which aren't JSON arrays
    c.execute("select id, missionNames from sessions where missionNames not like '[%'")
    sessions_to_encode = c.fetchall()

    if sessions_to_encode:
        # Build a 'set' of all mission names for quick lookup
        c.execute("select missionName from missions")
        mission_lookup = {row[0]: True for row in c.fetchall()}

        for (session_id, corrupt_mission_names) in sessions_to_encode:
            # These mission names might be corrupted as mission names containing a comma are erroneously split
            corrupt_missions = corrupt_mission_names.split(",")
            missions = []

            partial = []
            for name in corrupt_missions:
                # Build up a list of mission name fragments that aren't in the lookup
                # Once we find a valid name, it's a fair assumption that any previously built-up partials are a valid name
                if name in mission_lookup:
                    if partial:
                        missions.append(",".join(partial))
                        partial = []
                    missions.append(name)
                else:
                    partial.append(name)

            # Just in-case *no* names are valid, or corrupted were at the end
            if partial:
                missions.append(",".join(partial))

            c.execute("update sessions set missionNames = ? where id = ?", [json.dumps(missions), session_id])


def db_migrate_add_missions_cdlcflag(c):
    if c.execute("select count(*) from pragma_table_info('missions') where name = 'isCDLCMission'").fetchone()[0] == 0:
        c.execute('''ALTER TABLE missions add isCDLCMission integer default 0''')


def db_migrate_ensure_users_sessionkeys(c):
    c.execute("select * from users where sessionKey is null")
    usersWithout = c.fetchall()
    for user in usersWithout:
        sessionKey = Random.new().read(AES.block_size)
        c.execute("update users set sessionKey = ? where id = ?", [sessionKey, user['id']])


def db_migrate_add_users_resetpwlink(c):
    if c.execute("select count(*) from pragma_table_info('users') where name = 'resetPwLink'").fetchone()[0] == 0:
        c.execute('''ALTER TABLE users add resetPwLink text''')


def db_initial_create(c):
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
                     (id integer primary key, login text, email text, password text, createDate text, lastLogin text, permissionLevel integer, sessionKey text,
                     discordId text)''')

    c.execute('''CREATE TABLE if not exists versions
                     (id integer primary key, missionId integer, existsOnMM integer default 1, existsOnMain integer default 0, name text, createDate text, toBeDeletedMM integer default 0, toBeDeletedMain integer default 0, requestedTransfer integer default 0, requestedTesting integer default 0)''')

    c.execute('''CREATE TABLE if not exists comments
                     (id integer primary key autoincrement, contents text, user text, createDate text, missionId integer, versionId integer)''')

    c.execute('''CREATE TABLE if not exists sessions
                     (id integer primary key, missionNames text, date text, host text, name text, players integer)''')
