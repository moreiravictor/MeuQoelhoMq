import grpc

from protocols import meu_qoelho_mq_pb2
from protocols import meu_qoelho_mq_pb2_grpc

def main():
    channel = grpc.insecure_channel('localhost:50051')
    stub = meu_qoelho_mq_pb2_grpc.MeuQoelhoMqStub(channel)
    
    queue_data = meu_qoelho_mq_pb2.QueueData(
        name='my-queue',
        type=meu_qoelho_mq_pb2.QueueType.SIMPLE 
    )

    try:
        response = stub.CreateQueue(queue_data)
        print('Fila criada com sucesso:', response)
    except grpc.RpcError as e:
        print('Erro ao criar a fila:', e)

main()