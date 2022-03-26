from Levenshtein import ratio
from alphagram import alphagram
from calculator import equity, evaluate
from cipher import cipher
import config as cf
import discord
import dictionary
import inflect
import re

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
        message_content = message.content.lower()
        if message.content == '!bingo':
            msg = dictionary.random_word(7, self.config.discord['lexicon'])
            print(len(msg))
            await message.channel.send(msg)
        elif message.content == '!random':
            msg = dictionary.random_word(0, self.config.discord['lexicon'])
            print(len(msg))
            await message.channel.send(msg)
        elif message.content.startswith('!anagram '):
            words = message.content[9:].split(' ')
            if len(words) > 0:
                results = []
                msg = None
                length = -1
                for word in words:
                    result = dictionary.anagram_1(word.upper(),self.config.discord['lexicon'])
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
        elif message.content.startswith('!check '):
            words = message.content[7:].split(' ')
            if len(words) > 0:
                definitions = []
                msg = None
                length = -1
                for word in words:
                    definition = dictionary.check(word.upper(),self.config.discord['lexicon'])
                    length += len(definition) + 1
                    if length >= 500:
                        break
                    definitions.append(definition)
                msg = '\n'.join(definitions)
                print(len(msg))
                await message.channel.send(msg)
        elif message.content.startswith('!define '):
            words = message.content[8:].split(' ')
            if words and len(words) > 0:
                lexicon = self.config.discord['lexicon']
                definitions = []
                for word in words:
                    if re.search('[/!]', word):
                        return await message.channel.send('Words must not contain / or !')
                    offensive, word, entry = dictionary.check(word.upper(), lexicon)
                    if offensive:
                        pass
                    elif entry:
                        word, definition = dictionary.define(word, entry, lexicon)
                        definitions.append('%s%s - %s' % (word, dictionary.decorate(word, entry, lexicon, '')[1], definition))
                        while match := re.match(rf'(?:\([ A-Za-z]+\) )?(?:a |capable of (?:being )?|causing |characterized by |not |one that |one who |somewhat |the state of being |to |to make )?([a-z]+)(?:[,;]| \[)', definition):
                            term = match.group(1).upper()
                            if ratio(word, term) < 0.5:
                                break
                            word, definition = dictionary.define(term, lexicon)
                            definitions.append('%s%s - %s' % (word, dictionary.decorate(word, entry, lexicon, '')[1], definition))
                    else:
                        definitions.append(word + '* - not found')
                msg = '\n'.join(definitions)
                print(len(msg))
                await message.channel.send(msg)
        elif message.content.startswith('!related '):
            words = message.content[8:].split(' ')
            if len(words) > 0:
                results = []
                msg = None
                length = -1
                for word in words:
                    result = dictionary.related(word.upper(),self.config.discord['lexicon'])
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

