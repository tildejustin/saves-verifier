from typing import Any, Optional

from semver import Version


class Gamerule:
    """
    Represents a Minecraft gamerule. Can either be versioned or unversioned, a versioned gamerule must always
    have a minimum_version but not necessarily a maximum_version, unversioned gamerules are expected to have neither.
    """

    name: str
    default_value: Any
    minimum_version: Optional[Version] = None
    maximum_version: Optional[Version] = None

    def __init__(self, name: str, default_value: Any, minimum: str = None, maximum: str = None):
        self.name = name
        self.default_value = default_value
        if minimum is not None:
            self.minimum_version = Version.parse(minimum, True)
        if maximum is not None:
            if minimum is None:
                raise ValueError("improper versioned gamerule")
            self.maximum_version = Version.parse(maximum, True)

    def __str__(self):
        return f"{self.name}: {self.default_value}"


def gamerules(version: Version) -> list[Gamerule]:
    """
    :param version: the version which the gamerules must be included in
    :return: all gamerules that are compatible with the given version
    """
    return [rule for rule in rules if rule.minimum_version <= version and
            (rule.maximum_version >= version if rule.maximum_version is not None else True)]


# source for versions: https://minecraft.wiki/w/Game_rule
# generated from Fabric Loader, see gamerules_codegen.py and loader_versioning submodule
rules = [
    Gamerule("doFireTick", "true", "1.4.2-alpha.12.32.a"),
    Gamerule("mobGriefing", "true", "1.4.2-alpha.12.32.a"),
    Gamerule("keepInventory", "false", "1.4.2-alpha.12.32.a"),
    Gamerule("doMobSpawning", "true", "1.4.2-alpha.12.32.a"),
    Gamerule("doMobLoot", "true", "1.4.2-alpha.12.32.a"),
    Gamerule("doTileDrops", "true", "1.4.2-alpha.12.32.a"),
    Gamerule("commandBlockOutput", "true", "1.4.2-alpha.12.38.a"),
    Gamerule("naturalRegeneration", "true", "1.6.0-alpha.13.23.a"),
    Gamerule("doDaylightCycle", "true", "1.6.0-alpha.13.24.a"),
    Gamerule("logAdminCommands", "true", "1.8.0-alpha.14.3.a"),
    Gamerule("showDeathMessages", "true", "1.8.0-alpha.14.10.a"),
    Gamerule("randomTickSpeed", "3", "1.8.0-alpha.14.17.a"),
    Gamerule("sendCommandFeedback", "true", "1.8.0-alpha.14.26.a"),
    Gamerule("reducedDebugInfo", "false", "1.8.0-alpha.14.29.a"),
    Gamerule("doEntityDrops", "true", "1.8.1-rc.1"),
    Gamerule("spectatorsGenerateChunks", "true", "1.9.0-alpha.15.37.a"),
    Gamerule("spawnRadius", "10", "1.9.0-alpha.15.51.a"),
    Gamerule("disableElytraMovementCheck", "false", "1.9.0-alpha.16.7.a"),
    Gamerule("doWeatherCycle", "true", "1.11.0-alpha.16.38.a"),
    Gamerule("maxEntityCramming", "24", "1.11.0-alpha.16.38.a"),
    Gamerule("doLimitedCrafting", "false", "1.12.0-alpha.17.13.a"),
    Gamerule("maxCommandChainLength", "65536", "1.12.0-alpha.17.16.b"),
    Gamerule("announceAdvancements", "true", "1.12.0-alpha.17.18.a"),
    Gamerule("gameLoopFunction", "-", "1.12.0-rc.1", "1.13.0-alpha.17.49.a"),
    Gamerule("disableRaids", "false", "1.14.3-rc.3"),
    Gamerule("doInsomnia", "true", "1.15.0-alpha.19.36.a"),
    Gamerule("doImmediateRespawn", "false", "1.15.0-alpha.19.36.a"),
    Gamerule("drowningDamage", "true", "1.15.0-alpha.19.36.a"),
    Gamerule("fallDamage", "true", "1.15.0-alpha.19.36.a"),
    Gamerule("fireDamage", "true", "1.15.0-alpha.19.36.a"),
    Gamerule("doPatrolSpawning", "true", "1.15.2-rc.1"),
    Gamerule("doTraderSpawning", "true", "1.15.2-rc.1"),
    Gamerule("universalAnger", "false", "1.16.0-rc.1"),
    Gamerule("forgiveDeadPlayers", "true", "1.16.0-rc.1"),
    Gamerule("freezeDamage", "true", "1.17.0-alpha.20.48.a"),
    Gamerule("playersSleepingPercentage", "100", "1.17.0-alpha.20.51.a"),
    Gamerule("doWardenSpawning", "true", "1.19.0-alpha.22.16.a"),
    Gamerule("blockExplosionDropDecay", "true", "1.19.3-alpha.22.44.a"),
    Gamerule("mobExplosionDropDecay", "true", "1.19.3-alpha.22.44.a"),
    Gamerule("tntExplosionDropDecay", "false", "1.19.3-alpha.22.44.a"),
    Gamerule("snowAccumulationHeight", "1", "1.19.3-alpha.22.44.a"),
    Gamerule("waterSourceConversion", "true", "1.19.3-alpha.22.44.a"),
    Gamerule("lavaSourceConversion", "false", "1.19.3-alpha.22.44.a"),
    Gamerule("globalSoundEvents", "true", "1.19.3-alpha.22.44.a"),
    Gamerule("commandModificationBlockLimit", "32768", "1.19.4-alpha.23.3.a"),
    Gamerule("doVinesSpread", "true", "1.19.4-alpha.23.6.a"),
    Gamerule("enderPearlsVanishOnDeath", "true", "1.20.2-beta.1"),
    Gamerule("maxCommandForkCount", "65536", "1.20.3-alpha.23.41.a"),
    Gamerule("projectilesCanBreakBlocks", "True", "1.20.3-alpha.23.42.a"),
    Gamerule("playersNetherPortalDefaultDelay", "80", "1.20.3-alpha.23.42.a"),
    Gamerule("playersNetherPortalCreativeDelay", "1", "1.20.3-alpha.23.42.a")
]
