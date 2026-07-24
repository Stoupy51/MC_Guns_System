
# Zombies interaction feedback cues (wallbuys, doors, perks, traps, mystery box, PAP).
# Each cue is exactly one command, inlined at its call site via zb_sound() rather than emitted as a
# wrapper mcfunction — same sound, one fewer file and one fewer function dispatch per use.
from functools import cache

from stewbeet import Mem


@cache
def _sound_table(ns: str) -> dict[str, str]:
	""" Build the cue -> command table for a namespace (cached; ns is fixed within a build). """
	ingame: str = f"@a[scores={{{ns}.zb.in_game=1}}]"
	return {
		"success": "playsound minecraft:entity.experience_orb.pickup ambient @s ~ ~ ~ 0.8 1.25",
		"refill": "playsound minecraft:block.note_block.pling ambient @s ~ ~ ~ 0.8 1.45",
		"replace": "playsound minecraft:item.armor.equip_iron ambient @s ~ ~ ~ 0.9 1.0",
		"deny": "playsound minecraft:entity.villager.no ambient @s ~ ~ ~ 0.8 1.0",
		"announce": f"playsound minecraft:block.note_block.bit ambient {ingame} ~ ~ ~ 0.6 0.9",
		"power_on": f"playsound minecraft:block.beacon.activate ambient {ingame} ~ ~ ~ 0.9 1.0",
		"box_ready": f"playsound minecraft:entity.player.levelup ambient {ingame} ~ ~ ~ 0.7 1.0",

		## Mystery Box: Black Ops-style sound effects
		"box_spin": f"playsound {ns}:zombies/mystery_box/box_spin ambient {ingame} ~ ~ ~ 0.1 1.0",
		"music_box": f"playsound {ns}:zombies/mystery_box/music_box ambient {ingame} ~ ~ ~ 1.0 1.0",
		# Timeslip spin: the box tune sped up to match the 2x pull (exclusive to that case)
		"music_box_short": f"playsound {ns}:zombies/mystery_box/music_box_short ambient {ingame} ~ ~ ~ 1.0 1.0",
		"box_open": f"playsound {ns}:zombies/mystery_box/open ambient {ingame} ~ ~ ~ 1.0 1.0",
		"box_close": f"playsound {ns}:zombies/mystery_box/close ambient {ingame} ~ ~ ~ 1.0 1.0",
		"box_bye_bye": f"execute as {ingame} at @s run playsound {ns}:zombies/mystery_box/bye_bye ambient @s ~ ~ ~ 1.0 1.0",
		"box_woosh": f"playsound {ns}:zombies/mystery_box/woosh ambient {ingame} ~ ~ ~ 1.0 1.0",
		"box_disappear": f"playsound {ns}:zombies/mystery_box/disappear ambient {ingame} ~ ~ ~ 1.0 1.0",
		"box_poof": f"playsound {ns}:zombies/mystery_box/poof ambient {ingame} ~ ~ ~ 1.0 1.0",
		"box_land": f"playsound {ns}:zombies/mystery_box/land ambient {ingame} ~ ~ ~ 1.0 1.0",

		## PAP: Black Ops-style sound effects (positional, distance-limited)
		"pap_knuckle_crack": f"playsound {ns}:zombies/pap/knuckle_crack ambient {ingame} ~ ~ ~ 1.0 1.0",
		"pap_loop": f"playsound {ns}:zombies/pap/pap_loop ambient {ingame} ~ ~ ~ 0.25 1.0",
		"pap_dispense": f"playsound {ns}:zombies/pap/dispense ambient {ingame} ~ ~ ~ 1.0 1.0",
		"pap_upgrade": f"playsound {ns}:zombies/pap/upgrade ambient {ingame} ~ ~ ~ 0.5 1.0",
		"pap_jingle_sting": f"playsound {ns}:zombies/pap/jingle_sting ambient {ingame} ~ ~ ~ 1.0 1.0",
		# Timeslip x3 PAP: the 3x-speed jingle asset (ffmpeg atempo=1.5,2.0) fits the shorter animation
		"pap_jingle_sting_short": f"playsound {ns}:zombies/pap/jingle_sting_short ambient {ingame} ~ ~ ~ 1.0 1.0",
		"pap_ready": f"playsound {ns}:zombies/pap/ready ambient {ingame} ~ ~ ~ 1.0 1.0",
		"pap_retreat_loop": f"playsound {ns}:zombies/pap/retreat_loop ambient {ingame} ~ ~ ~ 0.5 1.0",
		"pap_power_on": f"playsound {ns}:zombies/pap/power_on ambient {ingame} ~ ~ ~ 1.0 1.0",
		"pap_deny": f"playsound {ns}:zombies/pap/deny ambient {ingame} ~ ~ ~ 1.0 1.0",
	}


def zb_sound(name: str) -> str:
	""" The single command playing a zombies feedback cue, for inlining into a caller's body. """
	return _sound_table(Mem.ctx.project_id)[name]
