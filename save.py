import json
import os
from datetime import timedelta, datetime
from pathlib import Path
from typing import Optional, Any

import nbtlib
import requests
from semver import Version

from SpeedrunIGTInfo import SpeedrunIGTInfo
from gamerules import Gamerule, gamerules
from seed_utils import is_random
from util import normalize_time


class WorldSave:
    world_name: str
    game_version: Version
    client: str = None
    modded: bool = None
    seed: int
    ticks: int
    time_played: str
    last_played: str
    datapacks: list[str]
    bonus_chest: Optional[bool] = None
    cheats: bool
    modded: bool
    difficulty: str
    dragon_killed: bool
    dragon_ever_killed: bool
    dragon_death_count: int
    generator_options: str = ""
    players: dict[str, str]
    gamerules: list[Gamerule]
    advancements: list[str] = None
    speedrunigt_data: SpeedrunIGTInfo = None

    def __init__(self, save_folder: Path):
        level_data: nbtlib.Compound = nbtlib.load(save_folder.joinpath("level.dat")).get("Data")
        for name, value in level_data.items():
            # print(name + ": " + str(value))
            match name:
                case "LevelName":
                    self.world_name = value
                case "ServerBrands":
                    self.client = value[0]
                case "Version":
                    self.game_version = Version.parse(value.get("Name"), True)
                case "Time":
                    self.ticks = int(value)
                    self.time_played = normalize_time(str(timedelta(seconds=value / 20)))
                case "LastPlayed":
                    self.last_played = (datetime.utcfromtimestamp(value // 1000)
                                        .replace(microsecond=value % 1000 * 1000)
                                        .strftime("%H:%M:%S %d-%b-%Y UTC"))
                case "allowCommands":
                    self.cheats = value == 1
                case "DragonFight":
                    self.parse_dragon_fight(value)
                case "DimensionData":
                    self.parse_dragon_fight(value.get("1").get("DragonFight"))
                case "hardcore":
                    self.hardcore = value == 1
                case "WasModded":
                    self.modded = value == 1
                case "RandomSeed":
                    self.seed = int(value)
                case "generatorOptions":
                    self.generator_options = value
                case "MapFeatures":
                    self.structures = value == 1
                case "WorldGenSettings":
                    self.seed = int(value.get("seed"))
                    self.bonus_chest = value.get("bonus_chest") == 1
                    self.structures = value.get("generate_features") == 1
                case "DataPacks":
                    self.datapacks = value.get("Enabled")
                case "GameRules":
                    self.gamerules = [Gamerule(rule_name, rule_value) for rule_name, rule_value in value.items()]
                case "Difficulty":
                    diffs = {
                        -1: "negative peaceful (1.6-)",
                        0: "peaceful",
                        1: "easy",
                        2: "normal",
                        3: "hard"
                    }
                    self.difficulty = diffs.get(value)

        self.players = self.parse_players(save_folder)
        speedrunigt_folder = save_folder.joinpath("speedrunigt")
        if speedrunigt_folder.exists():
            self.speedrunigt_data = self.parse_speedrunigt(speedrunigt_folder)
        advancements_folder = save_folder.joinpath("advancements")
        if os.path.exists(advancements_folder):
            advancements_files = os.listdir(advancements_folder)
            self.advancements = set()
            for f in advancements_files:
                with open(os.path.join(save_folder.joinpath("advancements"), f)) as f:
                    self.advancements.update(filter(lambda s: not s.startswith("minecraft:recipe") and "/" in s, json.load(f)))

    @staticmethod
    def yes_no(t: Any):
        try:
            return "yes" if t else "no"
        except AttributeError:
            return "unknown"

    def __str__(self):
        result = ""
        result += f"name: {self.world_name}, v{self.nullify(self.game_version)}\n"
        result += f"seed: {str(self.seed)}"
        if not is_random(self.seed):
            result += ", not random"
        result += f"\ndifficulty: {self.difficulty}, structures: {self.yes_no(self.structures)}, cheats: {self.yes_no(self.cheats)}, hardcore: {self.yes_no(self.hardcore)}{self.generator_options}"
        if self.bonus_chest is not None:
            result += ", bonus chest: " + self.yes_no(self.bonus_chest)
        result += "\n"
        if self.speedrunigt_data is not None:
            result += f"speedrunigt: igt: {self.speedrunigt_data.igt}, rta: {self.speedrunigt_data.rta}, cat: {self.speedrunigt_data.category}, "
            result += f"seed type: {self.speedrunigt_data.run_type}, v{self.speedrunigt_data.version}\n"
        else:
            result += "speedrunigt not found\n"
        result += f"ticks: {self.ticks} ({self.time_played}), last at {self.last_played}\n"
        if self.game_version is not None and self.game_version >= Version(1, 13) and self.datapacks is not None:
            result += f"datapacks: {'unknown' if self.datapacks is None else ', '.join(self.datapacks)}\n"
        result += f"dragon: " + ("dead" if self.dragon_killed else "alive") + ", has died: " + self.yes_no(self.dragon_ever_killed) + f", times: {str(self.dragon_death_count)}\n"
        result += "players: " + "\n".join([f"{name}, {uuid}" for uuid, name in self.players.items()]) + "\n"
        result += f"modded: {self.yes_no(self.modded)}, client: {self.client if self.client is not None else 'unknown'}\n"
        result += "gamerules: " + self.get_gamerule_text()
        if self.advancements is not None:
            result += "advancement count: " + str(len(self.advancements))
        # TODO: add the rest of the set vars in the big case statement
        return result

    @staticmethod
    def nullify(t: Any):
        return t if t is not None else "null"

    def parse_dragon_fight(self, dragon_fight: nbtlib.Compound):
        self.dragon_killed = dragon_fight.get("DragonKilled") == 1
        self.dragon_ever_killed = dragon_fight.get("PreviouslyKilled") == 1
        self.dragon_death_count = 20 - len(dragon_fight.get("Gateways"))

    @staticmethod
    def parse_speedrunigt(save_folder: Path) -> Optional[SpeedrunIGTInfo]:
        try:
            return SpeedrunIGTInfo(save_folder)
        except FileNotFoundError:
            return None

    @staticmethod
    def get_player_name(uuid: str) -> str:
        try:
            name = requests.get("https://api.minecraftservices.com/minecraft/profile/lookup/" + uuid).json().get("name")
            return "unknown uuid" if name is None else name
        except requests.ConnectionError:
            return "http error"

    def parse_players(self, save_folder: Path) -> dict[str, str]:
        stats_files = os.listdir(save_folder.joinpath("stats"))
        return {
            uuid: self.get_player_name(uuid)
            for uuid in [file.split(".")[0] for file in stats_files]
        }

    # we don't talk about this method
    def get_gamerule_text(self) -> str:
        correct_rules = gamerules(self.game_version)
        rule_names = {rule.name: rule for rule in self.gamerules}
        correct_rules_names = {rule.name: rule for rule in correct_rules}
        gamerule_text = ""
        for rule in self.gamerules:
            if rule.name not in correct_rules_names:
                gamerule_text += str(rule) + " not in correct ruleset\n"
            elif rule.default_value != correct_rules_names.get(rule.name).default_value:
                gamerule_text += str(rule) + ", should be: " + str(
                    correct_rules_names.get(rule.name).default_value) + "\n"
        for rule in correct_rules_names:
            if rule not in rule_names:
                gamerule_text += str(rule) + " not in current ruleset\n"
        if not gamerule_text:
            gamerule_text = "all normal"
        return gamerule_text + "\n"

#     def __str__(self):
#         correct_rules = gamerules(self.game_version)
#         rule_names = {rule.name: rule for rule in self.game_rules}
#         correct_rules_names = {rule.name: rule for rule in correct_rules}
#         gamerule_text = ""
#         for rule in self.game_rules:
#             if rule.name not in rule_names:
#                 gamerule_text += str(rule) + "not in correct ruleset\n"
#             elif rule.default_value != correct_rules_names.get(rule.name).default_value:
#                 gamerule_text += str(rule) + ", should be: " + str(
#                     correct_rules_names.get(rule.name).default_value) + "\n"
#         for rule in correct_rules_names:
#             if rule not in rule_names:
#                 gamerule_text += str(rule) + " not in current ruleset\n"
#         return f"""\
# name: {self.world_name}, v{self.game_version}
# seed: {str(self.seed) + (", not randomly generatable" if not is_random(self.seed) else "")}
# {f"{self.srigt_igt}, {self.srigt_rta}, cat: {self.srigt_category.lower()}, seed type: {self.srigt_run_type}, v{self.srigt_version}"
#         if self.has_srigt else "speedrunigt not present"}
# ticks: {self.ticks} ({self.time_played}), last at {self.last_played}
# datapacks: {"unknown" if self.datapacks is None else ", ".join(self.datapacks)}
# dragon: {"dead" if self.dragon_killed else "alive"}, was dead: {"yes" if self.dragon_been_killed else "no"}\
# {", times: " + str(self.dragon_death_count) if self.dragon_death_count is not None else ""}
# cheats: {"yes" if self.cheats else "no"}
# players: {os.linesep.join([f"{name if name is not None else 'unknown uuid'}: {uuid}" for uuid, name in self.players.items()])}
# gamerules: {"all normal" if not gamerule_text else gamerule_text}"""
