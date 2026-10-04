import discord
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(".", intents=intents)

bot = commands.Bot(command_prefix="!", intents=intents)

import discord
from discord.ext import commands, tasks
from discord.ui import Button, View

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
import discord
from discord.ext import commands, tasks
from discord.ui import Button, View

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ---------- GIF links ----------
GIFS = {
    "idle":  "https://media.discordapp.net/attachments/1001158082522517545/1553548400262119474/idlegif.gif?ex=6ab9a632&is=6ab854b2&hm=fbd3e5fb6f62be8710c23ec340663084a7aaf0baef2548d28e243c76025da82d&=",
    "sad":   "https://media.discordapp.net/attachments/1001158082522517545/1553548399884640386/sadgif.gif?ex=6ab9a632&is=6ab854b2&hm=b218934715fa4a2152da3034e48b776008be0386b04d5fed3fd4caf3f33f8aeb&=",
    "happy": "https://media.discordapp.net/attachments/1001158082522517545/1553548400849584248/happygif.gif?ex=6ab9a632&is=6ab854b2&hm=a0dae47643cb02f05656b34cccdd38eb5f240eda3f13fa31ba946a00326e67ca&=",
}
# ---------- Pet state (renamed to avoid conflict) ----------
class Pet:
    def __init__(self):
        self.state = "idle"
        self.message = None

tama = Pet()          # ← changed from "pet" to "tama"

# ---------- Helpers ----------
def make_embed():
    colors = {
        "idle":  0xAAAAAA,
        "sad":   0x3498DB,
        "happy": 0x2ECC71,
    }
    titles = {
        "idle":  "😐 Idle",
        "sad":   "😢 Sad",
        "happy": "😊 Happy",
    }

    embed = discord.Embed(
        title=f"Tamagotchi — {titles[tama.state]}",
        color=colors[tama.state]
    )
    embed.set_image(url=GIFS[tama.state])
    return embed

def get_view():
    if tama.state == "sad":
        return PetView()
    return None

# ---------- Button view ----------
class PetView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Cheer up!", style=discord.ButtonStyle.success, custom_id="cheer_up")
    async def cheer_up(self, interaction: discord.Interaction, button: Button):
        if tama.state != "sad":
            await interaction.response.send_message("Caine is not sad right now 🐾", ephemeral=True)
            return

        tama.state = "happy"
        await interaction.response.edit_message(embed=make_embed(), view=get_view())
        await interaction.followup.send(f"{interaction.user.mention} You cheered Caine up! ❤️", ephemeral=False)

# === Durations in seconds ===
DURATIONS = {
    "happy": 10 * 60,   # 10 minutes
    "idle":  10 * 60,   # 10 minutes
    # "sad" has no duration – it stays forever
}

# ---------- Background state machine ----------
@tasks.loop(minutes=1)

async def state_loop():
    if tama.state == "sad":
        return  # do nothing – sad is permanent until an event

    now = time.time()
        elapsed = now - tama.last_change
        max_duration = DURATIONS.get(tama.state)
    
        if max_duration is None or elapsed < max_duration:
            return  # still within the allowed time

async def state_loop():
    if tama.state == "idle":
        tama.state = "sad"
    elif tama.state == "happy":
        tama.state = "idle"

tama.last_change = now

    if tama.message:
        try:
            await tama.message.edit(embed=make_embed(), view=get_view())
        except discord.NotFound:
            tama.message = None

@state_loop.before_loop
async def before_state_loop():
    await bot.wait_until_ready()

# ---------- Events & Commands ----------
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    if not state_loop.is_running():
        state_loop.start()

@bot.command()
async def pet(ctx):
    """Show the current pet status + GIF"""
    embed = make_embed()
    view = get_view()
    msg = await ctx.send(embed=embed, view=view)
    tama.message = msg

# ---------- Run ----------
import os
bot.run(os.getenv("DISCORD_TOKEN"))
