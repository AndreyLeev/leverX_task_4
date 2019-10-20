import json
from abc import ABC, abstractmethod 


class DataLoader(ABC):
    @abstractmethod
    def load(self, filename):
        pass


class JSONLoader(DataLoader):
    def load(self, filename):
        with open(filename, 'r') as f:
            return json.loads(f.read())

