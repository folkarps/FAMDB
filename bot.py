#!/usr/local/bin/python
import logging

import discord

client = discord.Client(max_messages=101)


async def initBot():
    # Logging
    logging.basicConfig(filename="FA_bot.log", level=logging.DEBUG,
                        format="%(asctime)-15s %(message)s")
    logging.info("FAbot starting up")

    logging.info("Logging into Discord")

    client_email = ''
    client_pass = ''

    if client_email is None or client_pass is None:
        logging.critical("Could not find Discord authentication details "
                         "in config file.")
        print("Could not find Discord authentication details.")
        exit(1)

    await client.login(client_email, client_pass)

    if not client.is_logged_in:
        logging.critical("Logging into Discord failed")
        print('Logging in to Discord failed')
        exit(1)
    await client.connect()


@client.event
async def on_ready():
    print('Connected!')
    print('Username: ' + client.user.name)
    print('ID: ' + client.user.id)
