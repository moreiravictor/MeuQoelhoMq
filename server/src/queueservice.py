from db import DB
from models import Queue, QueueType, Subscriber, Message, MessageType
import random
from typing import Dict, List
import threading
from protocols import meu_qoelho_mq_pb2
from time import sleep

class QueueService:
  queues_map: Dict[str, Queue] = {}
  db: DB

  def __init__(self, db: DB):
    self.db = db
    self.queues_map = self.db.find_queues()

    print("loaded queues from file")

    for queue in self.queues_map.values():
      thread = threading.Thread(target=self.start_queue, kwargs={"queue":queue})
      thread.start()

    print("started all queues")

  def start_queue(self, queue: Queue):
    print("starting queue " + queue.name)

    while(True):
      if (len(queue.messages) and len(queue.subscribers)):
        print("message received on queue" + queue.name)
        message = queue.messages.pop()
        self.db.update_queues(self.queues_map)
        match queue.type:
          case QueueType.SIMPLE:
            sub = random.choice(queue.subscribers)
            print("queue " + queue.name + " notified " + sub.ip)
            thread = threading.Thread(target=sub.receive_message, kwargs={"message":message})
            thread.start()
          case QueueType.MULTIPLE:
            for sub in queue.subscribers:
              print("queue " + queue.name + " notified " + sub.ip)
              thread = threading.Thread(target=sub.receive_message, kwargs={"message":message})
              thread.start()
      sleep(1)

  def unsub(self, sub_ip: str, queues_names: List[str]):
    queues: list[Queue] = [self.queues_map.get(q) for q in queues_names]

    for queue in queues:
      queue.subscribers = [sub for sub in queue.subscribers if sub.ip != sub_ip]

    self.db.update_queues(self.queues_map)
    print("disconected sub" + sub_ip)

  def clear_subs(self):
    for queue_name in self.queues_map.keys():
      self.queues_map[queue_name].subscribers = []

    self.db.update_queues(self.queues_map)

  def add_queue(self, name: str, type: QueueType) -> Queue:

    if (self.queues_map.get(name) ==  None):
      q = Queue(name, QueueType(type), [], [])
      self.queues_map[name] = q
      self.db.update_queues(self.queues_map)

      thread = threading.Thread(target=self.start_queue, kwargs={"queue":self.queues_map[name]})
      thread.start()

      print("created queue successfully")
      return self.queues_map[name]

    print("queue already created")
    raise Exception("queue already created")

  def publish_messages(self, request: meu_qoelho_mq_pb2.PublishMessagesRequest):
    queue = self.queues_map.get(request.queueName)

    if (queue == None):
      print("tried to publish message to queue that does not exist")
      raise Exception("queue does not exist")

    messages: List[Message] = [
        Message(content=message.text_message, type=MessageType.STRING, origin_queue=queue.name) if message.text_message
        else Message(content=message.bytes_message, type=MessageType.BYTE, origin_queue=queue.name) for message in request.messages
      ]

    queue.messages.extend(messages)

    self.db.update_queues(self.queues_map)
    print("published message successfully")

  def remove_queue(self, request: meu_qoelho_mq_pb2.RemoveQueueRequest):
    try:
      self.queues_map.pop(request.name)
      self.db.update_queues(self.queues_map)
    except:
      print("tried to delete queue that does not exist")
      raise Exception("queue does not exist")

    print("deleted queue successfully")

  def list(self) -> List[Queue]:
    return [meu_qoelho_mq_pb2.Queue(name=queue.name, type=queue.get_type_as_int(), pendingMessages=len(queue.messages))
              for queue in self.queues_map.values()]

  def sign_to_queues(self, ip: str, queues_names: List[str]):
    sub = Subscriber(ip = ip, current_message=None)
    for name in queues_names:
      queue = self.queues_map.get(name)
      if (queue != None):
        print("subscribed " + ip + " to " + queue.name)
        queue.subscribe(sub)

    self.db.update_queues(self.queues_map)

    while (True):
      if (sub.current_message != None):
        print("received message")
        content = sub.current_message.content
        queue = sub.current_message.origin_queue
        message = meu_qoelho_mq_pb2.MessageType(text_message=content) if sub.current_message.type == MessageType.STRING else meu_qoelho_mq_pb2.MessageType(bytes_message=content)
        response = meu_qoelho_mq_pb2.SignToQueuesResponse(
          message=message,
          queueName= queue
        )

        yield response

        sub.current_message = None

  def consume_message(self, ip: str, queue: str) -> meu_qoelho_mq_pb2.ConsumeMessageResponse:
    generator = self.sign_to_queues(ip, [queue])
    res = next(generator)
    self.unsub(ip, [queue])
    return meu_qoelho_mq_pb2.ConsumeMessageResponse(response=res.message)
