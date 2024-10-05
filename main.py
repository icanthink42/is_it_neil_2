import json
import os

import discord

from buttons import ButtonsUI
from save_state import SaveState

bot = discord.Bot()


with open("token.txt") as f:
    token = f.read()

with open("config.json") as f:
    config = json.load(f)

if os.path.isfile(config["save_path"]):
    save_game = SaveState.load(config["save_path"])
    save_game.config = config
else:
    save_game = SaveState(config)


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")


@bot.slash_command(guild_ids=config["guild_ids"])
async def spawn_buttons(ctx):
    await ctx.respond(
        "Is it Neil???",
        view=ButtonsUI(save_game=save_game, client=bot),
    )


@bot.event
async def on_message(message: discord.Message):
    is_guesser = False
    if not (message.guild is None and not message.author.bot):
        return
    if message.reference is None:
        await message.reply("Reply to a message to specify who you want to reply to.")
        return
    else:
        reply_message = await message.channel.fetch_message(
            message.reference.message_id
        )
    split_message = reply_message.content.replace("@", "").replace("<", ">").split(">")
    if len(split_message) > 1:
        other_user_id = int(split_message[1])
        for game in save_game.games:
            if game.guesser_id == other_user_id and game.neiler_id == message.author.id:
                break
        else:
            await message.reply(
                f"You are not playing a game with <@{other_user_id}> right now!"
            )
            return
    else:
        is_guesser = True
        for game in save_game.games:
            if game.guesser_id == message.author.id:
                other_user_id = game.neiler_id
                break
        else:
            await message.reply("You are not playing a game as a guesser right now!")
            return
    other_user = await bot.fetch_user(other_user_id)
    if is_guesser:
        await other_user.send(f"<@{message.author.id}>: {message.content}")
    else:
        await other_user.send(f"????????: {message.content}")


bot.run(token)
