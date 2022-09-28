# 🔌💫 poe-backend
Fall 2022 poe backend based off of poe-iit summer 2022 IPRO setup.

## 📄 Info
### Important
System should be integrated into an isolated network as there.
### Implementation
Upon the instantiation of `poe.Sys()` a thread is created to manage new TCP connection requests.  Upon establishment of connection, a sperate thread is created to manage independent communications between self and the specific client.  Upon receiving data, it is pushed to the sqlite database.  Database connection instance is shared between all threads. 
### Protocol
Data over TCP as a byte array with the following structural representation.
```
[opt, id, type, data]
```

<b>opt  as ubyte:</b> Operation code informs the server on how to handle the data such as request to post the data

<b>id   as ubyte:</b> Unique sensor id provided by the client.

<b>type as ubyte:</b> Sensor type parsed as `{Fire: 0, Smoke: 1, Motion: 2, Humidity: 3, Temperature: 4, Water: 5}`

<b>data as ubyte:</b> Sensor readings

### Protocol Example
```
b'\x01\xFF\x00\x01'
```
### Data Lifecycle
```
Arduino.GetsDataFromSensors
Arduino.SendsDataOverTCP
    |
    v
Host.SendDataToDatabase
    |
    v
Database.Insert/ReplaceData
```

### Database Structure
```
sensors (
ip_id TEXT PRIMARY KEY NOT NULL,
sensor TEXT NOT NULL,
value INTEGER NOT NULL,
time REAL NOT NULL);
```

## 🔧 Setup
### Dependencies:
python3
### Installing requirements
```
pip3 install -r requirements.txt
```

## 🏎 Quick Start
Startup
```
python3 main.py
```

Getting Help
```
POE-TERM: h
```

## 💻 Usage
### Library Usage
```
import poeipro as poe
...
poe_db = poe.DB(db_path)
poe_main = poe.Sys(ip, port, max_connections, poe_db)
```
If no database exists at the provided `db_path`, a new Sqlite database will be instantiated.

`poe.Sys` listens on the provided `ip` and `port`.  `max_connections` governs the maximum amount of clients connecting to the system.  `poe_db` references the previously created `poe.DB` class.
