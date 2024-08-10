import grpc

from service import create_queue, publish_message, remove_queue, list_queues, sign_to_queues

from protocols import meu_qoelho_mq_pb2_grpc
from parser import builder as parser_builder


def main():
    parser = parser_builder.build()
    args = parser.parse_args()

    with grpc.insecure_channel('localhost:50051') as channel:
        stub = meu_qoelho_mq_pb2_grpc.MeuQoelhoMqStub(channel)

        if args.command == 'create':
            create_queue.perform(stub, args.name, args.type)
        elif args.command == 'publish':
            publish_message.perform(stub, args.name, args.message)
        elif args.command == 'list':
            list_queues.perform(stub)
        elif args.command == 'remove':
            remove_queue.perform(stub, args.name)
        elif args.command == 'sign':
            sign_to_queues.perform(stub, args.name)

main()