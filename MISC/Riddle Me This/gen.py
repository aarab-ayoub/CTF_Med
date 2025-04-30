import os
import random
from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8118975932:AAEx5L5lnJTxncPKmlqud4j08qv0Y4m7fIQ"

RIDDLES = {
    "riddle1": {
        "question": "How do you go from 98 to 720 using just one letter?",
        "answer": "x",
        "flag": "MED{98x7=720}"
    },
    "riddle2": {
        "question": "Solve this cryptarithmetic puzzle: SEND + MORE = MONEY (Each letter represents a unique digit from 0-9)",
        "answer": "s=9,e=5,n=6,d=7,m=1,o=0,r=8,y=2",
        "flag": "M3D{9567+1085=10652}"
    },
    "riddle3": {
        "question": "OM was in the final 2 time what is the team that beaten them?",
        "answer": "Crvena_zvezda",
        "flag": "MED{Crvena_zvezda}"
    },
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
        # "/skip - Skip the current riddle\n"
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