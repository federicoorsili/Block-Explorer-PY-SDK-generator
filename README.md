## Block Explorer PY SDK generator

Il programma si occupa di generare automaticamente sulla base dei file abi un SDK che consente di monitorare gli eventi emessi dal contratto.
Oltre agli eventi grazie all' sdk è possibile interagire integralmente con la blockchain di riferimento grazie alla presenza di Web3.

### Getting started

Per generare l'sdk è sufficiente inserire all' interno della cartella abis gli abi degli smart contract con i quali si intende lavorare.

Una volta inseriti gli abi (rigorosamente in formato json), è sufficiente eseguire da terminale  ```make generate```,
questo genererà all' interno di Classes le classi python che ti consentiranno di facilitare l'interazione con gli eventi. Inoltre lo stesso comando genererà una cartella ```structures``` con al suo delle sotto cartelle che si riferiscono agli abi inseriti.

Viene generato inoltre un file ```gen.env```, che deve essere compilato come verrà spiegato nel prossimo passaggio.

All' interno della cartella structures vengono generati dei file json corrispondenti alle risposte generate dal metodo ```BlockScanner.yourContract.get_events.[YourEventName]()```, è stata inserita in modo da poter sapere bene quale output aspettarsi e per la realizzazione di filtri efficaci.

Il programma è scritto per scopi perosnali (monitoring degli eventi di uno smart contract per l' inserimento all' interno di un database mongoDB), per questo motivo il costruttore dell' sdk presenta due campi non necessari, che sono: dbHost e dbPort.

Per eliminare tutti i file generati è sufficiente eseguire da terminale ```make clear```


### ESEMPIO DI CASO D' USO:

Supponiamo da ora in po di aver inserito all' interno della cartella abis un abi con il nome di sample.json e di aver eseguito il comando ```make generate```

Supponiamo inoltre che questo abi abbia un evento chiamato ```nftSold```

### 1.0 ENV:

La prima cosa da fare è rinominare il file gen.env con il nome .env.

Una volta rinominato va modificato e vanno inseriti i parametri, il file si presenterà in questo modo:

```
PROVIDER= 
DB_HOST= 
DB_PORT= 
SAMPLE_CONTRACT_ADDRESS= 
```

`PROVIDER`: va inserito l'url di un provider, se non ne conosci uno puoi usare alchemy che è gratuito.


`DB_HOST`: l' indirizzo del database mongoDB da collegare all' sdk. Se non si ha intenzione di collegare un db lasciare vuoto

`DB_PORT`: la porta del database mongoDB da collegare, Se non si ha intenzione di collegare un db lasciare vuoto

`SAMPLE_CONTRACT_ADDRESS`: va inserito l' indirizzo dello smart contract. (Non si chiama SAMPLE a caso. questo parametro prenderà il nome reso maiuscolo del file abi inserito. Nel caso in cui venissero inseriti più abi verrebbero generate più variabili con i vari nomi)

### 2 Istanziare l' SDK

```
from Classes.BlockScanner import BlockScanner
from dotenv import load_dotenv

load_dotenv()

SDK = BlockScanner(
    os.environ['PROVIDER'],
    os.environ['DB_HOST'],
    int(os.environ['DB_PORT']),
    os.environ['SAMPLE_CONTRACT_ADDRESS']
)
```

### 3 Monitorare un evento
```
SDK.sampleContract.get_events.nftSold()
```
Tutte i metodi di get_events hanno due parametri opzionali:

```get```: (string) permette di decidere se prendere gli tutti gli eventi, i nuovi eventi o nessun evento. In input prende una stringa tra "all", "new", "none", il valore di default è "all"
```
SDK.sampleContract.get_events.nftSold(get="new")
SDK.sampleContract.get_events.nftSold(get="all")
SDK.sampleContract.get_events.nftSold(get="none")
```

```filter```:(dict) filter consente di filtrare la ricerca attraverso un dizionario nel quale inserire il valore richiesto.

ATTENZIONE CON DIZIONARI INNESTATI USARE JSON PATH COME KEY

```
SDK.sampleContract.get_events.nftSold(filter={"txHash": "0x0000000000000000000000000"})

SDK.sampleContract.get_events.nftSold(filter={"args.hash": "0x1092394823980240923844903294390483"})
```


