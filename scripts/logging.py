import asyncio
import aiosqlite
from colorama import Fore, init
from datetime import datetime

init(autoreset=True)

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
    
    try:
        async with aiosqlite.connect('database.db') as db:
            await db.execute(
                'INSERT INTO logs (date, time, level, message) VALUES (?, ?, ?, ?)',
                (date, time, level, message)
            )
            await db.commit()
    except Exception as e:
        print(Fore.RED + f"{timestamp} | [Error]: Failed to log to database: {str(e)}")