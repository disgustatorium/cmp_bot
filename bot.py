#!/bin/python

import os
import discord
from dotenv import load_dotenv
from pyzbar.pyzbar import decode
from PIL import Image
import requests
from io import BytesIO

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} is online<3!')

@client.event
async def on_message(message):
    # if message has an attachment
    if message.attachments:
        for attachment in message.attachments:
            # if attachment is an image
            if 'image' in attachment.content_type:
                # gets image
                response = requests.get(attachment)
                img = Image.open(BytesIO(response.content))
                # searches for and attempts to decode a qr code
                decoded = decode(img)
                for qr in decoded:
                    # converts to utf-8 so it can send an accessible link
                    qr_url = (qr.data).decode("utf-8")
                    await message.channel.send("**Click below to register your attendance** (posted by " + message.author.name + ") " + qr_url)

client.run(TOKEN)
