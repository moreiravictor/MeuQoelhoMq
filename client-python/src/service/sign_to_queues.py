import grpc

from protocols import meu_qoelho_mq_pb2

def perform(stub, queue_names):
    try:
        req = meu_qoelho_mq_pb2.SignToQueuesRequest(queuesNames=queue_names)
        response = stub.signToQueues(req)
        print('Signed to queues:', response)
    except grpc.RpcError as e:
        print('Error signing to queues:', e)
