# MQ Traffic Generator

## Update .env file

```bash
QUEUE_MANAGER="QM1"
CHANNEL="DEV.APP.SVRCONN"
HOST="****************"
PORT=1414
QUEUE="DEV.QUEUE.1"
USER="app"
PASSWORD="****************"
```

## Put

```bash
python mqtg.py put --count 100 --delay 0.001
```

## Get

```bash
python mqtg.py get --delay 0.0001
```
