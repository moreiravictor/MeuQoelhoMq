from typing import Dict, List
from models import Queue, Subscriber, QueueType, Message, MessageType
import json
import os
from dataclasses import asdict, is_dataclass
import enum

# Check if the environment variable TEST_MODE is set to "true"
test_mode = os.getenv("TEST_MODE", "false").lower() == "true"
db_path = "../../tests/helpers/db.json" if test_mode else  "./db.json"

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if is_dataclass(obj):
            return asdict(obj)
        if isinstance(obj, enum.Enum):
            return obj.value
        if isinstance(obj, bytes):
            return obj.decode()
        return super().default(obj)

class DB:
  dirname = os.path.dirname(__file__)
  file_path = os.path.join(dirname, db_path)

  def __init__(self):
    try:
      print("db:::", db_path)
      print("test_mode:::", test_mode)
      open(self.file_path, "r")
      print("connected to db successfully")
    except:
      print("failed to connect to db")

  def __from_json_to_subscribers(self, datas: list[dict]) -> list[Subscriber]:
    return [Subscriber(ip=data['ip'], current_message=data['current_message']) for data in datas]

  def __from_json_to_messages(self, datas: list[dict]) -> list[Message]:
      parsed_messages = []

      for data in datas:
        type = MessageType(data["type"])
        content = bytes(data["content"], "utf-8") if type == MessageType.BYTE else data["content"]
        parsed_messages.append(Message(content=content, origin_queue=data["origin_queue"], type=type))

      return parsed_messages

  def __from_json_to_queue(self, data: dict) -> Queue:
    return Queue(
      name=data["name"],
      type=QueueType(data["type"]),
      messages=self.__from_json_to_messages(data['messages']),
      subscribers=self.__from_json_to_subscribers(data["subscribers"])
      )

  def find_queues(self) -> Dict[str, Queue]:
    file = open(self.file_path, "r").read()
    data = dict(json.loads(file))
    return dict([(queue[0], self.__from_json_to_queue(queue[1])) for queue in data.items()])


  def update_queues(self, queues: Dict[str, Queue]):
    file = open(self.file_path, "w")
    file.write(json.dumps(queues, cls=CustomJSONEncoder))
