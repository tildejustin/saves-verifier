import datetime
import json
from pathlib import Path

from semver import Version

from util import normalize_time


class SpeedrunIGTInfo:
    igt: str
    rta: str
    version: str
    category: str
    run_type: str
    result_parts: list[str]

    def __init__(self, folder: Path):
        """
        parses SpeedrunIGT information, if present

        :param folder: the speedrunigt/ folder in a save
        """
        if folder is None:
            raise FileNotFoundError("speedrunigt folder not present")
        record: dict = json.loads(folder.joinpath("record.json").read_text())
        self.version = record.get("speedrunigt_version")
        self.category = record.get("category").lower()
        self.run_type = record.get("run_type")
        self.igt = normalize_time(str(datetime.timedelta(milliseconds=record.get("retimed_igt"))))
        self.rta = normalize_time(str(datetime.timedelta(milliseconds=record.get("final_rta"))))

        # log = folder.joinpath("logs/igt_timer.log").read_text()
        # result_line: str = next(filter(lambda line: line.startswith("Result > "), log.splitlines()))
        # self.result_parts = result_line.replace("Result > ", "").split(",")
        # self.igt = self.result_parts[0].replace("IGT: ", "")
        # self.rta = self.result_parts[1]
