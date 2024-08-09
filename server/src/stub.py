from protocols import meu_qoelho_mq_pb2_grpc
from protocols import meu_qoelho_mq_pb2
import grpc

channel = grpc.insecure_channel('localhost:50051')
stub = meu_qoelho_mq_pb2_grpc.MeuQoelhoMqStub(channel)

# feature = stub.createQueue(meu_qoelho_mq_pb2.Queue(name="test0", type=2))
# print(feature)

# feature = stub.publishMessage(meu_qoelho_mq_pb2.PublishMessageRequest(queueName="test0", message=meu_qoelho_mq_pb2.MessageType(text_message="EITA")))
# print(feature)

# stub.removeQueue(meu_qoelho_mq_pb2.RemoveQueueRequest(name="test1"))

# res = stub.listQueues(meu_qoelho_mq_pb2.Empty())
# print(res.queues)

response_stream = stub.signToQueues(meu_qoelho_mq_pb2.SignToQueuesRequest(queuesNames=["test0", "test3"]))

for response in response_stream:
  print(response)