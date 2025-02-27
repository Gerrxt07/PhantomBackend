import asyncio
import aiosqlite
from colorama import Fore, init
from datetime import datetime
import os

init(autoreset=True)

async def setup_logging():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    logs_path = os.path.join(script_dir, 'logs')

    os.makedirs(logs_path, exist_ok=True)

    now = datetime.now()
    log_filename = now.strftime("%Y-%m-%d_%H-%M-%S.log")
    log_filepath = os.path.join(logs_path, log_filename)

    global log_file
    log_file = open(log_filepath, 'a')

async def log(level, message):
    now = datetime.now()
    date = now.strftime("%d.%m.%Y")
    time = now.strftime("%H:%M:%S")
    timestamp = f"{date} - {time}"
    
    if level == 'info':
        print(Fore.GREEN + f"{timestamp} | [Info]: {message}")
    elif level == 'warning':
        print(Fore.YELLOW + f"{timestamp} | [Warnung]: {message}")
    elif level == 'error':
        print(Fore.RED + f"{timestamp} | [Error]: {message}")
    else:
        pass
    
    log_file.write(f"{timestamp} | [{level.capitalize()}]: {message}\n")
    log_file.flush()
    
    try:
        async with aiosqlite.connect('database.db') as db:
            await db.execute(
                'INSERT INTO logs (date, time, level, message) VALUES (?, ?, ?, ?)',
                (date, time, level, message)
            )
            await db.commit()
    except Exception as e:
        print(Fore.RED + f"{timestamp} | [Error]: Failed to log to database: {str(e)}")
    pass