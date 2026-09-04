import json
from pathlib import Path
from ..exceptions import PersistenceError


class JsonStore:
    """Handles reading and writing JSON files.
    """

    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True,exist_ok=True)

    def _path(self, filename):
        return self.data_dir / filename

    def save(self, filename, data):

        path = self._path(filename)

        temp = path.with_suffix(path.suffix + ".tmp")

        try:

            temp.write_text(
                json.dumps(data,indent=2,ensure_ascii=False),encoding="utf-8"
            )
            temp.replace(path)

        except (OSError,TypeError,ValueError) as error:

            raise PersistenceError("Could not save JSON file: " + str(path)) from error

    def load(self, filename, default):

        path = self._path(filename)

        if not path.exists():

            self.save(filename,default)
            return default

        try:

            text = path.read_text(encoding="utf-8")
            return json.loads(text)

        except (OSError,json.JSONDecodeError) as error:

            raise PersistenceError("Could not load JSON file: " + str(path)) from error