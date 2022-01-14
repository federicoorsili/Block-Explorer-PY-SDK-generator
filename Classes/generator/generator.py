import argparse
from ast import arg
from io import TextIOWrapper
import json
import os

class Generator:
    def __init__(self, abiPath: str) -> None:
        self.abis = os.listdir(abiPath)
        self.abiPath = abiPath
        print(self.abis)
    
    def makeName(self, fileName):
        return str(fileName.split('.')[0]).capitalize() + "Events"

    def generate(self):
        tmpFile = open('./generate_structures.py','w')
        self.writeTmpIntestation(tmpFile)
        self.generateBlockScanner()
        self.writeEnv(self.abis)
        for abi in self.abis:
            file = open(self.abiPath + '/' + abi)
            schema = json.load(file)
            event = open("./Classes/" + self.makeName(abi) + '.py', 'w')
            event.write("from Classes.Interfaces.EventsInterface import EventsInterface, GetEntities\n\n")
            event.write("class " + self.makeName(abi) + "(EventsInterface):\n\n")
            names = []
            for block in schema:
                if block['type'] == 'event':
                    event.write("""
    def """ + block['name'] + """(
            self, 
            filter : dict = {}, 
            get : GetEntities = GetEntities.ALL
        ):
        event = self.BlockScanner.""" + abi.split('.')[0] + """Contract.contract.events.""" + block['name'] + """.createFilter(
            fromBlock = self.BlockScanner.latestBlockSniffed,
            toBlock = 'latest'
            );
        return self.apply_filters(event, filter, get)
                         
                    """)
                    names.append(block['name'])
            self.retriveSchemas(abi.split('.')[0], names, tmpFile)
            self.writeAllEvents(names, event)

    def writeTmpIntestation(self, file: TextIOWrapper):
        file.write("""
import os
from pprint import pprint
from Classes.BlockScanner import BlockScanner
from dotenv import load_dotenv
import json

load_dotenv()

bExp = BlockScanner(
    os.environ['PROVIDER'],
    os.environ['DB_HOST'],
    int(os.environ['DB_PORT']),
    os.environ['NFT_CONTRACT_ADDRESS'],
    os.environ['AUCTION_CONTRACT_ADDRESS']
)


         """)
    
    def writeTmpFile(self, abi: str ,name: str, file: TextIOWrapper):
        file.write("""
#Retriving schema for event named """ + name + """
file = open('./structures/""" + self.makeName(abi) + """/""" + name + """.json', 'w')
try:
    res = bExp.""" + abi + """Contract.get_events.""" + name + """()[0]
except:
    res = '{}'
file.write(json.dumps(res, indent=4))

        """)

    def retriveSchemas(self, abi: str, names: str, tmpFile: TextIOWrapper):
        try:
            os.makedirs('./structures/' + self.makeName(abi))
        except:
            pass
        for name in names:
            self.writeTmpFile(abi, name, tmpFile)
    
    def writeAllEvents(self, names, eventFile : TextIOWrapper):
        eventFile.write("""
    def AllEvents(
            self, 
            filter : dict = {}, 
            get : GetEntities = GetEntities.ALL
        ):   
        """)
        for i in range(len(names)):
            if i == 0:
                eventFile.write("""
        events = self.""" + names[i] +  """(filter=filter, get=get)
                """)
            else:
                eventFile.write("""
        events += self.""" + names[i] +  """(filter=filter, get=get)
                """)
        eventFile.write("""
        return events
        """)

    def generateBlockScanner(self):
        bsFile = open('./Classes/BlockScanner.py', 'w')
        bsFile.write("""
from pprint import pprint
from web3 import Web3
import pymongo
from web3.middleware import geth_poa_middleware
from Classes.AuctionEvents import AuctionEvents
from Classes.NftEvents import NftEvents
from Classes.Interfaces.ContractInterface import ContractInterface

class BlockScanner:
    def __init__(
            self,
            provider : str,
            dbHost: str,
            dbPort: int,""")
        for abi in self.abis:
            bsFile.write("""
            """ + abi.split('.')[0] + """ContractAddress: str,""")
        bsFile.write("""
        ) -> None:

        #Web3 init
        self.web3 = Web3(Web3.HTTPProvider(provider))
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        #MongoDb Init
        self.mongoClient = pymongo.MongoClient(host= dbHost, port= dbPort)
        self.db = self.mongoClient["testDb"]
        
        self.latestBlockSniffed = 21754323
        """)
        for abi in self.abis:
            bsFile.write("""
        #""" + self.makeName(abi) + """ Init
        self.""" + abi.split('.')[0] + """Contract = ContractInterface(
            """ + abi.split('.')[0] + """ContractAddress,
            self.web3,
            '""" + self.abiPath + '/' + abi + """',
            """ + self.makeName(abi) + """(self)
        )
            """)
        
    def writeEnv(self, abis):
        envFile = open('gen.env', 'w')
        envFile.write("""
PROVIDER=
DB_HOST=
DB_PORT=""")
        for abi in abis:
            envFile.write("""
""" + abi.split('.')[0].upper() + """_CONTRACT_ADDRESS=""")



parser = argparse.ArgumentParser()

parser.add_argument("-a", "--abis", dest = "abiPath", default = None, help="The path of the abis folder")

args = parser.parse_args()

if not args.abiPath:
    print("Error you have to insert the --abi and the --output flags")
    exit(-1) 

gen = Generator(args.abiPath)
gen.generate()

