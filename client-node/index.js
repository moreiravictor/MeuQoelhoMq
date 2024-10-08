var PROTO_PATH = __dirname + '/../protos/meu-qoelho-mq.proto';

var grpc = require('@grpc/grpc-js');
var protoLoader = require('@grpc/proto-loader');
var packageDefinition = protoLoader.loadSync(
    PROTO_PATH,
    {keepCase: true,
     longs: String,
     enums: String,
     defaults: true,
     oneofs: true
    });
var stub = grpc.loadPackageDefinition(packageDefinition);
var minimist = require('minimist');

var client = new stub.MeuQoelhoMq('localhost:50051',
  grpc.credentials.createInsecure());

var types = ['SIMPLE', 'MULTIPLE'];

var args = minimist(process.argv.slice(2));

if (args?.help || args?.h) {
  console.log(`
    Usage: node ./client-node/index.js [-h] {create,publish,list,remove,sign}

    Client Node for Meu QoelhoMQ

    positional arguments:
      {create,publish,list,remove,sign}
      create                Create a new queue
      publish               Publish messages to a queue
      list                  List all queues
      remove                Remove a queue
      sign                  Sign to one or more queues
    
    options:
      -h, --help
    `);
  return;
}

switch (args._[0]) {
  case 'create': 
    var name = args.name;
    var type = args.type;

    if (!name) {
      console.error('name param is required')
      return;
    }

    if (!type) {
      console.error('type param is required')
      return;
    }
    
    if (!types.includes(type)) {
      console.error('type must be ' + types.join(' or '))
      return;
    }

    var req = {
      name,
      type,
    };

      
    client.createQueue(req, function(err, response) {
      if (err) {
        console.error('error creating queue:', err);
        return;
      }

      console.log('queue created successfully:', response);
    });
    break;
  case 'publish': 
    var name = args.name;
    var messages = args.messages;

    if (!name) {
      console.error('name param is required')
      return;
    }

    if (!messages) {
      console.error('messages param is required')
      return;
    }

    var mappedMessages = messages.split(",").map(m => ({
      text_message: m // or use `bytes_message` for sending bytes
    }));


    var req = {
      queueName: name,
      messages: mappedMessages
    };
      
    client.publishMessages(req, function(err, response) {
      if (err) {
        console.error('error publishing message:', err);
        return;
      }

      console.log('messages published');
    });
    break;
  case 'remove': 
    var name = args.name;

    if (!name) {
      console.error('name param is required')
      return;
    }

    var req = {
      name: name,
    };
      
    client.removeQueue(req, function(err, response) {
      if (err) {
        console.error('error remove queue:', err);
        return;
      }

      console.log('queue removed');
    });
    break;
  case 'list': 
    client.listQueues(null, function(err, response) {
      if (err) {
        console.error('error list queues:', err);
        return;
      }

      console.log('list os queues:', response);
    });
    break;
  case 'sign': 
    var names = args.names;

    if (!names) {
      console.error('name param is required')
      return;
    }

    var namesArr = names.split(',')

    var req = {
      queuesNames: namesArr 
    }

    client.signToQueues(req)
      .on('data', function(response) {
        console.log('sign response queue:', response.queueName);
        console.log('sign response message:', response.message);
      })
      .on('error', function(error) {
          console.error('error to sign:', error);
      })
      .on('end', function() {
        console.log('sign ended.');
    });
    break;
  default:
    console.error('Method does not exists');
    break;
}

