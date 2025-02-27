from colorama import Fore, init
import asyncio
import aiosqlite  # Using aiosqlite for async SQLite operations
import scripts.logging as logging
import toml

init(autoreset=True)

async def database_startup():
    try:
        # Connect to the database asynchronously
        async with aiosqlite.connect('database.db') as db:
            # Create logs table
            await db.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                date TEXT,
                time TEXT,
                level TEXT,
                message TEXT
            )
            ''')
            
            # Create ip table
            await db.execute('''
            CREATE TABLE IF NOT EXISTS ip (
                ip TEXT PRIMARY KEY,
                country TEXT,
                city TEXT,
                isp TEXT
            )
            ''')
            
            # Create users table
            await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                password TEXT,
                discord TEXT,
                last_login TEXT
            )
            ''')
            
            # Commit changes automatically when context manager exits
            await db.commit()
        
        await logging.log('info', 'Datenbank wurde erfolgreich initialisiert.')
    except Exception as e:
        await logging.log('error', f'Fehler bei der Datenbank-Initialisierung: {str(e)}')

async def startup():
    logo = r""" ____             _                  _ 
| __ )  __ _  ___| | _____ _ __   __| |
|  _ \ / _` |/ __| |/ / _ \ '_ \ / _` |
| |_) | (_| | (__|   <  __/ | | | (_| |
|____/ \__,_|\___|_|\_\___|_| |_|\__,_|
    """
    
    print(Fore.MAGENTA + logo)
    
    # Load the configuration file
    config = toml.load('config.toml')
    version = config['Version']
    
    await database_startup()
    await logging.log('info', "Phantom Backend (Version " + version + ") wurde erfolgreich gestartet.")

# To run the startup function
def run_startup():
    asyncio.run(startup())

# If this file is run directly
if __name__ == "__main__":
    run_startup()