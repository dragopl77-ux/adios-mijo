import discord
from discord.ext import commands
import datetime
import os

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} — Adios Mijo is online!")

@bot.command(name="inactive")
@commands.has_permissions(administrator=True)
async def inactive(ctx, days: int = 120):
    await ctx.send(f"🔍 Scanning channels for members silent for **{days}** days... Please wait.")
    
    cutoff_date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days)
    active_users = set()

    for channel in ctx.guild.text_channels:
        try:
            async for message in channel.history(limit=3000, after=cutoff_date):
                if message.author:
                    active_users.add(message.author.id)
        except discord.Forbidden:
            continue

    inactive_members = []
    for member in ctx.guild.members:
        if member.bot:
            continue
        if member.guild_permissions.administrator:
            continue

        if member.id not in active_users:
            inactive_members.append(member.name)

    if not inactive_members:
        await ctx.send("🎉 Clean sheet! No inactive members found in this timeframe.")
        return

    chunks = [inactive_members[i:i + 25] for i in range(0, len(inactive_members), 25)]
    await ctx.send(f"📋 **Inactivity Report ({len(inactive_members)} members found):**")
    for chunk in chunks:
        await ctx.send("\n".join(chunk))

# Safely load the token from Render's hidden environment variables
bot.run(os.environ.get("DISCORD_TOKEN"))
