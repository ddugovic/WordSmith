
import os
import discord
import dictionary
import inflect
import twitchbot

dictionary.open_files()
engine = inflect.engine()

token = os.getenv("DISCORD_TOKEN")
my_guild = os.getenv("DISCORD_GUILD")

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == my_guild:
            break
    await client.change_presence(activity=discord.Game('OMGWORDS'))

    print(
        f"{client.user} is connected to the following guild:\n"
        f"{guild.name}(id: {guild.id})"
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    message_content = message.content.lower()
    if message.content == "!bingo":
        msg = dictionary.random_word(7, "csw")
        print(len(msg))
        await message.channel.send(msg)
    elif message.content == "!random":
        msg = dictionary.random_word(0, "csw")
        print(len(msg))
        await message.channel.send(msg)
    elif message.content.startswith("!anagram "):
        words = message.content[9:].split(' ')
        if len(words) > 0:
            results = []
            msg = None
            length = -1
            for word in words:
                result = dictionary.anagram_1(word.upper(),"csw")
                count, words = result
                msg = f'{count} %s:\n{words}' % engine.plural('result', count)
                print(len(msg))
                length += len(msg) + 1
                if length >= 500:
                    break
                results.append(msg)
            msg = '\n'.join(results)
            print(len(msg))
            await message.channel.send(msg)
    elif message.content.startswith("!check "):
        words = message.content[7:].split(' ')
        if len(words) > 0:
            definitions = []
            msg = None
            length = -1
            for word in words:
                definition = dictionary.check(word.upper(),"csw")
                length += len(definition) + 1
                if length >= 500:
                    break
                definitions.append(definition)
            msg = '\n'.join(definitions)
            print(len(msg))
            await message.channel.send(msg)
    elif message.content.startswith("!define "):
        words = message.content[8:].split(' ')
        if len(words) > 0:
            definitions = []
            msg = None
            length = -1
            for word in words:
                definition = dictionary.define(word.upper(),"csw")
                length += len(definition) + 1
                if length >= 500:
                    break
                definitions.append(definition)
            msg = '\n'.join(definitions)
            print(len(msg))
            await message.channel.send(msg)
    elif message.content.startswith("!related "):
        words = message.content[8:].split(' ')
        if len(words) > 0:
            results = []
            msg = None
            length = -1
            for word in words:
                result = dictionary.related(word.upper(),"csw")
                count, words = result
                msg = f'{count} %s:\n{words}' % engine.plural('result', count)
                print(len(msg))
                length += len(msg) + 1
                if length >= 500:
                    break
                results.append(msg)
            msg = '\n'.join(results)
            print(len(msg))
            await message.channel.send(msg)

client.run(token)

