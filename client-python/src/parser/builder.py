from argparse import ArgumentParser, _SubParsersAction

def add_create_command(parser: ArgumentParser, subparsers: _SubParsersAction):
    create_parser = subparsers.add_parser('create', help='Create a new queue')
    create_parser.add_argument('--name', required=True, help='Name of the queue')
    create_parser.add_argument('--type', required=True, help='Type of the queue')

def add_publish_command(parser: ArgumentParser, subparsers: _SubParsersAction):
    publish_parser = subparsers.add_parser('publish', help='Publish a message to a queue')
    publish_parser.add_argument('--name', required=True, help='Name of the queue')
    publish_parser.add_argument('--message', required=True, help='Message to publish')

def add_list_command(parser: ArgumentParser, subparsers: _SubParsersAction):
    subparsers.add_parser('list', help='List all queues')

def add_remove_command(parser: ArgumentParser, subparsers: _SubParsersAction):
    remove_parser = subparsers.add_parser('remove', help='Remove a queue')
    remove_parser.add_argument('--name', required=True, help='Name of the queue')

def add_sign_command(parser: ArgumentParser, subparsers: _SubParsersAction):
    sign_parser = subparsers.add_parser('sign', help='Sign to one or more queues')
    sign_parser.add_argument('--name', required=True, help='Comma-separated list of queue names')


def build() -> ArgumentParser:
    parser = ArgumentParser(description='Client Python for Meu Qoelho MQ')
    subparsers = parser.add_subparsers(dest='command')

    add_create_command(parser, subparsers)
    add_publish_command(parser, subparsers)
    add_list_command(parser, subparsers)
    add_remove_command(parser, subparsers)
    add_sign_command(parser, subparsers)

    return parser
    