
# Shared command builders for zombies modules.
from ..helpers import MGS_TAG


def game_active_guard_cmd(ns: str) -> str:
	""" Return the standard guard command for active zombies games. """
	return f'execute unless data storage {ns}:zombies game{{state:"active"}} run return fail'


def deny_not_enough_points_body(ns: str, version: str, price_score: str) -> str:
	""" Standardized not-enough-points response body. """
	return f"""
tellraw @s [{MGS_TAG},{{"text":"You don't have enough points (","color":"red"}},{{"score":{{"name":"{price_score}","objective":"{ns}.data"}},"color":"yellow"}},{{"text":" needed).","color":"red"}}]
function {ns}:v{version}/zombies/feedback/sound_deny
""".strip()


def deny_requires_power_body(ns: str, version: str, label: str) -> str:
	""" Standardized requires-power response body. """
	return f"""
tellraw @s [{MGS_TAG},{{"text":"This {label} requires power.","color":"red"}}]
function {ns}:v{version}/zombies/feedback/sound_deny
""".strip()

