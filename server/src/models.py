from enum import Enum
from typing import List, Union
from dataclasses import dataclass

class QueueType(Enum):
  SIMPLE = 1
  MULTIPLE = 2

class MessageType(Enum):
   STRING = 1
   BYTE = 2

@dataclass
class Message:
   type: MessageType
   origin_queue: str
   content: str | bytes

@dataclass
class Subscriber:
    ip: str
    current_message: Message | None

    def receive_message(self, message: Message):
      while (True):
        if (self.current_message == None):
          self.current_message = message
          return

@dataclass
class Queue:
  name: str
  type: QueueType
  messages: List[Message]
  subscribers: List[Subscriber]

  def subscribe(self, subscriber_id: str):
    self.subscribers.append(subscriber_id)

  def get_type_as_int(self) -> int:
        return self.type.value