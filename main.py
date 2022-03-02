"""
EMBED-FIXER

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <https://www.gnu.org/licenses/>.
"""


import json
import inspect

import discord
bot = discord.Client()

def log(s: str, level: str = 'info'):
    fn = inspect.currentframe().f_back.f_code.co_name

    if fn == '<module>':
        fn = 'main'

    print(f'[{fn}] [{level}] {s}')

@bot.event
async def on_ready():
    log(f'logged in as {bot.user}')

@bot.event
async def on_message(msg: discord.Message):
    if msg.author.bot:
        return

    if msg.author.id == bot.user.id:
        return

    if 'https://media.discordapp.net' in msg.content:
        # await msg.delete()
        await msg.reply(
            ':hammer_pick: Changed **media.discordapp.net** to **cdn.discordapp.com** so the media plays properly! You\'re welcome!\n'
            + msg.content.replace(
                'https://media.discordapp.net', 'https://cdn.discordapp.com'
            )
        )

def write_config(_config):
    """Writes the config file to disk."""
    with open('config.json', 'w+', encoding='utf-8') as f:
        json.dump(_config, f, indent=4)

def main():
    config = {
        'token': ''
    }

    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        log('config file created now, token will probably be invalid', 'warn')
    finally:
        write_config(config)

    try:
        log('logging in')
        bot.run(
            config.get('token')
        )
    except discord.LoginFailure as e:
        log(f'login failed: {e}', 'fatal')


if __name__ == '__main__':
    main()
