import json
from csv import DictReader
from pathlib import Path
from typing import Dict, List, Set, Tuple
import pandas
import datetime
import os

class GraphHandler:

    @property
    def number_of_graphs(self):
        return len(self.df.index)

    def __init__(self, path: Path) -> None:
        self.path = path
        if "created_graphs.csv" in os.listdir(self.path):
            self.df = pandas.read_csv(self.path / "created_graphs.csv",header=0)
        else:
            column_names = ["file_name","timestamp","included_applications"]
            self.df = pandas.DataFrame(columns=column_names)
