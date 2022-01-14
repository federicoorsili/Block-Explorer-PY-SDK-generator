import argparse
import os

class Cleaner:
    def __init__(self, abiPath) -> None:
        self.abis = os.listdir(abiPath)
    
    def makeName(self, fileName):
        return str(fileName.split('.')[0]).capitalize() + "Events"
    
    def clear(self):
        try:
            os.remove('gen.env')
        except:
            pass
        try:
            os.remove('generate_structures.env')
        except:
            pass
        try:
            os.remove('./Classes/BlockScanner.py')
        except:
            pass
        for abi in self.abis:
            try:
                os.remove('./Classes/' + self.makeName(abi) + '.py')
            except:
                pass
            file = os.listdir('./structures/' + self.makeName(abi))
            for f in file:
                try:
                    os.remove('./structures/' + self.makeName(abi) + '/' + f)
                except:
                    pass
            try:
                os.removedirs('./structures/' + self.makeName(abi))
            except:
                pass
            
        

parser = argparse.ArgumentParser()

parser.add_argument("-a", "--abis", dest = "abiPath", default = None, help="The path of the abis folder")

args = parser.parse_args()

if not args.abiPath:
    print("Error you have to insert the --abi and the --output flags")
    exit(-1) 

c = Cleaner(args.abiPath)
c.clear()