import json
from csv import DictReader
from pathlib import Path
from typing import Dict, List, Set, Tuple
import pandas

class PPDataHandler:

    @property
    def number_of_apps(self):
        return self.df.App_Title.unique().size

    def __init__(self, csv_path: Path) -> None:
        self.csv_path = csv_path
        self.df = pandas.read_csv(csv_path,header=0)

    def apps(self):
        return self.df.App_Title.unique().tolist()
