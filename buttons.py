import random

import discord
from discord.ui import Item

from game import Game


class ButtonsUI(discord.ui.View):
    def __init__(
        self,
        *items: Item,
        timeout: float | None = 180,
        disable_on_timeout: bool = False,
        save_game,
        client,
    ):
        super().__init__(*items, timeout=timeout, disable_on_timeout=disable_on_timeout)
        self.save_game = save_game
        self.client = client

    @discord.ui.button(label="Play", style=discord.ButtonStyle.primary, emoji="🎮")
    async def play_callback(self, button, interaction):
        if self.save_game.config["neil"] == interaction.user.id:
            await interaction.response.send_message("You are Neil💀", ephemeral=True)
            return
        for g in self.save_game.games:
            if interaction.user.id == g.guesser_id:
                await interaction.response.send_message(
                    "You are already in a game as a guesser!", ephemeral=True
                )
                return

        if random.randint(0, 1) == 0:
            neiler_id = self.save_game.config["neil"]
            neiler = await self.client.fetch_user(neiler_id)
            await neiler.send(
                f"<@{interaction.user.id}> is playing Is it Neil? Try to convince them they are not talking to Neil!"
            )
        else:
            neiler_id = 0
            while neiler_id == 0 or neiler_id == interaction.user.id:
                neiler_id = random.choice(self.save_game.neilers)
            neiler = await self.client.fetch_user(neiler_id)
            await neiler.send(
                f"<@{interaction.user.id}> is playing Is it Neil? Try to convince them they are talking to Neil!"
            )
        game = Game(interaction.user.id, neiler_id)
        self.save_game.games.append(game)
        await interaction.response.send_message(
            "A game has begun! Wait for a DM.", ephemeral=True
        )
        self.save_game.save()

    @discord.ui.button(label="Guess Neil", style=discord.ButtonStyle.green, emoji="✅")
    async def neil_callback(self, button, interaction):
        if self.save_game.config["neil"] == interaction.user.id:
            await interaction.response.send_message("You are Neil💀", ephemeral=True)
            return
        for g in self.save_game.games:
            if interaction.user.id == g.guesser_id:
                game = g
                break
        else:
            await interaction.response.send_message(
                "You are not a guesser in any game right now!", ephemeral=True
            )
            return

        if game.is_neil(self.save_game.config):
            neiler_id = game.neiler_id
            neiler = await self.client.fetch_user(neiler_id)
            await neiler.send(
                f"<@{interaction.user.id}> succesfully guessed you were Neil!"
            )
            await interaction.response.send_message(
                "You guessed correctly! You were talking to Neil.", ephemeral=True
            )
        else:
            neiler_id = game.neiler_id
            neiler = await self.client.fetch_user(neiler_id)
            await neiler.send(
                f"<@{interaction.user.id}> guessed incorrectly! They thought you were Neil. Good job!"
            )
            await interaction.response.send_message(
                f"You guessed incorrectly! You were talking to <@{neiler_id}>.",
                ephemeral=True,
            )
        self.save_game.games.remove(g)
        self.save_game.save()

    @discord.ui.button(label="Guess not Neil", style=discord.ButtonStyle.red, emoji="✖️")
    async def not_neil_callback(self, button, interaction):
        if self.save_game.config["neil"] == interaction.user.id:
            await interaction.response.send_message("You are Neil💀", ephemeral=True)
            return
        for g in self.save_game.games:
            if interaction.user.id == g.guesser_id:
                game = g
                break
        else:
            await interaction.response.send_message(
                "You are not a guesser in any game right now!", ephemeral=True
            )
            return

        if game.is_neil(self.save_game.config):
            neiler_id = game.neiler_id
            neiler = await self.client.fetch_user(neiler_id)
            await neiler.send(
                f"<@{interaction.user.id}> thought they were talking to Neil! Good job!"
            )
            await interaction.response.send_message(
                "You guessed incorrectly! You were talking to Neil.", ephemeral=True
            )
        else:
            neiler_id = game.neiler_id
            neiler = await self.client.fetch_user(neiler_id)
            await neiler.send(
                f"<@{interaction.user.id}> guessed correctly! They realized you were not Neil."
            )
            await interaction.response.send_message(
                f"You guessed correctly! You were talking to <@{neiler_id}>.",
                ephemeral=True,
            )
        self.save_game.games.remove(g)
        self.save_game.save()

    @discord.ui.button(
        label="Add/Remove me from the Neil List",
        style=discord.ButtonStyle.primary,
        emoji="🥸",
    )
    async def add_remove_callback(self, button, interaction):
        if self.save_game.config["neil"] == interaction.user.id:
            await interaction.response.send_message("You are Neil💀", ephemeral=True)
            return
        if interaction.user.id in self.save_game.neilers:
            self.save_game.neilers.remove(interaction.user.id)
            await interaction.response.send_message(
                "You are no longer a Neiler", ephemeral=True
            )
        else:
            self.save_game.neilers.append(interaction.user.id)
            await interaction.response.send_message(
                "You are now a Neiler! Wait to recieve a DM from the bot.",
                ephemeral=True,
            )
        self.save_game.save()
