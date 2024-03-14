import os.path
from dataclasses import dataclass
from subprocess import Popen, DEVNULL
from time import sleep
from typing import Any, Optional

from py4j.java_gateway import JavaGateway
from semver import Version

folder = "loader_versioning/build/libs"
process = Popen(["java", "-jar", os.path.join(folder, os.listdir(folder)[0])], shell=False, stdout=DEVNULL, stderr=DEVNULL)
# let the jvm start up
sleep(.2)


@dataclass
class GameRule:
    name: str
    default_value: Any
    minimum_version: Version
    maximum_version: Optional[Version] = None

    def __str__(self):
        return f"{self.name}: {self.default_value}"


def gamerules(max_version: Version) -> list[GameRule]:
    return list(filter(lambda _: _.minimum_version <= max_version, rules))


loader_versioning = JavaGateway().entry_point


def parse(version: str) -> Optional[Version]:
    try:
        return Version.parse(loader_versioning.normalizedVersion(version), True)
    except ValueError:
        return None


rules = list()
try:
    # source for versions: https://minecraft.wiki/w/Game_rule
    rules = [
        GameRule("doFireTick", "true", parse("12w32a")),
        GameRule("mobGriefing", "true", parse("12w32a")),
        GameRule("keepInventory", "false", parse("12w32a")),
        GameRule("doMobSpawning", "true", parse("12w32a")),
        GameRule("doMobLoot", "true", parse("12w32a")),
        GameRule("doTileDrops", "true", parse("12w32a")),
        GameRule("commandBlockOutput", "true", parse("12w38a")),
        GameRule("naturalRegeneration", "true", parse("13w23a")),
        GameRule("doDaylightCycle", "true", parse("13w24a")),
        GameRule("logAdminCommands", "true", parse("14w03a")),
        GameRule("showDeathMessages", "true", parse("14w10a")),
        GameRule("randomTickSpeed", "3", parse("14w17a")),
        GameRule("sendCommandFeedback", "true", parse("14w26a")),
        GameRule("reducedDebugInfo", "false", parse("14w29a")),
        GameRule("doEntityDrops", "true", parse("1.8.1-pre1")),
        GameRule("spectatorsGenerateChunks", "true", parse("15w37a")),
        GameRule("spawnRadius", "10", parse("15w51a")),
        GameRule("disableElytraMovementCheck", "false", parse("16w07a")),
        GameRule("doWeatherCycle", "true", parse("16w38a")),
        GameRule("maxEntityCramming", "24", parse("16w38a")),
        GameRule("doLimitedCrafting", "false", parse("17w13a")),
        GameRule("maxCommandChainLength", "65536", parse("17w16b")),
        GameRule("announceAdvancements", "true", parse("17w18a")),
        GameRule("gameLoopFunction", "-", parse("1.12-pre1"), parse("17w49a")),
        GameRule("disableRaids", "false", parse("1.14.3-pre3")),
        GameRule("doInsomnia", "true", parse("19w36a")),
        GameRule("doImmediateRespawn", "false", parse("19w36a")),
        GameRule("drowningDamage", "true", parse("19w36a")),
        GameRule("fallDamage", "true", parse("19w36a")),
        GameRule("fireDamage", "true", parse("19w36a")),
        GameRule("doPatrolSpawning", "true", parse("1.15.2-pre1")),
        GameRule("doTraderSpawning", "true", parse("1.15.2-pre1")),
        GameRule("universalAnger", "false", parse("1.16-pre1")),
        GameRule("forgiveDeadPlayers", "true", parse("1.16-pre1")),
        GameRule("freezeDamage", "true", parse("20w48a")),
        GameRule("playersSleepingPercentage", "100", parse("20w51a")),
        GameRule("doWardenSpawning", "true", parse("22w16a")),
        GameRule("blockExplosionDropDecay", "true", parse("22w44a")),
        GameRule("mobExplosionDropDecay", "true", parse("22w44a")),
        GameRule("tntExplosionDropDecay", "false", parse("22w44a")),
        GameRule("snowAccumulationHeight", "1", parse("22w44a")),
        GameRule("waterSourceConversion", "true", parse("22w44a")),
        GameRule("lavaSourceConversion", "false", parse("22w44a")),
        GameRule("globalSoundEvents", "true", parse("22w44a")),
        GameRule("commandModificationBlockLimit", "32768", parse("23w03a")),
        GameRule("doVinesSpread", "true", parse("23w06a")),
        GameRule("enderPearlsVanishOnDeath", "true", parse("1.20.2-pre1")),
        GameRule("maxCommandForkCount", "65536", parse("23w41a")),
        GameRule("projectilesCanBreakBlocks", "True", parse("23w42a")),
        GameRule("playersNetherPortalDefaultDelay", "80", parse("23w42a")),
        GameRule("playersNetherPortalCreativeDelay", "1", parse("23w42a")),
        GameRule("spawnChunkRadius", "2", parse("24w03a"))
    ]
finally:
    # if the process isn't killed, bad things happen
    process.kill()

for rule in rules:
    quote = "\""
    print(f'Gamerule("{rule.name}", "{rule.default_value}", "{str(rule.minimum_version)}"{", " + quote + str(rule.maximum_version) + quote if rule.maximum_version is not None else ""}),')
