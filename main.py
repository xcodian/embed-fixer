import json
import inspect

import discord
from discord.ext import commands

bot = commands.Bot('ef!')

def log(s: str, level: str = 'info'):
    fn = inspect.currentframe().f_back.f_code.co_name

    if fn == '<module>':
        fn = 'main'

    print(f'[{fn}] [{level}] {s}')


@bot.event
async def on_ready():
    log(f'logged in as {bot.user}')

if __name__ == '__main__':
    def write_config(_config):
        """Writes the config file to disk."""
        with open('config.json', 'w+') as f:
            json.dump(_config, f, indent=4)
    
    config = {
        'token': ''
    }

    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
    except:
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