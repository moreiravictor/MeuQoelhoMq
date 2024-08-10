import grpc

from protocols import meu_qoelho_mq_pb2
from protocols import meu_qoelho_mq_pb2_grpc

def create_queue(stub, name, queue_type):
    queue_data = meu_qoelho_mq_pb2.Queue(
        name=name,
        type=queue_type
    )
    try:
        response = stub.createQueue(queue_data)
        print('Queue created successfully:', response)
    except grpc.RpcError as e:
        print('Error creating queue:', e)

def publish_message(stub, name, message):
    msg = meu_qoelho_mq_pb2.MessageType(
        text_message=message
    )
    req = meu_qoelho_mq_pb2.PublishMessageRequest(
        queueName=name,
        message=msg
    )
    try:
        response = stub.publishMessage(req)
        print('Message published:', response)
    except grpc.RpcError as e:
        print('Error publishing message:', e)

def remove_queue(stub, name):
    req = meu_qoelho_mq_pb2.RemoveQueueRequest(
        name=name
    )
    try:
        response = stub.removeQueue(req)
        print('Queue removed:', response)
    except grpc.RpcError as e:
        print('Error removing queue:', e)

def list_queues(stub):
    try:
        response = stub.listQueues(meu_qoelho_mq_pb2.Empty())
        print('List of queues:', response)
    except grpc.RpcError as e:
        print('Error listing queues:', e)

def sign_to_queues(stub, queue_names):
    try:
        req = meu_qoelho_mq_pb2.SignToQueuesRequest(queuesNames=queue_names)
        response = stub.signToQueues(req)
        print('Signed to queues:', response)
    except grpc.RpcError as e:
        print('Error signing to queues:', e)

def main():
    channel = grpc.insecure_channel('localhost:50051')
    stub = meu_qoelho_mq_pb2_grpc.MeuQoelhoMqStub(channel)

    create_queue(stub, 'my-queue3', meu_qoelho_mq_pb2.QueueType.SIMPLE)
    publish_message(stub, 'my-queue3', 'Hello, World!')
    remove_queue(stub, 'my-queue3')
    list_queues(stub)
    sign_to_queues(stub, ['my-queue3'])

main()