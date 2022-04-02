import discord
import config as cf
import inflect
import random as rd
import re
from alphagram import alphagram
from calculator import equity, evaluate
from cipher import cipher
import dictionary
from pager import paginate, truncate

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

    def check(self, words):
        lexicon = self.config.discord['lexicon']
        results = []
        for word in words:
            offensive, word, entry = dictionary.check(word.upper(), lexicon)
            if not offensive:
                msg = ('%s%s' % dictionary.decorate(word, entry, lexicon, '')) if entry else ('%s*' % word)
                results.append((msg + ' is valid :white_check_mark:') if dictionary.common(word.lower()) else (msg + ' not found :negative_squared_cross_mark:'))
        return results

    def common(self, words):
        lexicon = self.config.discord['lexicon']
        results = []
        for word in words:
            offensive, word, entry = dictionary.check(word.upper(), lexicon)
            if not offensive:
                msg = ('%s%s' % dictionary.decorate(word, entry, lexicon, '')) if entry else ('%s*' % word)
                results.append(msg = (msg + ' is common :white_check_mark:') if dictionary.common(word.lower()) else (msg + ' not common :negative_squared_cross_mark:'))
        return results

    def wordnik(self, words):
        lexicon = self.config.discord['lexicon']
        results = []
        for word in words:
            offensive, word, entry = dictionary.check(word.upper(), lexicon)
            if not offensive:
                msg = ('%s%s' % dictionary.decorate(word, entry, lexicon, '')) if entry else ('%s*' % word)
                results.append((msg + ' is open-source :white_check_mark:') if dictionary.common(word.lower()) else (msg + ' not open-source :negative_squared_cross_mark:'))
        return results

    def equity(self, racks):
        lexicon = self.config.discord['lexicon']
        alphabet = self.config.discord['alphabet']
        results = []
        for rack in racks:
            if len(rack) >= 2 and len(rack) <= 5:
                result = equity(rack, lexicon)
                if result[0] == '{':
                    msg = '%s: %s' % (alphagram(rack.upper(), alphabet), result)
                else:
                    msg = '%s: %0.3f' % (alphagram(result[0], alphabet), result[1])
            else:
                msg = alphagram(rack.upper(), alphabet) + ': ?'
            results.append(msg)
        return results

    def sum(self, racks):
        alphabet = self.config.discord['alphabet']
        results = []
        for rack in racks:
            msg = '%s: %d' % (alphagram(rack.upper(), alphabet), evaluate(rack.upper()))
            results.append(msg)
        return results

    def define(self, words):
        lexicon = self.config.discord['lexicon']
        definitions = []
        msg = None
        length = -1
        for word in words:
            offensive, word, entry = dictionary.check(word.upper(), lexicon)
            if offensive:
                pass
            elif entry:
                word, entry, definition, mark = dictionary.define(word, entry, lexicon, '')
                length += len(definition) + 1
                definitions.append('%s%s - %s' % (word, mark, definition))
            else:
                definitions.append(word + '* - not found')
        return definitions

    def inflect(self, words):
        lexicon = self.config.discord['lexicon']
        inflections = []
        for word in words:
            if re.search('[/!]', word):
                return ('Words must not contain / or !')
            offensive, word, entry = dictionary.check(word.upper(), lexicon)
            if offensive:
                pass
            elif entry:
                inflections.append(dictionary.inflect(word.upper(), entry, lexicon))
            else:
                inflections.append(word.upper() + '* - not found')
        return inflections

    def related(self, stem, page='1'):
        result = dictionary.related(stem.upper(), self.config.discord['lexicon'])
        num, msg = paginate(result, int(page))
        print(len(msg))
        return (f'{num} %s:\n{msg}' % engine.plural('result', num))

    def beginswith(self, hook, page='1'):
        result = dictionary.begins_with(hook.upper(), self.config.discord['lexicon'])
        num, msg = paginate(result, int(page))
        print(len(msg))
        return (f'{num} %s:\n{msg}' % engine.plural('result', num))

    def endswith(self, hook, page='1'):
        result = dictionary.ends_with(hook.upper(), self.config.discord['lexicon'])
        num, msg = paginate(result, int(page))
        print(len(msg))
        return (f'{num} %s:\n{msg}' % engine.plural('result', num))

    def contains(self, stem, page='1'):
        result = dictionary.contains(stem.upper(), self.config.discord['lexicon'])
        num, msg = paginate(result, int(page))
        print(len(msg))
        return (f'{num} %s:\n{msg}' % engine.plural('result', num))

    def pattern(self, pattern, page='1'):
        result = dictionary.pattern(pattern.upper(), self.config.discord['lexicon'])
        num, msg = paginate(result, int(page))
        print(len(msg))
        return (f'{num} %s:\n{msg}' % engine.plural('result', num))

    def regex(self, pattern, page='1'):
        result = dictionary.find(pattern.upper(), self.config.discord['lexicon'])
        num, msg = paginate(result, int(page))
        print(len(msg))
        return (f'{num} %s:\n{msg}' % engine.plural('result', num))

    def hook(self, stem):
        msg = dictionary.hook(stem.upper(), self.config.discord['lexicon'])
        print(len(msg))
        return (msg)

    def unhook(self, rack, page='1'):
        result = dictionary.unhook(rack, self.config.discord['lexicon'])
        num, msg = paginate(result, int(page))
        print(len(msg))
        return (msg)

    def info(self, stems):
        lexicon = self.config.discord['lexicon']
        alphabet = self.config.discord['alphabet']
        results = []
        for stem in stems:
            msg = dictionary.info(stem.upper(), lexicon, alphabet)
            if len(stem) >= 2 and len(stem) <= 5:
                result = equity(stem, lexicon)
                if result[0] == '{':
                    msg += ' Equity: %s' % result
                else:
                    msg += ' Equity: %0.3f' % result[1]
            results.append(msg)
        return results

    def anagram(self, racks):
        lexicon = self.config.discord['lexicon']
        results = []
        msg = None
        for rack in racks:
            if anagrams := dictionary.anagram(rack.upper(), lexicon):
                count = len(anagrams)
                msg = f'{count} %s' % engine.plural('result', count)
                for n, element in enumerate(anagrams):
                    word, entry = element
                    msg += ' %s%s' % dictionary.decorate(word, entry, lexicon, '')
            else:
                msg = 'No anagrams found'
            results.append(msg)
        return results

    def bingo(self, length):
        return dictionary.random_word(int(length), self.config.discord['lexicon'])

    def random(self, option):
        if option.isnumeric():
            return dictionary.random_word(int(option), self.config.discord['lexicon'])
        else:
            result = dictionary.related(option.upper(), self.config.discord['lexicon'], '')
            return '%s%s' % result[0] if len(result) else ''

    def pronounce(self, word):
        offensive, word, entry = dictionary.check(word, self.config.discord['lexicon'])
        if not offensive:
            if entry:
                return f'https://collinsdictionary.com/sounds/hwd_sounds/en_gb_{word.lower()}.mp3'
            else:
                return f'{word}* not found'

    def crypto(self, text, page='1'):
        pattern = cipher(text.upper())
        result = dictionary.find(pattern, self.config.discord['lexicon'])
        num, msg = paginate(result, int(page))
        return (f'{num} %s:\n{msg}' % engine.plural('result', num))

    def hidden(self, length, phrase='', page='1'):
        result = dictionary.hidden(int(length), phrase, self.config.discord['lexicon'])
        num, msg = paginate(result, int(page))
        return (f'{num} %s:\n{msg}' % engine.plural('result', num))

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
        elif match := re.match(rf'!check((?: [a-z]+)+)', command):
            msg = '\n'.join(self.check(match.group(1).upper().strip().split(' ')))
            print(len(msg))
            await message.channel.send(msg)
        elif match := re.match(rf'!common((?: [a-z]+)+)', command):
            msg = '\n'.join(self.common(match.group(1).upper().strip().split(' ')))
            print(len(msg))
            await message.channel.send(msg)
        elif match := re.match(rf'!wordnik((?: [a-z]+)+)', command):
            msg = '\n'.join(self.wordnik(match.group(1).upper().strip().split(' ')))
            print(len(msg))
            await message.channel.send(msg)
        elif match := re.match(rf'!equity((?: [a-z]+)+)', command):
            msg = '\n'.join(self.equity(match.group(1).upper().strip().split(' ')))
            print(len(msg))
            await message.channel.send(msg)
        elif match := re.match(rf'!sum((?: [a-z]+)+)', command):
            msg = '\n'.join(self.sum(match.group(1).upper().strip().split(' ')))
            print(len(msg))
            await message.channel.send(msg)
        elif match := re.match(rf'!define((?: [a-z]+)+)', command):
            msg = '\n'.join(self.define(match.group(1).upper().strip().split(' ')))
            print(len(msg))
            await message.channel.send(msg)
        elif match := re.match(rf'!inflect((?: [a-z]+)+)', command):
            msg = '\n'.join(self.inflect(match.group(1).upper().strip().split(' ')))
            print(len(msg))
            await message.channel.send(msg)
        elif match := re.match(rf'!related((?: [a-z]+)+)', command):
            msg = '\n'.join(self.related(match.group(1).upper().strip().split(' ')))
            print(len(msg))
            await message.channel.send(msg)
        elif match := re.match(rf'!(?:beginswith|startswith)((?: [a-z]+)+)', command):
            msg = '\n'.join(self.beginswith(match.group(1).upper().strip().split(' ')))
            print(len(msg))
            await message.channel.send(msg)
        elif match := re.match(rf'!(?:endswith|finisheswith)((?: [a-z]+)+)', command):
            msg = '\n'.join(self.endswith(match.group(1).upper().strip().split(' ')))
            print(len(msg))
            await message.channel.send(msg)
        elif match := re.match(rf'!contains((?: [a-z]+)+)', command):
            msg = '\n'.join(self.contains(match.group(1).upper().strip().split(' ')))
            print(len(msg))
            await message.channel.send(msg)
        elif match := re.match(rf'!pattern((?: [a-z]+)+)', command):
            msg = '\n'.join(self.pattern(match.group(1).upper().strip().split(' ')))
            print(len(msg))
            await message.channel.send(msg)
        elif match := re.match(rf'!regex((?: [a-z]+)+)', command):
            msg = '\n'.join(self.regex(match.group(1).upper().strip().split(' ')))
            print(len(msg))
            await message.channel.send(msg)
        elif match := re.match(rf'!hook((?: [a-z]+)+)', command):
            msg = '\n'.join(self.hook(match.group(1).upper().strip().split(' ')))
            print(len(msg))
            await message.channel.send(msg)
        elif match := re.match(rf'!unhook((?: [a-z]+)+)', command):
            msg = '\n'.join(self.unhook(match.group(1).upper().strip().split(' ')))
            print(len(msg))
            await message.channel.send(msg)
        elif match := re.match(rf'!info((?: [a-z]+)+)', command):
            msg = '\n'.join(self.info(match.group(1).upper().strip().split(' ')))
            print(len(msg))
            await message.channel.send(msg)
        elif match := re.match(rf'!anagram((?: [a-z]+)+)', command):
            msg = '\n'.join(self.anagram(match.group(1).upper().strip().split(' ')))
            print(len(msg))
            await message.channel.send(msg)
        elif match := re.match(rf'!bingo(?: (\d+))?', command):
            msg = self.bingo(match)
            print(len(msg))
            await message.channel.send(msg)
        elif match := re.match(rf'!random(?: (\d+))?', command):
            msg = self.random(match.group(1).upper().strip().split(' ') or '0')
            print(len(msg))
            await message.channel.send(msg)
        elif match := re.match(rf'!pronounce ([a-z])+', command):
            msg = self.pronounce(match.group(1).upper())
            print(len(msg))
            await message.channel.send(msg)
        elif match := re.match(rf'!crypto((?: [a-z]+)+)', command):
            msg = '\n'.join(self.crypto(match.group(1).upper().strip().split(' ')))
            print(len(msg))
            await message.channel.send(msg)
        elif match := re.match(rf'!hidden (\d+)((?: [a-z]+)+)', command):
            msg = '\n'.join(self.hidden(match.group(1), match.group(2).upper().strip().split(' ')))
            print(len(msg))
            await message.channel.send(msg)

def main():
    DiscordBot().run()

if __name__ == "__main__":
    main()

