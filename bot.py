"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           ELURA UTILITY BOT                                   ║
║                         Aurora Engine™ v1.0                                   ║
║              Premium Trillion-Dollar Discord Bot Experience                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
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

# ══════════════════════════════════════════════════════════════════════════════
# CONSTANTS & CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════

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

# ══════════════════════════════════════════════════════════════════════════════
# JSON FILE MANAGEMENT
# ══════════════════════════════════════════════════════════════════════════════

DEFAULT_FILES = {
    "roles.json": {
        "punishment_tiers": {
            "tier1": ["1444276505872957511"],
            "tier2": ["1444277015095279628"],
            "tier3": ["1438894984677031957"],
            "tier4": ["1438894983456227418"],
            "tier5": ["1438894982537810081"]
        },
        "party_leaders": [
            "1443857665586499664",
            "1443857720129097849",
            "1443857784687952003"
        ],
        "party_roles": {
            "communist": "1443690293835858093",
            "republic": "1443690180140732488",
            "democratic": "1443689962942758943"
        },
        "restricted_voters": [
            "1443690293835858093",
            "1443690180140732488",
            "1443689962942758943"
        ],
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

# ══════════════════════════════════════════════════════════════════════════════
# COMMAND LOCKS (Zero Duplicate Response Policy)
# ══════════════════════════════════════════════════════════════════════════════

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

# ══════════════════════════════════════════════════════════════════════════════
# PREMIUM UI BUILDERS
# ══════════════════════════════════════════════════════════════════════════════

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

# ══════════════════════════════════════════════════════════════════════════════
# BOT INITIALIZATION
# ══════════════════════════════════════════════════════════════════════════════

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

# ══════════════════════════════════════════════════════════════════════════════
# COOLDOWN MANAGEMENT
# ══════════════════════════════════════════════════════════════════════════════

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

# ══════════════════════════════════════════════════════════════════════════════
# ECONOMY SYSTEM
# ══════════════════════════════════════════════════════════════════════════════

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

# ══════════════════════════════════════════════════════════════════════════════
# CASINO SYSTEM
# ══════════════════════════════════════════════════════════════════════════════

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
            
            display = f"╔═══════════════════╗\n║  {reels[0]}  │  {reels[1]}  │  {reels[2]}  ║\n╚═══════════════════╝"
            
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

# ══════════════════════════════════════════════════════════════════════════════
# BLACKJACK GAME
# ══════════════════════════════════════════════════════════════════════════════

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

# ══════════════════════════════════════════════════════════════════════════════
# CRASH GAME
# ══════════════════════════════════════════════════════════════════════════════

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

# ══════════════════════════════════════════════════════════════════════════════
# FUN GAMES
# ══════════════════════════════════════════════════════════════════════════════

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

# ══════════════════════════════════════════════════════════════════════════════
# GTW (GUESS THE WORD) GAME
# ══════════════════════════════════════════════════════════════════════════════

gtw_sessions: Dict[int, dict] = {}

class GTWVotingView(discord.ui.View):
    def __init__(self, session_id: str, players: List[discord.Member], impostor_id: int):
        super().__init__(timeout=45)
        self.session_id = session_id
        self.players = players
        self.impostor_id = impostor_id
        self.votes: Dict[int, int] = {}
        self.voted_users: set = set()
        self.vote_lock = asyncio.Lock()
        self.processed_interactions: set = set()
        
        for player in players:
            button = discord.ui.Button(
                label=player.display_name[:20],
                custom_id=f"gtw_vote_{session_id}_{player.id}_{uuid.uuid4().hex[:6]}",
                style=discord.ButtonStyle.secondary
            )
            button.callback = self.create_vote_callback(player.id)
            self.add_item(button)
    
    def create_vote_callback(self, target_id: int):
        async def callback(interaction: discord.Interaction):
            interaction_token = f"{self.session_id}_{interaction.user.id}_{interaction.id}"
            error_msg = None
            success = False
            should_stop = False
            
            async with self.vote_lock:
                if interaction_token in self.processed_interactions:
                    try:
                        await interaction.response.defer()
                    except:
                        pass
                    return
                
                if interaction.user.id in self.voted_users:
                    error_msg = "You already voted!"
                elif interaction.user.id == target_id:
                    error_msg = "You can't vote for yourself!"
                elif interaction.user.id not in [p.id for p in self.players]:
                    error_msg = "You're not in this game!"
                else:
                    self.processed_interactions.add(interaction_token)
                    self.voted_users.add(interaction.user.id)
                    self.votes[target_id] = self.votes.get(target_id, 0) + 1
                    success = True
                    should_stop = len(self.voted_users) >= len(self.players)
            
            if error_msg:
                await interaction.response.send_message(error_msg, ephemeral=True)
            elif success:
                await interaction.response.send_message(f"You voted for <@{target_id}>!", ephemeral=True)
                if should_stop:
                    self.stop()
        return callback

async def gtw_handler(ctx_or_interaction, players: List[discord.Member] = None):
    """Unified GTW game handler"""
    is_slash = isinstance(ctx_or_interaction, discord.Interaction)
    user = ctx_or_interaction.user if is_slash else ctx_or_interaction.author
    channel = ctx_or_interaction.channel
    
    if not players or len(players) < 3:
        embed = create_glass_embed(
            title=f"{Emojis.SPARKLE} GUESS THE WORD",
            description="You need at least **3 players** to start!\n\nUsage: `gtw @player1 @player2 @player3 ...`",
            color=Colors.WARNING
        )
        if is_slash:
            await ctx_or_interaction.response.send_message(embed=embed)
        else:
            await ctx_or_interaction.send(embed=embed)
        return
    
    session_id = str(uuid.uuid4())[:8]
    impostor = random.choice(players)
    
    gtw_words = load_json("gtw_words.json")
    prompt_pair = random.choice(gtw_words["prompts"])
    
    session = {
        "id": session_id,
        "players": [p.id for p in players],
        "impostor": impostor.id,
        "prompt_normal": prompt_pair["normal"],
        "prompt_impostor": prompt_pair["impostor"],
        "answers": {},
        "round": 1,
        "max_rounds": 3,
        "message_id": None,
        "channel_id": channel.id
    }
    gtw_sessions[channel.id] = session
    
    embed = create_hologram_embed(
        title=f"{Emojis.GLASS} GUESS THE WORD",
        description=f"**Session:** `{session_id}`\n**Players:** {', '.join([p.display_name for p in players])}\n**Rounds:** 3\n\n**Rules:**\n• Reply to this message with your 1-2 word answer\n• One player is the impostor with a different prompt\n• Find the impostor!\n\n**Round 1 Prompt:**\n```{prompt_pair['normal']}```",
        color=Colors.NEON_PURPLE
    )
    embed.set_footer(text=f"◈ {FOOTER_TEXT} ◈ | Reply to this message with your answer!")
    
    for player in players:
        try:
            if player.id == impostor.id:
                dm_embed = create_glass_embed(
                    title=f"{Emojis.GLASS} YOU ARE THE IMPOSTOR!",
                    description=f"Your prompt is different:\n```{prompt_pair['impostor']}```\n\nBlend in with the others!",
                    color=Colors.ERROR
                )
            else:
                dm_embed = create_glass_embed(
                    title=f"{Emojis.GLASS} GTW - Round 1",
                    description=f"Your prompt:\n```{prompt_pair['normal']}```",
                    color=Colors.INFO
                )
            await player.send(embed=dm_embed)
        except:
            pass
    
    if is_slash:
        await ctx_or_interaction.response.send_message(embed=embed)
        message = await ctx_or_interaction.original_response()
    else:
        message = await ctx_or_interaction.send(embed=embed)
    
    session["message_id"] = message.id
    
    valid_answers = 0
    banned_words = ["best", "worst", "bad", "good", "holiday", "nice", "great", "terrible"]
    
    def check_answer(m):
        if m.reference and m.reference.message_id == session["message_id"]:
            if m.author.id in session["players"]:
                words = m.content.strip().split()
                if 1 <= len(words) <= 2:
                    if not any(bw in m.content.lower() for bw in banned_words):
                        return True
        return False
    
    timeout_time = 90 * session["max_rounds"]
    start_time = time.time()
    
    while valid_answers < 9 and time.time() - start_time < timeout_time:
        try:
            response = await bot.wait_for("message", check=check_answer, timeout=30)
            player_id = response.author.id
            
            if player_id not in session["answers"]:
                session["answers"][player_id] = []
            session["answers"][player_id].append(response.content.strip())
            valid_answers += 1
            
        except asyncio.TimeoutError:
            if valid_answers >= 3:
                break
            continue
    
    if valid_answers < 3:
        embed = create_glass_embed(
            title=f"{Emojis.CROSS} GAME CANCELLED",
            description="Not enough answers received!",
            color=Colors.ERROR
        )
        await channel.send(embed=embed)
        del gtw_sessions[channel.id]
        return
    
    view = GTWVotingView(session_id, players, impostor.id)
    
    answers_text = "\n".join([f"**{bot.get_user(pid).display_name}:** {', '.join(ans)}" for pid, ans in session["answers"].items()])
    
    embed = create_hologram_embed(
        title=f"{Emojis.VOTE} VOTING TIME!",
        description=f"**Answers:**\n{answers_text}\n\n**Vote for who you think is the impostor!**",
        color=Colors.NEON_CYAN
    )
    
    vote_message = await channel.send(embed=embed, view=view)
    
    await view.wait()
    
    if view.votes:
        most_voted = max(view.votes, key=view.votes.get)
        most_votes = view.votes[most_voted]
    else:
        most_voted = None
        most_votes = 0
    
    if most_voted == impostor.id:
        result = f"{Emojis.TROPHY} **PLAYERS WIN!**\n\nThe impostor was **{impostor.display_name}** and they were caught!"
        color = Colors.SUCCESS
        
        for player in players:
            if player.id != impostor.id:
                user_data = get_user_economy(player.id)
                user_data["wallet"] += 100
                user_data["total_earned"] += 100
                update_user_economy(player.id, user_data)
    else:
        result = f"{Emojis.FIRE} **IMPOSTOR WINS!**\n\nThe impostor was **{impostor.display_name}** and they escaped!"
        color = Colors.ERROR
        
        user_data = get_user_economy(impostor.id)
        user_data["wallet"] += 200
        user_data["total_earned"] += 200
        update_user_economy(impostor.id, user_data)
    
    stats = load_json("games_stats.json")
    for player in players:
        pid = str(player.id)
        if pid not in stats["gtw"]["leaderboard"]:
            stats["gtw"]["leaderboard"][pid] = {"wins": 0, "losses": 0, "impostor_wins": 0}
        
        if player.id == impostor.id:
            if most_voted != impostor.id:
                stats["gtw"]["leaderboard"][pid]["impostor_wins"] += 1
                stats["gtw"]["leaderboard"][pid]["wins"] += 1
            else:
                stats["gtw"]["leaderboard"][pid]["losses"] += 1
        else:
            if most_voted == impostor.id:
                stats["gtw"]["leaderboard"][pid]["wins"] += 1
            else:
                stats["gtw"]["leaderboard"][pid]["losses"] += 1
    save_json("games_stats.json", stats)
    
    vote_breakdown = "\n".join([f"<@{uid}>: **{count}** votes" for uid, count in view.votes.items()])
    
    embed = create_hologram_embed(
        title=f"{Emojis.GLASS} GAME OVER!",
        description=f"{result}\n\n**Vote Breakdown:**\n{vote_breakdown}\n\n**Normal Prompt:** {session['prompt_normal']}\n**Impostor Prompt:** {session['prompt_impostor']}",
        color=color
    )
    
    await channel.send(embed=embed)
    
    if channel.id in gtw_sessions:
        del gtw_sessions[channel.id]

@bot.tree.command(name="gtw", description="Start a Guess The Word game")
@app_commands.describe(player1="First player", player2="Second player", player3="Third player")
async def gtw_slash(interaction: discord.Interaction, player1: discord.Member, player2: discord.Member, player3: discord.Member):
    async with get_command_lock("gtw"):
        players = [player1, player2, player3]
        if interaction.user not in players:
            players.append(interaction.user)
        await gtw_handler(interaction, players)

@bot.command(name="gtw")
async def gtw_prefix(ctx, *members: discord.Member):
    async with get_command_lock("gtw"):
        players = list(members)
        if ctx.author not in players:
            players.append(ctx.author)
        await gtw_handler(ctx, players)

# ══════════════════════════════════════════════════════════════════════════════
# GYI (GUESS YOUR IMPOSTOR) GAME
# ══════════════════════════════════════════════════════════════════════════════

gyi_sessions: Dict[int, dict] = {}

async def gyi_handler(ctx_or_interaction, players: List[discord.Member] = None):
    """Unified GYI game handler"""
    is_slash = isinstance(ctx_or_interaction, discord.Interaction)
    user = ctx_or_interaction.user if is_slash else ctx_or_interaction.author
    channel = ctx_or_interaction.channel
    
    if not players or len(players) < 3:
        embed = create_glass_embed(
            title=f"{Emojis.GLASS} GUESS THE IMPOSTOR",
            description="You need at least **3 players** to start!\n\nUsage: `gyi @player1 @player2 @player3 ...`",
            color=Colors.WARNING
        )
        if is_slash:
            await ctx_or_interaction.response.send_message(embed=embed)
        else:
            await ctx_or_interaction.send(embed=embed)
        return
    
    session_id = str(uuid.uuid4())[:8]
    impostor = random.choice(players)
    
    gyi_words = load_json("gyi_words.json")
    word_pair = random.choice(gyi_words["pairs"])
    
    session = {
        "id": session_id,
        "players": [p.id for p in players],
        "impostor": impostor.id,
        "normal_word": word_pair["normal"],
        "impostor_word": word_pair["impostor"],
        "answers": {},
        "round": 1,
        "max_rounds": 3,
        "message_id": None,
        "channel_id": channel.id
    }
    gyi_sessions[channel.id] = session
    
    embed = create_hologram_embed(
        title=f"{Emojis.GLASS} GUESS THE IMPOSTOR",
        description=f"**Session:** `{session_id}`\n**Players:** {', '.join([p.display_name for p in players])}\n**Rounds:** 3\n\n**Rules:**\n• Reply to this message with a 1-2 word descriptor\n• One player has a DIFFERENT word!\n• Find the impostor based on their descriptions!\n\n**Describe your word!**",
        color=Colors.NEON_PURPLE
    )
    embed.set_footer(text=f"◈ {FOOTER_TEXT} ◈ | Reply with a 1-2 word descriptor!")
    
    for player in players:
        try:
            if player.id == impostor.id:
                dm_embed = create_glass_embed(
                    title=f"{Emojis.GLASS} YOU ARE THE IMPOSTOR!",
                    description=f"Your word is: **{word_pair['impostor']}**\n\nOthers have: **{word_pair['normal']}**\n\nBlend in with your descriptions!",
                    color=Colors.ERROR
                )
            else:
                dm_embed = create_glass_embed(
                    title=f"{Emojis.GLASS} GYI - Your Word",
                    description=f"Your word is: **{word_pair['normal']}**\n\nDescribe it without saying the word!",
                    color=Colors.INFO
                )
            await player.send(embed=dm_embed)
        except:
            pass
    
    if is_slash:
        await ctx_or_interaction.response.send_message(embed=embed)
        message = await ctx_or_interaction.original_response()
    else:
        message = await ctx_or_interaction.send(embed=embed)
    
    session["message_id"] = message.id
    
    valid_answers = 0
    
    def check_answer(m):
        if m.reference and m.reference.message_id == session["message_id"]:
            if m.author.id in session["players"]:
                words = m.content.strip().split()
                if 1 <= len(words) <= 2:
                    return True
        return False
    
    timeout_time = 90 * session["max_rounds"]
    start_time = time.time()
    
    while valid_answers < 9 and time.time() - start_time < timeout_time:
        try:
            response = await bot.wait_for("message", check=check_answer, timeout=30)
            player_id = response.author.id
            
            if player_id not in session["answers"]:
                session["answers"][player_id] = []
            session["answers"][player_id].append(response.content.strip())
            valid_answers += 1
            
        except asyncio.TimeoutError:
            if valid_answers >= 3:
                break
            continue
    
    if valid_answers < 3:
        embed = create_glass_embed(
            title=f"{Emojis.CROSS} GAME CANCELLED",
            description="Not enough answers received!",
            color=Colors.ERROR
        )
        await channel.send(embed=embed)
        del gyi_sessions[channel.id]
        return
    
    view = GTWVotingView(session_id, players, impostor.id)
    
    answers_text = "\n".join([f"**{bot.get_user(pid).display_name}:** {', '.join(ans)}" for pid, ans in session["answers"].items()])
    
    embed = create_hologram_embed(
        title=f"{Emojis.VOTE} VOTING TIME!",
        description=f"**Descriptions:**\n{answers_text}\n\n**Vote for who you think is the impostor!**",
        color=Colors.NEON_CYAN
    )
    
    vote_message = await channel.send(embed=embed, view=view)
    
    await view.wait()
    
    if view.votes:
        most_voted = max(view.votes, key=view.votes.get)
        most_votes = view.votes[most_voted]
    else:
        most_voted = None
        most_votes = 0
    
    if most_voted == impostor.id:
        result = f"{Emojis.TROPHY} **PLAYERS WIN!**\n\nThe impostor was **{impostor.display_name}** and they were caught!"
        color = Colors.SUCCESS
        
        for player in players:
            if player.id != impostor.id:
                user_data = get_user_economy(player.id)
                user_data["wallet"] += 100
                user_data["total_earned"] += 100
                update_user_economy(player.id, user_data)
    else:
        result = f"{Emojis.FIRE} **IMPOSTOR WINS!**\n\nThe impostor was **{impostor.display_name}** and they escaped!"
        color = Colors.ERROR
        
        user_data = get_user_economy(impostor.id)
        user_data["wallet"] += 200
        user_data["total_earned"] += 200
        update_user_economy(impostor.id, user_data)
    
    stats = load_json("games_stats.json")
    for player in players:
        pid = str(player.id)
        if pid not in stats["gyi"]["leaderboard"]:
            stats["gyi"]["leaderboard"][pid] = {"wins": 0, "losses": 0, "impostor_wins": 0}
        
        if player.id == impostor.id:
            if most_voted != impostor.id:
                stats["gyi"]["leaderboard"][pid]["impostor_wins"] += 1
                stats["gyi"]["leaderboard"][pid]["wins"] += 1
            else:
                stats["gyi"]["leaderboard"][pid]["losses"] += 1
        else:
            if most_voted == impostor.id:
                stats["gyi"]["leaderboard"][pid]["wins"] += 1
            else:
                stats["gyi"]["leaderboard"][pid]["losses"] += 1
    save_json("games_stats.json", stats)
    
    vote_breakdown = "\n".join([f"<@{uid}>: **{count}** votes" for uid, count in view.votes.items()])
    
    embed = create_hologram_embed(
        title=f"{Emojis.GLASS} GAME OVER!",
        description=f"{result}\n\n**Vote Breakdown:**\n{vote_breakdown}\n\n**Normal Word:** {session['normal_word']}\n**Impostor Word:** {session['impostor_word']}",
        color=color
    )
    
    await channel.send(embed=embed)
    
    if channel.id in gyi_sessions:
        del gyi_sessions[channel.id]

@bot.tree.command(name="gyi", description="Start a Guess Your Impostor game")
@app_commands.describe(player1="First player", player2="Second player", player3="Third player")
async def gyi_slash(interaction: discord.Interaction, player1: discord.Member, player2: discord.Member, player3: discord.Member):
    async with get_command_lock("gyi"):
        players = [player1, player2, player3]
        if interaction.user not in players:
            players.append(interaction.user)
        await gyi_handler(interaction, players)

@bot.command(name="gyi", aliases=["imposter", "impostor"])
async def gyi_prefix(ctx, *members: discord.Member):
    async with get_command_lock("gyi"):
        players = list(members)
        if ctx.author not in players:
            players.append(ctx.author)
        await gyi_handler(ctx, players)

# ══════════════════════════════════════════════════════════════════════════════
# PUNISHMENT SYSTEM
# ══════════════════════════════════════════════════════════════════════════════

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
    
    if action == "warn":
        case_id = await create_case(guild.id, user.id, target.id, "WARN", reason)
        
        try:
            dm_embed = create_glass_embed(
                title=f"{Emojis.WARN} WARNING",
                description=f"You have been warned in **{guild.name}**\n\n**Reason:** {reason}\n**Case ID:** #{case_id}",
                color=Colors.WARNING
            )
            await target.send(embed=dm_embed)
        except:
            pass
        
        embed = create_neon_embed(
            title=f"{Emojis.WARN} USER WARNED",
            description=f"**Target:** {target.mention}\n**Moderator:** {user.mention}\n**Reason:** {reason}\n**Case ID:** #{case_id}",
            color=Colors.WARNING
        )
        
    elif action == "unwarn":
        punishments = load_json("punishments.json")
        user_warnings = [c for c in punishments["cases"] if c["target_id"] == target.id and c["action"] == "WARN" and c["active"]]
        
        if not user_warnings:
            embed = create_glass_embed(
                title=f"{Emojis.CROSS} NO WARNINGS",
                description=f"{target.mention} has no active warnings!",
                color=Colors.ERROR
            )
        else:
            latest_warning = user_warnings[-1]
            for case in punishments["cases"]:
                if case["id"] == latest_warning["id"]:
                    case["active"] = False
                    break
            save_json("punishments.json", punishments)
            
            embed = create_neon_embed(
                title=f"{Emojis.CHECK} WARNING REMOVED",
                description=f"Removed warning #{latest_warning['id']} from {target.mention}",
                color=Colors.SUCCESS
            )
    
    elif action == "warnings":
        punishments = load_json("punishments.json")
        user_warnings = [c for c in punishments["cases"] if c["target_id"] == target.id and c["action"] == "WARN" and c["active"]]
        
        if not user_warnings:
            embed = create_glass_embed(
                title=f"{Emojis.CHECK} NO WARNINGS",
                description=f"{target.mention} has no active warnings!",
                color=Colors.SUCCESS
            )
        else:
            warnings_text = "\n".join([f"**#{w['id']}** - {w['reason'][:50]}" for w in user_warnings])
            embed = create_glass_embed(
                title=f"{Emojis.WARN} WARNINGS ({len(user_warnings)})",
                description=f"**User:** {target.mention}\n\n{warnings_text}",
                color=Colors.WARNING
            )
    
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

# Punishment Prefix Commands
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

# ══════════════════════════════════════════════════════════════════════════════
# POLITICAL PARTY SYSTEM
# ══════════════════════════════════════════════════════════════════════════════

class PartyJoinView(discord.ui.View):
    def __init__(self, user_id: int):
        super().__init__(timeout=60)
        self.user_id = user_id
        self.selected_party = None
    
    @discord.ui.select(
        placeholder="Select a party to join...",
        options=[
            discord.SelectOption(label="Communist Party", value="communist", emoji="🔴"),
            discord.SelectOption(label="Republic Party", value="republic", emoji="🔵"),
            discord.SelectOption(label="Democratic Party", value="democratic", emoji="🟢")
        ]
    )
    async def party_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This menu isn't for you!", ephemeral=True)
            return
        
        self.selected_party = select.values[0]
        self.stop()
        
        roles_data = load_json("roles.json")
        party_role_id = int(roles_data["party_roles"][self.selected_party])
        
        for party in ["communist", "republic", "democratic"]:
            party_data = load_json(f"{party}.json")
            if interaction.user.id in party_data["members"]:
                party_data["members"].remove(interaction.user.id)
                save_json(f"{party}.json", party_data)
                
                old_role_id = int(roles_data["party_roles"][party])
                old_role = interaction.guild.get_role(old_role_id)
                if old_role and old_role in interaction.user.roles:
                    try:
                        await interaction.user.remove_roles(old_role)
                    except:
                        pass
        
        party_data = load_json(f"{self.selected_party}.json")
        if interaction.user.id not in party_data["members"]:
            party_data["members"].append(interaction.user.id)
            save_json(f"{self.selected_party}.json", party_data)
        
        role = interaction.guild.get_role(party_role_id)
        if role:
            try:
                await interaction.user.add_roles(role)
            except:
                pass
        
        party_names = {"communist": "Communist", "republic": "Republic", "democratic": "Democratic"}
        
        embed = create_hologram_embed(
            title=f"{Emojis.PARTY} PARTY JOINED!",
            description=f"Welcome to the **{party_names[self.selected_party]} Party**!",
            color=Colors.SUCCESS
        )
        
        await interaction.response.edit_message(embed=embed, view=None)

async def party_handler(ctx_or_interaction, action: str, target: discord.Member = None):
    """Unified party handler"""
    is_slash = isinstance(ctx_or_interaction, discord.Interaction)
    user = ctx_or_interaction.user if is_slash else ctx_or_interaction.author
    guild = ctx_or_interaction.guild
    
    roles_data = load_json("roles.json")
    
    if action == "join":
        embed = create_hologram_embed(
            title=f"{Emojis.PARTY} JOIN A PARTY",
            description="Select your political party from the dropdown below.\n\n**Available Parties:**\n🔴 Communist Party\n🔵 Republic Party\n🟢 Democratic Party",
            color=Colors.NEON_PURPLE
        )
        
        view = PartyJoinView(user.id)
        
        if is_slash:
            await ctx_or_interaction.response.send_message(embed=embed, view=view)
        else:
            await ctx_or_interaction.send(embed=embed, view=view)
    
    elif action == "leave":
        left_party = None
        for party in ["communist", "republic", "democratic"]:
            party_data = load_json(f"{party}.json")
            if user.id in party_data["members"]:
                party_data["members"].remove(user.id)
                save_json(f"{party}.json", party_data)
                left_party = party
                
                role_id = int(roles_data["party_roles"][party])
                role = guild.get_role(role_id)
                if role and role in user.roles:
                    try:
                        await user.remove_roles(role)
                    except:
                        pass
                break
        
        if left_party:
            party_names = {"communist": "Communist", "republic": "Republic", "democratic": "Democratic"}
            embed = create_glass_embed(
                title=f"{Emojis.CHECK} LEFT PARTY",
                description=f"You have left the **{party_names[left_party]} Party**.",
                color=Colors.SUCCESS
            )
        else:
            embed = create_glass_embed(
                title=f"{Emojis.CROSS} NOT IN A PARTY",
                description="You are not a member of any party!",
                color=Colors.ERROR
            )
        
        if is_slash:
            await ctx_or_interaction.response.send_message(embed=embed)
        else:
            await ctx_or_interaction.send(embed=embed)
    
    elif action == "info":
        party_stats = []
        for party in ["communist", "republic", "democratic"]:
            party_data = load_json(f"{party}.json")
            member_count = len(party_data["members"])
            execs = party_data["executives"]
            
            party_names = {"communist": "Communist", "republic": "Republic", "democratic": "Democratic"}
            party_emojis = {"communist": "🔴", "republic": "🔵", "democratic": "🟢"}
            
            exec_text = []
            if execs["president"]:
                exec_text.append(f"President: <@{execs['president']}>")
            if execs["vice_president"]:
                exec_text.append(f"VP: <@{execs['vice_president']}>")
            if execs["general_secretary"]:
                exec_text.append(f"GS: <@{execs['general_secretary']}>")
            
            bar = progress_bar(member_count, 100, 15)
            
            party_stats.append(f"{party_emojis[party]} **{party_names[party]} Party**\n{bar}\nMembers: **{member_count}**\n{chr(10).join(exec_text) if exec_text else 'No executives set'}")
        
        embed = create_hologram_embed(
            title=f"{Emojis.PARLIAMENT} PARTY INFORMATION",
            description="\n\n".join(party_stats),
            color=Colors.NEON_PURPLE
        )
        
        if is_slash:
            await ctx_or_interaction.response.send_message(embed=embed)
        else:
            await ctx_or_interaction.send(embed=embed)
    
    elif action == "expel":
        if target is None:
            embed = create_glass_embed(
                title=f"{Emojis.CROSS} ERROR",
                description="Please specify a user to expel!",
                color=Colors.ERROR
            )
            if is_slash:
                await ctx_or_interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await ctx_or_interaction.send(embed=embed)
            return
        
        user_role_ids = [str(r.id) for r in user.roles]
        is_leader = any(lid in user_role_ids for lid in roles_data["party_leaders"])
        
        if not is_leader:
            embed = create_glass_embed(
                title=f"{Emojis.SHIELD} UNAUTHORIZED",
                description="Only party leaders can expel members!",
                color=Colors.ERROR
            )
            if is_slash:
                await ctx_or_interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await ctx_or_interaction.send(embed=embed)
            return
        
        expelled_from = None
        for party in ["communist", "republic", "democratic"]:
            party_data = load_json(f"{party}.json")
            if target.id in party_data["members"]:
                party_data["members"].remove(target.id)
                save_json(f"{party}.json", party_data)
                expelled_from = party
                
                role_id = int(roles_data["party_roles"][party])
                role = guild.get_role(role_id)
                if role and role in target.roles:
                    try:
                        await target.remove_roles(role)
                    except:
                        pass
                break
        
        if expelled_from:
            party_names = {"communist": "Communist", "republic": "Republic", "democratic": "Democratic"}
            embed = create_neon_embed(
                title=f"{Emojis.GAVEL} MEMBER EXPELLED",
                description=f"{target.mention} has been expelled from the **{party_names[expelled_from]} Party**.",
                color=Colors.ERROR
            )
        else:
            embed = create_glass_embed(
                title=f"{Emojis.CROSS} NOT IN A PARTY",
                description=f"{target.mention} is not a member of any party!",
                color=Colors.ERROR
            )
        
        if is_slash:
            await ctx_or_interaction.response.send_message(embed=embed)
        else:
            await ctx_or_interaction.send(embed=embed)

# Party Command Group
party_group = app_commands.Group(name="party", description="Political party commands")

@party_group.command(name="join", description="Join a political party")
async def party_join_slash(interaction: discord.Interaction):
    async with get_command_lock("party_join"):
        await party_handler(interaction, "join")

@party_group.command(name="leave", description="Leave your current party")
async def party_leave_slash(interaction: discord.Interaction):
    async with get_command_lock("party_leave"):
        await party_handler(interaction, "leave")

@party_group.command(name="info", description="View party information")
async def party_info_slash(interaction: discord.Interaction):
    async with get_command_lock("party_info"):
        await party_handler(interaction, "info")

@party_group.command(name="expel", description="Expel a member from a party (Leaders only)")
@app_commands.describe(target="User to expel")
async def party_expel_slash(interaction: discord.Interaction, target: discord.Member):
    async with get_command_lock("party_expel"):
        await party_handler(interaction, "expel", target)

bot.tree.add_command(party_group)

# Party Prefix Commands
@bot.group(name="party", invoke_without_command=True)
async def party_prefix(ctx):
    async with get_command_lock("party_info"):
        await party_handler(ctx, "info")

@party_prefix.command(name="join")
async def party_join_prefix(ctx):
    async with get_command_lock("party_join"):
        await party_handler(ctx, "join")

@party_prefix.command(name="leave")
async def party_leave_prefix(ctx):
    async with get_command_lock("party_leave"):
        await party_handler(ctx, "leave")

@party_prefix.command(name="info")
async def party_info_prefix(ctx):
    async with get_command_lock("party_info"):
        await party_handler(ctx, "info")

@party_prefix.command(name="expel")
async def party_expel_prefix(ctx, target: discord.Member = None):
    async with get_command_lock("party_expel"):
        await party_handler(ctx, "expel", target)

# ══════════════════════════════════════════════════════════════════════════════
# ELECTION SYSTEM
# ══════════════════════════════════════════════════════════════════════════════

class ElectionVoteView(discord.ui.View):
    def __init__(self, candidates: List[dict]):
        super().__init__(timeout=None)
        self.candidates = candidates
        self.vote_lock = asyncio.Lock()
        self.session_id = str(uuid.uuid4())[:8]
        
        options = []
        for candidate in candidates:
            options.append(discord.SelectOption(
                label=candidate["name"][:25],
                value=str(candidate["id"]),
                description=f"Party: {candidate['party']}"
            ))
        
        select = discord.ui.Select(
            placeholder="Cast your vote...",
            options=options,
            custom_id=f"election_vote_select_{self.session_id}"
        )
        select.callback = self.vote_callback
        self.add_item(select)
    
    async def vote_callback(self, interaction: discord.Interaction):
        error_msg = None
        success = False
        
        async with self.vote_lock:
            election = load_json("election.json")
            
            if not election["active"]:
                error_msg = "This election has ended!"
            elif interaction.user.id in election["voters"]:
                error_msg = "You have already voted in this election!"
            else:
                roles_data = load_json("roles.json")
                user_role_ids = [str(r.id) for r in interaction.user.roles]
                is_restricted = any(rid in user_role_ids for rid in roles_data["restricted_voters"])
                
                if is_restricted:
                    error_msg = "You are not eligible to vote!"
                else:
                    candidate_id = interaction.data["values"][0]
                    
                    if candidate_id not in election["votes"]:
                        election["votes"][candidate_id] = 0
                    election["votes"][candidate_id] += 1
                    election["voters"].append(interaction.user.id)
                    
                    save_json("election.json", election)
                    success = True
        
        if error_msg:
            await interaction.response.send_message(error_msg, ephemeral=True)
        elif success:
            await interaction.response.send_message(
                f"{Emojis.CHECK} Your vote has been recorded!",
                ephemeral=True
            )

async def election_handler(ctx_or_interaction, action: str):
    """Unified election handler"""
    is_slash = isinstance(ctx_or_interaction, discord.Interaction)
    user = ctx_or_interaction.user if is_slash else ctx_or_interaction.author
    guild = ctx_or_interaction.guild
    
    election = load_json("election.json")
    roles_data = load_json("roles.json")
    
    if action == "start":
        user_tier = get_user_punishment_tier(user)
        if user_tier < 3:
            embed = create_glass_embed(
                title=f"{Emojis.SHIELD} UNAUTHORIZED",
                description="You need Tier 3+ permissions to start elections!",
                color=Colors.ERROR
            )
            if is_slash:
                await ctx_or_interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await ctx_or_interaction.send(embed=embed)
            return
        
        if election["active"]:
            embed = create_glass_embed(
                title=f"{Emojis.CROSS} ELECTION ACTIVE",
                description="An election is already in progress!",
                color=Colors.ERROR
            )
            if is_slash:
                await ctx_or_interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await ctx_or_interaction.send(embed=embed)
            return
        
        candidates = []
        for party in ["communist", "republic", "democratic"]:
            party_data = load_json(f"{party}.json")
            if party_data["executives"]["president"]:
                member = guild.get_member(party_data["executives"]["president"])
                if member:
                    candidates.append({
                        "id": member.id,
                        "name": member.display_name,
                        "party": party.capitalize()
                    })
        
        if len(candidates) < 2:
            for party in ["communist", "republic", "democratic"]:
                party_data = load_json(f"{party}.json")
                if party_data["members"]:
                    member = guild.get_member(party_data["members"][0])
                    if member and member.id not in [c["id"] for c in candidates]:
                        candidates.append({
                            "id": member.id,
                            "name": member.display_name,
                            "party": party.capitalize()
                        })
        
        election = {
            "active": True,
            "candidates": {str(c["id"]): c for c in candidates},
            "votes": {},
            "voters": [],
            "start_time": datetime.utcnow().isoformat(),
            "end_time": None
        }
        save_json("election.json", election)
        
        view = ElectionVoteView(candidates)
        
        candidates_text = "\n".join([f"• **{c['name']}** ({c['party']})" for c in candidates])
        
        embed = create_hologram_embed(
            title=f"{Emojis.VOTE} ELECTION STARTED!",
            description=f"**Candidates:**\n{candidates_text}\n\n**Cast your vote using the dropdown below!**",
            color=Colors.NEON_CYAN
        )
        
        if is_slash:
            await ctx_or_interaction.response.send_message(embed=embed, view=view)
        else:
            await ctx_or_interaction.send(embed=embed, view=view)
    
    elif action == "live":
        if not election["active"]:
            embed = create_glass_embed(
                title=f"{Emojis.CROSS} NO ACTIVE ELECTION",
                description="There is no active election!",
                color=Colors.ERROR
            )
            if is_slash:
                await ctx_or_interaction.response.send_message(embed=embed)
            else:
                await ctx_or_interaction.send(embed=embed)
            return
        
        total_votes = sum(election["votes"].values()) if election["votes"] else 0
        
        results = []
        for cid, candidate in election["candidates"].items():
            votes = election["votes"].get(cid, 0)
            percentage = (votes / total_votes * 100) if total_votes > 0 else 0
            bar = progress_bar(votes, max(total_votes, 1), 15)
            results.append(f"**{candidate['name']}** ({candidate['party']})\n{bar}\n{votes} votes ({percentage:.1f}%)")
        
        embed = create_hologram_embed(
            title=f"{Emojis.VOTE} LIVE ELECTION RESULTS",
            description="\n\n".join(results) + f"\n\n**Total Votes:** {total_votes}",
            color=Colors.NEON_CYAN
        )
        
        if is_slash:
            await ctx_or_interaction.response.send_message(embed=embed)
        else:
            await ctx_or_interaction.send(embed=embed)
    
    elif action == "stop":
        user_tier = get_user_punishment_tier(user)
        if user_tier < 3:
            embed = create_glass_embed(
                title=f"{Emojis.SHIELD} UNAUTHORIZED",
                description="You need Tier 3+ permissions to stop elections!",
                color=Colors.ERROR
            )
            if is_slash:
                await ctx_or_interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await ctx_or_interaction.send(embed=embed)
            return
        
        if not election["active"]:
            embed = create_glass_embed(
                title=f"{Emojis.CROSS} NO ACTIVE ELECTION",
                description="There is no active election to stop!",
                color=Colors.ERROR
            )
            if is_slash:
                await ctx_or_interaction.response.send_message(embed=embed)
            else:
                await ctx_or_interaction.send(embed=embed)
            return
        
        election["active"] = False
        election["end_time"] = datetime.utcnow().isoformat()
        save_json("election.json", election)
        
        total_votes = sum(election["votes"].values()) if election["votes"] else 0
        
        if election["votes"]:
            winner_id = max(election["votes"], key=election["votes"].get)
            winner = election["candidates"].get(winner_id, {})
            winner_votes = election["votes"][winner_id]
        else:
            winner = {"name": "No one", "party": "N/A"}
            winner_votes = 0
        
        results = []
        for cid, candidate in election["candidates"].items():
            votes = election["votes"].get(cid, 0)
            percentage = (votes / total_votes * 100) if total_votes > 0 else 0
            bar = progress_bar(votes, max(total_votes, 1), 15)
            results.append(f"**{candidate['name']}** ({candidate['party']})\n{bar}\n{votes} votes ({percentage:.1f}%)")
        
        all_members = set()
        for member in guild.members:
            if not member.bot:
                user_role_ids = [str(r.id) for r in member.roles]
                if not any(rid in user_role_ids for rid in roles_data["restricted_voters"]):
                    all_members.add(member.id)
        
        non_voters = all_members - set(election["voters"])
        shame_mentions = " ".join([f"<@{uid}>" for uid in list(non_voters)[:10]])
        if len(non_voters) > 10:
            shame_mentions += f" and {len(non_voters) - 10} more..."
        
        embed = create_hologram_embed(
            title=f"{Emojis.CROWN} ELECTION CONCLUDED!",
            description=f"**{Emojis.TROPHY} WINNER: {winner['name']}** ({winner.get('party', 'N/A')})\n\n**Final Results:**\n" + "\n\n".join(results) + f"\n\n**Total Votes:** {total_votes}",
            color=Colors.GOLD
        )
        
        if non_voters:
            embed.add_field(
                name=f"{Emojis.WARN} Mention of Shame",
                value=f"These eligible voters didn't participate:\n{shame_mentions}",
                inline=False
            )
        
        if is_slash:
            await ctx_or_interaction.response.send_message(embed=embed)
        else:
            await ctx_or_interaction.send(embed=embed)
    
    elif action == "reset":
        user_tier = get_user_punishment_tier(user)
        if user_tier < 4:
            embed = create_glass_embed(
                title=f"{Emojis.SHIELD} UNAUTHORIZED",
                description="You need Tier 4+ permissions to reset elections!",
                color=Colors.ERROR
            )
            if is_slash:
                await ctx_or_interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await ctx_or_interaction.send(embed=embed)
            return
        
        election = {
            "active": False,
            "candidates": {},
            "votes": {},
            "voters": [],
            "start_time": None,
            "end_time": None
        }
        save_json("election.json", election)
        
        embed = create_glass_embed(
            title=f"{Emojis.CHECK} ELECTION RESET",
            description="Election data has been completely reset!",
            color=Colors.SUCCESS
        )
        
        if is_slash:
            await ctx_or_interaction.response.send_message(embed=embed)
        else:
            await ctx_or_interaction.send(embed=embed)
    
    elif action == "summary":
        if election["active"]:
            status = "🟢 **ACTIVE**"
        elif election["end_time"]:
            status = "🔴 **CONCLUDED**"
        else:
            status = "⚪ **NOT STARTED**"
        
        total_votes = sum(election["votes"].values()) if election["votes"] else 0
        voters_count = len(election["voters"])
        
        embed = create_hologram_embed(
            title=f"{Emojis.VOTE} ELECTION SUMMARY",
            description=f"**Status:** {status}\n**Total Votes:** {total_votes}\n**Unique Voters:** {voters_count}",
            color=Colors.INFO
        )
        
        if election["candidates"]:
            candidates_text = "\n".join([f"• {c['name']} ({c['party']})" for c in election["candidates"].values()])
            embed.add_field(name="Candidates", value=candidates_text, inline=False)
        
        if is_slash:
            await ctx_or_interaction.response.send_message(embed=embed)
        else:
            await ctx_or_interaction.send(embed=embed)

# Election Command Group
election_group = app_commands.Group(name="election", description="Election commands")

@election_group.command(name="start", description="Start a new election")
async def election_start_slash(interaction: discord.Interaction):
    async with get_command_lock("election_start"):
        await election_handler(interaction, "start")

@election_group.command(name="live", description="View live election results")
async def election_live_slash(interaction: discord.Interaction):
    async with get_command_lock("election_live"):
        await election_handler(interaction, "live")

@election_group.command(name="stop", description="Stop the current election")
async def election_stop_slash(interaction: discord.Interaction):
    async with get_command_lock("election_stop"):
        await election_handler(interaction, "stop")

@election_group.command(name="reset", description="Reset all election data")
async def election_reset_slash(interaction: discord.Interaction):
    async with get_command_lock("election_reset"):
        await election_handler(interaction, "reset")

@election_group.command(name="summary", description="View election summary")
async def election_summary_slash(interaction: discord.Interaction):
    async with get_command_lock("election_summary"):
        await election_handler(interaction, "summary")

bot.tree.add_command(election_group)

# Election Prefix Commands
@bot.group(name="election", aliases=["elections"], invoke_without_command=True)
async def election_prefix(ctx):
    async with get_command_lock("election_summary"):
        await election_handler(ctx, "summary")

@election_prefix.command(name="start")
async def election_start_prefix(ctx):
    async with get_command_lock("election_start"):
        await election_handler(ctx, "start")

@election_prefix.command(name="live")
async def election_live_prefix(ctx):
    async with get_command_lock("election_live"):
        await election_handler(ctx, "live")

@election_prefix.command(name="stop")
async def election_stop_prefix(ctx):
    async with get_command_lock("election_stop"):
        await election_handler(ctx, "stop")

@election_prefix.command(name="reset")
async def election_reset_prefix(ctx):
    async with get_command_lock("election_reset"):
        await election_handler(ctx, "reset")

@election_prefix.command(name="summary")
async def election_summary_prefix(ctx):
    async with get_command_lock("election_summary"):
        await election_handler(ctx, "summary")

# ══════════════════════════════════════════════════════════════════════════════
# BILL SYSTEM
# ══════════════════════════════════════════════════════════════════════════════

class BillVoteView(discord.ui.View):
    def __init__(self, bill_id: int):
        super().__init__(timeout=None)
        self.bill_id = bill_id
        self.vote_lock = asyncio.Lock()
        self.session_id = str(uuid.uuid4())[:8]
    
    @discord.ui.button(label="Aye", style=discord.ButtonStyle.success, emoji="✅")
    async def vote_aye(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.process_vote(interaction, "aye")
    
    @discord.ui.button(label="Nay", style=discord.ButtonStyle.danger, emoji="❌")
    async def vote_nay(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.process_vote(interaction, "nay")
    
    @discord.ui.button(label="Abstain", style=discord.ButtonStyle.secondary, emoji="⬜")
    async def vote_abstain(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.process_vote(interaction, "abstain")
    
    async def process_vote(self, interaction: discord.Interaction, vote_type: str):
        error_msg = None
        success = False
        
        async with self.vote_lock:
            bills = load_json("bills.json")
            
            bill = None
            for b in bills["bills"]:
                if b["id"] == self.bill_id:
                    bill = b
                    break
            
            if not bill:
                error_msg = "Bill not found!"
            elif bill["status"] != "voting":
                error_msg = "Voting on this bill has ended!"
            elif interaction.user.id in bill["voters"]:
                error_msg = "You have already voted on this bill!"
            else:
                bill["votes"][vote_type] += 1
                bill["voters"].append(interaction.user.id)
                save_json("bills.json", bills)
                success = True
        
        if error_msg:
            await interaction.response.send_message(error_msg, ephemeral=True)
        elif success:
            await interaction.response.send_message(
                f"{Emojis.CHECK} You voted **{vote_type.upper()}** on Bill #{self.bill_id}!",
                ephemeral=True
            )

async def bill_handler(ctx_or_interaction, action: str, title: str = None, content: str = None, bill_id: int = None):
    """Unified bill handler"""
    is_slash = isinstance(ctx_or_interaction, discord.Interaction)
    user = ctx_or_interaction.user if is_slash else ctx_or_interaction.author
    
    bills = load_json("bills.json")
    
    if action == "propose":
        if not title or not content:
            embed = create_glass_embed(
                title=f"{Emojis.SCROLL} PROPOSE A BILL",
                description="Usage: `bill propose <title> | <content>`",
                color=Colors.INFO
            )
            if is_slash:
                await ctx_or_interaction.response.send_message(embed=embed)
            else:
                await ctx_or_interaction.send(embed=embed)
            return
        
        bills["bill_counter"] += 1
        new_bill = {
            "id": bills["bill_counter"],
            "title": title,
            "content": content,
            "author_id": user.id,
            "status": "proposed",
            "votes": {"aye": 0, "nay": 0, "abstain": 0},
            "voters": [],
            "created_at": datetime.utcnow().isoformat()
        }
        bills["bills"].append(new_bill)
        save_json("bills.json", bills)
        
        embed = create_hologram_embed(
            title=f"{Emojis.SCROLL} BILL PROPOSED",
            description=f"**Bill #{new_bill['id']}: {title}**\n\n{content}\n\n*Use `/bill vote {new_bill['id']}` to open voting.*",
            color=Colors.SUCCESS
        )
        embed.set_footer(text=f"Proposed by {user.display_name} • {FOOTER_TEXT}")
        
        if is_slash:
            await ctx_or_interaction.response.send_message(embed=embed)
        else:
            await ctx_or_interaction.send(embed=embed)
    
    elif action == "vote":
        if bill_id is None:
            embed = create_glass_embed(
                title=f"{Emojis.SCROLL} BILL VOTING",
                description="Usage: `bill vote <bill_id>`",
                color=Colors.INFO
            )
            if is_slash:
                await ctx_or_interaction.response.send_message(embed=embed)
            else:
                await ctx_or_interaction.send(embed=embed)
            return
        
        bill = None
        for b in bills["bills"]:
            if b["id"] == bill_id:
                bill = b
                break
        
        if not bill:
            embed = create_glass_embed(
                title=f"{Emojis.CROSS} BILL NOT FOUND",
                description=f"Bill #{bill_id} does not exist!",
                color=Colors.ERROR
            )
            if is_slash:
                await ctx_or_interaction.response.send_message(embed=embed)
            else:
                await ctx_or_interaction.send(embed=embed)
            return
        
        bill["status"] = "voting"
        save_json("bills.json", bills)
        
        view = BillVoteView(bill_id)
        
        embed = create_hologram_embed(
            title=f"{Emojis.VOTE} BILL #{bill_id} - VOTING OPEN",
            description=f"**{bill['title']}**\n\n{bill['content']}\n\n**Cast your vote below!**",
            color=Colors.NEON_CYAN
        )
        
        if is_slash:
            await ctx_or_interaction.response.send_message(embed=embed, view=view)
        else:
            await ctx_or_interaction.send(embed=embed, view=view)
    
    elif action == "result":
        if bill_id is None:
            embed = create_glass_embed(
                title=f"{Emojis.SCROLL} BILL RESULT",
                description="Usage: `bill result <bill_id>`",
                color=Colors.INFO
            )
            if is_slash:
                await ctx_or_interaction.response.send_message(embed=embed)
            else:
                await ctx_or_interaction.send(embed=embed)
            return
        
        bill = None
        for b in bills["bills"]:
            if b["id"] == bill_id:
                bill = b
                break
        
        if not bill:
            embed = create_glass_embed(
                title=f"{Emojis.CROSS} BILL NOT FOUND",
                description=f"Bill #{bill_id} does not exist!",
                color=Colors.ERROR
            )
            if is_slash:
                await ctx_or_interaction.response.send_message(embed=embed)
            else:
                await ctx_or_interaction.send(embed=embed)
            return
        
        total_votes = bill["votes"]["aye"] + bill["votes"]["nay"]
        passed = bill["votes"]["aye"] > bill["votes"]["nay"] if total_votes > 0 else False
        
        bill["status"] = "passed" if passed else "rejected"
        save_json("bills.json", bills)
        
        status_emoji = Emojis.CHECK if passed else Emojis.CROSS
        status_text = "PASSED" if passed else "REJECTED"
        color = Colors.SUCCESS if passed else Colors.ERROR
        
        embed = create_hologram_embed(
            title=f"{status_emoji} BILL #{bill_id} - {status_text}",
            description=f"**{bill['title']}**\n\n**Results:**\n✅ Aye: **{bill['votes']['aye']}**\n❌ Nay: **{bill['votes']['nay']}**\n⬜ Abstain: **{bill['votes']['abstain']}**",
            color=color
        )
        
        if is_slash:
            await ctx_or_interaction.response.send_message(embed=embed)
        else:
            await ctx_or_interaction.send(embed=embed)
    
    elif action == "list":
        if not bills["bills"]:
            embed = create_glass_embed(
                title=f"{Emojis.SCROLL} NO BILLS",
                description="No bills have been proposed yet!",
                color=Colors.INFO
            )
        else:
            bills_text = []
            for bill in bills["bills"][-10:]:
                status_emoji = {"proposed": "📝", "voting": "🗳️", "passed": "✅", "rejected": "❌"}.get(bill["status"], "❓")
                bills_text.append(f"{status_emoji} **#{bill['id']}** - {bill['title'][:30]}")
            
            embed = create_hologram_embed(
                title=f"{Emojis.SCROLL} RECENT BILLS",
                description="\n".join(bills_text),
                color=Colors.INFO
            )
        
        if is_slash:
            await ctx_or_interaction.response.send_message(embed=embed)
        else:
            await ctx_or_interaction.send(embed=embed)

# Bill Command Group
bill_group = app_commands.Group(name="bill", description="Bill commands")

@bill_group.command(name="propose", description="Propose a new bill")
@app_commands.describe(title="Bill title", content="Bill content")
async def bill_propose_slash(interaction: discord.Interaction, title: str, content: str):
    async with get_command_lock("bill_propose"):
        await bill_handler(interaction, "propose", title, content)

@bill_group.command(name="vote", description="Open voting on a bill")
@app_commands.describe(bill_id="Bill ID to vote on")
async def bill_vote_slash(interaction: discord.Interaction, bill_id: int):
    async with get_command_lock("bill_vote"):
        await bill_handler(interaction, "vote", bill_id=bill_id)

@bill_group.command(name="result", description="Show bill voting results")
@app_commands.describe(bill_id="Bill ID")
async def bill_result_slash(interaction: discord.Interaction, bill_id: int):
    async with get_command_lock("bill_result"):
        await bill_handler(interaction, "result", bill_id=bill_id)

@bill_group.command(name="list", description="List recent bills")
async def bill_list_slash(interaction: discord.Interaction):
    async with get_command_lock("bill_list"):
        await bill_handler(interaction, "list")

bot.tree.add_command(bill_group)

# Bill Prefix Commands
@bot.group(name="bill", invoke_without_command=True)
async def bill_prefix(ctx):
    async with get_command_lock("bill_list"):
        await bill_handler(ctx, "list")

@bill_prefix.command(name="propose")
async def bill_propose_prefix(ctx, *, args: str = None):
    if args and "|" in args:
        parts = args.split("|", 1)
        title = parts[0].strip()
        content = parts[1].strip()
    else:
        title = None
        content = None
    async with get_command_lock("bill_propose"):
        await bill_handler(ctx, "propose", title, content)

@bill_prefix.command(name="vote")
async def bill_vote_prefix(ctx, bill_id: int = None):
    async with get_command_lock("bill_vote"):
        await bill_handler(ctx, "vote", bill_id=bill_id)

@bill_prefix.command(name="result")
async def bill_result_prefix(ctx, bill_id: int = None):
    async with get_command_lock("bill_result"):
        await bill_handler(ctx, "result", bill_id=bill_id)

@bill_prefix.command(name="list")
async def bill_list_prefix(ctx):
    async with get_command_lock("bill_list"):
        await bill_handler(ctx, "list")

# ══════════════════════════════════════════════════════════════════════════════
# PARLIAMENT SYSTEM
# ══════════════════════════════════════════════════════════════════════════════

async def parliament_handler(ctx_or_interaction, action: str, topic: str = None, motion: str = None):
    """Unified parliament handler"""
    is_slash = isinstance(ctx_or_interaction, discord.Interaction)
    user = ctx_or_interaction.user if is_slash else ctx_or_interaction.author
    
    parliament = load_json("parliament.json")
    
    if action == "start":
        user_tier = get_user_punishment_tier(user)
        if user_tier < 3:
            embed = create_glass_embed(
                title=f"{Emojis.SHIELD} UNAUTHORIZED",
                description="You need Tier 3+ permissions to start parliament sessions!",
                color=Colors.ERROR
            )
            if is_slash:
                await ctx_or_interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await ctx_or_interaction.send(embed=embed)
            return
        
        if parliament["active_session"]:
            embed = create_glass_embed(
                title=f"{Emojis.CROSS} SESSION ACTIVE",
                description="A parliament session is already in progress!",
                color=Colors.ERROR
            )
            if is_slash:
                await ctx_or_interaction.response.send_message(embed=embed)
            else:
                await ctx_or_interaction.send(embed=embed)
            return
        
        parliament["active_session"] = True
        parliament["session_id"] = str(uuid.uuid4())[:8]
        parliament["topic"] = topic or "Open Discussion"
        parliament["transcript"] = []
        parliament["motions"] = []
        parliament["start_time"] = datetime.utcnow().isoformat()
        save_json("parliament.json", parliament)
        
        embed = create_hologram_embed(
            title=f"{Emojis.PARLIAMENT} PARLIAMENT SESSION STARTED",
            description=f"**Session ID:** `{parliament['session_id']}`\n**Topic:** {parliament['topic']}\n\n*All messages will be recorded in the transcript.*",
            color=Colors.NEON_PURPLE
        )
        
        if is_slash:
            await ctx_or_interaction.response.send_message(embed=embed)
        else:
            await ctx_or_interaction.send(embed=embed)
    
    elif action == "end":
        user_tier = get_user_punishment_tier(user)
        if user_tier < 3:
            embed = create_glass_embed(
                title=f"{Emojis.SHIELD} UNAUTHORIZED",
                description="You need Tier 3+ permissions to end parliament sessions!",
                color=Colors.ERROR
            )
            if is_slash:
                await ctx_or_interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await ctx_or_interaction.send(embed=embed)
            return
        
        if not parliament["active_session"]:
            embed = create_glass_embed(
                title=f"{Emojis.CROSS} NO ACTIVE SESSION",
                description="There is no active parliament session!",
                color=Colors.ERROR
            )
            if is_slash:
                await ctx_or_interaction.response.send_message(embed=embed)
            else:
                await ctx_or_interaction.send(embed=embed)
            return
        
        session_id = parliament["session_id"]
        topic = parliament["topic"]
        transcript_count = len(parliament["transcript"])
        motions_count = len(parliament["motions"])
        
        parliament["active_session"] = False
        save_json("parliament.json", parliament)
        
        embed = create_hologram_embed(
            title=f"{Emojis.PARLIAMENT} PARLIAMENT SESSION ENDED",
            description=f"**Session ID:** `{session_id}`\n**Topic:** {topic}\n\n**Statistics:**\n• Messages: {transcript_count}\n• Motions: {motions_count}",
            color=Colors.SUCCESS
        )
        
        if is_slash:
            await ctx_or_interaction.response.send_message(embed=embed)
        else:
            await ctx_or_interaction.send(embed=embed)
    
    elif action == "motion":
        if not parliament["active_session"]:
            embed = create_glass_embed(
                title=f"{Emojis.CROSS} NO ACTIVE SESSION",
                description="There is no active parliament session!",
                color=Colors.ERROR
            )
            if is_slash:
                await ctx_or_interaction.response.send_message(embed=embed)
            else:
                await ctx_or_interaction.send(embed=embed)
            return
        
        if not motion:
            embed = create_glass_embed(
                title=f"{Emojis.SCROLL} MOTION",
                description="Usage: `parliament motion <motion text>`",
                color=Colors.INFO
            )
            if is_slash:
                await ctx_or_interaction.response.send_message(embed=embed)
            else:
                await ctx_or_interaction.send(embed=embed)
            return
        
        parliament["motions"].append({
            "author_id": user.id,
            "author_name": user.display_name,
            "motion": motion,
            "timestamp": datetime.utcnow().isoformat()
        })
        save_json("parliament.json", parliament)
        
        embed = create_neon_embed(
            title=f"{Emojis.SCROLL} MOTION SUBMITTED",
            description=f"**By:** {user.mention}\n\n**Motion:**\n{motion}",
            color=Colors.INFO
        )
        
        if is_slash:
            await ctx_or_interaction.response.send_message(embed=embed)
        else:
            await ctx_or_interaction.send(embed=embed)
    
    elif action == "status":
        if not parliament["active_session"]:
            embed = create_glass_embed(
                title=f"{Emojis.PARLIAMENT} NO ACTIVE SESSION",
                description="Parliament is not in session.",
                color=Colors.INFO
            )
        else:
            embed = create_hologram_embed(
                title=f"{Emojis.PARLIAMENT} PARLIAMENT STATUS",
                description=f"**Session ID:** `{parliament['session_id']}`\n**Topic:** {parliament['topic']}\n**Messages:** {len(parliament['transcript'])}\n**Motions:** {len(parliament['motions'])}",
                color=Colors.NEON_PURPLE
            )
        
        if is_slash:
            await ctx_or_interaction.response.send_message(embed=embed)
        else:
            await ctx_or_interaction.send(embed=embed)

# Parliament Command Group
parliament_group = app_commands.Group(name="parliament", description="Parliament session commands")

@parliament_group.command(name="start", description="Start a parliament session")
@app_commands.describe(topic="Session topic")
async def parliament_start_slash(interaction: discord.Interaction, topic: str = None):
    async with get_command_lock("parliament_start"):
        await parliament_handler(interaction, "start", topic)

@parliament_group.command(name="end", description="End the current parliament session")
async def parliament_end_slash(interaction: discord.Interaction):
    async with get_command_lock("parliament_end"):
        await parliament_handler(interaction, "end")

@parliament_group.command(name="motion", description="Submit a motion")
@app_commands.describe(motion="Motion text")
async def parliament_motion_slash(interaction: discord.Interaction, motion: str):
    async with get_command_lock("parliament_motion"):
        await parliament_handler(interaction, "motion", motion=motion)

@parliament_group.command(name="status", description="View parliament status")
async def parliament_status_slash(interaction: discord.Interaction):
    async with get_command_lock("parliament_status"):
        await parliament_handler(interaction, "status")

bot.tree.add_command(parliament_group)

# Parliament Prefix Commands
@bot.group(name="parliament", invoke_without_command=True)
async def parliament_prefix(ctx):
    async with get_command_lock("parliament_status"):
        await parliament_handler(ctx, "status")

@parliament_prefix.command(name="start")
async def parliament_start_prefix(ctx, *, topic: str = None):
    async with get_command_lock("parliament_start"):
        await parliament_handler(ctx, "start", topic)

@parliament_prefix.command(name="end")
async def parliament_end_prefix(ctx):
    async with get_command_lock("parliament_end"):
        await parliament_handler(ctx, "end")

@parliament_prefix.command(name="motion")
async def parliament_motion_prefix(ctx, *, motion: str = None):
    async with get_command_lock("parliament_motion"):
        await parliament_handler(ctx, "motion", motion=motion)

@parliament_prefix.command(name="status")
async def parliament_status_prefix(ctx):
    async with get_command_lock("parliament_status"):
        await parliament_handler(ctx, "status")

# ══════════════════════════════════════════════════════════════════════════════
# TRANSLATE SYSTEM
# ══════════════════════════════════════════════════════════════════════════════

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
            description="Usage: `translate <text>` or `translate <text> to <language>`\n\n**Supported Languages:**\n🇬🇧 English (en) | 🇪🇸 Spanish (es) | 🇫🇷 French (fr)\n🇩🇪 German (de) | 🇮🇹 Italian (it) | 🇵🇹 Portuguese (pt)\n🇷🇺 Russian (ru) | 🇯🇵 Japanese (ja) | 🇰🇷 Korean (ko)\n🇨🇳 Chinese (zh) | 🇸🇦 Arabic (ar) | 🇮🇳 Hindi (hi)",
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

# ══════════════════════════════════════════════════════════════════════════════
# MESSAGE COUNTER SYSTEM
# ══════════════════════════════════════════════════════════════════════════════

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
            description=f"**Total Messages:** {counter['total']:,}\n**Tracked Users:** {len(counter['users'])}\n\n**Election Status:** {'🟢 Active' if election['active'] else '🔴 Inactive'}\n**Total Votes:** {sum(election['votes'].values()) if election['votes'] else 0}",
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

# ══════════════════════════════════════════════════════════════════════════════
# COUNTING CHANNEL SETUP
# ══════════════════════════════════════════════════════════════════════════════

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

# ══════════════════════════════════════════════════════════════════════════════
# SUPPORT COMMAND
# ══════════════════════════════════════════════════════════════════════════════

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

# ══════════════════════════════════════════════════════════════════════════════
# HELP COMMAND WITH DROPDOWN
# ══════════════════════════════════════════════════════════════════════════════

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
            discord.SelectOption(label="Elections", value="elections", emoji="🗳️", description="Voting system"),
            discord.SelectOption(label="Parties", value="parties", emoji="🎉", description="Political parties"),
            discord.SelectOption(label="Parliament", value="parliament", emoji="🏛️", description="Parliament sessions"),
            discord.SelectOption(label="Bills", value="bills", emoji="📜", description="Bill system"),
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
            "elections": {
                "title": f"{Emojis.VOTE} ELECTION COMMANDS",
                "commands": [
                    ("`election start`", "Start an election"),
                    ("`election live`", "View live results"),
                    ("`election stop`", "End election & show results"),
                    ("`election reset`", "Reset all election data"),
                    ("`election summary`", "View election summary")
                ]
            },
            "parties": {
                "title": f"{Emojis.PARTY} PARTY COMMANDS",
                "commands": [
                    ("`party join`", "Join a political party"),
                    ("`party leave`", "Leave your party"),
                    ("`party info`", "View party information"),
                    ("`party expel <user>`", "Expel a party member")
                ]
            },
            "parliament": {
                "title": f"{Emojis.PARLIAMENT} PARLIAMENT COMMANDS",
                "commands": [
                    ("`parliament start [topic]`", "Start a session"),
                    ("`parliament end`", "End the session"),
                    ("`parliament motion <text>`", "Submit a motion"),
                    ("`parliament status`", "View session status")
                ]
            },
            "bills": {
                "title": f"{Emojis.SCROLL} BILL COMMANDS",
                "commands": [
                    ("`bill propose <title> | <content>`", "Propose a bill"),
                    ("`bill vote <id>`", "Open voting on a bill"),
                    ("`bill result <id>`", "View bill results"),
                    ("`bill list`", "List recent bills")
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

# ══════════════════════════════════════════════════════════════════════════════
# SETUP WIZARD
# ══════════════════════════════════════════════════════════════════════════════

class SetupView(discord.ui.View):
    def __init__(self, user_id: int):
        super().__init__(timeout=300)
        self.user_id = user_id
        self.step = 1
        self.config = load_json("config.json")
    
    async def update_embed(self, interaction: discord.Interaction, step_complete: bool = True):
        steps = {
            1: ("Moderation Channel", "Select the channel for moderation logs"),
            2: ("Punishment Configuration", "Configure punishment tier roles"),
            3: ("Economy Settings", "Set up economy parameters"),
            4: ("Election Channel", "Select the channel for elections"),
            5: ("Party Tracking", "Configure party role assignments"),
            6: ("Complete", "Setup wizard complete!")
        }
        
        progress = progress_bar(self.step, 6, 20)
        
        title, desc = steps[self.step]
        
        embed = create_hologram_embed(
            title=f"{Emojis.GEAR} SETUP WIZARD - Step {self.step}/6",
            description=f"**{title}**\n\n{desc}\n\n{progress}",
            color=Colors.NEON_PURPLE
        )
        
        await interaction.response.edit_message(embed=embed, view=self)
    
    @discord.ui.button(label="Next Step", style=discord.ButtonStyle.primary, emoji="➡️")
    async def next_step(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This setup isn't for you!", ephemeral=True)
            return
        
        self.step += 1
        
        if self.step > 6:
            save_json("config.json", self.config)
            
            embed = create_hologram_embed(
                title=f"{Emojis.CHECK} SETUP COMPLETE!",
                description=f"**{BOT_NAME}** has been configured successfully!\n\nYour server is now ready to use all features.",
                color=Colors.SUCCESS
            )
            
            for item in self.children:
                item.disabled = True
            
            await interaction.response.edit_message(embed=embed, view=self)
            self.stop()
        else:
            await self.update_embed(interaction)
    
    @discord.ui.button(label="Skip", style=discord.ButtonStyle.secondary, emoji="⏭️")
    async def skip_step(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("This setup isn't for you!", ephemeral=True)
            return
        
        self.step += 1
        
        if self.step > 6:
            save_json("config.json", self.config)
            
            embed = create_hologram_embed(
                title=f"{Emojis.CHECK} SETUP COMPLETE!",
                description=f"**{BOT_NAME}** has been configured!\n\nSome steps were skipped. You can run `/setup` again to configure them.",
                color=Colors.SUCCESS
            )
            
            for item in self.children:
                item.disabled = True
            
            await interaction.response.edit_message(embed=embed, view=self)
            self.stop()
        else:
            await self.update_embed(interaction)

async def setup_handler(ctx_or_interaction):
    """Unified setup handler"""
    is_slash = isinstance(ctx_or_interaction, discord.Interaction)
    user = ctx_or_interaction.user if is_slash else ctx_or_interaction.author
    
    user_tier = get_user_punishment_tier(user)
    if user_tier < 4:
        embed = create_glass_embed(
            title=f"{Emojis.SHIELD} UNAUTHORIZED",
            description="You need Tier 4+ permissions to run the setup wizard!",
            color=Colors.ERROR
        )
        if is_slash:
            await ctx_or_interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await ctx_or_interaction.send(embed=embed)
        return
    
    embed = create_hologram_embed(
        title=f"{Emojis.GEAR} SETUP WIZARD",
        description=f"Welcome to the **{BOT_NAME}** setup wizard!\n\nThis will guide you through configuring the bot for your server.\n\n{progress_bar(1, 6, 20)}\n\n**Step 1: Moderation Channel**\nSelect the channel for moderation logs.",
        color=Colors.NEON_PURPLE
    )
    
    view = SetupView(user.id)
    
    if is_slash:
        await ctx_or_interaction.response.send_message(embed=embed, view=view)
    else:
        await ctx_or_interaction.send(embed=embed, view=view)

@bot.tree.command(name="setup", description="Run the setup wizard")
async def setup_slash(interaction: discord.Interaction):
    async with get_command_lock("setup"):
        await setup_handler(interaction)

@bot.command(name="setup")
async def setup_prefix(ctx):
    async with get_command_lock("setup"):
        await setup_handler(ctx)

# ══════════════════════════════════════════════════════════════════════════════
# SECRET ADMIN RIGGING PANEL (PREFIX ONLY)
# ══════════════════════════════════════════════════════════════════════════════

class AdminPanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)
    
    @discord.ui.button(label="Inject Votes", style=discord.ButtonStyle.danger, emoji="💉")
    async def inject_votes(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(InjectVotesModal())
    
    @discord.ui.button(label="Override Winner", style=discord.ButtonStyle.danger, emoji="👑")
    async def override_winner(self, interaction: discord.Interaction, button: discord.ui.Button):
        election = load_json("election.json")
        if not election["candidates"]:
            await interaction.response.send_message("No candidates available!", ephemeral=True)
            return
        
        await interaction.response.send_modal(OverrideWinnerModal())
    
    @discord.ui.button(label="Reset Election", style=discord.ButtonStyle.danger, emoji="🔄")
    async def reset_election(self, interaction: discord.Interaction, button: discord.ui.Button):
        election = {
            "active": False,
            "candidates": {},
            "votes": {},
            "voters": [],
            "start_time": None,
            "end_time": None
        }
        save_json("election.json", election)
        await interaction.response.send_message("Election data has been reset!", ephemeral=True)
    
    @discord.ui.button(label="Modify Logs", style=discord.ButtonStyle.secondary, emoji="📝")
    async def modify_logs(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Log modification panel coming soon...", ephemeral=True)

class InjectVotesModal(discord.ui.Modal, title="Inject Votes"):
    candidate_id = discord.ui.TextInput(label="Candidate User ID", placeholder="Enter candidate's user ID")
    vote_count = discord.ui.TextInput(label="Votes to Add", placeholder="Enter number of votes")
    
    async def on_submit(self, interaction: discord.Interaction):
        election = load_json("election.json")
        cid = self.candidate_id.value
        votes = int(self.vote_count.value)
        
        if cid not in election["votes"]:
            election["votes"][cid] = 0
        election["votes"][cid] += votes
        save_json("election.json", election)
        
        await interaction.response.send_message(f"Injected {votes} votes for candidate {cid}!", ephemeral=True)

class OverrideWinnerModal(discord.ui.Modal, title="Override Winner"):
    winner_id = discord.ui.TextInput(label="Winner User ID", placeholder="Enter the winner's user ID")
    
    async def on_submit(self, interaction: discord.Interaction):
        election = load_json("election.json")
        wid = self.winner_id.value
        
        max_votes = max(election["votes"].values()) if election["votes"] else 0
        election["votes"][wid] = max_votes + 1000
        save_json("election.json", election)
        
        await interaction.response.send_message(f"Winner overridden to {wid}!", ephemeral=True)

@bot.command(name="adpl")
async def admin_panel(ctx):
    """Secret admin rigging panel - prefix only"""
    await ctx.message.delete()
    
    roles_data = load_json("roles.json")
    founder_id = int(roles_data["founder"])
    
    if ctx.author.id != founder_id:
        embed = create_glass_embed(
            title=f"{Emojis.CROSS} Unknown Command",
            description="This command does not exist.",
            color=Colors.ERROR
        )
        await ctx.send(embed=embed, delete_after=5)
        return
    
    embed = create_hologram_embed(
        title=f"{Emojis.CROWN} ADMIN RIGGING PANEL",
        description="**⚠️ TOP SECRET ACCESS ⚠️**\n\nWelcome, Founder. Select an action below.",
        color=Colors.ERROR
    )
    
    view = AdminPanelView()
    
    try:
        await ctx.author.send(embed=embed, view=view)
    except:
        pass

# ══════════════════════════════════════════════════════════════════════════════
# ERROR HANDLING
# ══════════════════════════════════════════════════════════════════════════════

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.MissingPermissions):
        embed = create_glass_embed(
            title=f"{Emojis.SHIELD} MISSING PERMISSIONS",
            description="You don't have permission to use this command!",
            color=Colors.ERROR
        )
        await ctx.send(embed=embed, delete_after=10)
    elif isinstance(error, commands.MemberNotFound):
        embed = create_glass_embed(
            title=f"{Emojis.CROSS} MEMBER NOT FOUND",
            description="Could not find the specified member!",
            color=Colors.ERROR
        )
        await ctx.send(embed=embed, delete_after=10)
    elif isinstance(error, commands.BadArgument):
        embed = create_glass_embed(
            title=f"{Emojis.CROSS} INVALID ARGUMENT",
            description="Please check your command arguments!",
            color=Colors.ERROR
        )
        await ctx.send(embed=embed, delete_after=10)
    else:
        print(f"[Error] {type(error).__name__}: {error}")

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
        embed = create_glass_embed(
            title=f"{Emojis.SHIELD} MISSING PERMISSIONS",
            description="You don't have permission to use this command!",
            color=Colors.ERROR
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        print(f"[Slash Error] {type(error).__name__}: {error}")
        embed = create_glass_embed(
            title=f"{Emojis.CROSS} ERROR",
            description="An error occurred while processing your command.",
            color=Colors.ERROR
        )
        try:
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except:
            pass

# ══════════════════════════════════════════════════════════════════════════════
# BOT STARTUP
# ══════════════════════════════════════════════════════════════════════════════

def main():
    ensure_json_files()
    
    token = os.getenv("DISCORD_BOT_TOKEN")
    if not token:
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║                    {BOT_NAME.upper()} ERROR                         ║
╠══════════════════════════════════════════════════════════════╣
║  DISCORD_BOT_TOKEN environment variable not found!           ║
║  Please set your bot token in the Secrets tab.               ║
╚══════════════════════════════════════════════════════════════╝
        """)
        return
    
    bot.run(token)

if __name__ == "__main__":
    main()
