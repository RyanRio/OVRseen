import json
from csv import DictReader
from pathlib import Path
from typing import Dict, List, Set, Tuple
import pandas
import datetime
import os

class PriPolGraphHandler:

    def __init__(self, path: Path) -> None:
        self.path = path

    def graphs(self):
        return os.listdir(self.path)
