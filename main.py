import scripts.startup as startup
import scripts.logging as logging
import asyncio
import toml

if __name__ == "__main__":
    asyncio.run(startup.startup())