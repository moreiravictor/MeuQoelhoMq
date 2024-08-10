from protocols import meu_qoelho_mq_pb2_grpc
from protocols import meu_qoelho_mq_pb2
from db import DB
from queueservice import QueueService
import grpc

class MeuQoelhoMqServicer(meu_qoelho_mq_pb2_grpc.MeuQoelhoMqServicer):
  service: QueueService

  def __init__(self):
    self.service = QueueService(DB())

  def createQueue(self, request, context):
    print("received request to create queue " + request.name + " - type: "+ str(request.type))

    created_queue = self.service.add_queue(name = request.name, type = request.type)

    return meu_qoelho_mq_pb2.Queue(name = created_queue.name, type = request.type)


  def publishMessages(self, request, context):
    print("received request to publish a message to queue " + request.queueName)

    create_queue_request = meu_qoelho_mq_pb2.PublishMessagesRequest(messages = request.messages, queueName = request.queueName)

    self.service.publish_messages(create_queue_request)

    return meu_qoelho_mq_pb2.Empty()


  def removeQueue(self, request, context):
    print("received request to remove a queue")
    request = meu_qoelho_mq_pb2.RemoveQueueRequest(name=request.name)

    self.service.remove_queue(request)
    return meu_qoelho_mq_pb2.Empty()

  def listQueues(self, _request, _context):
    print("received request to list queues")
    return meu_qoelho_mq_pb2.ListQueueResponse(queues=self.service.list())

  def signToQueues(self, request, context):
    ip = context.peer()
    context.add_callback(lambda: self.service.unsub(ip, request.queuesNames))

    try:
      print("received request to sign to queues")
      return self.service.sign_to_queues(ip=ip, queues_names=request.queuesNames)
    except grpc.RpcError as e:
      print(f"RPC Error: {e}")

  def consumeMessageFromQueue(self, request, context):
    print("received request to consume message from queue")
    ip = context.peer()
    context.add_callback(lambda: self.service.unsub(ip, request.queuesNames))
    print("received request to consume message")
    return self.service.consume_message(ip=ip, queue=request.queueName)



