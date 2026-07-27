""" The power-up registry: what each one looks like, how long it lasts and how it sounds. """
# ruff: noqa: E501
# Imports
from dataclasses import dataclass


# Classes
@dataclass(frozen=True)
class PowerupType:
	""" One power-up drop: its appearance, its dispatch number, and how it activates. """
	item: str
	""" Placeholder item id for the dropped item entity. """
	display: str
	color: str
	type_num: int
	""" Integer used in scoreboards and in the spawn dispatch. """
	tier: str
	""" "common" | "rare" — rare has a 25% chance to appear each shuffle cycle. """

	# Timed power-ups only; a non-zero duration is what makes one timed (see TIMED_POWERUPS).
	duration: int = 0
	""" Active duration in ticks. """
	scoreboard: str = ""
	""" The {ns}.special.<scoreboard> objective name. """
	bossbar_id: str = ""
	""" The {ns}:pu_<bossbar_id> bossbar name. """
	bb_color: str = ""

	# Sounds, relative to {ns}:zombies/powerups/. Without `sound` the generic level-up chime plays.
	sound: str = ""
	additional: str = ""
	""" A second sound played simultaneously with `sound`. """
	end_sound: str = ""
	""" Played once when a timed effect expires. """

# Constants
POWERUP_TYPES: dict[str, PowerupType] = {
	"max_ammo":        PowerupType(item="minecraft:amethyst_shard",       display="Max Ammo",       color="aqua",         type_num=1, tier="common", sound="max_ammo", additional="max_ammo_additional"),
	"insta_kill":      PowerupType(item="minecraft:fermented_spider_eye", display="Insta Kill",     color="red",          type_num=2, tier="common", duration=600, scoreboard="instant_kill",  bossbar_id="pu_insta_kill",     bb_color="red",    sound="insta_kill", end_sound="insta_kill_off"),
	"double_points":   PowerupType(item="minecraft:gold_ingot",           display="Double Points",  color="yellow",       type_num=3, tier="common", duration=600, scoreboard="double_points", bossbar_id="pu_double_points",  bb_color="yellow", sound="double_points", end_sound="double_points_off"),
	"carpenter":       PowerupType(item="minecraft:oak_log",              display="Carpenter",      color="gold",         type_num=4, tier="common", sound="carpenter"),
	"nuke":            PowerupType(item="minecraft:tnt",                  display="Nuke",           color="red",          type_num=5, tier="common", sound="nuke", additional="nuke_additional"),
	"unlimited_ammo":  PowerupType(item="minecraft:blaze_rod",            display="Unlimited Ammo", color="green",        type_num=6, tier="rare",   duration=600, scoreboard="infinite_ammo", bossbar_id="pu_unlimited_ammo", bb_color="green"),
	"random_perk":     PowerupType(item="minecraft:glass_bottle",         display="Random Perk",    color="light_purple", type_num=7, tier="rare",   sound="random_perk"),
	"free_pap":        PowerupType(item="minecraft:diamond",              display="Free PAP",       color="aqua",         type_num=8, tier="rare"),
	"cash_drop":       PowerupType(item="minecraft:emerald",              display="Cash Drop",      color="green",        type_num=9, tier="rare",   sound="bonus_points"),
	"fire_sale":       PowerupType(item="minecraft:firework_star",        display="Fire Sale",      color="light_purple", type_num=10, tier="rare",  sound="fire_sale"),
	"bonfire_sale":    PowerupType(item="minecraft:campfire",             display="Bonfire Sale",   color="gold",         type_num=11, tier="rare",  sound="bonfire_sale"),
}

POWERUP_LIFETIME: int    = 530
""" 26.5 seconds in ticks. """
POWERUP_BLINK_START: int = 200
""" Blink warning when this many ticks remain (~10s). """
FIRE_SALE_DURATION: int  = 600
""" 30 seconds in ticks: Mystery Box costs 10 points. """
BONFIRE_SALE_DURATION: int = 600
""" 30 seconds in ticks: Pack-a-Punch costs 200 points (1000/5). """

# Convenience view: only power-ups with a timed duration
TIMED_POWERUPS: dict[str, PowerupType] = {k: v for k, v in POWERUP_TYPES.items() if v.duration}

# Functions
def pu_snd(ns: str, name: str, vol: float = 0.7, pitch: float = 1.0, at_s: bool = False) -> str:
	""" A power-up cue played for every in-game player at their OWN position.

	Power-ups affect everyone, so their cues must be GLOBAL rather than positional: playing at each
	player's own feet means all of them hear it at full volume however far they were from the drop.
	`at_s` returns a bare fragment for use after an `execute if ...` of the caller's own.
	"""
	body = f"as @a[scores={{{ns}.zb.in_game=1}}] at @s run playsound {ns}:zombies/powerups/{name} ambient @s ~ ~ ~ {vol} {pitch}"
	return body if at_s else f"execute {body}"

def pu_activate_sound(ns: str, v: PowerupType, vol: float = 1.0) -> str:
	""" The activation cue for a power-up, including its "additional" layer when it has one. """
	if not v.sound:
		return f"playsound minecraft:entity.player.levelup ambient @a[scores={{{ns}.zb.in_game=1}}] ~ ~ ~ 1.0 1.0"
	lines = [pu_snd(ns, v.sound, vol)]
	if v.additional:
		lines.append(pu_snd(ns, v.additional, vol))
	return "\n".join(lines)

