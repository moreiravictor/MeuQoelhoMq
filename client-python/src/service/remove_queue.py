import grpc

from protocols import meu_qoelho_mq_pb2

def perform(stub, name):
    req = meu_qoelho_mq_pb2.RemoveQueueRequest(
        name=name
    )
    try:
        response = stub.removeQueue(req)
        print('Queue removed:', response)
    except grpc.RpcError as e:
        print('Error removing queue:', e)
