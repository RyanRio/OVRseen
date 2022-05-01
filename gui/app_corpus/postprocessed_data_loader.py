import json
from csv import DictReader
from pathlib import Path
from typing import Dict, List, Set, Tuple
import pandas
import datetime

class PPDataHandler:

    @property
    def number_of_apps(self):
        return self.df.App_Title.unique().size

    def __init__(self, csv_path: Path, outpath: Path) -> None:
        self.outpath = out_path
        self.csv_path = csv_path
        self.df = pandas.read_csv(csv_path,header=0)

    def apps(self):
        return self.df.App_Title.unique().tolist()

    def create_narrowed_csv(self, selected):
        narrowed = self.df['App_Title'].isin(selected)
        narrowed.to_csv(outpath / "tmp_postprocessed_data.csv")
