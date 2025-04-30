import os
import random
from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8118975932:AAEx5L5lnJTxncPKmlqud4j08qv0Y4m7fIQ"

RIDDLES = {
    "riddle1": {
        "question": "I am concealed in what you seek, yet I'm right before your eyes. I am what connects the beginning to the end, but not what's in between. What ASCII value am I?",
        "answer": "123",
        "flag": "M3D{0p3n_cUrLy_br4c3}"
    },
    "riddle2": {
        "question": "Solve this cryptarithmetic puzzle: SEND + MORE = MONEY (Each letter represents a unique digit from 0-9)",
        "answer": "s=9,e=5,n=6,d=7,m=1,o=0,r=8,y=2",
        "flag": "M3D{9567+1085=10652}"
    },
    "riddle3": {
        "question": "Find the missing 5-letter word: 'I am a fruit when whole. Remove my first letter, I'm a crime. Remove my first two letters, I'm an animal. Remove my first and last letters, I'm a form of music.' What am I?",
        "answer": "grape",
        "flag": "M3D{gr4p3_m3t4m0rph0s1s}"
    },
    "riddle4": {
        "question": "What's the next sequence in this pattern?: 10, 11, 12, 13, 14, 15, 16, 17, 20, 21, 22...",
        "answer": "23",
        "flag": "M3D{0ct4l_5y5t3m_h4ck3r}"
    },
    "riddle5": {
        "question": "Decrypt this: '76 61 70 6F 72 77 61 76 65' (Hint: It's not ASCII directly)",
        "answer": "vaporwave",
        "flag": "M3D{h3x_2_4sc11_c0nv3rt3r}"
    },
    "riddle6": {
        "question": "I am a 4-digit number. My first digit is 4 times my second digit. My third digit is 3 more than my second digit. My last digit is twice my third digit. What number am I?",
        "answer": "8362",
        "flag": "M3D{l0g1c4l_numb3r_r3l4t10n5}"
    },
    "riddle7": {
        "question": "Using only the letters ABCDEFG and each letter exactly once, what 7-letter English word can you form that is related to computer security?",
        "answer": "defaced",
        "flag": "M3D{w3b51t3_d3f4c3d_ch4ll3ng3}"
    },
    "riddle8": {
        "question": "I'm hiding in plain sight. The key is: 'The quick brown fox jumps over the lazy dog'. The lock is: 'kyv hlztb sifne wfo aldgj fmvi kyv crqp ufx'. What's the secret?",
        "answer": "atbash",
        "flag": "M3D{r3v3rs3_4lph4b3t_c1ph3r}"
    },
    "riddle9": {
        "question": "Compute the SHA-256 hash of 'cybersecurity' and give me only the first 6 characters of the hash.",
        "answer": "f99a2e",
        "flag": "M3D{h4sh_c0l1s10n_ma5t3r}"
    },
    "riddle10": {
        "question": "What 5-letter word becomes shorter when you add two letters to it?",
        "answer": "short",
        "flag": "M3D{w0rd_p4r4d0x_l0g1c}"
    },
    "riddle11": {
        "question": "What's the value of the following expression? 2^(2^(2^0)) - 1",
        "answer": "15",
        "flag": "M3D{3xp0n3nt14l_t0w3r_s0lv3r}"
    },
    "riddle12": {
        "question": "What is the next line in this pattern?\n1\n11\n21\n1211\n111221\n?",
        "answer": "312211",
        "flag": "M3D{l00k_4nd_s4y_s3qu3nc3}"
    }
}

# Store active user riddles
user_riddles = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when the command /start is issued."""
    await update.message.reply_text(
        "🔒 *Welcome to the CTF Riddle Bot*\n\n"
        "Test your problem-solving skills with these challenges:\n"
        "• Use /riddle to get a random riddle\n"
        "• Use /answer [your_answer] to submit your answer\n"
        "• Use /help to see all available commands\n\n"
        "Good luck, hacker! 🕵️‍♂️",
        parse_mode="Markdown"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send help info when the command /help is issued."""
    await update.message.reply_text(
        "*CTF Riddle Bot Commands:*\n\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/riddle - Get a random riddle\n"
        "/answer [your_answer] - Submit your answer\n"
        "/hint - Get a hint for the current riddle\n"
        "/skip - Skip the current riddle\n"
        "/status - Check your progress",
        parse_mode="Markdown"
    )

async def riddle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a random riddle to the user."""
    user_id = update.effective_user.id
    
    # Select a random riddle
    riddle_id = random.choice(list(RIDDLES.keys()))
    riddle_data = RIDDLES[riddle_id]
    
    # Store the current riddle for this user
    user_riddles[user_id] = {
        "riddle_id": riddle_id,
        "attempts": 0
    }
    
    await update.message.reply_text(
        f"🧩 *Riddle Challenge*\n\n{riddle_data['question']}\n\n"
        "Reply with /answer [your_answer]",
        parse_mode="Markdown"
    )

async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Check the user's answer to the riddle."""
    user_id = update.effective_user.id
    
    # Check if the user has an active riddle
    if user_id not in user_riddles:
        await update.message.reply_text(
            "You don't have an active riddle. Use /riddle to get one."
        )
        return
    
    # Get user's active riddle
    riddle_id = user_riddles[user_id]["riddle_id"]
    riddle_data = RIDDLES[riddle_id]
    
    # Increment attempt counter
    user_riddles[user_id]["attempts"] += 1
    
    # Get the user's answer
    try:
        user_answer = ' '.join(context.args).lower().strip()
    except IndexError:
        await update.message.reply_text("Please provide an answer. Format: /answer [your_answer]")
        return
    
    # Check the answer
    if user_answer == riddle_data["answer"]:
        attempts = user_riddles[user_id]["attempts"]
        del user_riddles[user_id]  # Remove the solved riddle
        
        await update.message.reply_text(
            f"🎉 *Correct!*\n\n"
            f"You solved it in {attempts} attempts.\n\n"
            f"Flag: `{riddle_data['flag']}`\n\n"
            f"Type /riddle for another challenge.",
            parse_mode="Markdown"
        )
    else:
        attempts = user_riddles[user_id]["attempts"]
        await update.message.reply_text(
            f"❌ Incorrect answer. Try again!\n"
            f"Attempts: {attempts}"
        )

async def hint(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Provide a hint for the current riddle."""
    user_id = update.effective_user.id
    
    if user_id not in user_riddles:
        await update.message.reply_text(
            "You don't have an active riddle. Use /riddle to get one."
        )
        return
    
    riddle_id = user_riddles[user_id]["riddle_id"]
    riddle_data = RIDDLES[riddle_id]
    answer = riddle_data["answer"]
    
    # Create a hint by revealing part of the answer
    hint_length = max(1, len(answer) // 3)
    hint = answer[:hint_length] + "_" * (len(answer) - hint_length)
    
    await update.message.reply_text(
        f"🔍 *Hint*\n\nThe answer starts with: {hint}",
        parse_mode="Markdown"
    )

async def skip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Skip the current riddle."""
    user_id = update.effective_user.id
    
    if user_id not in user_riddles:
        await update.message.reply_text(
            "You don't have an active riddle. Use /riddle to get one."
        )
        return
    
    riddle_id = user_riddles[user_id]["riddle_id"]
    riddle_data = RIDDLES[riddle_id]
    
    await update.message.reply_text(
        f"⏩ Riddle skipped.\n\n"
        f"The answer was: *{riddle_data['answer']}*\n\n"
        f"Use /riddle to get a new challenge.",
        parse_mode="Markdown"
    )
    
    # Remove the skipped riddle
    del user_riddles[user_id]

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show the user's current status."""
    user_id = update.effective_user.id
    
    if user_id not in user_riddles:
        await update.message.reply_text(
            "You don't have an active riddle. Use /riddle to get one."
        )
    else:
        riddle_id = user_riddles[user_id]["riddle_id"]
        attempts = user_riddles[user_id]["attempts"]
        riddle_data = RIDDLES[riddle_id]
        
        await update.message.reply_text(
            f"📊 *Current Status*\n\n"
            f"Active riddle: {riddle_data['question']}\n"
            f"Attempts made: {attempts}\n\n"
            f"Use /hint if you need help or /skip to move to the next riddle.",
            parse_mode="Markdown"
        )

async def post_init(application: Application) -> None:
    """Set up bot commands after initialization."""
    commands = [
        BotCommand("start", "Start the bot"),
        BotCommand("help", "Show help information"),
        BotCommand("riddle", "Get a random riddle"),
        BotCommand("answer", "Submit your answer"),
        BotCommand("hint", "Get a hint for the current riddle"),
        BotCommand("skip", "Skip the current riddle"),
        BotCommand("status", "Check your progress")
    ]
    await application.bot.set_my_commands(commands)

def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(TOKEN).post_init(post_init).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("riddle", riddle))
    application.add_handler(CommandHandler("answer", answer))
    application.add_handler(CommandHandler("hint", hint))
    application.add_handler(CommandHandler("skip", skip))
    application.add_handler(CommandHandler("status", status))

    # Start the Bot
    application.run_polling()

if __name__ == "__main__":
    main()