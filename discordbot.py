import discord
import config as cf
import inflect
import random as rd
import re
from alphagram import alphagram
from calculator import equity, evaluate
from cipher import cipher
import dictionary

custom_commands = cf.custom_commands()
engine = inflect.engine()

class DiscordBot(discord.Client):

    def __init__(self, config=cf.config()):
        super().__init__(intents=discord.Intents.default())
        self.config = config

    def run(self):
        dictionary.open_files()
        super().run(self.config.discord['token'])

    async def on_ready(self):
        for guild in self.guilds:
            if guild.name == self.config.discord['guild']:
                break
        await self.change_presence(activity=discord.Game('OMGWords'))
        print(
            f'{self.user} is connected to the following guild:\n'
            f'{guild.name}(id: {guild.id})'
        )

    async def on_message(self, message):
        if message.author == self.user:
            return
        command = message.content.lower()
        print(command)
        if command[1:] in custom_commands.keys():
            with open(custom_commands[command[1:]], 'r') as f:
               messages = list(f)
            msg = rd.choice(messages).strip()
            print(len(msg))
            await message.channel.send(msg)
        elif match := re.match(rf'!bingo(?: (\d+))?', command):
            length = int(match.group(1) or '7')
            msg = dictionary.random_word(length, self.config.discord['lexicon'])
            print(len(msg))
            await message.channel.send(msg)
        elif match := re.match(rf'!random(?: (\d+))?', command):
            length = int(match.group(1) or '0')
            msg = dictionary.random_word(length, self.config.discord['lexicon'])
            print(len(msg))
            await message.channel.send(msg)
        elif match := re.match(rf'!anagram((?: [a-z]+)+)', command):
            lexicon = self.config.discord['lexicon']
            results = []
            for rack in match.group(1).strip().split(' '):
                msg = None
                if anagrams := dictionary.anagram(rack.upper(), lexicon):
                    count = len(anagrams)
                    msg = f'{count} %s' % engine.plural('result', count)
                    for n, element in enumerate(anagrams):
                        word, entry = element
                        if len(msg) + len(word) > 465:
                            msg += f'Limited to first {n} results'
                            break
                        msg += ' %s%s' % dictionary.decorate(word, entry, lexicon, '')
                else:
                    msg = 'No anagrams found'
                results.append(msg)
            msg = '; '.join(results)
            print(len(msg))
            await message.channel.send(msg)
        elif match := re.match(rf'!define((?: [a-z]+)+)', command):
            lexicon = self.config.discord['lexicon']
            definitions = []
            msg = None
            length = -1
            for word in match.group(1).strip().split(' '):
                offensive, word, entry = dictionary.check(word.upper(), lexicon)
                word, entry, definition, mark = dictionary.define(word, entry, lexicon, '')
                length += len(definition) + 1
                if length >= 500:
                    break
                definitions.append('%s%s - %s' % (word, mark, definition))
            msg = '\n'.join(definitions)
            print(len(msg))
            await message.channel.send(msg)
        elif match := re.match(rf'!check((?: [a-z]+)+)', command):
            lexicon = self.config.discord['lexicon']
            definitions = []
            for word in match.group(1).strip().split(' '):
                if re.search('[/!]', word):
                    return await message.channel.send('Words must not contain / or !')
                offensive, word, entry = dictionary.check(word.upper(), lexicon)
                if offensive:
                    pass
                elif entry:
                    word, entry, definition, mark = dictionary.define(word, entry, lexicon, '')
                    if match := re.match(r'[A-Z]{2,}', entry[1]):
                        word, entry, definition, mark = dictionary.define(match.group(0), entry, lexicon, '')
                    definitions.append('%s%s - %s' % (word, mark, definition))
                else:
                    definitions.append(word + '* - not found')
            msg = '\n'.join(definitions)
            print(len(msg))
            await message.channel.send(msg)
        elif match := re.match(rf'!related((?: [a-z]+)+)', command):
            lexicon = self.config.discord['lexicon']
            results = []
            msg = None
            length = -1
            for word in match.group(1).strip().split(' '):
                result = dictionary.related(word.upper(), lexicon)
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

def main():
    DiscordBot().run()

if __name__ == "__main__":
    main()

