# Elura Utility Discord Bot

## Overview
Elura Utility is a premium, trillion-dollar UI Discord bot powered by the Aurora Engine. It features advanced political systems, economy, casino games, moderation, and party management - all in a single Python file.

## Project Structure
```
/
├── bot.py              # Main bot file (single file architecture)
├── requirements.txt    # Python dependencies
├── roles.json          # Role ID storage (auto-generated)
├── config.json         # Server configuration (auto-generated)
├── economy.json        # Economy data (auto-generated)
├── casino.json         # Casino sessions/stats (auto-generated)
├── punishments.json    # Punishment cases (auto-generated)
├── election.json       # Election data (auto-generated)
├── vote_data.json      # Bill votes/sessions (auto-generated)
├── communist.json      # Communist party data (auto-generated)
├── republic.json       # Republic party data (auto-generated)
├── democratic.json     # Democratic party data (auto-generated)
├── message_counter.json # Message tracking (auto-generated)
├── support.json        # Support link config (auto-generated)
├── gtw_words.json      # GTW game prompts (auto-generated)
├── gyi_words.json      # GYI game word pairs (auto-generated)
├── games_stats.json    # Game leaderboards (auto-generated)
├── parliament.json     # Parliament sessions (auto-generated)
└── bills.json          # Bills data (auto-generated)
```

## Features

### Economy System
- Wallet, bank, deposit, withdraw
- Work, crime, daily, weekly rewards
- Cooldowns and multipliers
- JSON storage with premium UI

### Casino Games
- Coinflip, Blackjack, Slots
- Roulette, Dice Duel, Crash
- Anti-spam and session locks
- Win/loss tracking

### Fun Games
- Trivia, Hangman, Number Guess, RPS
- GTW (Guess The Word) - Impostor-style game
- GYI (Guess Your Impostor) - Word description game
- 3+ player social games with voting

### Moderation (Tier-based)
- Warn/unwarn/warnings
- Mute/unmute with timeout
- Kick, softban, ban/unban
- Case IDs and DM alerts
- Tier 1-5 permission system

### Political System
- 3 parties: Communist, Republic, Democratic
- Join/leave/info/expel commands
- Executive tracking (President, VP, GS)
- Party leaders can expel members

### Election System
- Start/stop/reset elections
- Live vote tallies
- Dropdown voting with anti-double-vote
- Mention of Shame for non-voters
- Animated progress bars

### Bill & Parliament
- Bill propose/vote/debate/result
- Parliament sessions with transcripts
- Motion submissions
- Session management

### Utility
- Translation (auto-detect to English)
- Message counter with leaderboard
- Counting channel with +1 enforcement
- Wick-style setup wizard

## Commands
All commands support both:
- Slash commands: `/command`
- Prefix commands: `eu command` or `elura command`

## Configuration
The bot requires a `DISCORD_BOT_TOKEN` secret to run. All JSON files are auto-generated on startup with default values.

## UI Design
Aurora Engine Hybrid UI (Mode 3):
- Glassmorphism panels
- Neon borders and accents
- Animated progress bars
- Holographic aesthetics
- Footer watermark: "Elura Utility • Aurora Engine"

## Recent Changes
- Initial bot creation with all systems
- Single-file architecture for easy deployment
- Zero duplicate response policy with asyncio locks
- Idempotency tokens for UI interactions

## User Preferences
- All in one file (no cogs)
- JSON storage for persistence
- Premium trillion-dollar UI aesthetic
- Dual prefix support (eu/elura)
