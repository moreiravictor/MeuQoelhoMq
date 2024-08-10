import grpc

from protocols import meu_qoelho_mq_pb2

def perform(stub, name, message):
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
