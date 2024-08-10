from typing import Dict, List
from models import Queue, Subscriber, QueueType
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

  def __from_json_to_subscriber(self, data: dict) -> Subscriber:
    return Subscriber(ip=data['ip'], current_message=data['current_message'])

  def __from_json_to_queue(self, data: dict) -> Queue:
    subscribers: List[Subscriber] = [self.__from_json_to_subscriber(sub) for sub in data["subscribers"]]
    queue_type = QueueType(data["type"])
    return Queue(name=data["name"], type=queue_type, messages=data['messages'], subscribers=subscribers)

  def find_queues(self) -> Dict[str, Queue]:
    file = open(self.file_path, "r").read()
    data = dict(json.loads(file))
    return dict([(queue[0], self.__from_json_to_queue(queue[1])) for queue in data.items()])


  def update_queues(self, queues: Dict[str, Queue]):
    file = open(self.file_path, "w")
    file.write(json.dumps(queues, cls=CustomJSONEncoder))
