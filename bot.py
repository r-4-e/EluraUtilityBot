"""
╔═════════════════════════════════════════════════════════════════��[...]
║                           ELURA UTILITY BOT                                   ║
║                         Aurora Engine™ v1.0                                   ║
║              Premium Trillion-Dollar Discord Bot Experience                   ║
╚═════════════════════════════════════════════════════════════════��[...]
"""

import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import aiohttp
import json
import os
import random
import time
import uuid
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Union
from dotenv import load_dotenv
import re
import subprocess
import sys
import tempfile
import shutil

load_dotenv()

# ══════════════════════════════════════════════════════════════════[...]
# CONSTANTS & CONFIGURATION
# ══════════════════════════════════════════════════════════════════[...]

BOT_NAME = "Elura Utility"
ENGINE_NAME = "Aurora Engine™"
FOOTER_TEXT = f"{BOT_NAME} • {ENGINE_NAME}"
PREFIXES = ["eu ", "elura "]

# Premium UI Colors
class Colors:
    PRIMARY = 0x7C3AED      # Purple
    SUCCESS = 0x10B981      # Green
    ERROR = 0xEF4444        # Red
    WARNING = 0xF59E0B      # Orange
    INFO = 0x3B82F6         # Blue
    GOLD = 0xFFD700         # Gold
    GLASS = 0x1E1E2E        # Dark glass
    NEON_PURPLE = 0x8B5CF6  # Neon purple
    NEON_CYAN = 0x06B6D4    # Neon cyan
    HOLOGRAM = 0xA855F7     # Hologram purple

# Emoji decorations for premium UI
class Emojis:
    WALLET = "💎"
    BANK = "🏦"
    COIN = "🪙"
    MONEY = "💰"
    DICE = "🎲"
    CARDS = "🃏"
    SLOT = "🎰"
    TROPHY = "🏆"
    STAR = "⭐"
    CROWN = "👑"
    SHIELD = "🛡️"
    SWORD = "⚔️"
    GAVEL = "🔨"
    WARN = "⚠️"
    CHECK = "✅"
    CROSS = "❌"
    VOTE = "🗳️"
    PARTY = "🎉"
    PARLIAMENT = "🏛️"
    SCROLL = "📜"
    GLOBE = "🌐"
    CLOCK = "⏰"
    FIRE = "🔥"
    LIGHTNING = "⚡"
    SPARKLE = "✨"
    DIAMOND = "💠"
    GLASS = "🔮"
    GEAR = "⚙️"
    LINK = "🔗"
    SUPPORT = "💬"

# ══════════════════════════════════════════════════════════════════[...]
# JSON FILE MANAGEMENT
# ══════════════════════════════════════════════════════════════════[...]

DEFAULT_FILES = {
    "roles.json": {
        "punishment_tiers": {
            "tier1": ["1444276505872957511"],
            "tier2": ["1444277015095279628"],
            "tier3": ["1438894984677031957"],
            "tier4": ["1438894983456227418"],
            "tier5": ["1438894982537810081"]
        },
        "founder": "1438894978230259793"
    },
    "config.json": {
        "mod_channel": None,
        "counting_channel": None,
        "election_channel": None,
        "parliament_channel": None,
        "economy_enabled": True,
        "casino_enabled": True,
        "elections_enabled": True,
        "tax_rate": 0.05,
        "daily_amount": 1000,
        "weekly_amount": 7500,
        "work_min": 100,
        "work_max": 500,
        "crime_min": 200,
        "crime_max": 1500,
        "crime_fail_chance": 0.4
    },
    "economy.json": {},
    "casino.json": {
        "sessions": {},
        "stats": {}
    },
    "punishments.json": {
        "cases": [],
        "case_counter": 0
    },
    "election.json": {
        "active": False,
        "candidates": {},
        "votes": {},
        "voters": [],
        "start_time": None,
        "end_time": None
    },
    "vote_data.json": {
        "bills": {},
        "sessions": {}
    },
    "communist.json": {
        "members": [],
        "executives": {"president": None, "vice_president": None, "general_secretary": None}
    },
    "republic.json": {
        "members": [],
        "executives": {"president": None, "vice_president": None, "general_secretary": None}
    },
    "democratic.json": {
        "members": [],
        "executives": {"president": None, "vice_president": None, "general_secretary": None}
    },
    "message_counter.json": {
        "users": {},
        "total": 0
    },
    "support.json": {
        "support_link": "https://discord.gg/KgeDgVUTNH"
    },
    "gtw_words.json": {
        "prompts": [
            {"normal": "Something you find at the beach", "impostor": "Something you find in the desert"},
            {"normal": "A fruit that is red", "impostor": "A fruit that is yellow"},
            {"normal": "Something cold", "impostor": "Something hot"},
            {"normal": "A pet people love", "impostor": "A wild animal"},
            {"normal": "Something you wear on your head", "impostor": "Something you wear on your feet"},
            {"normal": "A breakfast food", "impostor": "A dinner food"},
            {"normal": "Something in a kitchen", "impostor": "Something in a bathroom"},
            {"normal": "A sport with a ball", "impostor": "A sport without a ball"},
            {"normal": "Something that flies", "impostor": "Something that swims"},
            {"normal": "A musical instrument", "impostor": "A tool for building"}
        ]
    },
    "gyi_words.json": {
        "pairs": [
            {"normal": "Beach", "impostor": "Desert"},
            {"normal": "Apple", "impostor": "Banana"},
            {"normal": "Dog", "impostor": "Cat"},
            {"normal": "Summer", "impostor": "Winter"},
            {"normal": "Mountain", "impostor": "Valley"},
            {"normal": "Ocean", "impostor": "Lake"},
            {"normal": "Car", "impostor": "Bicycle"},
            {"normal": "Pizza", "impostor": "Burger"},
            {"normal": "Coffee", "impostor": "Tea"},
            {"normal": "Guitar", "impostor": "Piano"}
        ]
    },
    "games_stats.json": {
        "gtw": {"leaderboard": {}},
        "gyi": {"leaderboard": {}}
    },
    "parliament.json": {
        "active_session": False,
        "session_id": None,
        "topic": None,
        "transcript": [],
        "motions": [],
        "start_time": None
    },
    "bills.json": {
        "bills": [],
        "bill_counter": 0
    }
}

def ensure_json_files():
    """Auto-generate all required JSON files on startup"""
    for filename, default_content in DEFAULT_FILES.items():
        if not os.path.exists(filename):
            with open(filename, 'w') as f:
                json.dump(default_content, f, indent=2)
            print(f"[Aurora Engine] Created {filename}")

def load_json(filename: str) -> dict:
    """Load JSON file with error handling"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        if filename in DEFAULT_FILES:
            save_json(filename, DEFAULT_FILES[filename])
            return DEFAULT_FILES[filename]
        return {}

def save_json(filename: str, data: dict):
    """Save JSON file atomically using temp file + rename"""
    dir_name = os.path.dirname(filename) or '.'
    try:
        fd, tmp_path = tempfile.mkstemp(suffix='.tmp', dir=dir_name)
        try:
            with os.fdopen(fd, 'w') as f:
                json.dump(data, f, indent=2)
                f.flush()
                os.fsync(f.fileno())
            shutil.move(tmp_path, filename)
        except:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
            raise
    except Exception as e:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

# ══════════════════════════════════════════════════════════════════[...]
# COMMAND LOCKS (Zero Duplicate Response Policy)
# ══════════════════════════════════════════════════════════════════[...]

command_locks: Dict[str, asyncio.Lock] = {}
interaction_tokens: Dict[str, float] = {}
IDEMPOTENCY_EXPIRY = 300

def get_command_lock(command_name: str) -> asyncio.Lock:
    """Get or create a lock for a specific command"""
    if command_name not in command_locks:
        command_locks[command_name] = asyncio.Lock()
    return command_locks[command_name]

def generate_idempotency_token(interaction: discord.Interaction, action: str = "") -> str:
    """Generate unique token for interaction"""
    return f"{interaction.id}_{interaction.user.id}_{action}"

def check_idempotency(token: str) -> bool:
    """Check if an idempotency token has been used. Returns True if action should proceed."""
    current_time = time.time()
    
    expired = [k for k, v in interaction_tokens.items() if current_time - v > IDEMPOTENCY_EXPIRY]
    for k in expired:
        del interaction_tokens[k]
    
    if token in interaction_tokens:
        return False
    
    interaction_tokens[token] = current_time
    
    if len(interaction_tokens) > 10000:
        sorted_tokens = sorted(interaction_tokens.items(), key=lambda x: x[1])
        interaction_tokens.clear()
        interaction_tokens.update(dict(sorted_tokens[-5000:]))
    
    return True

async def safe_interaction_response(interaction: discord.Interaction, action: str, **kwargs) -> bool:
    """Safely respond to interaction with idempotency check. Returns True if responded."""
    token = generate_idempotency_token(interaction, action)
    if not check_idempotency(token):
        return False
    
    try:
        if not interaction.response.is_done():
            await interaction.response.send_message(**kwargs)
        else:
            await interaction.followup.send(**kwargs)
        return True
    except discord.errors.InteractionResponded:
        return False
    except Exception:
        return False

# ══════════════════════════════════════════════════════════════════[...]
# PREMIUM UI BUILDERS
# ══════════════════════════════════════════════════════════════════[...]

def create_glass_embed(
    title: str,
    description: str = "",
    color: int = Colors.GLASS,
    author_name: str = None,
    author_icon: str = None,
    thumbnail: str = None,
    image: str = None,
    fields: List[tuple] = None
) -> discord.Embed:
    """Create a premium glassmorphism-style embed"""
    embed = discord.Embed(
        title=f"╔══ {title} ══╗",
        description=f"```ansi\n\u001b[0;35m{description}\u001b[0m\n```" if description else "",
        color=color,
        timestamp=datetime.utcnow()
    )
    
    if author_name:
        embed.set_author(name=author_name, icon_url=author_icon)
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
    if image:
        embed.set_image(url=image)
    
    if fields:
        for name, value, inline in fields:
            embed.add_field(name=f"▸ {name}", value=value, inline=inline)
    
    embed.set_footer(text=f"◈ {FOOTER_TEXT} ◈", icon_url=None)
    return embed

def create_neon_embed(
    title: str,
    description: str = "",
    color: int = Colors.NEON_PURPLE
) -> discord.Embed:
    """Create a neon-styled embed"""
    border = "═" * 30
    embed = discord.Embed(
        title=f"⟨ {title} ⟩",
        description=f"╔{border}╗\n{description}\n╚{border}╝",
        color=color,
        timestamp=datetime.utcnow()
    )
    embed.set_footer(text=f"◈ {FOOTER_TEXT} ◈")
    return embed

def create_hologram_embed(
    title: str,
    description: str = "",
    color: int = Colors.HOLOGRAM
) -> discord.Embed:
    """Create a futuristic hologram-style embed"""
    embed = discord.Embed(
        title=f"◈━━━━━ {title} ━━━━━◈",
        description=f"```\n{description}\n```" if description else "",
        color=color,
        timestamp=datetime.utcnow()
    )
    embed.set_footer(text=f"⟦ {FOOTER_TEXT} ⟧")
    return embed

def progress_bar(current: int, total: int, length: int = 10) -> str:
    """Create an animated progress bar"""
    filled = int(length * current / total) if total > 0 else 0
    empty = length - filled
    bar = "█" * filled + "░" * empty
    percentage = (current / total * 100) if total > 0 else 0
    return f"[{bar}] {percentage:.1f}%"

def format_currency(amount: int) -> str:
    """Format currency with commas and symbol"""
    return f"{Emojis.COIN} **{amount:,}**"

def format_time_remaining(seconds: int) -> str:
    """Format time remaining in human readable format"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        return f"{seconds // 60}m {seconds % 60}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"

# ══════════════════════════════════════════════════════════════════[...]
# BOT INITIALIZATION
# ══════════════════════════════════════════════════════════════════[...]

class EluraBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.guilds = True
        
        super().__init__(
            command_prefix=self.get_prefix,
            intents=intents,
            help_command=None
        )
        
        self.cooldowns: Dict[str, Dict[int, float]] = {}
        self.game_sessions: Dict[str, dict] = {}
        self.counting_data: Dict[int, int] = {}
        
    async def get_prefix(self, message: discord.Message):
        return commands.when_mentioned_or(*PREFIXES)(self, message)
    
    async def setup_hook(self):
        ensure_json_files()
        print(f"[{ENGINE_NAME}] JSON files verified")
        
        await self.tree.sync()
        print(f"[{ENGINE_NAME}] Slash commands synced")
    
    async def on_ready(self):
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║                    {BOT_NAME.upper()} ONLINE                        ║
║                    {ENGINE_NAME} Active                        ║
╠══════════════════════════════════════════════════════════════╣
║  Bot: {self.user.name}#{self.user.discriminator}
║  ID: {self.user.id}
║  Guilds: {len(self.guilds)}
║  Users: {sum(g.member_count for g in self.guilds)}
╚══════════════════════════════════════════════════════════════╝
        """)
        
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="eu help | /help"
            )
        )

bot = EluraBot()

# ══════════════════════════════════════════════════════════════════[...]
# COOLDOWN MANAGEMENT
# ══════════════════════════════════════════════════════════════════[...]

def check_cooldown(command: str, user_id: int, cooldown_seconds: int) -> tuple[bool, int]:
    """Check if user is on cooldown. Returns (is_on_cooldown, seconds_remaining)"""
    if command not in bot.cooldowns:
        bot.cooldowns[command] = {}
    
    current_time = time.time()
    if user_id in bot.cooldowns[command]:
        elapsed = current_time - bot.cooldowns[command][user_id]
        if elapsed < cooldown_seconds:
            return True, int(cooldown_seconds - elapsed)
    
    bot.cooldowns[command][user_id] = current_time
    return False, 0

# ══════════════════════════════════════════════════════════════════[...]
# ECONOMY SYSTEM
# ══════════════════════════════════════════════════════════════════[...]

def get_user_economy(user_id: int) -> dict:
    """Get user's economy data"""
    economy = load_json("economy.json")
    user_key = str(user_id)
    if user_key not in economy:
        economy[user_key] = {
            "wallet": 0,
            "bank": 0,
            "last_daily": None,
            "last_weekly": None,
            "last_work": None,
            "last_crime": None,
            "multiplier": 1.0,
            "total_earned": 0,
            "total_lost": 0
        }
        save_json("economy.json", economy)
    return economy[user_key]

def update_user_economy(user_id: int, data: dict):
    """Update user's economy data"""
    economy = load_json("economy.json")
    economy[str(user_id)] = data
    save_json("economy.json", economy)

async def economy_handler(ctx_or_interaction, command: str, amount: int = None, target: discord.Member = None):
    """Unified economy command handler"""
    is_slash = isinstance(ctx_or_interaction, discord.Interaction)
    user = ctx_or_interaction.user if is_slash else ctx_or_interaction.author
    config = load_json("config.json")
    
    user_data = get_user_economy(user.id)
    embed = None
    
    if command == "wallet":
        embed = create_glass_embed(
            title=f"{Emojis.WALLET} WALLET",
            description=f"{user.display_name}'s Holdings",
            color=Colors.GOLD,
            fields=[
                ("Wallet", format_currency(user_data["wallet"]), True),
                ("Bank", format_currency(user_data["bank"]), True),
                ("Net Worth", format_currency(user_data["wallet"] + user_data["bank"]), True),
                ("Multiplier", f"**{user_data['multiplier']}x**", True),
                ("Total Earned", format_currency(user_data["total_earned"]), True),
                ("Total Lost", format_currency(user_data["total_lost"]), True)
            ]
        )
        embed.set_thumbnail(url=user.display_avatar.url)
        
    elif command == "bank":
        embed = create_glass_embed(
            title=f"{Emojis.BANK} BANK ACCOUNT",
            description=f"Secure vault for {user.display_name}",
            color=Colors.NEON_CYAN,
            fields=[
                ("Balance", format_currency(user_data["bank"]), True),
                ("Interest Rate", "**0.5%** daily", True),
                ("Protection", "**100%** secured", True)
            ]
        )
        
    elif command == "deposit":
        if amount is None or amount <= 0:
            embed = create_glass_embed(
                title=f"{Emojis.CROSS} DEPOSIT FAILED",
                description="Please specify a valid amount to deposit.",
                color=Colors.ERROR
            )
        elif amount > user_data["wallet"]:
            embed = create_glass_embed(
                title=f"{Emojis.CROSS} INSUFFICIENT FUNDS",
                description=f"You only have {format_currency(user_data['wallet'])} in your wallet.",
                color=Colors.ERROR
            )
        else:
            user_data["wallet"] -= amount
            user_data["bank"] += amount
            update_user_economy(user.id, user_data)
            embed = create_glass_embed(
                title=f"{Emojis.CHECK} DEPOSIT SUCCESSFUL",
                description=f"Deposited {format_currency(amount)} into your bank.",
                color=Colors.SUCCESS,
                fields=[
                    ("New Wallet Balance", format_currency(user_data["wallet"]), True),
                    ("New Bank Balance", format_currency(user_data["bank"]), True)
                ]
            )
            
    elif command == "withdraw":
        if amount is None or amount <= 0:
            embed = create_glass_embed(
                title=f"{Emojis.CROSS} WITHDRAWAL FAILED",
                description="Please specify a valid amount to withdraw.",
                color=Colors.ERROR
            )
        elif amount > user_data["bank"]:
            embed = create_glass_embed(
                title=f"{Emojis.CROSS} INSUFFICIENT FUNDS",
                description=f"You only have {format_currency(user_data['bank'])} in your bank.",
                color=Colors.ERROR
            )
        else:
            user_data["bank"] -= amount
            user_data["wallet"] += amount
            update_user_economy(user.id, user_data)
            embed = create_glass_embed(
                title=f"{Emojis.CHECK} WITHDRAWAL SUCCESSFUL",
                description=f"Withdrew {format_currency(amount)} from your bank.",
                color=Colors.SUCCESS,
                fields=[
                    ("New Wallet Balance", format_currency(user_data["wallet"]), True),
                    ("New Bank Balance", format_currency(user_data["bank"]), True)
                ]
            )
            
    elif command == "daily":
        on_cooldown, remaining = check_cooldown("daily", user.id, 86400)
        if on_cooldown:
            embed = create_glass_embed(
                title=f"{Emojis.CLOCK} DAILY COOLDOWN",
                description=f"You can claim your daily reward in **{format_time_remaining(remaining)}**",
                color=Colors.WARNING
            )
        else:
            reward = int(config["daily_amount"] * user_data["multiplier"])
            user_data["wallet"] += reward
            user_data["total_earned"] += reward
            update_user_economy(user.id, user_data)
            embed = create_glass_embed(
                title=f"{Emojis.STAR} DAILY REWARD CLAIMED!",
                description=f"You received {format_currency(reward)}!",
                color=Colors.GOLD,
                fields=[
                    ("Multiplier Applied", f"**{user_data['multiplier']}x**", True),
                    ("New Balance", format_currency(user_data["wallet"]), True)
                ]
            )
            
    elif command == "weekly":
        on_cooldown, remaining = check_cooldown("weekly", user.id, 604800)
        if on_cooldown:
            embed = create_glass_embed(
                title=f"{Emojis.CLOCK} WEEKLY COOLDOWN",
                description=f"You can claim your weekly reward in **{format_time_remaining(remaining)}**",
                color=Colors.WARNING
            )
        else:
            reward = int(config["weekly_amount"] * user_data["multiplier"])
            user_data["wallet"] += reward
            user_data["total_earned"] += reward
            update_user_economy(user.id, user_data)
            embed = create_glass_embed(
                title=f"{Emojis.CROWN} WEEKLY REWARD CLAIMED!",
                description=f"You received {format_currency(reward)}!",
                color=Colors.GOLD,
                fields=[
                    ("Multiplier Applied", f"**{user_data['multiplier']}x**", True),
                    ("New Balance", format_currency(user_data["wallet"]), True)
                ]
            )
            
    elif command == "work":
        on_cooldown, remaining = check_cooldown("work", user.id, 3600)
        if on_cooldown:
            embed = create_glass_embed(
                title=f"{Emojis.CLOCK} WORK COOLDOWN",
                description=f"You can work again in **{format_time_remaining(remaining)}**",
                color=Colors.WARNING
            )
        else:
            jobs = [
                "software developer", "chef", "artist", "teacher", "doctor",
                "engineer", "musician", "writer", "designer", "scientist"
            ]
            job = random.choice(jobs)
            earnings = random.randint(config["work_min"], config["work_max"])
            earnings = int(earnings * user_data["multiplier"])
            user_data["wallet"] += earnings
            user_data["total_earned"] += earnings
            update_user_economy(user.id, user_data)
            embed = create_glass_embed(
                title=f"{Emojis.MONEY} WORK COMPLETE",
                description=f"You worked as a **{job}** and earned {format_currency(earnings)}!",
                color=Colors.SUCCESS,
                fields=[
                    ("New Balance", format_currency(user_data["wallet"]), True)
                ]
            )
            
    elif command == "crime":
        on_cooldown, remaining = check_cooldown("crime", user.id, 7200)
        if on_cooldown:
            embed = create_glass_embed(
                title=f"{Emojis.CLOCK} CRIME COOLDOWN",
                description=f"You need to lay low for **{format_time_remaining(remaining)}**",
                color=Colors.WARNING
            )
        else:
            if random.random() < config["crime_fail_chance"]:
                fine = random.randint(200, 800)
                if user_data["wallet"] >= fine:
                    user_data["wallet"] -= fine
                    user_data["total_lost"] += fine
                    update_user_economy(user.id, user_data)
                    embed = create_glass_embed(
                        title=f"{Emojis.CROSS} CRIME FAILED!",
                        description=f"You got caught and paid a {format_currency(fine)} fine!",
                        color=Colors.ERROR,
                        fields=[
                            ("New Balance", format_currency(user_data["wallet"]), True)
                        ]
                    )
                else:
                    embed = create_glass_embed(
                        title=f"{Emojis.CROSS} CRIME FAILED!",
                        description="You got caught but had no money to pay the fine. Lucky you!",
                        color=Colors.WARNING
                    )
            else:
                earnings = random.randint(config["crime_min"], config["crime_max"])
                earnings = int(earnings * user_data["multiplier"])
                user_data["wallet"] += earnings
                user_data["total_earned"] += earnings
                update_user_economy(user.id, user_data)
                crimes = ["robbed a bank", "hacked a database", "stole diamonds", "smuggled goods"]
                crime = random.choice(crimes)
                embed = create_glass_embed(
                    title=f"{Emojis.FIRE} CRIME SUCCESS!",
                    description=f"You {crime} and got {format_currency(earnings)}!",
                    color=Colors.SUCCESS,
                    fields=[
                        ("New Balance", format_currency(user_data["wallet"]), True)
                    ]
                )
    
    if is_slash:
        await ctx_or_interaction.response.send_message(embed=embed)
    else:
        await ctx_or_interaction.send(embed=embed)

# Economy Slash Commands
@bot.tree.command(name="wallet", description="View your wallet and economy stats")
async def wallet_slash(interaction: discord.Interaction):
    async with get_command_lock("wallet"):
        await economy_handler(interaction, "wallet")

@bot.tree.command(name="bank", description="View your bank account")
async def bank_slash(interaction: discord.Interaction):
    async with get_command_lock("bank"):
        await economy_handler(interaction, "bank")

@bot.tree.command(name="deposit", description="Deposit coins into your bank")
@app_commands.describe(amount="Amount to deposit")
async def deposit_slash(interaction: discord.Interaction, amount: int):
    async with get_command_lock("deposit"):
        await economy_handler(interaction, "deposit", amount)

@bot.tree.command(name="withdraw", description="Withdraw coins from your bank")
@app_commands.describe(amount="Amount to withdraw")
async def withdraw_slash(interaction: discord.Interaction, amount: int):
    async with get_command_lock("withdraw"):
        await economy_handler(interaction, "withdraw", amount)

@bot.tree.command(name="daily", description="Claim your daily reward")
async def daily_slash(interaction: discord.Interaction):
    async with get_command_lock("daily"):
        await economy_handler(interaction, "daily")

@bot.tree.command(name="weekly", description="Claim your weekly reward")
async def weekly_slash(interaction: discord.Interaction):
    async with get_command_lock("weekly"):
        await economy_handler(interaction, "weekly")

@bot.tree.command(name="work", description="Work for coins")
async def work_slash(interaction: discord.Interaction):
    async with get_command_lock("work"):
        await economy_handler(interaction, "work")

@bot.tree.command(name="crime", description="Attempt a risky crime for big rewards")
async def crime_slash(interaction: discord.Interaction):
    async with get_command_lock("crime"):
        await economy_handler(interaction, "crime")

# Economy Prefix Commands
@bot.command(name="wallet", aliases=["bal", "balance"])
async def wallet_prefix(ctx):
    async with get_command_lock("wallet"):
        await economy_handler(ctx, "wallet")

@bot.command(name="bank")
async def bank_prefix(ctx):
    async with get_command_lock("bank"):
        await economy_handler(ctx, "bank")

@bot.command(name="deposit", aliases=["dep"])
async def deposit_prefix(ctx, amount: int = None):
    async with get_command_lock("deposit"):
        await economy_handler(ctx, "deposit", amount)

@bot.command(name="withdraw", aliases=["with"])
async def withdraw_prefix(ctx, amount: int = None):
    async with get_command_lock("withdraw"):
        await economy_handler(ctx, "withdraw", amount)

@bot.command(name="daily")
async def daily_prefix(ctx):
    async with get_command_lock("daily"):
        await economy_handler(ctx, "daily")

@bot.command(name="weekly")
async def weekly_prefix(ctx):
    async with get_command_lock("weekly"):
        await economy_handler(ctx, "weekly")

@bot.command(name="work")
async def work_prefix(ctx):
    async with get_command_lock("work"):
        await economy_handler(ctx, "work")

@bot.command(name="crime")
async def crime_prefix(ctx):
    async with get_command_lock("crime"):
        await economy_handler(ctx, "crime")

# ══════════════════════════════════════════════════════════════════[...]
# CASINO SYSTEM
# ══════════════════════════════════════════════════════════════════[...]

async def casino_handler(ctx_or_interaction, game: str, bet: int = None, choice: str = None):
    """Unified casino game handler"""
    is_slash = isinstance(ctx_or_interaction, discord.Interaction)
    user = ctx_or_interaction.user if is_slash else ctx_or_interaction.author
    user_data = get_user_economy(user.id)
    
    casino_data = load_json("casino.json")
    user_key = str(user.id)
    if user_key not in casino_data["stats"]:
        casino_data["stats"][user_key] = {"wins": 0, "losses": 0, "total_won": 0, "total_lost": 0}
    
    embed = None
    
    if game == "coinflip":
        if bet is None or bet <= 0:
            embed = create_glass_embed(
                title=f"{Emojis.COIN} COINFLIP",
                description="Usage: `coinflip <bet> <heads/tails>`",
                color=Colors.INFO
            )
        elif bet > user_data["wallet"]:
            embed = create_glass_embed(
                title=f"{Emojis.CROSS} INSUFFICIENT FUNDS",
                description=f"You need {format_currency(bet)} to play!",
                color=Colors.ERROR
            )
        elif choice not in ["heads", "tails", "h", "t"]:
            embed = create_glass_embed(
                title=f"{Emojis.CROSS} INVALID CHOICE",
                description="Choose **heads** or **tails**!",
                color=Colors.ERROR
            )
        else:
            result = random.choice(["heads", "tails"])
            player_choice = "heads" if choice in ["heads", "h"] else "tails"
            
            if result == player_choice:
                winnings = bet * 2
                user_data["wallet"] += bet
                user_data["total_earned"] += bet
                casino_data["stats"][user_key]["wins"] += 1
                casino_data["stats"][user_key]["total_won"] += bet
                embed = create_neon_embed(
                    title=f"{Emojis.TROPHY} YOU WIN!",
                    description=f"The coin landed on **{result}**!\nYou won {format_currency(bet)}!",
                    color=Colors.SUCCESS
                )
            else:
                user_data["wallet"] -= bet
                user_data["total_lost"] += bet
                casino_data["stats"][user_key]["losses"] += 1
                casino_data["stats"][user_key]["total_lost"] += bet
                embed = create_neon_embed(
                    title=f"{Emojis.CROSS} YOU LOSE!",
                    description=f"The coin landed on **{result}**.\nYou lost {format_currency(bet)}.",
                    color=Colors.ERROR
                )
            
            update_user_economy(user.id, user_data)
            save_json("casino.json", casino_data)
            
    elif game == "slots":
        if bet is None or bet <= 0:
            embed = create_glass_embed(
                title=f"{Emojis.SLOT} SLOTS",
                description="Usage: `slots <bet>`",
                color=Colors.INFO
            )
        elif bet > user_data["wallet"]:
            embed = create_glass_embed(
                title=f"{Emojis.CROSS} INSUFFICIENT FUNDS",
                description=f"You need {format_currency(bet)} to play!",
                color=Colors.ERROR
            )
        else:
            symbols = ["🍒", "🍋", "🍊", "🍇", "💎", "7️⃣", "🎰"]
            weights = [30, 25, 20, 15, 7, 2, 1]
            
            reels = random.choices(symbols, weights=weights, k=3)
            
            display = f"╔═══════════════════╗\n║  {reels[0]}  │  {reels[1]}  │  {reels[2]}  ║\n╚═════════════════�[...]
            
            if reels[0] == reels[1] == reels[2]:
                if reels[0] == "7️⃣":
                    multiplier = 50
                elif reels[0] == "💎":
                    multiplier = 25
                elif reels[0] == "🎰":
                    multiplier = 100
                else:
                    multiplier = 10
                    
                winnings = bet * multiplier
                user_data["wallet"] += winnings - bet
                user_data["total_earned"] += winnings - bet
                casino_data["stats"][user_key]["wins"] += 1
                casino_data["stats"][user_key]["total_won"] += winnings - bet
                embed = create_hologram_embed(
                    title=f"{Emojis.SLOT} JACKPOT!",
                    description=f"{display}\n\n{Emojis.TROPHY} **{multiplier}x MULTIPLIER!**\nYou won {format_currency(winnings)}!",
                    color=Colors.GOLD
                )
            elif reels[0] == reels[1] or reels[1] == reels[2]:
                winnings = bet * 2
                user_data["wallet"] += bet
                user_data["total_earned"] += bet
                casino_data["stats"][user_key]["wins"] += 1
                casino_data["stats"][user_key]["total_won"] += bet
                embed = create_hologram_embed(
                    title=f"{Emojis.SLOT} PARTIAL WIN!",
                    description=f"{display}\n\n{Emojis.STAR} **2x MULTIPLIER!**\nYou won {format_currency(winnings)}!",
                    color=Colors.SUCCESS
                )
            else:
                user_data["wallet"] -= bet
                user_data["total_lost"] += bet
                casino_data["stats"][user_key]["losses"] += 1
                casino_data["stats"][user_key]["total_lost"] += bet
                embed = create_hologram_embed(
                    title=f"{Emojis.SLOT} NO MATCH",
                    description=f"{display}\n\n{Emojis.CROSS} Better luck next time!\nYou lost {format_currency(bet)}.",
                    color=Colors.ERROR
                )
            
            update_user_economy(user.id, user_data)
            save_json("casino.json", casino_data)
            
    elif game == "dice":
        if bet is None or bet <= 0:
            embed = create_glass_embed(
                title=f"{Emojis.DICE} DICE DUEL",
                description="Usage: `dice <bet>`\nRoll higher than the dealer to win!",
                color=Colors.INFO
            )
        elif bet > user_data["wallet"]:
            embed = create_glass_embed(
                title=f"{Emojis.CROSS} INSUFFICIENT FUNDS",
                description=f"You need {format_currency(bet)} to play!",
                color=Colors.ERROR
            )
        else:
            player_roll = random.randint(1, 6) + random.randint(1, 6)
            dealer_roll = random.randint(1, 6) + random.randint(1, 6)
            
            dice_display = f"🎲 Your Roll: **{player_roll}**\n🎲 Dealer Roll: **{dealer_roll}**"
            
            if player_roll > dealer_roll:
                user_data["wallet"] += bet
                user_data["total_earned"] += bet
                casino_data["stats"][user_key]["wins"] += 1
                casino_data["stats"][user_key]["total_won"] += bet
                embed = create_neon_embed(
                    title=f"{Emojis.TROPHY} YOU WIN!",
                    description=f"{dice_display}\n\nYou won {format_currency(bet)}!",
                    color=Colors.SUCCESS
                )
            elif player_roll < dealer_roll:
                user_data["wallet"] -= bet
                user_data["total_lost"] += bet
                casino_data["stats"][user_key]["losses"] += 1
                casino_data["stats"][user_key]["total_lost"] += bet
                embed = create_neon_embed(
                    title=f"{Emojis.CROSS} YOU LOSE!",
                    description=f"{dice_display}\n\nYou lost {format_currency(bet)}.",
                    color=Colors.ERROR
                )
            else:
                embed = create_neon_embed(
                    title=f"{Emojis.DICE} TIE!",
                    description=f"{dice_display}\n\nIt's a tie! Your bet has been returned.",
                    color=Colors.WARNING
                )
            
            update_user_economy(user.id, user_data)
            save_json("casino.json", casino_data)
            
    elif game == "roulette":
        if bet is None or bet <= 0:
            embed = create_glass_embed(
                title=f"{Emojis.DICE} ROULETTE",
                description="Usage: `roulette <bet> <red/black/green/number>`",
                color=Colors.INFO
            )
        elif bet > user_data["wallet"]:
            embed = create_glass_embed(
                title=f"{Emojis.CROSS} INSUFFICIENT FUNDS",
                description=f"You need {format_currency(bet)} to play!",
                color=Colors.ERROR
            )
        else:
            result = random.randint(0, 36)
            red_numbers = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
            
            if result == 0:
                result_color = "green"
            elif result in red_numbers:
                result_color = "red"
            else:
                result_color = "black"
            
            color_emoji = "🟢" if result_color == "green" else "🔴" if result_color == "red" else "⚫"
            
            won = False
            multiplier = 0
            
            if choice:
                choice = choice.lower()
                if choice == result_color:
                    won = True
                    multiplier = 14 if choice == "green" else 2
                elif choice.isdigit() and int(choice) == result:
                    won = True
                    multiplier = 35
            
            if won:
                winnings = bet * multiplier
                user_data["wallet"] += winnings - bet
                user_data["total_earned"] += winnings - bet
                casino_data["stats"][user_key]["wins"] += 1
                casino_data["stats"][user_key]["total_won"] += winnings - bet
                embed = create_hologram_embed(
                    title=f"{Emojis.TROPHY} ROULETTE WIN!",
                    description=f"{color_emoji} **{result}** ({result_color})\n\n{Emojis.STAR} **{multiplier}x!**\nYou won {format_currency(winnings)}!",
                    color=Colors.GOLD
                )
            else:
                user_data["wallet"] -= bet
                user_data["total_lost"] += bet
                casino_data["stats"][user_key]["losses"] += 1
                casino_data["stats"][user_key]["total_lost"] += bet
                embed = create_hologram_embed(
                    title=f"{Emojis.CROSS} ROULETTE LOSS",
                    description=f"{color_emoji} **{result}** ({result_color})\n\nYou lost {format_currency(bet)}.",
                    color=Colors.ERROR
                )
            
            update_user_economy(user.id, user_data)
            save_json("casino.json", casino_data)
    
    if embed:
        if is_slash:
            await ctx_or_interaction.response.send_message(embed=embed)
        else:
            await ctx_or_interaction.send(embed=embed)

# Casino Slash Commands
@bot.tree.command(name="coinflip", description="Flip a coin and bet on the outcome")
@app_commands.describe(bet="Amount to bet", choice="heads or tails")
@app_commands.choices(choice=[
    app_commands.Choice(name="Heads", value="heads"),
    app_commands.Choice(name="Tails", value="tails")
])
async def coinflip_slash(interaction: discord.Interaction, bet: int, choice: str):
    async with get_command_lock("coinflip"):
        await casino_handler(interaction, "coinflip", bet, choice)

@bot.tree.command(name="slots", description="Play the slot machine")
@app_commands.describe(bet="Amount to bet")
async def slots_slash(interaction: discord.Interaction, bet: int):
    async with get_command_lock("slots"):
        await casino_handler(interaction, "slots", bet)

@bot.tree.command(name="dice", description="Roll dice against the dealer")
@app_commands.describe(bet="Amount to bet")
async def dice_slash(interaction: discord.Interaction, bet: int):
    async with get_command_lock("dice"):
        await casino_handler(interaction, "dice", bet)

@bot.tree.command(name="roulette", description="Play roulette")
@app_commands.describe(bet="Amount to bet", choice="red, black, green, or a number 0-36")
async def roulette_slash(interaction: discord.Interaction, bet: int, choice: str):
    async with get_command_lock("roulette"):
        await casino_handler(interaction, "roulette", bet, choice)

# Casino Prefix Commands
@bot.command(name="coinflip", aliases=["cf", "flip"])
async def coinflip_prefix(ctx, bet: int = None, choice: str = None):
    async with get_command_lock("coinflip"):
        await casino_handler(ctx, "coinflip", bet, choice)

@bot.command(name="slots", aliases=["slot"])
async def slots_prefix(ctx, bet: int = None):
    async with get_command_lock("slots"):
        await casino_handler(ctx, "slots", bet)

@bot.command(name="dice", aliases=["roll"])
async def dice_prefix(ctx, bet: int = None):
    async with get_command_lock("dice"):
        await casino_handler(ctx, "dice", bet)

@bot.command(name="roulette", aliases=["rl"])
async def roulette_prefix(ctx, bet: int = None, choice: str = None):
    async with get_command_lock("roulette"):
        await casino_handler(ctx, "roulette", bet, choice)

# ══════════════════════════════════════════════════════════════════[...]
# BLACKJACK GAME
# ══════════════════════════════════════════════════════════════════[...]

class BlackjackView(discord.ui.View):
    def __init__(self, user_id: int, bet: int, player_hand: list, dealer_hand: list):
        super().__init__(timeout=60)
        self.user_id = user_id
        self.bet = bet
        self.player_hand = player_hand
        self.dealer_hand = dealer_hand
        self.deck = self.create_deck()
        self.game_over = False
        self.session_id = str(uuid.uuid4())[:8]
        self.processed_actions: set = set()
        
    def create_deck(self):
        suits = ["♠", "♥", "♦", "♣"]
        values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        deck = [(v, s) for s in suits for v in values]
        random.shuffle(deck)
        return deck
    
    def card_value(self, hand):
        value = 0
        aces = 0
        for card, _ in hand:
            if card in ["J", "Q", "K"]:
                value += 10
            elif card == "A":
                aces += 1
                value += 11
            else:
                value += int(card)
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value
    
    def format_hand(self, hand, hide_second=False):
        if hide_second and len(hand) > 1:
            return f"{hand[0][0]}{hand[0][1]} | ??"
        return " | ".join([f"{c[0]}{c[1]}" for c in hand])
    
    def create_embed(self, status="playing"):
        player_value = self.card_value(self.player_hand)
        dealer_value = self.card_value(self.dealer_hand) if status != "playing" else "?"
        
        embed = create_hologram_embed(
            title=f"{Emojis.CARDS} BLACKJACK",
            color=Colors.NEON_PURPLE
        )
        
        embed.add_field(
            name=f"Your Hand ({player_value})",
            value=self.format_hand(self.player_hand),
            inline=False
        )
        embed.add_field(
            name=f"Dealer's Hand ({dealer_value})",
            value=self.format_hand(self.dealer_hand, status == "playing"),
            inline=False
        )
        embed.add_field(name="Bet", value=format_currency(self.bet), inline=True)
        
        return embed
    
    async def end_game(self, interaction, result):
        self.game_over = True
        user_data = get_user_economy(self.user_id)
        casino_data = load_json("casino.json")
        user_key = str(self.user_id)
        
        if result == "win":
            user_data["wallet"] += self.bet
            user_data["total_earned"] += self.bet
            casino_data["stats"][user_key]["wins"] += 1
            casino_data["stats"][user_key]["total_won"] += self.bet
            title = f"{Emojis.TROPHY} YOU WIN!"
            color = Colors.SUCCESS
        elif result == "blackjack":
            winnings = int(self.bet * 1.5)
            user_data["wallet"] += winnings
            user_data["total_earned"] += winnings
            casino_data["stats"][user_key]["wins"] += 1
            casino_data["stats"][user_key]["total_won"] += winnings
            title = f"{Emojis.CROWN} BLACKJACK!"
            color = Colors.GOLD
        elif result == "push":
            title = f"{Emojis.CARDS} PUSH!"
            color = Colors.WARNING
        else:
            user_data["wallet"] -= self.bet
            user_data["total_lost"] += self.bet
            casino_data["stats"][user_key]["losses"] += 1
            casino_data["stats"][user_key]["total_lost"] += self.bet
            title = f"{Emojis.CROSS} DEALER WINS!"
            color = Colors.ERROR
        
        update_user_economy(self.user_id, user_data)
        save_json("casino.json", casino_data)
        
        embed = self.create_embed(status="ended")
        embed.title = title
        embed.color = color
        
        for item in self.children:
            item.disabled = True
        
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="Hit", style=discord.ButtonStyle.primary, emoji="🃏")
    async def hit(self, interaction: discord.Interaction, button: discord.ui.Button):
        action_token = f"{self.session_id}_hit_{interaction.id}"
        if action_token in self.processed_actions or self.game_over:
            try:
                await interaction.response.defer()
            except:
                pass
            return
        self.processed_actions.add(action_token)
        
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This isn't your game!", ephemeral=True)
            return
        
        self.player_hand.append(self.deck.pop())
        player_value = self.card_value(self.player_hand)
        
        if player_value > 21:
            await self.end_game(interaction, "lose")
        elif player_value == 21:
            await self.stand(interaction, button)
        else:
            embed = self.create_embed()
            await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="Stand", style=discord.ButtonStyle.secondary, emoji="✋")
    async def stand(self, interaction: discord.Interaction, button: discord.ui.Button):
        action_token = f"{self.session_id}_stand_{interaction.id}"
        if action_token in self.processed_actions or self.game_over:
            try:
                await interaction.response.defer()
            except:
                pass
            return
        self.processed_actions.add(action_token)
        
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This isn't your game!", ephemeral=True)
            return
        
        while self.card_value(self.dealer_hand) < 17:
            self.dealer_hand.append(self.deck.pop())
        
        player_value = self.card_value(self.player_hand)
        dealer_value = self.card_value(self.dealer_hand)
        
        if dealer_value > 21:
            await self.end_game(interaction, "win")
        elif player_value > dealer_value:
            await self.end_game(interaction, "win")
        elif player_value < dealer_value:
            await self.end_game(interaction, "lose")
        else:
            await self.end_game(interaction, "push")
    
    @discord.ui.button(label="Double Down", style=discord.ButtonStyle.success, emoji="💰")
    async def double_down(self, interaction: discord.Interaction, button: discord.ui.Button):
        action_token = f"{self.session_id}_double_{interaction.id}"
        if action_token in self.processed_actions or self.game_over:
            try:
                await interaction.response.defer()
            except:
                pass
            return
        self.processed_actions.add(action_token)
        
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This isn't your game!", ephemeral=True)
            return
        
        user_data = get_user_economy(self.user_id)
        if user_data["wallet"] < self.bet:
            await interaction.response.send_message("Not enough funds to double down!", ephemeral=True)
            return
        
        self.bet *= 2
        self.player_hand.append(self.deck.pop())
        
        if self.card_value(self.player_hand) > 21:
            await self.end_game(interaction, "lose")
        else:
            await self.stand(interaction, button)

async def blackjack_handler(ctx_or_interaction, bet: int = None):
    """Unified blackjack handler"""
    is_slash = isinstance(ctx_or_interaction, discord.Interaction)
    user = ctx_or_interaction.user if is_slash else ctx_or_interaction.author
    user_data = get_user_economy(user.id)
    
    if bet is None or bet <= 0:
        embed = create_glass_embed(
            title=f"{Emojis.CARDS} BLACKJACK",
            description="Usage: `blackjack <bet>`",
            color=Colors.INFO
        )
        if is_slash:
            await ctx_or_interaction.response.send_message(embed=embed)
        else:
            await ctx_or_interaction.send(embed=embed)
        return
    
    if bet > user_data["wallet"]:
        embed = create_glass_embed(
            title=f"{Emojis.CROSS} INSUFFICIENT FUNDS",
            description=f"You need {format_currency(bet)} to play!",
            color=Colors.ERROR
        )
        if is_slash:
            await ctx_or_interaction.response.send_message(embed=embed)
        else:
            await ctx_or_interaction.send(embed=embed)
        return
    
    deck = [(v, s) for s in ["♠", "♥", "♦", "♣"] for v in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]]
    random.shuffle(deck)
    
    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]
    
    view = BlackjackView(user.id, bet, player_hand, dealer_hand)
    view.deck = deck
    
    embed = view.create_embed()
    
    if is_slash:
        await ctx_or_interaction.response.send_message(embed=embed, view=view)
    else:
        await ctx_or_interaction.send(embed=embed, view=view)

@bot.tree.command(name="blackjack", description="Play a game of blackjack")
@app_commands.describe(bet="Amount to bet")
async def blackjack_slash(interaction: discord.Interaction, bet: int):
    async with get_command_lock("blackjack"):
        await blackjack_handler(interaction, bet)

@bot.command(name="blackjack", aliases=["bj", "21"])
async def blackjack_prefix(ctx, bet: int = None):
    async with get_command_lock("blackjack"):
        await blackjack_handler(ctx, bet)

# ══════════════════════════════════════════════════════════════════[...]
# CRASH GAME
# ══════════════════════════════════════════════════════════════════[...]

class CrashView(discord.ui.View):
    def __init__(self, user_id: int, bet: int):
        super().__init__(timeout=30)
        self.user_id = user_id
        self.bet = bet
        self.multiplier = 1.0
        self.crashed = False
        self.cashed_out = False
        self.crash_point = self.generate_crash_point()
        self.session_id = str(uuid.uuid4())[:8]
        self.cashout_lock = asyncio.Lock()
        
    def generate_crash_point(self):
        r = random.random()
        return max(1.0, (1 / (1 - r)) * 0.97)
    
    @discord.ui.button(label="CASH OUT", style=discord.ButtonStyle.success, emoji="💰")
    async def cash_out(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This isn't your game!", ephemeral=True)
            return
        
        async with self.cashout_lock:
            if self.crashed or self.cashed_out:
                try:
                    await interaction.response.defer()
                except:
                    pass
                return
            
            self.cashed_out = True
        winnings = int(self.bet * self.multiplier)
        profit = winnings - self.bet
        
        user_data = get_user_economy(self.user_id)
        user_data["wallet"] += profit
        user_data["total_earned"] += profit
        update_user_economy(self.user_id, user_data)
        
        embed = create_hologram_embed(
            title=f"{Emojis.TROPHY} CASHED OUT!",
            description=f"Multiplier: **{self.multiplier:.2f}x**\nWinnings: {format_currency(winnings)}\nProfit: {format_currency(profit)}",
            color=Colors.SUCCESS
        )
        
        button.disabled = True
        await interaction.response.edit_message(embed=embed, view=self)
        self.stop()

async def crash_handler(ctx_or_interaction, bet: int = None):
    """Unified crash game handler"""
    is_slash = isinstance(ctx_or_interaction, discord.Interaction)
    user = ctx_or_interaction.user if is_slash else ctx_or_interaction.author
    user_data = get_user_economy(user.id)
    
    if bet is None or bet <= 0:
        embed = create_glass_embed(
            title=f"{Emojis.FIRE} CRASH",
            description="Usage: `crash <bet>`\nCash out before it crashes!",
            color=Colors.INFO
        )
        if is_slash:
            await ctx_or_interaction.response.send_message(embed=embed)
        else:
            await ctx_or_interaction.send(embed=embed)
        return
    
    if bet > user_data["wallet"]:
        embed = create_glass_embed(
            title=f"{Emojis.CROSS} INSUFFICIENT FUNDS",
            description=f"You need {format_currency(bet)} to play!",
            color=Colors.ERROR
        )
        if is_slash:
            await ctx_or_interaction.response.send_message(embed=embed)
        else:
            await ctx_or_interaction.send(embed=embed)
        return
    
    view = CrashView(user.id, bet)
    
    embed = create_hologram_embed(
        title=f"{Emojis.FIRE} CRASH STARTING...",
        description=f"Bet: {format_currency(bet)}\nMultiplier: **1.00x**",
        color=Colors.NEON_PURPLE
    )
    
    if is_slash:
        await ctx_or_interaction.response.send_message(embed=embed, view=view)
        message = await ctx_or_interaction.original_response()
    else:
        message = await ctx_or_interaction.send(embed=embed, view=view)
    
    while not view.crashed and not view.cashed_out:
        await asyncio.sleep(0.5)
        view.multiplier += random.uniform(0.05, 0.15)
        
        if view.multiplier >= view.crash_point:
            view.crashed = True
            user_data["wallet"] -= bet
            user_data["total_lost"] += bet
            update_user_economy(user.id, user_data)
            
            embed = create_hologram_embed(
                title=f"{Emojis.CROSS} CRASHED!",
                description=f"Crashed at **{view.crash_point:.2f}x**\nYou lost {format_currency(bet)}!",
                color=Colors.ERROR
            )
            
            view.children[0].disabled = True
            await message.edit(embed=embed, view=view)
            view.stop()
            break
        
        if not view.cashed_out:
            embed = create_hologram_embed(
                title=f"{Emojis.FIRE} CRASH",
                description=f"Bet: {format_currency(bet)}\nMultiplier: **{view.multiplier:.2f}x**\n\nPotential Win: {format_currency(int(bet * view.multiplier))}",
                color=Colors.NEON_PURPLE
            )
            try:
                await message.edit(embed=embed, view=view)
            except:
                break

@bot.tree.command(name="crash", description="Play the crash game - cash out before it crashes!")
@app_commands.describe(bet="Amount to bet")
async def crash_slash(interaction: discord.Interaction, bet: int):
    async with get_command_lock("crash"):
        await crash_handler(interaction, bet)

@bot.command(name="crash")
async def crash_prefix(ctx, bet: int = None):
    async with get_command_lock("crash"):
        await crash_handler(ctx, bet)

# ══════════════════════════════════════════════════════════════════[...]
# FUN GAMES
# ══════════════════════════════════════════════════════════════════[...]

# TRIVIA
trivia_questions = [
    {"question": "What is the capital of France?", "answer": "paris", "options": ["London", "Paris", "Berlin", "Madrid"]},
    {"question": "How many planets are in our solar system?", "answer": "8", "options": ["7", "8", "9", "10"]},
    {"question": "What year did World War II end?", "answer": "1945", "options": ["1943", "1944", "1945", "1946"]},
    {"question": "What is the largest mammal?", "answer": "blue whale", "options": ["Elephant", "Blue Whale", "Giraffe", "Hippopotamus"]},
    {"question": "What is the chemical symbol for gold?", "answer": "au", "options": ["Ag", "Au", "Fe", "Cu"]}
]

async def trivia_handler(ctx_or_interaction):
    """Unified trivia handler"""
    is_slash = isinstance(ctx_or_interaction, discord.Interaction)
    user = ctx_or_interaction.user if is_slash else ctx_or_interaction.author
    
    question = random.choice(trivia_questions)
    options = question["options"].copy()
    random.shuffle(options)
    
    options_text = "\n".join([f"**{i+1}.** {opt}" for i, opt in enumerate(options)])
    
    embed = create_glass_embed(
        title=f"{Emojis.SPARKLE} TRIVIA TIME!",
        description=f"**{question['question']}**\n\n{options_text}",
        color=Colors.INFO
    )
    embed.set_footer(text="Reply with the number of your answer! (30 seconds)")
    
    if is_slash:
        await ctx_or_interaction.response.send_message(embed=embed)
        message = await ctx_or_interaction.original_response()
    else:
        message = await ctx_or_interaction.send(embed=embed)
    
    def check(m):
        return m.author.id == user.id and m.channel.id == message.channel.id
    
    try:
        response = await bot.wait_for("message", check=check, timeout=30)
        try:
            choice_idx = int(response.content) - 1
            if 0 <= choice_idx < len(options):
                chosen = options[choice_idx].lower()
                if chosen == question["answer"] or question["answer"] in chosen.lower():
                    reward = random.randint(50, 150)
                    user_data = get_user_economy(user.id)
                    user_data["wallet"] += reward
                    user_data["total_earned"] += reward
                    update_user_economy(user.id, user_data)
                    
                    embed = create_glass_embed(
                        title=f"{Emojis.CHECK} CORRECT!",
                        description=f"You earned {format_currency(reward)}!",
                        color=Colors.SUCCESS
                    )
                else:
                    embed = create_glass_embed(
                        title=f"{Emojis.CROSS} INCORRECT!",
                        description=f"The correct answer was: **{question['options'][question['options'].index([o for o in question['options'] if question['answer'] in o.lower()][0])]}**",
                        color=Colors.ERROR
                    )
            else:
                embed = create_glass_embed(
                    title=f"{Emojis.CROSS} INVALID CHOICE",
                    description="Please choose a number from the options!",
                    color=Colors.ERROR
                )
        except ValueError:
            embed = create_glass_embed(
                title=f"{Emojis.CROSS} INVALID INPUT",
                description="Please reply with a number!",
                color=Colors.ERROR
            )
        
        await message.channel.send(embed=embed)
    except asyncio.TimeoutError:
        embed = create_glass_embed(
            title=f"{Emojis.CLOCK} TIME'S UP!",
            description="You didn't answer in time!",
            color=Colors.WARNING
        )
        await message.channel.send(embed=embed)

@bot.tree.command(name="trivia", description="Play a trivia game")
async def trivia_slash(interaction: discord.Interaction):
    async with get_command_lock("trivia"):
        await trivia_handler(interaction)

@bot.command(name="trivia")
async def trivia_prefix(ctx):
    async with get_command_lock("trivia"):
        await trivia_handler(ctx)

# RPS (Rock Paper Scissors)
async def rps_handler(ctx_or_interaction, choice: str = None):
    """Unified RPS handler"""
    is_slash = isinstance(ctx_or_interaction, discord.Interaction)
    user = ctx_or_interaction.user if is_slash else ctx_or_interaction.author
    
    choices = {"rock": "🪨", "paper": "📄", "scissors": "✂️"}
    
    if not choice or choice.lower() not in choices:
        embed = create_glass_embed(
            title=f"{Emojis.DICE} ROCK PAPER SCISSORS",
            description="Usage: `rps <rock/paper/scissors>`",
            color=Colors.INFO
        )
        if is_slash:
            await ctx_or_interaction.response.send_message(embed=embed)
        else:
            await ctx_or_interaction.send(embed=embed)
        return
    
    player_choice = choice.lower()
    bot_choice = random.choice(list(choices.keys()))
    
    wins = {"rock": "scissors", "paper": "rock", "scissors": "paper"}
    
    if player_choice == bot_choice:
        result = "TIE"
        color = Colors.WARNING
        reward = 0
    elif wins[player_choice] == bot_choice:
        result = "YOU WIN!"
        color = Colors.SUCCESS
        reward = random.randint(25, 75)
    else:
        result = "YOU LOSE!"
        color = Colors.ERROR
        reward = 0
    
    if reward > 0:
        user_data = get_user_economy(user.id)
        user_data["wallet"] += reward
        user_data["total_earned"] += reward
        update_user_economy(user.id, user_data)
    
    embed = create_glass_embed(
        title=f"{Emojis.DICE} {result}",
        description=f"You: {choices[player_choice]} **{player_choice.upper()}**\nBot: {choices[bot_choice]} **{bot_choice.upper()}**" + 
                    (f"\n\nYou earned {format_currency(reward)}!" if reward > 0 else ""),
        color=color
    )
    
    if is_slash:
        await ctx_or_interaction.response.send_message(embed=embed)
    else:
        await ctx_or_interaction.send(embed=embed)

@bot.tree.command(name="rps", description="Play Rock Paper Scissors")
@app_commands.describe(choice="rock, paper, or scissors")
@app_commands.choices(choice=[
    app_commands.Choice(name="Rock", value="rock"),
    app_commands.Choice(name="Paper", value="paper"),
    app_commands.Choice(name="Scissors", value="scissors")
])
async def rps_slash(interaction: discord.Interaction, choice: str):
    async with get_command_lock("rps"):
        await rps_handler(interaction, choice)

@bot.command(name="rps")
async def rps_prefix(ctx, choice: str = None):
    async with get_command_lock("rps"):
        await rps_handler(ctx, choice)

# Number Guess
async def guess_handler(ctx_or_interaction):
    """Unified number guess handler"""
    is_slash = isinstance(ctx_or_interaction, discord.Interaction)
    user = ctx_or_interaction.user if is_slash else ctx_or_interaction.author
    channel = ctx_or_interaction.channel
    
    target = random.randint(1, 100)
    attempts = 5
    
    embed = create_glass_embed(
        title=f"{Emojis.SPARKLE} NUMBER GUESS",
        description=f"I'm thinking of a number between **1** and **100**.\nYou have **{attempts}** attempts!",
        color=Colors.INFO
    )
    
    if is_slash:
        await ctx_or_interaction.response.send_message(embed=embed)
    else:
        await ctx_or_interaction.send(embed=embed)
    
    def check(m):
        return m.author.id == user.id and m.channel.id == channel.id and m.content.isdigit()
    
    for i in range(attempts):
        try:
            response = await bot.wait_for("message", check=check, timeout=30)
            guess = int(response.content)
            
            if guess == target:
                reward = (attempts - i) * 50
                user_data = get_user_economy(user.id)
                user_data["wallet"] += reward
                user_data["total_earned"] += reward
                update_user_economy(user.id, user_data)
                
                embed = create_glass_embed(
                    title=f"{Emojis.TROPHY} CORRECT!",
                    description=f"The number was **{target}**!\nYou guessed it in **{i + 1}** attempts!\n\nReward: {format_currency(reward)}",
                    color=Colors.SUCCESS
                )
                await channel.send(embed=embed)
                return
            elif guess < target:
                hint = "📈 **Higher!**"
            else:
                hint = "📉 **Lower!**"
            
            remaining = attempts - i - 1
            if remaining > 0:
                embed = create_glass_embed(
                    title=f"{Emojis.SPARKLE} NUMBER GUESS",
                    description=f"{hint}\n\nAttempts remaining: **{remaining}**",
                    color=Colors.WARNING
                )
                await channel.send(embed=embed)
        except asyncio.TimeoutError:
            embed = create_glass_embed(
                title=f"{Emojis.CLOCK} TIME'S UP!",
                description=f"The number was **{target}**!",
                color=Colors.ERROR
            )
            await channel.send(embed=embed)
            return
    
    embed = create_glass_embed(
        title=f"{Emojis.CROSS} GAME OVER!",
        description=f"The number was **{target}**!",
        color=Colors.ERROR
    )
    await channel.send(embed=embed)

@bot.tree.command(name="guess", description="Guess the number between 1-100")
async def guess_slash(interaction: discord.Interaction):
    async with get_command_lock("guess"):
        await guess_handler(interaction)

@bot.command(name="guess", aliases=["numguess"])
async def guess_prefix(ctx):
    async with get_command_lock("guess"):
        await guess_handler(ctx)

# Hangman
hangman_words = ["python", "discord", "aurora", "elura", "gaming", "developer", "community", "server", "moderator", "premium"]

async def hangman_handler(ctx_or_interaction):
    """Unified hangman handler"""
    is_slash = isinstance(ctx_or_interaction, discord.Interaction)
    user = ctx_or_interaction.user if is_slash else ctx_or_interaction.author
    channel = ctx_or_interaction.channel
    
    word = random.choice(hangman_words)
    guessed = set()
    max_wrong = 6
    wrong = 0
    
    def get_display():
        return " ".join([c if c in guessed else "_" for c in word])
    
    def get_hangman():
        stages = [
            "```\n  +---+\n      |\n      |\n      |\n     ===\n```",
            "```\n  +---+\n  O   |\n      |\n      |\n     ===\n```",
            "```\n  +---+\n  O   |\n  |   |\n      |\n     ===\n```",
            "```\n  +---+\n  O   |\n /|   |\n      |\n     ===\n```",
            "```\n  +---+\n  O   |\n /|\\  |\n      |\n     ===\n```",
            "```\n  +---+\n  O   |\n /|\\  |\n /    |\n     ===\n```",
            "```\n  +---+\n  O   |\n /|\\  |\n / \\  |\n     ===\n```"
        ]
        return stages[wrong]
    
    embed = create_glass_embed(
        title=f"{Emojis.SPARKLE} HANGMAN",
        description=f"{get_hangman()}\n\n**Word:** `{get_display()}`\n**Wrong guesses:** {wrong}/{max_wrong}\n**Guessed:** {', '.join(sorted(guessed)) or 'None'}",
        color=Colors.INFO
    )
    
    if is_slash:
        await ctx_or_interaction.response.send_message(embed=embed)
    else:
        await ctx_or_interaction.send(embed=embed)
    
    def check(m):
        return m.author.id == user.id and m.channel.id == channel.id and len(m.content) == 1 and m.content.isalpha()
    
    while wrong < max_wrong:
        try:
            response = await bot.wait_for("message", check=check, timeout=60)
            letter = response.content.lower()
            
            if letter in guessed:
                continue
            
            guessed.add(letter)
            
            if letter not in word:
                wrong += 1
            
            display = get_display()
            
            if "_" not in display:
                reward = (max_wrong - wrong) * 30 + 50
                user_data = get_user_economy(user.id)
                user_data["wallet"] += reward
                user_data["total_earned"] += reward
                update_user_economy(user.id, user_data)
                
                embed = create_glass_embed(
                    title=f"{Emojis.TROPHY} YOU WIN!",
                    description=f"The word was **{word}**!\n\nReward: {format_currency(reward)}",
                    color=Colors.SUCCESS
                )
                await channel.send(embed=embed)
                return
            
            if wrong >= max_wrong:
                break
            
            embed = create_glass_embed(
                title=f"{Emojis.SPARKLE} HANGMAN",
                description=f"{get_hangman()}\n\n**Word:** `{display}`\n**Wrong guesses:** {wrong}/{max_wrong}\n**Guessed:** {', '.join(sorted(guessed))}",
                color=Colors.WARNING if wrong >= 4 else Colors.INFO
            )
            await channel.send(embed=embed)
            
        except asyncio.TimeoutError:
            embed = create_glass_embed(
                title=f"{Emojis.CLOCK} TIME'S UP!",
                description=f"The word was **{word}**!",
                color=Colors.ERROR
            )
            await channel.send(embed=embed)
            return
    
    embed = create_glass_embed(
        title=f"{Emojis.CROSS} GAME OVER!",
        description=f"{get_hangman()}\n\nThe word was **{word}**!",
        color=Colors.ERROR
    )
    await channel.send(embed=embed)

@bot.tree.command(name="hangman", description="Play hangman")
async def hangman_slash(interaction: discord.Interaction):
    async with get_command_lock("hangman"):
        await hangman_handler(interaction)

@bot.command(name="hangman")
async def hangman_prefix(ctx):
    async with get_command_lock("hangman"):
        await hangman_handler(ctx)
# ─────────────────────────────────────────────────────────────
# Elura GTW & GYI Discord Game Bot
# ─────────────────────────────────────────────────────────────
import discord
from discord.ext import commands, tasks
from discord import app_commands
import asyncio
import random
import time
from typing import List, Dict

# ------------------------- Helper Functions -------------------------
def load_json(file_path: str):
    """Load a JSON file and return its contents."""
    import json
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(file_path: str, data: dict):
    """Save a Python dict to a JSON file."""
    import json
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def create_embed(title: str, description: str, color: int = 0x3498DB):
    """Create a discord.Embed with default style."""
    return discord.Embed(title=title, description=description, color=color)

def progress_bar(current: int, total: int, length: int = 20):
    """Return a text-based progress bar."""
    filled = int(current / total * length)
    return "▓" * filled + "░" * (length - filled)

def get_bot_user(bot: commands.Bot, user_id: int):
    """Helper to fetch bot user object from ID."""
    return bot.get_user(user_id)

# ------------------------- Shared Game Manager -------------------------
class GameManager:
    """Unified manager for GTW and GYI games with shared logic."""
    def __init__(self, bot: commands.Bot, game_type: str):
        """
        :param bot: discord.Bot or commands.Bot instance
        :param game_type: 'GTW' or 'GYI'
        """
        self.bot = bot
        self.game_type = game_type
        self.lobbies: Dict[str, dict] = {}  # lobby code -> lobby dict
        self.cooldowns: Dict[int,float] = {}  # user_id -> last lobby create timestamp
        self.config = load_json("config.json").get("gtw", {})  # shared settings
        self.cleanup_task.start()

    # ----------------- Word Handling -----------------
    def load_words(self) -> list:
        """Load words from respective JSON based on game type."""
        if self.game_type == "GTW":
            return load_json("gtw_words.json").get("prompts", [{"normal":"WORD1","impostor":"WORD2"}])
        else:
            return load_json("gyi_words.json").get("pairs", [{"normal":"WORD1","impostor":"WORD2"}])

    # ----------------- Lobby Creation -----------------
    async def create_lobby(self, host: discord.Member, channel: discord.TextChannel, optional_players: List[discord.Member]=[]):
        """Create a new lobby with optional extra players."""
        now = time.time()
        if host.id in self.cooldowns and now - self.cooldowns[host.id] < self.config.get("cooldown",60):
            return None, f"⏳ You must wait before creating another lobby."

        code = ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=4))
        self.cooldowns[host.id] = now

        players = [host] + optional_players
        self.lobbies[code] = {
            "host": host.id,
            "channel": channel.id,
            "players": [p.id for p in players],
            "started": False,
            "prompts": [],
            "round": 1,
            "max_rounds": self.config.get("max_rounds",3),
            "answers": {},
            "impostors": [],
            "message_id": None,
            "created_at": now
        }
        return code, f"🎮 {self.game_type} Lobby `{code}` created by {host.display_name} with {len(players)} player(s)."

    async def join_lobby(self, user: discord.Member, code: str):
        """Add a user to an existing lobby."""
        lobby = self.lobbies.get(code)
        if not lobby:
            return f"❌ Lobby `{code}` not found."
        if lobby["started"]:
            return f"❌ Lobby `{code}` has already started."
        if user.id in lobby["players"]:
            return f"❌ You are already in this lobby."
        lobby["players"].append(user.id)
        return f"✅ {user.display_name} joined lobby `{code}`!"

    # ----------------- Start Lobby -----------------
    async def start_lobby(self, code: str):
        """Start the game in a lobby, assign impostors, DM words."""
        lobby = self.lobbies.get(code)
        if not lobby or lobby["started"]:
            return False

        channel = self.bot.get_channel(lobby["channel"])
        players = [self.bot.get_user(pid) for pid in lobby["players"]]

        if len(players) < 3:
            await channel.send("⚠️ Need at least 3 players to start!")
            return False

        # ----------------- Impostor Assignment -----------------
        num_players = len(players)
        max_impostors = self.config.get("max_impostors",2)
        impostor_count = min(max(1, num_players//4), max_impostors)
        impostors = random.sample(players, impostor_count)
        lobby["impostors"] = [p.id for p in impostors]

        # ----------------- Word Assignment -----------------
        word_list = self.load_words()
        prompt_pair = random.choice(word_list)
        lobby["prompts"] = [prompt_pair]

        # ----------------- DM Words -----------------
        for p in players:
            try:
                if p.id in lobby["impostors"]:
                    embed = create_embed(f"⚠️ YOU ARE THE IMPOSTOR!", f"Your word: {prompt_pair['impostor']}", 0xE74C3C)
                else:
                    embed = create_embed(f"💡 YOUR WORD", f"Your word: {prompt_pair['normal']}", 0x3498DB)
                await p.send(embed=embed)
            except:
                continue

        lobby["started"] = True
        lobby["round"] = 1
        await self.run_round(code)
        return True

    # ----------------- Run Game Rounds -----------------
    async def run_round(self, code: str):
        """Run all rounds of the game, handle banned words and player messages."""
        lobby = self.lobbies.get(code)
        if not lobby: return
        channel = self.bot.get_channel(lobby["channel"])
        players = [self.bot.get_user(pid) for pid in lobby["players"]]
        prompt_pair = lobby["prompts"][0]

        banned_words = self.config.get("banned_words", ["bad","good","best","worst"])
        round_time = self.config.get("round_time", 90)

        for r in range(lobby["round"], lobby["max_rounds"]+1):
            lobby["round"] = r
            embed = create_embed(f"Round {r}", f"Prompt: {prompt_pair['normal']}", 0x8E44AD)
            msg = await channel.send(embed=embed)
            lobby["answers"][r] = {}

            def check(m):
                return m.reference and m.reference.message_id==msg.id and m.author.id in lobby["players"] \
                       and 1<=len(m.content.split())<=2 and not any(bw in m.content.lower() for bw in banned_words)

            round_end = time.time() + round_time
            while time.time() < round_end:
                try:
                    m = await self.bot.wait_for("message", check=check, timeout=10)
                    lobby["answers"][r][m.author.id] = m.content.strip()
                except asyncio.TimeoutError:
                    continue

        await self.continue_or_vote(lobby)

    # ----------------- Continue or Vote -----------------
    async def continue_or_vote(self, lobby):
        channel = self.bot.get_channel(lobby["channel"])
        players = [self.bot.get_user(pid) for pid in lobby["players"]]

        view = ContinueOrVoteView(players)
        embed = create_embed("⚡ Continue or Vote?", "Majority decides: continue game or vote impostor.", 0xF1C40F)
        await channel.send(embed=embed, view=view)
        await view.wait()

        continue_count = list(view.choices.values()).count("continue")
        vote_count = list(view.choices.values()).count("vote")

        if continue_count >= vote_count:
            await channel.send("✅ Majority chose **Continue**! Starting next round...")
            lobby["round"] += 1
            await self.run_round(lobby_code_from_lobby(lobby))
        else:
            await self.voting_phase(lobby)

    # ----------------- Voting Phase -----------------
    async def voting_phase(self, lobby):
        channel = self.bot.get_channel(lobby["channel"])
        players = [self.bot.get_user(pid) for pid in lobby["players"]]

        view = GTWVotingView(players)
        embed = create_embed("🗳️ Voting Phase", "Vote for who you think is the impostor!", 0x1ABC9C)
        await channel.send(embed=embed, view=view)
        await view.wait()

        if view.votes:
            max_votes = max(view.votes.values())
            candidates = [pid for pid,count in view.votes.items() if count==max_votes]

            if len(candidates) > 1:
                await channel.send("Tie detected! Tie-breaker via RPS.")
                loser = await self.rps(channel, candidates)
            else:
                loser = candidates[0]

            if loser in lobby["impostors"]:
                await channel.send(f"🎉 The impostor <@{loser}> was caught!")
            else:
                await channel.send(f"❌ <@{loser}> was eliminated but was not an impostor!")

    # ----------------- RPS Tie-breaker -----------------
    async def rps(self, channel, candidates):
        moves = {"✊":"rock","✋":"paper","✌️":"scissors"}
        player_moves = {}
        def check(reaction, user):
            return user.id in candidates and str(reaction.emoji) in moves
        await channel.send(f"Tie between: {', '.join([f'<@{c}>' for c in candidates])}. React with ✊, ✋, ✌️.")
        while len(player_moves)<len(candidates):
            try:
                reaction,user = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)
                if user.id not in player_moves:
                    player_moves[user.id] = moves[str(reaction.emoji)]
                    await channel.send(f"<@{user.id}> chose {moves[str(reaction.emoji)]}")
            except asyncio.TimeoutError:
                break
        if len(player_moves)<len(candidates):
            return random.choice(candidates)
        ids=list(player_moves.keys())
        m1,m2=player_moves[ids[0]],player_moves[ids[1]]
        if m1==m2:
            return random.choice(ids)
        elif (m1,m2) in [("rock","scissors"),("paper","rock"),("scissors","paper")]:
            return ids[1]
        else:
            return ids[0]

    # ----------------- Auto Cleanup -----------------
    @tasks.loop(seconds=60)
    async def cleanup_task(self):
        now = time.time()
        expired=[]
        for code,lobby in self.lobbies.items():
            if not lobby["started"] and now-lobby["created_at"]>self.config.get("lobby_timeout",600):
                expired.append(code)
                channel=self.bot.get_channel(lobby["channel"])
                host=self.bot.get_user(lobby["host"])
                if channel:
                    await channel.send(f"⌛ Lobby `{code}` created by {host.display_name} expired due to inactivity.")
        for code in expired:
            del self.lobbies[code]

# ------------------------- UI Components -------------------------
class ContinueOrVoteView(discord.ui.View):
    """Interactive view for Continue or Vote buttons."""
    def __init__(self, players):
        super().__init__(timeout=60)
        self.choices: Dict[int,str] = {}
        for pid in players:
            continue_btn=discord.ui.Button(label="Continue",style=discord.ButtonStyle.success)
            vote_btn=discord.ui.Button(label="Vote",style=discord.ButtonStyle.danger)
            continue_btn.callback=self.make_callback(pid,"continue")
            vote_btn.callback=self.make_callback(pid,"vote")
            self.add_item(continue_btn)
            self.add_item(vote_btn)
    def make_callback(self,pid,choice):
        async def callback(interaction:discord.Interaction):
            if interaction.user.id!=pid:
                await interaction.response.send_message("This button is not for you.",ephemeral=True)
                return
            self.choices[pid]=choice
            await interaction.response.send_message(f"You chose **{choice}**!",ephemeral=True)
            if len(self.choices)>=len(self.children)//2:
                self.stop()
        return callback

class GTWVotingView(discord.ui.View):
    """Voting view for choosing impostor."""
    def __init__(self, players):
        super().__init__(timeout=60)
        self.votes: Dict[int,int]={}
        self.voted_users:set=set()
        for p in players:
            btn=discord.ui.Button(label=p.display_name[:20],style=discord.ButtonStyle.secondary)
            btn.callback=self.make_callback(p.id)
            self.add_item(btn)
    def make_callback(self,target_id):
        async def callback(interaction:discord.Interaction):
            if interaction.user.id in self.voted_users:
                await interaction.response.send_message("Already voted!",ephemeral=True)
                return
            self.voted_users.add(interaction.user.id)
            self.votes[target_id]=self.votes.get(target_id,0)+1
            await interaction.response.send_message(f"You voted for <@{target_id}>!",ephemeral=True)
            if len(self.voted_users)>=len(self.children):
                self.stop()
        return callback

# ------------------------- Bot Setup -------------------------
prefixes = ["eu","elura"]
bot = commands.Bot(command_prefix=prefixes,intents=discord.Intents.all())
try:
    bot.remove_command("help")
except Exception:
    pass
gtw_manager: GameManager = None
gyi_manager: GameManager = None

@bot.event
async def on_ready():
    global gtw_manager, gyi_manager
    gtw_manager = GameManager(bot, "GTW")
    gyi_manager = GameManager(bot, "GYI")
    print(f"{bot.user} is online!")

# ------------------------- Slash Commands -------------------------
# Assuming 'List' is imported from 'typing' or Python 3.9+ 'list' is used.
# Since the problematic type is removed, the import is no longer strictly needed for this file.

@bot.tree.command(name="gtw_create", description="Create a GTW lobby")
@app_commands.describe(
    optional_players="Optional extra players User IDs, separated by spaces (e.g., 12345 67890)"
)
async def gtw_create(interaction: discord.Interaction, optional_players: str = ""):
    # NOTE: You will need to modify the gtw_manager.create_lobby function
    # to handle the 'optional_players' parameter as a string of IDs, 
    # split it, and fetch the Member objects.
    code, msg = await gtw_manager.create_lobby(interaction.user, interaction.channel, optional_players)
    await interaction.response.send_message(msg)

@bot.tree.command(name="gyi_create", description="Create a GYI lobby")
@app_commands.describe(
    optional_players="Optional extra players User IDs, separated by spaces (e.g., 12345 67890)"
)
async def gyi_create(interaction: discord.Interaction, optional_players: str = ""):
    # NOTE: You will need to modify the gyi_manager.create_lobby function
    # to handle the 'optional_players' parameter as a string of IDs, 
    # split it, and fetch the Member objects.
    code, msg = await gyi_manager.create_lobby(interaction.user, interaction.channel, optional_players)
    await interaction.response.send_message(msg)

@bot.tree.command(name="gtw_join", description="Join a GTW lobby")
@app_commands.describe(code="Lobby code to join")
async def gtw_join(interaction: discord.Interaction, code: str):
    msg = await gtw_manager.join_lobby(interaction.user, code.upper())
    await interaction.response.send_message(msg)

@bot.tree.command(name="gyi_join", description="Join a GYI lobby")
@app_commands.describe(code="Lobby code to join")
async def gyi_join(interaction: discord.Interaction, code: str):
    msg = await gyi_manager.join_lobby(interaction.user, code.upper())
    await interaction.response.send_message(msg)
    
# ------------------------- Prefix Commands -------------------------
@bot.command(name="gtwcreate")
async def gtw_create_prefix(ctx, *optional_players: discord.Member):
    code, msg = await gtw_manager.create_lobby(ctx.author, ctx.channel, list(optional_players))
    await ctx.send(msg)

@bot.command(name="gyicreate")
async def gyi_create_prefix(ctx, *optional_players: discord.Member):
    code, msg = await gyi_manager.create_lobby(ctx.author, ctx.channel, list(optional_players))
    await ctx.send(msg)

@bot.command(name="gtwjoin")
async def gtw_join_prefix(ctx, code: str):
    msg = await gtw_manager.join_lobby(ctx.author, code.upper())
    await ctx.send(msg)

@bot.command(name="gyijoin")
async def gyi_join_prefix(ctx, code: str):
    msg = await gyi_manager.join_lobby(ctx.author, code.upper())
    await ctx.send(msg)

# ------------------------- Helper -------------------------
def lobby_code_from_lobby(lobby: dict):
    """Get the code of a lobby from lobby dict."""
    for code, l in gtw_manager.lobbies.items():
        if l == lobby: return code
    return None
# ----------------- Helper Functions -----------------
def load_json(file_path):
    import json
    with open(file_path,"r",encoding="utf-8") as f:
        return json.load(f)

def create_embed(title, description, color=0x3498DB):
    return discord.Embed(title=title, description=f"```{description}```", color=color)
    
# ══════════════════════════════════════════════════════════════════[...]
# PUNISHMENT SYSTEM
# ══════════════════════════════════════════════════════════════════[...]

def get_user_punishment_tier(member: discord.Member) -> int:
    """Get the highest punishment tier a user has"""
    roles = load_json("roles.json")
    member_role_ids = [str(r.id) for r in member.roles]
    
    for tier in range(5, 0, -1):
        tier_key = f"tier{tier}"
        if tier_key in roles["punishment_tiers"]:
            for role_id in roles["punishment_tiers"][tier_key]:
                if role_id in member_role_ids:
                    return tier
    return 0

def can_moderate(moderator: discord.Member, target: discord.Member, required_tier: int) -> bool:
    """Check if moderator can take action against target"""
    mod_tier = get_user_punishment_tier(moderator)
    target_tier = get_user_punishment_tier(target)
    
    if mod_tier < required_tier:
        return False
    if target_tier >= mod_tier:
        return False
    return True

def get_user_punishment_tier(member: discord.Member) -> int:
    """Get the highest punishment tier a user has"""
    roles = load_json("roles.json")
    member_role_ids = [str(r.id) for r in member.roles]
    
    for tier in range(5, 0, -1):
        tier_key = f"tier{tier}"
        if tier_key in roles["punishment_tiers"]:
            for role_id in roles["punishment_tiers"][tier_key]:
                if role_id in member_role_ids:
                    return tier
    return 0

def can_moderate(moderator: discord.Member, target: discord.Member, required_tier: int) -> bool:
    """Check if moderator can take action against target"""
    mod_tier = get_user_punishment_tier(moderator)
    target_tier = get_user_punishment_tier(target)
    
    if mod_tier < required_tier:
        return False
    if target_tier >= mod_tier:
        return False
    return True

async def create_case(guild_id: int, mod_id: int, target_id: int, action: str, reason: str) -> int:
    """Create a new punishment case"""
    punishments = load_json("punishments.json")
    punishments["case_counter"] += 1
    case_id = punishments["case_counter"]
    
    case = {
        "id": case_id,
        "guild_id": guild_id,
        "moderator_id": mod_id,
        "target_id": target_id,
        "action": action,
        "reason": reason,
        "timestamp": datetime.utcnow().isoformat(),
        "active": True
    }
    
    punishments["cases"].append(case)
    save_json("punishments.json", punishments)
    
    return case_id

async def punishment_handler(ctx_or_interaction, action: str, target: discord.Member = None, reason: str = "No reason provided", duration: int = None):
    """Unified punishment handler"""
    is_slash = isinstance(ctx_or_interaction, discord.Interaction)
    user = ctx_or_interaction.user if is_slash else ctx_or_interaction.author
    guild = ctx_or_interaction.guild
    
    tier_requirements = {
        "warn": 1,
        "unwarn": 1,
        "mute": 2,
        "unmute": 2,
        "kick": 3,
        "softban": 4,
        "ban": 4,
        "unban": 4
    }
    
    required_tier = tier_requirements.get(action, 5)
    
    # --- Validation ---
    if action not in ["unban"]:
        if target is None:
            embed = create_glass_embed(
                title=f"{Emojis.CROSS} ERROR",
                description="Please specify a target user!",
                color=Colors.ERROR
            )
            if is_slash:
                await ctx_or_interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await ctx_or_interaction.send(embed=embed)
            return
        
        if not can_moderate(user, target, required_tier):
            embed = create_glass_embed(
                title=f"{Emojis.SHIELD} INSUFFICIENT PERMISSIONS",
                description=f"You need **Tier {required_tier}+** permissions to {action} this user!",
                color=Colors.ERROR
            )
            if is_slash:
                await ctx_or_interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await ctx_or_interaction.send(embed=embed)
            return
    
    embed = None

    # --- Make sure target exists for certain actions ---
    if target is None and action in ["warn", "unwarn", "warnings", "mute", "unmute", "kick", "softban", "ban"]:
        embed = discord.Embed(
            title="❌ Error",
            description="Please specify a user to warn/unwarn/check warnings!",
            color=0xFF0000
        )
        if is_slash:
            await ctx_or_interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await ctx_or_interaction.send(embed=embed)
        return

    # --- Action Logic ---
    if action == "warn":
        case_id = await create_case(guild.id, user.id, target.id, "WARN", reason)

        try:
            dm_embed = discord.Embed(
                title="⚠️ You have been warned!",
                description=f"You have received a warning in **{guild.name}**.",
                color=0xFFA500
            )
            dm_embed.add_field(name="Reason", value=reason, inline=False)
            dm_embed.add_field(name="Case ID", value=f"#{case_id}", inline=False)
            dm_embed.set_footer(text="Please adhere to the server rules.")
            await target.send(embed=dm_embed)
        except:
            pass

        embed = discord.Embed(
            title="⚠️ User Warned",
            description=f"{target.mention} has been warned.",
            color=0xFFA500
        )
        embed.add_field(name="Moderator", value=user.mention, inline=True)
        embed.add_field(name="Reason", value=reason, inline=True)
        embed.add_field(name="Case ID", value=f"#{case_id}", inline=True)

    elif action == "unwarn":
        punishments = load_json("punishments.json")

        user_warnings = [
            c for c in punishments["cases"]
            if c["target_id"] == target.id and c["action"] == "WARN" and c["active"]
        ]

        if not user_warnings:
            embed = discord.Embed(
                title="✅ No Active Warnings",
                description=f"{target.mention} has no active warnings.",
                color=0x00FF00
            )

        else:
            if not case_id:
                embed = discord.Embed(
                    title="❌ Case ID Required",
                    description=(
                        f"Please specify a Case ID.\n"
                        f"Use `/warnings target:{target.display_name}` to view active warnings."
                    ),
                    color=0xFF0000
                )

            else:
                warning_to_remove = next(
                    (c for c in user_warnings if c["id"] == case_id),
                    None
                )

                if not warning_to_remove:
                    embed = discord.Embed(
                        title="❌ Warning Not Found",
                        description=f"No active warning found with Case ID #{case_id}.",
                        color=0xFF0000
                    )

                else:
                    for case in punishments["cases"]:
                        if case["id"] == warning_to_remove["id"]:
                            case["active"] = False
                            break

                    save_json("punishments.json", punishments)

                    embed = discord.Embed(
                        title="✅ Warning Removed",
                        description=f"Removed warning #{warning_to_remove['id']} from {target.mention}.",
                        color=0x00FF00
    )            
    elif action == "warnings":
        punishments = load_json("punishments.json")
        user_warnings = [c for c in punishments["cases"] if c["target_id"] == target.id and c["action"] == "WARN" and c["active"]]
        if not user_warnings:
            embed = discord.Embed(
                title="✅ No Active Warnings",
                description=f"{target.mention} has no active warnings.",
                color=0x00FF00
            )
        else:
            embed = discord.Embed(
                title=f"⚠️ Warnings ({len(user_warnings)})",
                description=f"Active warnings for {target.mention}:",
                color=0xFFA500
            )
            for w in user_warnings:
                embed.add_field(name=f"Case #{w['id']}", value=w['reason'], inline=False)

    elif action == "mute":
        timeout_duration = timedelta(minutes=duration or 10)
        try:
            await target.timeout(timeout_duration, reason=reason)
            case_id = await create_case(guild.id, user.id, target.id, "MUTE", reason)
            try:
                dm_embed = create_glass_embed(
                    title=f"{Emojis.CROSS} MUTED",
                    description=f"You have been muted in **{guild.name}**\n\n**Duration:** {duration or 10} minutes\n**Reason:** {reason}\n**Case ID:** #{case_id}",
                    color=Colors.ERROR
                )
                await target.send(embed=dm_embed)
            except:
                pass
            embed = create_neon_embed(
                title=f"{Emojis.CROSS} USER MUTED",
                description=f"**Target:** {target.mention}\n**Duration:** {duration or 10} minutes\n**Moderator:** {user.mention}\n**Reason:** {reason}\n**Case ID:** #{case_id}",
                color=Colors.ERROR
            )
        except discord.Forbidden:
            embed = create_glass_embed(
                title=f"{Emojis.CROSS} FAILED",
                description="I don't have permission to mute this user!",
                color=Colors.ERROR
            )

    elif action == "unmute":
        try:
            await target.timeout(None, reason=f"Unmuted by {user}")
            embed = create_neon_embed(
                title=f"{Emojis.CHECK} USER UNMUTED",
                description=f"**Target:** {target.mention}\n**Moderator:** {user.mention}",
                color=Colors.SUCCESS
            )
        except discord.Forbidden:
            embed = create_glass_embed(
                title=f"{Emojis.CROSS} FAILED",
                description="I don't have permission to unmute this user!",
                color=Colors.ERROR
            )

    elif action == "kick":
        try:
            case_id = await create_case(guild.id, user.id, target.id, "KICK", reason)
            try:
                dm_embed = create_glass_embed(
                    title=f"{Emojis.SWORD} KICKED",
                    description=f"You have been kicked from **{guild.name}**\n\n**Reason:** {reason}\n**Case ID:** #{case_id}",
                    color=Colors.ERROR
                )
                await target.send(embed=dm_embed)
            except:
                pass
            await target.kick(reason=reason)
            embed = create_neon_embed(
                title=f"{Emojis.SWORD} USER KICKED",
                description=f"**Target:** {target.mention} ({target.id})\n**Moderator:** {user.mention}\n**Reason:** {reason}\n**Case ID:** #{case_id}",
                color=Colors.ERROR
            )
        except discord.Forbidden:
            embed = create_glass_embed(
                title=f"{Emojis.CROSS} FAILED",
                description="I don't have permission to kick this user!",
                color=Colors.ERROR
            )

    elif action == "ban":
        try:
            case_id = await create_case(guild.id, user.id, target.id, "BAN", reason)
            try:
                dm_embed = create_glass_embed(
                    title=f"{Emojis.GAVEL} BANNED",
                    description=f"You have been banned from **{guild.name}**\n\n**Reason:** {reason}\n**Case ID:** #{case_id}",
                    color=Colors.ERROR
                )
                await target.send(embed=dm_embed)
            except:
                pass
            await target.ban(reason=reason, delete_message_days=0)
            embed = create_neon_embed(
                title=f"{Emojis.GAVEL} USER BANNED",
                description=f"**Target:** {target.mention} ({target.id})\n**Moderator:** {user.mention}\n**Reason:** {reason}\n**Case ID:** #{case_id}",
                color=Colors.ERROR
            )
        except discord.Forbidden:
            embed = create_glass_embed(
                title=f"{Emojis.CROSS} FAILED",
                description="I don't have permission to ban this user!",
                color=Colors.ERROR
            )

    elif action == "softban":
        try:
            case_id = await create_case(guild.id, user.id, target.id, "SOFTBAN", reason)
            await target.ban(reason=f"Softban: {reason}", delete_message_days=7)
            await guild.unban(target, reason="Softban unban")
            embed = create_neon_embed(
                title=f"{Emojis.GAVEL} USER SOFTBANNED",
                description=f"**Target:** {target.mention} ({target.id})\n**Moderator:** {user.mention}\n**Reason:** {reason}\n**Case ID:** #{case_id}\n\n*User's messages deleted, user can rejoin.*",
                color=Colors.WARNING
            )
        except discord.Forbidden:
            embed = create_glass_embed(
                title=f"{Emojis.CROSS} FAILED",
                description="I don't have permission to softban this user!",
                color=Colors.ERROR
            )

    # --- Send the final embed ---
    if embed:
        if is_slash:
            await ctx_or_interaction.response.send_message(embed=embed)
        else:
            await ctx_or_interaction.send(embed=embed)
            
# Punishment Slash Commands
@bot.tree.command(name="warn", description="Warn a user")
@app_commands.describe(target="User to warn", reason="Reason for warning")
async def warn_slash(interaction: discord.Interaction, target: discord.Member, reason: str = "No reason provided"):
    async with get_command_lock("warn"):
        await punishment_handler(interaction, "warn", target, reason)

@bot.tree.command(name="unwarn", description="Remove a warning from a user")
@app_commands.describe(target="User to unwarn")
async def unwarn_slash(interaction: discord.Interaction, target: discord.Member):
    async with get_command_lock("unwarn"):
        await punishment_handler(interaction, "unwarn", target)

@bot.tree.command(name="warnings", description="View a user's warnings")
@app_commands.describe(target="User to check")
async def warnings_slash(interaction: discord.Interaction, target: discord.Member):
    async with get_command_lock("warnings"):
        await punishment_handler(interaction, "warnings", target)

@bot.tree.command(name="mute", description="Mute a user")
@app_commands.describe(target="User to mute", duration="Duration in minutes", reason="Reason for mute")
async def mute_slash(interaction: discord.Interaction, target: discord.Member, duration: int = 10, reason: str = "No reason provided"):
    async with get_command_lock("mute"):
        await punishment_handler(interaction, "mute", target, reason, duration)

@bot.tree.command(name="unmute", description="Unmute a user")
@app_commands.describe(target="User to unmute")
async def unmute_slash(interaction: discord.Interaction, target: discord.Member):
    async with get_command_lock("unmute"):
        await punishment_handler(interaction, "unmute", target)

@bot.tree.command(name="kick", description="Kick a user")
@app_commands.describe(target="User to kick", reason="Reason for kick")
async def kick_slash(interaction: discord.Interaction, target: discord.Member, reason: str = "No reason provided"):
    async with get_command_lock("kick"):
        await punishment_handler(interaction, "kick", target, reason)

@bot.tree.command(name="ban", description="Ban a user")
@app_commands.describe(target="User to ban", reason="Reason for ban")
async def ban_slash(interaction: discord.Interaction, target: discord.Member, reason: str = "No reason provided"):
    async with get_command_lock("ban"):
        await punishment_handler(interaction, "ban", target, reason)

@bot.tree.command(name="softban", description="Softban a user (ban + unban to delete messages)")
@app_commands.describe(target="User to softban", reason="Reason for softban")
async def softban_slash(interaction: discord.Interaction, target: discord.Member, reason: str = "No reason provided"):
    async with get_command_lock("softban"):
        await punishment_handler(interaction, "softban", target, reason)

@bot.command(name="warn")
async def warn_prefix(ctx, target: discord.Member = None, *, reason: str = "No reason provided"):
    async with get_command_lock("warn"):
        await punishment_handler(ctx, "warn", target, reason)

@bot.command(name="unwarn")
async def unwarn_prefix(ctx, target: discord.Member = None):
    async with get_command_lock("unwarn"):
        await punishment_handler(ctx, "unwarn", target)

@bot.command(name="warnings")
async def warnings_prefix(ctx, target: discord.Member = None):
    async with get_command_lock("warnings"):
        await punishment_handler(ctx, "warnings", target)

@bot.command(name="mute")
async def mute_prefix(ctx, target: discord.Member = None, duration: int = 10, *, reason: str = "No reason provided"):
    async with get_command_lock("mute"):
        await punishment_handler(ctx, "mute", target, reason, duration)

@bot.command(name="unmute")
async def unmute_prefix(ctx, target: discord.Member = None):
    async with get_command_lock("unmute"):
        await punishment_handler(ctx, "unmute", target)

@bot.command(name="kick")
async def kick_prefix(ctx, target: discord.Member = None, *, reason: str = "No reason provided"):
    async with get_command_lock("kick"):
        await punishment_handler(ctx, "kick", target, reason)

@bot.command(name="ban")
async def ban_prefix(ctx, target: discord.Member = None, *, reason: str = "No reason provided"):
    async with get_command_lock("ban"):
        await punishment_handler(ctx, "ban", target, reason)

@bot.command(name="softban")
async def softban_prefix(ctx, target: discord.Member = None, *, reason: str = "No reason provided"):
    async with get_command_lock("softban"):
        await punishment_handler(ctx, "softban", target, reason)
           
# ══════════════════════════════════════════════════════════════════[...]
# TRANSLATE SYSTEM
# ══════════════════════════════════════════════════════════════════[...]

LANGUAGE_FLAGS = {
    "en": "🇬🇧", "es": "🇪🇸", "fr": "🇫🇷", "de": "🇩🇪", "it": "🇮🇹",
    "pt": "🇵🇹", "ru": "🇷🇺", "ja": "🇯🇵", "ko": "🇰🇷", "zh": "🇨🇳",
    "ar": "🇸🇦", "hi": "🇮🇳", "tr": "🇹🇷", "nl": "🇳🇱", "pl": "🇵🇱"
}

async def translate_handler(ctx_or_interaction, text: str = None, target_lang: str = "en"):
    """Unified translate handler"""
    is_slash = isinstance(ctx_or_interaction, discord.Interaction)
    
    if not text:
        embed = create_glass_embed(
            title=f"{Emojis.GLOBE} TRANSLATE",
            description="Usage: `translate <text>` or `translate <text> to <language>`\n\n**Supported Languages:**\n🇬🇧 English (en) | 🇪🇸 Spanish (es) | 🇫🇷 French (fr)\n🇩🇪 Germa[...]
            color=Colors.INFO
        )
        if is_slash:
            await ctx_or_interaction.response.send_message(embed=embed)
        else:
            await ctx_or_interaction.send(embed=embed)
        return
    
    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://api.mymemory.translated.net/get?q={text}&langpair=autodetect|{target_lang}"
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    translated = data["responseData"]["translatedText"]
                    detected_lang = data.get("responseData", {}).get("detectedLanguage", "unknown")
                    
                    source_flag = LANGUAGE_FLAGS.get(detected_lang, "🌐")
                    target_flag = LANGUAGE_FLAGS.get(target_lang, "🌐")
                    
                    embed = create_glass_embed(
                        title=f"{Emojis.GLOBE} TRANSLATION",
                        color=Colors.SUCCESS,
                        fields=[
                            (f"{source_flag} Original", f"```{text}```", False),
                            (f"{target_flag} Translated", f"```{translated}```", False)
                        ]
                    )
                else:
                    embed = create_glass_embed(
                        title=f"{Emojis.CROSS} TRANSLATION FAILED",
                        description="Could not translate the text. Please try again.",
                        color=Colors.ERROR
                    )
    except Exception as e:
        embed = create_glass_embed(
            title=f"{Emojis.CROSS} TRANSLATION ERROR",
            description=f"An error occurred: {str(e)[:100]}",
            color=Colors.ERROR
        )
    
    if is_slash:
        await ctx_or_interaction.response.send_message(embed=embed)
    else:
        await ctx_or_interaction.send(embed=embed)

@bot.tree.command(name="translate", description="Translate text to another language")
@app_commands.describe(text="Text to translate", language="Target language code (e.g., en, es, fr)")
async def translate_slash(interaction: discord.Interaction, text: str, language: str = "en"):
    async with get_command_lock("translate"):
        await translate_handler(interaction, text, language)

@bot.command(name="translate", aliases=["tr"])
async def translate_prefix(ctx, *, args: str = None):
    text = args
    target_lang = "en"
    if args and " to " in args.lower():
        parts = args.lower().rsplit(" to ", 1)
        text = parts[0]
        target_lang = parts[1].strip()
    async with get_command_lock("translate"):
        await translate_handler(ctx, text, target_lang)

# ══════════════════════════════════════════════════════════════════[...]
# MESSAGE COUNTER SYSTEM
# ══════════════════════════════════════════════════════════════════[...]

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    
    counter = load_json("message_counter.json")
    user_id = str(message.author.id)
    
    if user_id not in counter["users"]:
        counter["users"][user_id] = 0
    counter["users"][user_id] += 1
    counter["total"] += 1
    save_json("message_counter.json", counter)
    
    config = load_json("config.json")
    if config["counting_channel"] and message.channel.id == config["counting_channel"]:
        if message.channel.id not in bot.counting_data:
            bot.counting_data[message.channel.id] = 0
        
        try:
            number = int(message.content)
            expected = bot.counting_data[message.channel.id] + 1
            
            if number == expected:
                bot.counting_data[message.channel.id] = number
                await message.add_reaction("✅")
            else:
                bot.counting_data[message.channel.id] = 0
                await message.add_reaction("❌")
                embed = create_glass_embed(
                    title=f"{Emojis.CROSS} COUNTING FAILED!",
                    description=f"{message.author.mention} ruined it! The next number was **{expected}**.\n\nCount reset to **0**. Start again with **1**!",
                    color=Colors.ERROR
                )
                await message.channel.send(embed=embed)
        except ValueError:
            pass
    
    await bot.process_commands(message)

async def counter_handler(ctx_or_interaction, action: str):
    """Unified message counter handler"""
    is_slash = isinstance(ctx_or_interaction, discord.Interaction)
    
    counter = load_json("message_counter.json")
    
    if action == "leaderboard":
        sorted_users = sorted(counter["users"].items(), key=lambda x: x[1], reverse=True)[:10]
        
        leaderboard_text = []
        for i, (user_id, count) in enumerate(sorted_users, 1):
            medal = ["🥇", "🥈", "🥉"][i-1] if i <= 3 else f"**{i}.**"
            leaderboard_text.append(f"{medal} <@{user_id}> — **{count:,}** messages")
        
        embed = create_hologram_embed(
            title=f"{Emojis.TROPHY} MESSAGE LEADERBOARD",
            description="\n".join(leaderboard_text) if leaderboard_text else "No messages tracked yet!",
            color=Colors.GOLD
        )
        embed.add_field(name="Total Server Messages", value=f"**{counter['total']:,}**", inline=False)
        
        if is_slash:
            await ctx_or_interaction.response.send_message(embed=embed)
        else:
            await ctx_or_interaction.send(embed=embed)
    
    elif action == "summary":
        election = load_json("election.json")
        
        embed = create_hologram_embed(
            title=f"{Emojis.SPARKLE} SERVER SUMMARY",
            description=f"**Total Messages:** {counter['total']:,}\n**Tracked Users:** {len(counter['users'])}\n\n**Election Status:** {'🟢 Active' if election['active'] else '🔴 Inactive'}\n**Tot[...]
            color=Colors.INFO
        )
        
        if is_slash:
            await ctx_or_interaction.response.send_message(embed=embed)
        else:
            await ctx_or_interaction.send(embed=embed)

@bot.tree.command(name="leaderboard", description="View message leaderboard")
async def leaderboard_slash(interaction: discord.Interaction):
    async with get_command_lock("leaderboard"):
        await counter_handler(interaction, "leaderboard")

@bot.tree.command(name="summary", description="View server summary")
async def summary_slash(interaction: discord.Interaction):
    async with get_command_lock("summary"):
        await counter_handler(interaction, "summary")

@bot.command(name="leaderboard", aliases=["lb", "top"])
async def leaderboard_prefix(ctx):
    async with get_command_lock("leaderboard"):
        await counter_handler(ctx, "leaderboard")

@bot.command(name="summary", aliases=["stats"])
async def summary_prefix(ctx):
    async with get_command_lock("summary"):
        await counter_handler(ctx, "summary")

# ══════════════════════════════════════════════════════════════════[...]
# COUNTING CHANNEL SETUP
# ══════════════════════════════════════════════════════════════════[...]

@bot.tree.command(name="setcounting", description="Set the counting channel")
@app_commands.describe(channel="Channel to use for counting")
async def setcounting_slash(interaction: discord.Interaction, channel: discord.TextChannel):
    user_tier = get_user_punishment_tier(interaction.user)
    if user_tier < 3:
        embed = create_glass_embed(
            title=f"{Emojis.SHIELD} UNAUTHORIZED",
            description="You need Tier 3+ permissions!",
            color=Colors.ERROR
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    
    config = load_json("config.json")
    config["counting_channel"] = channel.id
    save_json("config.json", config)
    
    bot.counting_data[channel.id] = 0
    
    embed = create_glass_embed(
        title=f"{Emojis.CHECK} COUNTING CHANNEL SET",
        description=f"Counting channel set to {channel.mention}!\n\nStart counting from **1**!",
        color=Colors.SUCCESS
    )
    await interaction.response.send_message(embed=embed)

@bot.command(name="setcounting")
async def setcounting_prefix(ctx, channel: discord.TextChannel = None):
    user_tier = get_user_punishment_tier(ctx.author)
    if user_tier < 3:
        embed = create_glass_embed(
            title=f"{Emojis.SHIELD} UNAUTHORIZED",
            description="You need Tier 3+ permissions!",
            color=Colors.ERROR
        )
        await ctx.send(embed=embed)
        return
    
    if not channel:
        channel = ctx.channel
    
    config = load_json("config.json")
    config["counting_channel"] = channel.id
    save_json("config.json", config)
    
    bot.counting_data[channel.id] = 0
    
    embed = create_glass_embed(
        title=f"{Emojis.CHECK} COUNTING CHANNEL SET",
        description=f"Counting channel set to {channel.mention}!\n\nStart counting from **1**!",
        color=Colors.SUCCESS
    )
    await ctx.send(embed=embed)

# ══════════════════════════════════════════════════════════════════[...]
# SUPPORT COMMAND
# ══════════════════════════════════════════════════════════════════[...]

async def support_handler(ctx_or_interaction):
    """Unified support handler"""
    is_slash = isinstance(ctx_or_interaction, discord.Interaction)
    
    support_data = load_json("support.json")
    
    embed = create_glass_embed(
        title=f"{Emojis.SUPPORT} SUPPORT",
        description=f"Need help? Join our support server!\n\n{Emojis.LINK} **[Click here to join]({support_data['support_link']})**",
        color=Colors.NEON_PURPLE
    )
    
    if is_slash:
        await ctx_or_interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        try:
            await ctx_or_interaction.author.send(embed=embed)
            await ctx_or_interaction.message.add_reaction(Emojis.CHECK)
        except:
            await ctx_or_interaction.send(embed=embed)

@bot.tree.command(name="support", description="Get support server link")
async def support_slash(interaction: discord.Interaction):
    async with get_command_lock("support"):
        await support_handler(interaction)

@bot.command(name="support")
async def support_prefix(ctx):
    async with get_command_lock("support"):
        await support_handler(ctx)

# ══════════════════════════════════════════════════════════════════[...]
# HELP COMMAND WITH DROPDOWN
# ══════════════════════════════════════════════════════════════════[...]

class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)
    
    @discord.ui.select(
        placeholder="Select a category...",
        options=[
            discord.SelectOption(label="Economy", value="economy", emoji="💰", description="Money commands"),
            discord.SelectOption(label="Casino", value="casino", emoji="🎰", description="Gambling games"),
            discord.SelectOption(label="Fun", value="fun", emoji="🎮", description="Fun games & activities"),
            discord.SelectOption(label="Moderation", value="moderation", emoji="🛡️", description="Server moderation"),
            discord.SelectOption(label="Utility", value="utility", emoji="⚙️", description="Utility commands"),
            discord.SelectOption(label="Support", value="support", emoji="💬", description="Get help")
        ]
    )
    async def help_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        category = select.values[0]
        
        categories = {
            "economy": {
                "title": f"{Emojis.MONEY} ECONOMY COMMANDS",
                "commands": [
                    ("`wallet`", "View your wallet"),
                    ("`bank`", "View your bank"),
                    ("`deposit <amount>`", "Deposit coins"),
                    ("`withdraw <amount>`", "Withdraw coins"),
                    ("`daily`", "Claim daily reward"),
                    ("`weekly`", "Claim weekly reward"),
                    ("`work`", "Work for coins"),
                    ("`crime`", "Risky crime for big rewards")
                ]
            },
            "casino": {
                "title": f"{Emojis.SLOT} CASINO COMMANDS",
                "commands": [
                    ("`coinflip <bet> <h/t>`", "Flip a coin"),
                    ("`slots <bet>`", "Play slots"),
                    ("`blackjack <bet>`", "Play blackjack"),
                    ("`dice <bet>`", "Roll dice"),
                    ("`roulette <bet> <choice>`", "Play roulette"),
                    ("`crash <bet>`", "Play crash game")
                ]
            },
            "fun": {
                "title": f"{Emojis.SPARKLE} FUN COMMANDS",
                "commands": [
                    ("`trivia`", "Answer trivia questions"),
                    ("`hangman`", "Play hangman"),
                    ("`guess`", "Guess the number"),
                    ("`rps <choice>`", "Rock Paper Scissors"),
                    ("`gtw @players`", "Guess The Word game"),
                    ("`gyi @players`", "Guess The Impostor game")
                ]
            },
            "moderation": {
                "title": f"{Emojis.SHIELD} MODERATION COMMANDS",
                "commands": [
                    ("`warn <user> [reason]`", "Warn a user"),
                    ("`unwarn <user>`", "Remove a warning"),
                    ("`warnings <user>`", "View warnings"),
                    ("`mute <user> [duration] [reason]`", "Mute a user"),
                    ("`unmute <user>`", "Unmute a user"),
                    ("`kick <user> [reason]`", "Kick a user"),
                    ("`ban <user> [reason]`", "Ban a user"),
                    ("`softban <user> [reason]`", "Softban a user")
                ]
            },
            "utility": {
                "title": f"{Emojis.GEAR} UTILITY COMMANDS",
                "commands": [
                    ("`translate <text> [to lang]`", "Translate text"),
                    ("`leaderboard`", "Message leaderboard"),
                    ("`summary`", "Server summary"),
                    ("`setcounting <channel>`", "Set counting channel"),
                    ("`setup`", "Run setup wizard")
                ]
            },
            "support": {
                "title": f"{Emojis.SUPPORT} SUPPORT",
                "commands": [
                    ("`support`", "Get support server link"),
                    ("`help`", "Show this help menu")
                ]
            }
        }
        
        cat = categories[category]
        commands_text = "\n".join([f"**{cmd}** — {desc}" for cmd, desc in cat["commands"]])
        
        embed = create_hologram_embed(
            title=cat["title"],
            description=f"{commands_text}\n\n*Use `/` for slash commands or `eu`/`elura` prefix*",
            color=Colors.NEON_PURPLE
        )
        
        await interaction.response.edit_message(embed=embed, view=self)

async def help_handler(ctx_or_interaction):
    """Unified help handler"""
    is_slash = isinstance(ctx_or_interaction, discord.Interaction)
    
    embed = create_hologram_embed(
        title=f"{Emojis.DIAMOND} ELURA UTILITY - HELP",
        description=f"**Welcome to {BOT_NAME}!**\n\nSelect a category from the dropdown below to view commands.\n\n**Prefixes:** `eu` | `elura` | `/`\n\n{Emojis.SPARKLE} *Powered by {ENGINE_NAME}*",
        color=Colors.NEON_PURPLE
    )
    
    view = HelpView()
    
    if is_slash:
        await ctx_or_interaction.response.send_message(embed=embed, view=view)
    else:
        await ctx_or_interaction.send(embed=embed, view=view)

@bot.tree.command(name="help", description="Show the help menu")
async def help_slash(interaction: discord.Interaction):
    async with get_command_lock("help"):
        await help_handler(interaction)

@bot.command(name="help", aliases=["h", "commands"])
async def help_prefix(ctx):
    async with get_command_lock("help"):
        await help_handler(ctx)

# ══════════════════════════════════════════════════════════════════[...]
# PROFESSIONAL FINAL SETUP WIZARD
# ══════════════════════════════════════════════════════════════════[...]

import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import json

# ---------------------- Helper Functions ----------------------
def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def create_embed(title, description, color=0x9B59B6):
    return discord.Embed(title=title, description=description, color=color)

def progress_bar(current, total, length=20):
    filled = int(length * current / total)
    empty = length - filled
    return f"[{'■' * filled}{'□' * empty}] Step {current}/{total}"

# ---------------------- Wizard Class ----------------------
class SetupWizard(discord.ui.View):
    def __init__(self, user_id: int, ctx_or_interaction):
        super().__init__(timeout=300)
        self.user_id = user_id
        self.ctx_or_interaction = ctx_or_interaction
        self.step = 1
        self.config = load_json("config.json")
        self.selected_channel = None
        self.selected_roles = []
        self.economy_value = 100
        self.cooldown_seconds = 60

        # Populate dropdowns dynamically
        guild = ctx_or_interaction.guild
        self.channel_options = [discord.SelectOption(label=c.name, value=str(c.id)) for c in guild.text_channels]
        self.role_options = [discord.SelectOption(label=r.name, value=str(r.id)) for r in guild.roles if r != guild.default_role]

        # Setup dropdowns
        self.channel_dropdown = discord.ui.Select(
            placeholder="Select moderation channel",
            min_values=1,
            max_values=1,
            options=self.channel_options
        )
        self.channel_dropdown.callback = self.select_channel
        self.add_item(self.channel_dropdown)

        self.roles_dropdown = discord.ui.Select(
            placeholder="Select punishment roles",
            min_values=1,
            max_values=5,
            options=self.role_options
        )
        self.roles_dropdown.callback = self.select_roles
        self.add_item(self.roles_dropdown)

    # ---------------- Update embed with live preview ----------------
    async def update_embed(self):
        steps = {
            1: ("Moderation Channel", "Select the channel for moderation logs."),
            2: ("Punishment Roles", "Select roles for punishments."),
            3: ("Economy Settings", "Set starting wallet amount."),
            4: ("Cooldown Settings", "Set cooldown in seconds."),
            5: ("Summary", "Review selections and save configuration.")
        }
        title, desc = steps[self.step]

        embed_desc = f"{desc}\n\n{progress_bar(self.step, len(steps))}"

        # Live preview of selections
        embed_desc += f"\n\n**Selected Channel:** {self.selected_channel.mention if self.selected_channel else 'None'}"
        embed_desc += f"\n**Selected Roles:** {', '.join([r.mention for r in self.selected_roles]) if self.selected_roles else 'None'}"
        embed_desc += f"\n**Starting Wallet:** {self.economy_value}"
        embed_desc += f"\n**Cooldown:** {self.cooldown_seconds} seconds"

        embed = create_embed(f"⚙️ Setup Wizard - Step {self.step}", embed_desc)

        # Update the message
        await self.ctx_or_interaction.edit_original_response(embed=embed, view=self)

    # ---------------- Dropdown callbacks ----------------
    async def select_channel(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This wizard isn't for you!", ephemeral=True)
            return
        self.selected_channel = interaction.guild.get_channel(int(interaction.data["values"][0]))
        await interaction.response.send_message(f"Selected channel: {self.selected_channel.mention}", ephemeral=True)
        await self.update_embed()

    async def select_roles(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This wizard isn't for you!", ephemeral=True)
            return
        self.selected_roles = [interaction.guild.get_role(int(rid)) for rid in interaction.data["values"]]
        await interaction.response.send_message(f"Selected roles: {', '.join([r.mention for r in self.selected_roles])}", ephemeral=True)
        await self.update_embed()

    # ---------------- Modals for numeric input ----------------
    async def prompt_economy_modal(self, interaction: discord.Interaction):
        class EconomyModal(discord.ui.Modal, title="Economy Settings"):
            amount = discord.ui.TextInput(label="Starting Wallet Amount", default=str(self.economy_value))

            async def on_submit(modal_interaction: discord.Interaction):
                self.economy_value = int(self.amount.value)
                await modal_interaction.response.send_message(f"Starting wallet set to {self.economy_value}", ephemeral=True)
                await self.update_embed()
        await interaction.response.send_modal(EconomyModal())

    async def prompt_cooldown_modal(self, interaction: discord.Interaction):
        class CooldownModal(discord.ui.Modal, title="Cooldown Settings"):
            seconds = discord.ui.TextInput(label="Cooldown in Seconds", default=str(self.cooldown_seconds))

            async def on_submit(modal_interaction: discord.Interaction):
                self.cooldown_seconds = int(self.seconds.value)
                await modal_interaction.response.send_message(f"Cooldown set to {self.cooldown_seconds}s", ephemeral=True)
                await self.update_embed()
        await interaction.response.send_modal(CooldownModal())

    # ---------------- Buttons ----------------
    @discord.ui.button(label="Next", style=discord.ButtonStyle.success, emoji="➡️")
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This wizard isn't for you!", ephemeral=True)
            return

        # Trigger modals for numeric input steps
        if self.step == 3:
            await self.prompt_economy_modal(interaction)
            return
        elif self.step == 4:
            await self.prompt_cooldown_modal(interaction)
            return

        self.step += 1
        if self.step > 5:
            # Save config
            self.config["moderation_channel"] = self.selected_channel.id if self.selected_channel else None
            self.config["punishment_roles"] = [r.id for r in self.selected_roles]
            self.config["economy_start"] = self.economy_value
            self.config["cooldown"] = self.cooldown_seconds
            save_json("config.json", self.config)

            for item in self.children:
                item.disabled = True
            embed = create_embed("✅ Setup Complete!", "Configuration saved successfully!")
            await interaction.response.edit_message(embed=embed, view=self)
            self.stop()
        else:
            await self.update_embed()

    @discord.ui.button(label="Skip", style=discord.ButtonStyle.secondary, emoji="⏭️")
    async def skip_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This wizard isn't for you!", ephemeral=True)
            return
        self.step += 1
        await self.update_embed()

# ---------------- Handler ----------------
async def setup_handler(ctx_or_interaction):
    is_slash = isinstance(ctx_or_interaction, discord.Interaction)
    user = ctx_or_interaction.user if is_slash else ctx_or_interaction.author

    embed = create_embed("⚙️ Setup Wizard", "Welcome! This wizard will guide you through setting up the bot.\n\nUse the dropdowns, modals, and buttons to configure settings.")
    view = SetupWizard(user.id, ctx_or_interaction)

    if is_slash:
        await ctx_or_interaction.response.send_message(embed=embed, view=view)
    else:
        await ctx_or_interaction.send(embed=embed, view=view)

# ══════════════════════════════════════════════════════════════════[...]
# ELURA / EU PROFESSIONAL SETUP WIZARD
# Fully interactive, multi-step, motion-glass, hover-enabled
# Founder-verified, 6 steps, modular & scalable
# ══════════════════════════════════════════════════════════════════[...]

import discord
from discord.ext import commands, tasks
import asyncio
import json
from typing import Dict, List

# ------------------------- Global Data -------------------------
setup_sessions: Dict[int, dict] = {}

# ---------------------- Helper Functions ----------------------
def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def create_embed(title: str, description: str, color=0x3498DB):
    return discord.Embed(title=title, description=f"```{description}```", color=color)

def progress_bar(step, total, length=20):
    filled = int(length * step / total)
    empty = length - filled
    return f"[{'█'*filled}{'─'*empty}] {step}/{total}"

def is_founder(user_id: int, guild_id: int):
    roles_data = load_json("roles.json")
    guild_roles = roles_data.get(str(guild_id), {})
    founder_ids = guild_roles.get("founders", [])
    return user_id in founder_ids

# ---------------------- Setup Wizard Class ----------------------
class SetupWizard(discord.ui.View):
    """Professional 6-step interactive setup wizard"""
    def __init__(self, user_id: int, guild: discord.Guild):
        super().__init__(timeout=900)
        self.user_id = user_id
        self.guild = guild
        self.step = 1
        self.max_steps = 6
        self.config = load_json("config.json").get(str(guild.id), {})
        self.embed_message: discord.Message = None

    # ---------------------- Embed Handling ----------------------
    def get_embed(self):
        step_titles = {
            1: "Set Moderation Logs Channel",
            2: "Configure Game Settings",
            3: "Economy & Casino Channels",
            4: "Auto-Moderation & Filters",
            5: "Active Monitoring Channels",
            6: "Founder Strictness & Confirmation"
        }
        step_descs = {
            1: "Select the moderation logs channel where all mod actions will be recorded.",
            2: "Enable/disable games, set rounds, max players, banned words.",
            3: "Set channels for wallet, casino, and leaderboard functionalities.",
            4: "Enable automod and filters to keep your server safe.",
            5: "Choose the channels where the bot should actively monitor messages.",
            6: "Select moderation strictness and confirm your settings."
        }
        return discord.Embed(
            title=f"⚙️ ELURA / EU Setup Wizard - Step {self.step}/{self.max_steps}",
            description=f"**{step_titles[self.step]}**\n{step_descs[self.step]}\n\nProgress: {progress_bar(self.step, self.max_steps)}",
            color=0x9B59B6
        )

    async def update_embed(self):
        if self.embed_message:
            await self.embed_message.edit(embed=self.get_embed(), view=self)

    def check_user(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            asyncio.create_task(interaction.response.send_message("This setup isn't for you!", ephemeral=True))
            return False
        return True

    async def save_config(self):
        all_config = load_json("config.json")
        all_config[str(self.guild.id)] = self.config
        save_json("config.json", all_config)

    # ---------------------- Buttons ----------------------
    @discord.ui.button(label="Next Step ➡️", style=discord.ButtonStyle.success)
    async def next_step(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not self.check_user(interaction): return
        self.step += 1
        if self.step > self.max_steps:
            await self.save_config()
            for item in self.children:
                item.disabled = True
            embed = discord.Embed(
                title="✅ Setup Complete!",
                description="All settings are saved! Your server
