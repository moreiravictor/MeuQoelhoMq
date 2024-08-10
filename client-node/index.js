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
    var message = args.message;

    if (!name) {
      console.error('name param is required')
      return;
    }

    if (!message) {
      console.error('message param is required')
      return;
    }

    var req = {
      queueName: name,
      message: {
        text_message: message // or use `bytes_message` for sending bytes
      }
    };
      
    client.publishMessage(req, function(err, response) {
      if (err) {
        console.error('error publishing message:', err);
        return;
      }

      console.log('message published:', response);
    });
    break;
  case 'remove': 
    var name = args.name;
    var message = args.message;

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

      console.log('queue removed:', response);
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

