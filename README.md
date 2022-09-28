# 🔌💫 poe-backend
Fall 2022 poe backend built in python.

## 📄 Info
### Protocol
Data over TCP as a byte array with the following structural represetation.
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

## 🔧 Setup
### Dependencies:
python3
### Installing requirements
```
pip3 install -r requirements.txt
```

## 🏎 Quick Start
```
python3 main.py
```

## 💻 Usage
```
import poeipro as poe
...
poe_db = poe.DB(db_path)
poe_main = poe.Sys(ip, port, max_connections, poe_db)
```
If no database exists at the provided `db_path`, a new Sqlite database will be instantiated.

`poe.Sys` listens on the provided `ip` and `port`.  `max_connections` governs the maximum amount of clients connecting to the system.  `poe_db` references the previously created `poe.DB` class.

