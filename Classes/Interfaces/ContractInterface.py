import json
from web3 import Web3

from Classes.Interfaces.EventsInterface import EventsInterface

class ContractInterface():
    def __init__(
            self, 
            contractAddress: str, 
            web3: Web3, 
            abiPath: str, 
            events: EventsInterface
        ) -> None:
        abiFile = open(abiPath)
        abi = json.load(abiFile)
        self.contract = web3.eth.contract(address=contractAddress, abi=abi)
        self.address = contractAddress
        self.abi = abi
        self.get_events = events