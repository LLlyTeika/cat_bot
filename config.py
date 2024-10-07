import os
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()

@dataclass
class Config:
    token: str = os.getenv('BOT_TOKEN')
