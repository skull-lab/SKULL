import os
import random
import time
import asyncio
from io import BytesIO
from flask import Flask
from threading import Thread
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    CallbackContext,
    CallbackQueryHandler,
    filters,
)
import httpx  # Asynchronous HTTP requests
import logging

# Load environment variables
load_dotenv(".env")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
HF_TOKEN = os.getenv("HF_API_KEY")
LORAS = os.getenv("LORAS", "").split(",")  # List of LoRAs

# Initialize Flask app
app = Flask(__name__)

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot States
GENERATE, SELECT_ASPECT_RATIO, CANCEL = range(3)

# Globals for stats and data
total_images_generated = 0
active_users = set()
total_users = set()
last_generated_image = {}

# Flask route for keeping the app alive
@app.route("/")
def home():
    return "Bot is running!"

def run_flask():
    """Run Flask app in a separate thread."""
    app.run(host="0.0.0.0", port=5001, use_reloader=False)

# Read variations from a text file (variations.txt)
def load_variations():
    if os.path.exists("variations.txt"):
        with open("variations.txt", "r") as file:
            return [line.strip() for line in file.readlines()]
    return []

variations = load_variations()

# Default negative prompt to guide image generation
negative_prompt = "low quality, blurry, distorted, poorly drawn, bad anatomy, incorrect proportions, artifacts, low resolution"

# Telegram Handlers
async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("❓ Help", callback_data="help"),
         InlineKeyboardButton("🎨 Generate", callback_data="generate")],
        [InlineKeyboardButton("📊 Stats", callback_data="stats"),
         InlineKeyboardButton("💾 Saved Prompts", callback_data="saved_prompts")]
        [InlineKeyboardButton("ℹ️ About", callback_data="about")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)


async def handle_menu(update: Update, context: CallbackContext) -> None:
    """Handle menu button clicks."""
    query = update.callback_query
    await query.answer()  # Acknowledge the callback query

    if query.data == "help":
        await help_command(query, context)
    elif query.data == "generate":
        await generate_command(query, context)
    elif query.data == "stats":
        await stats(query, context)
    elif query.data == "saved prompts":
        await get_promptss(query, context)
    elif query.data == "about":
        await about_command(query, context)    

    await update.message.reply_text(
        "✨ *Welcome to the AI Image Bot!* ✨\n\n"
        "Generate high-quality AI images with ease. Tap an option below:",
        parse_mode="Markdown",
        reply_markup=reply_markup,
    )

async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "❓ *Commands:*\n\n"
        "/start - Start the bot\n"
        "/help - View all commands\n"
        "/generate [aspect_ratio] - Generate an AI image\n"
        "/save_prompt - Save a favorite prompt\n"
        "/get_prompts - View saved prompts\n"
        "/last_image - Retrieve the last generated image\n"
        "/cancel - Cancel generation\n"
        "/stats - Bot statistics\n"
        "/about - About this bot\n"
        "/saved_prompts - View saved prompts",
        parse_mode="Markdown",
    )

async def stats(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        f"📊 *Stats:*\n\n"
        f"👥 Active Users: {len(active_users)}\n"
        f"🎨 Total Images Generated: {total_images_generated}\n"
        f"🌍 Total Users: {len(total_users)}",
        parse_mode="Markdown",
    )

async def save_prompt(update: Update, context: CallbackContext) -> None:
    user_prompt = context.user_data.get("prompt", "")
    if user_prompt:
        try:
            with open("saved_prompts.txt", "a") as file:
                file.write(f"{user_prompt}\n")
            await update.message.reply_text(f"✅ Saved prompt: {user_prompt}")
        except Exception as e:
            logger.error(f"Error saving prompt: {e}")
            await update.message.reply_text("❌ Failed to save prompt. Please try again.")
    else:
        await update.message.reply_text("❌ No prompt found to save. Please generate an image first.")

async def get_prompts(update: Update, context: CallbackContext) -> None:
    try:
        if os.path.exists("saved_prompts.txt"):
            with open("saved_prompts.txt", "r") as file:
                prompts = file.readlines()
            if prompts:
                await update.message.reply_text("💾 Saved Prompts:\n" + "".join(prompts))
            else:
                await update.message.reply_text("❌ No saved prompts found.")
        else:
            await update.message.reply_text("❌ No saved prompts found.")
    except Exception as e:
        logger.error(f"Error retrieving prompts: {e}")
        await update.message.reply_text("❌ Failed to retrieve saved prompts. Please try again.")

async def last_image(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id in last_generated_image:
        await update.message.reply_photo(photo=last_generated_image[user_id])
    else:
        await update.message.reply_text("❌ No last image found. Please generate an image first.")

async def about(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "🤖 *About this bot:*\n\n"
        "This bot allows you to generate AI-powered images based on your text prompts. "
        "You can adjust the aspect ratio, save prompts, and retrieve your last generated images.\n\n"
        "Developed by the AI Image Bot team.",
        parse_mode="Markdown",
    )

async def generate(update: Update, context: CallbackContext) -> int:
    active_users.add(update.effective_user.id)
    total_users.add(update.effective_user.id)

    await update.message.reply_text("✨ Send a prompt to generate an image:")
    return GENERATE

async def handle_prompt(update: Update, context: CallbackContext) -> int:
    user_prompt = update.message.text.strip()

    if variations:
        variation = random.choice(variations)
        prompt_with_variation = f"{user_prompt} {variation}"
    else:
        prompt_with_variation = user_prompt

    prompt_with_variation += " Detailed, accurate anatomy, no distortions or unrealistic proportions"

    await update.message.reply_text(
        f"✨ Prompt received! Generating image with the following description:\n{prompt_with_variation}",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("1:1", callback_data="1:1"),
             InlineKeyboardButton("16:9", callback_data="16:9"),
             InlineKeyboardButton("9:16", callback_data="9:16")]
        ])
    )

    context.user_data["prompt"] = prompt_with_variation
    return SELECT_ASPECT_RATIO

async def aspect_ratio_selected(update: Update, context: CallbackContext) -> int:
    user_id = update.callback_query.from_user.id
    aspect_ratio = update.callback_query.data
    context.user_data["aspect_ratio"] = aspect_ratio

    prompt = context.user_data["prompt"]
    seed = random.randint(0, 2**32 - 1)
    width, height = 2048, 2048  # Default 1:1 resolution

    if aspect_ratio == "1:1":
        width, height = 2048, 2048
    elif aspect_ratio == "16:9":
        width, height = 3840, 2160
    elif aspect_ratio == "9:16":
        width, height = 2160, 3840

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        f"🎨 Generating image...\nAspect Ratio: {aspect_ratio}\nPrompt: {prompt}"
    )

    start_time = time.time()

    retries = 3
    last_exception = None

    async with httpx.AsyncClient() as client:  # Use async HTTP client for better performance
        for attempt in range(retries):
            try:
                # Simulate progress and real-time updates
                for i in range(0, 101, 10):
                    await asyncio.sleep(1)  # Simulating real-time processing

                    # Update the message with progress
                    await update.callback_query.edit_message_text(
                        f"🎨 Generating image... {i}% complete\nAspect Ratio: {aspect_ratio}\nPrompt: {prompt}"
                    )

                # Generate image using Hugging Face API
                response = await client.post(
                    "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell",
                    headers={"Authorization": f"Bearer {HF_TOKEN}"},
                    json={"inputs": prompt, "options": {"use_cache": False}},
                    timeout=120
                )

                response.raise_for_status()  # Ensure no 4xx/5xx errors
                image = response.content  # Assuming the image is returned as binary content

                if not image:
                    await update.callback_query.edit_message_text("❌ Image generation failed. Please try again.")
                    return ConversationHandler.END

                img_byte_arr = BytesIO(image)
                img_byte_arr.seek(0)

                end_time = time.time()
                time_taken = round(end_time - start_time, 2)

                # Send image as a document to avoid compression
                await update.callback_query.edit_message_text(
                    f"✨ Image generated successfully in {time_taken} seconds!\nAspect Ratio: {aspect_ratio}"
                )
                await update.callback_query.message.reply_document(
                    document=img_byte_arr,
                    filename="generated_image.png"
                )

                global total_images_generated
                total_images_generated += 1
                last_generated_image[user_id] = img_byte_arr

                return ConversationHandler.END

            except httpx.RequestError as e:
                logger.error(f"Request error: {e}")
                last_exception = e
                if attempt < retries - 1:
                    await update.callback_query.edit_message_text(
                        f"❌ Retry {attempt + 1} failed. Retrying in {2 ** (attempt + 1)} seconds..."
                    )
                    await asyncio.sleep(2 ** (attempt + 1))
                else:
                    await update.callback_query.edit_message_text(
                        "❌ An error occurred during image generation. Please try again later."
                    )
                    return ConversationHandler.END

async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("❌ Image generation has been canceled.")
    return ConversationHandler.END

# Conversation Handler
conv_handler = ConversationHandler(
    entry_points=[CommandHandler("generate", generate)],
    states={
        GENERATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_prompt)],
        SELECT_ASPECT_RATIO: [CallbackQueryHandler(aspect_ratio_selected)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

# Main function to run the bot
def main() -> None:
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("save_prompt", save_prompt))
    application.add_handler(CommandHandler("get_prompts", get_prompts))
    application.add_handler(CommandHandler("last_image", last_image))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(conv_handler)

    # Run Flask app in a separate thread for 24/7 hosting
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
