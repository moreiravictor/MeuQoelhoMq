import grpc

from protocols import meu_qoelho_mq_pb2

def perform(stub, name, queue_type):
    queue_data = meu_qoelho_mq_pb2.Queue(
        name=name,
        type=queue_type
    )
    try:
        response = stub.createQueue(queue_data)
        print('Queue created successfully:', response)
    except grpc.RpcError as e:
        print('Error creating queue:', e)
