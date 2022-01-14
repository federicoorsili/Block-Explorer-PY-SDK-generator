import json
from web3 import Web3
from hexbytes import HexBytes
class GetEntities:
    ALL = "all"
    NEW = "new"
    NONE = "none"


class EventsInterface:
    def __init__(self, blockScanner) -> None:
        self.BlockScanner = blockScanner
    
    def apply_filters(
            self, 
            events, 
            filter: dict = {}, 
            get : GetEntities = GetEntities.ALL
        ):
        if get == GetEntities.ALL:
            out = events.get_all_entries()
        elif get == GetEntities.NEW:
            out = events.get_new_entries()
        elif get == GetEntities.NONE:
            out = events
        else:
            return None
        
        for i in range(len(out)):
            out[i] = self.toDict(out[i])
            
        if filter != {}:
            return self.__where(out, filter)

        return out
    
    def __where(self, dictionaryList: dict, filter : dict):
        tmp = []
        for dic in dictionaryList:
            score = 0
            for key in filter:
                value = filter[key]
                keys = key.split('.')
                dictVal = dic
                for k in keys:
                    try:
                        dictVal = dictVal[k]
                    except:
                        break
                if dictVal == value:
                    print(dictVal, value)
                    score += 1
            if score == len(filter):
                tmp.append(dic)
        return tmp
    
    def toDict(self, dictToParse):
        # convert any 'AttributeDict' type found to 'dict'
        parsedDict = dict(dictToParse)
        for key, val in parsedDict.items():
            # check for nested dict structures to iterate through
            if  'dict' in str(type(val)).lower():
                parsedDict[key] = self.toDict(val)
            # convert 'HexBytes' type to 'str'
            elif 'HexBytes' in str(type(val)):
                parsedDict[key] = val.hex()
            elif 'bytes' in str(type(val)):
                parsedDict[key] = HexBytes(val).hex()
        return parsedDict
