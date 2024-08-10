import grpc
from concurrent import futures
from protocols import meu_qoelho_mq_pb2_grpc
from servicer import MeuQoelhoMqServicer
from signal import signal, SIGTERM, SIGINT, pause
import threading
import os

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    servicer = MeuQoelhoMqServicer()

    meu_qoelho_mq_pb2_grpc.add_MeuQoelhoMqServicer_to_server(servicer, server)
    server.add_insecure_port("[::]:50051")

    server.start()
    print("running server")

    def handle_termination(*_: any) -> None :
      server.stop(None)
      servicer.service.clear_subs()
      print('Cleared subs')
      os._exit(0)

    signal(SIGINT, handle_termination)
    signal(SIGTERM, handle_termination)
    server.wait_for_termination()
serve()
