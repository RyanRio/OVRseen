import json
from csv import DictReader
from pathlib import Path
from typing import Dict, List, Set, Tuple
import pandas
import datetime

class GraphHandler:

    @property
    def number_of_graphs(self):
        return len(self.df.index)

    def __init__(self, path: Path) -> None:
        self.path = path
        # TODO if no csv of created graphs, create, else load
        self.df =

    def graphs(self):
        # TODO return graphs info
        return

    def delete_graphs():
