import json
from csv import DictReader
from pathlib import Path
from typing import Dict, List, Set, Tuple

app_load_type = Dict[Path, Tuple[List[str], List[Dict[str, str]]]] # mapping of store -> apps. apps are a tuple with ([fieldnames], [key->value mappings])
app_store_type = Dict[Path, List[Dict[str, str]]] # mapping of store -> apps. apps are a dict of key->value

class AppLoader:

    @property
    def number_of_apps(self):
        count = 0
        for _, store_info in self.apps.items():
            count += len(store_info)
        return count

    def __init__(self) -> None:
        self.module_path = Path(__file__).parent
        self.fieldnames: Dict[Path, Set[str]] = dict()
        with open(self.module_path / "apps.json", "r") as f:
            _apps: app_load_type = json.load(f)
            _apps_store: app_store_type = dict()
            for store_name, store_info in _apps.items():
                store_name = Path(store_name)
                if store_name not in self.fieldnames:
                    self.fieldnames[store_name] = set()
                fieldnames = store_info[0]
                self.fieldnames[store_name].update(fieldnames)
                _apps_store[store_name] = store_info[1]
            self.apps = _apps_store

    def load_app_store(self, filename: Path) -> List[Dict[str, str]]:
        new_app_data = []
        with open(filename, newline='') as csvfile:
            app_reader = DictReader(csvfile)
            assert "App_Title" in app_reader.fieldnames
            
            if filename not in self.fieldnames or filename not in self.apps:
                self.fieldnames[filename] = set()
                self.apps[filename] = list()
            self.fieldnames[filename].update(app_reader.fieldnames)

            for row in app_reader:
                self.apps[filename].append(row)
                new_app_data.append(row)

            return new_app_data
    
    def close(self):
        apps_save = dict()
        for store, fieldnames in self.fieldnames.items():
            app_data = self.apps[store]
            apps_save[str(store.absolute())] = (list(fieldnames), app_data)
        with open(self.module_path / "apps.json", "w") as f:
            json.dump(apps_save, f)