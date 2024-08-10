# distributed-systems-2024


## How to install dependencies


## Python

To setup your virtual env firstly run:

```
virtualenv .venv
source .venv/bin/activate
```

## Node

Install Node 20. We recommend to do using [NVM](https://github.com/nvm-sh/nvm), but you can also use [the official](https://nodejs.org/en) website if you like.


After install run `node -v` command to check if everything worked well. It should return something like `v20.X.X`

## Generate protocol files and install dependencies

Run:
```
./setup.sh
```

This file will:
- Create python protocol files using `protos/meu-qoelho-mq.proto` and put them in the `server/src/protocols` folder
- Install python dependencies from `server/requirements.txt`
- Install node dependencies from `client-node/package.json`

## Server

To run server:

```
python3 ./server/src/server.py
```

## Clients

To tryout test stub, open another terminal tab and run:

### Python
```
python3 ./client-python/src/client.py
```

## Client Flags

- create --name=channel1 --type=SIMPLE
- publish  --name=channel1 --message=abc
- remove --name=channel1
- list
- sign --names=channel1,test0


### Node examples

Create a queue

```
node ./client-node/index.js create --name=channel1 --type=SIMPLE
```

Publish messages to queue

```
node ./client-node/index.js publish --name=channel1 --messages=abc,xyz
```

List queues
```
node ./client-node/index.js list
```

Remove queue
```
node ./client-node/index.js remove --name=channel1
```

Sign queues
```
node ./client-node/index.js sign --name=channel1,test0
```


### Run tests

```
./test.sh
```