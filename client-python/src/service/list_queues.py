import grpc

from protocols import meu_qoelho_mq_pb2

def perform(stub):
    try:
        response = stub.listQueues(meu_qoelho_mq_pb2.Empty())
        print('List of queues:', response)
    except grpc.RpcError as e:
        print('Error listing queues:', e)
