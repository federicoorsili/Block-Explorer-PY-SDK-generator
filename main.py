from curses import beep
import os
from pprint import pprint
from Classes.BlockScanner import BlockScanner
from dotenv import load_dotenv

load_dotenv()

bExp = BlockScanner(
    os.environ['PROVIDER'],
    os.environ['DB_HOST'],
    int(os.environ['DB_PORT']),
    os.environ['NFT_CONTRACT_ADDRESS'],
    os.environ['AUCTION_CONTRACT_ADDRESS']
)

