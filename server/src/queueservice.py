from db import DB
from models import Queue, QueueType, Subscriber
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
      if (len(queue.messages)):
        print("message received on queue")
        message = queue.messages.pop()
        self.db.update_queues(self.queues_map)
        print(queue.type)
        match queue.type:
          case QueueType.SIMPLE:
            sub = random.choice(queue.subscribers) # TODO use another algorithm
            print("queue " + queue.name + " notified " + sub.ip)
            thread = threading.Thread(target=sub.receive_message, kwargs={"message":message})
            thread.start()
          case QueueType.MULTIPLE:
            for sub in queue.subscribers:
              print("queue " + queue.name + " notified " + sub.ip)
              thread = threading.Thread(target=sub.receive_message, kwargs={"message":message})
              thread.start()
      sleep(5)

  def unsub(self, sub_ip: str, queues_names: List[str]):
    print(sub_ip)
    queues: list[Queue] = [self.queues_map.get(q) for q in queues_names]

    for queue in queues:
      queue.subscribers = [sub for sub in queue.subscribers if sub.ip != sub_ip]

    self.db.update_queues(self.queues_map)
    print("disconected")

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

  def publish_message(self, request: meu_qoelho_mq_pb2.PublishMessageRequest):
    queue = self.queues_map.get(request.queueName)

    if (queue == None):
      print("tried to publish message to queue that does not exist")
      raise Exception("queue does not exist")

    message = request.message.text_message or request.message.bytes_message

    queue.messages.append(message)

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
        message = meu_qoelho_mq_pb2.MessageType(text_message=sub.current_message) if isinstance(sub.current_message, str) else meu_qoelho_mq_pb2.MessageType(bytes_message==sub.current_message)
        response = meu_qoelho_mq_pb2.SignToQueuesResponse(
          message=message,
          queueName= "mocked_queue_name"
        )

        yield response

        sub.current_message = None
