# MeuQoelhoMq


## O Projeto

Este projeto trata da implementação de um sistema de mensageria baseado no conceito de filas, utilizando como middleware de comunicação o GRPC e como base de dados o arquivo `src/db.json`.


A documentação dos métodos em detalhes pode ser encontrada em `/protos/meu-qoelho-mq.proto`, mas os métodos principais disponibilizados são:


1. rpc createQueue(Queue) returns (Queue) {}

  Utilizado para criar uma nova fila que pode ser de tipo simples ou múltiplo. Para o tipo simples as mensagens são notificadas para um subscriber aleatório, já para o tipo múltiplo todos os subscribers são notificados de todas as mensagens.

2. rpc removeQueue(RemoveQueueRequest) returns (Empty) {}

  Utilizado para remover uma fila já existente. Caso a fila não exista lança um erro.

3. rpc listQueues(Empty) returns (ListQueueResponse) {}

  Lista todas as filas existentes, exibindo seu nome, tipo e mensagens que ainda não foram consumidas.

4. rpc publishMessages(PublishMessagesRequest) returns (Empty) {}

  Utilizado para publicar mensagens em uma fila. Caso seja necessário enviar apenas uma mensagem, basta que seja enviado como argumento uma lista contendo uma única mensagem. As mensagens podem ser bytes ou strings.

5. rpc signToQueues(SignToQueuesRequest) returns (stream SignToQueuesResponse) {}

  Realiza a assinatura de um subscriber em diferentes filas. Trata-se de um método bloqueante que fará com que o cliente mantenha uma conexão aberta com o servidor, escutando novas mensagens a serem enviadas para as filas de inscrição. Para que o cliente não fique eternamente conectado esperando por mensagens, é possível passar o argumento `timeout`, que especifica o número de segundos que o cliente ficará esperando sem que novas mensagens sejam enviadas para a fila.

6. rpc consumeMessageFromQueue(ConsumeMessageRequest) returns (ConsumeMessageResponse) {}

  Consome apenas uma única mensagem que esteja disponível na fila enviada. Para que o cliente não fique eternamente conectado esperando por mensagens, é possível passar o argumento `timeout`, que especifica o número de segundos que o cliente ficará esperando sem que novas mensagens sejam enviadas para a fila.

## Dificuldades, surpresas e destaques

1. Como utilizamos threads únicas por fila em nossa implementação, ficamos dependentes da configuração `max_workers` do GRPC, que limita o número máximo de threads a serem executadas pelo servidor. Por isto, o número máximo de filas que podem ser criadas atualmente é 10 (este número foi escolhido arbitrariamente com o intuito de não sobrecarregar nenhuma máquina que venha a executar esse código).

2. Encontramos dificuldades no parse entre json e classes do python. A linguagem não oferece um suporte nativo suficiente para as manipulações realizadas pelo servidor.

3. O reset de subscribers ao finalizar a execução de um servidor se mostrou uma tarefa não built-in do GRPC, que não fornece nenhum tipo de hook ou listener que permite monitorar esta ação.

4. Gostaríamos de destacar algumas implementações mais específicas, como no método `receive_message`, que utiliza um lock para o recurso de mensagem atual, de modo que diferentes filas que estejam tentando notificar um mesmo subscriber não interfiram umas nas outras. Além disso, o método `sign_to_queues` utiliza um loop "infinito" e retorna um `generator` que envia novas mensagens para o client indefinidamente, até que a conexão caia ou o timeout seja atingido.

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

Help commad

```
node ./client-node/index.js --help
```

Create a new queue

```
node ./client-node/index.js create --name=channel1 --type=SIMPLE
```

Publish messages to a queue
```
node ./client-node/index.js publish --name=channel1 --messages=abc,xyz
```

List all queues
```
node ./client-node/index.js list
```

Remove a queue
```
node ./client-node/index.js remove --name=channel1
```

Sign to one or more queues
```
node ./client-node/index.js sign --names=channel1,test0
```

### Python examples

Help commad

```
python3 ./client-python/src/client.py --help list all arguments available
```

Create a queue

```
python3 ./client-python/src/client.py create --name=channel1 --type=SIMPLE
```

Publish a message to queue

```
python3 ./client-python/src/client.py publish --name=channel1 --message=abc
```

List queues
```
python3 ./client-python/src/client.py list
```

Remove queue
```
python3 ./client-python/src/client.py remove --name=channel1
```

Sign queues
```
python3 ./client-python/src/client.py sign --name=channel1,test0
```


### Run tests

First stop all the running services to not generate inconsistences. The run:
```
./test.sh
```