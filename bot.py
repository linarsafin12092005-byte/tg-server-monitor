import os
import logging
import subprocess
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    logger.error("BOT_TOKEN не задан в переменных окружения!")
    exit(1)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Приветствие"""
    await update.message.reply_text(
        "Привет! Я бот для мониторинга сервера.\n"
        "Доступные команды:\n"
        "/status — состояние сервера\n"
        "/disk — свободное место на диске\n"
        "/cpu — загрузка процессора\n"
        "/help — справка"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Справка"""
    await update.message.reply_text(
        "Стек проекта:\n"
        "Python 3.11 | Docker | GitHub Actions\n"
        "Разработан с использованием AI-инструментов.\n"
        "Автор: Линар Сафин\n"
        "GitHub: github.com/ТВОЙ_ЛОГИН/tg-server-monitor"
    )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Полный статус сервера"""
    try:
        uptime = subprocess.check_output("uptime", shell=True).decode().strip()
        await update.message.reply_text(f"Uptime:\n{uptime}")
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")


async def disk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Свободное место на диске"""
    try:
        disk_info = subprocess.check_output("df -h /", shell=True).decode().strip()
        await update.message.reply_text(f"Диск:\n{disk_info}")
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")


async def cpu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Загрузка CPU"""
    try:
        cpu_info = subprocess.check_output(
            "top -bn1 | grep 'Cpu(s)'", shell=True
        ).decode().strip()
        await update.message.reply_text(f"CPU:\n{cpu_info}")
    except Exception as e:
        await update.message.reply_text(f"Ошибка: {e}")


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("disk", disk))
    app.add_handler(CommandHandler("cpu", cpu))

    logger.info("Бот запущен и готов к работе")
    app.run_polling()


if __name__ == "__main__":
    main()