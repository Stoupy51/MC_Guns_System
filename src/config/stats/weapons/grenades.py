""" Throwable stat tables and the zombies lethal-slot ordering. """
# Imports
from stewbeet import JsonDict

from ..fire_modes import SEMI, FireMode
from ..keys import (
	BASE_WEAPON,
	CAPACITY,
	COOLDOWN,
	EXPLOSION_DAMAGE,
	EXPLOSION_DECAY,
	EXPLOSION_RADIUS,
	GRENADE_DURATION,
	GRENADE_EFFECT_RADIUS,
	GRENADE_FUSE,
	GRENADE_TYPE,
	PROJECTILE_GRAVITY,
	PROJECTILE_MODEL,
	PROJECTILE_SPEED,
	REMAINING_BULLETS,
)

# Constants
FRAG_GRENADE: JsonDict = {
	"stats": {
		GRENADE_TYPE: "frag", **FireMode.stats(SEMI),
		CAPACITY: 1, REMAINING_BULLETS: 1, COOLDOWN: 20,
		PROJECTILE_SPEED: 1000, PROJECTILE_GRAVITY: 60, PROJECTILE_MODEL: "frag_grenade",
		GRENADE_FUSE: 80,  # 4 seconds
		EXPLOSION_RADIUS: 6, EXPLOSION_DAMAGE: 25, EXPLOSION_DECAY: 0.75,
	}
}

SEMTEX: JsonDict = {
	"stats": {
		GRENADE_TYPE: "semtex", **FireMode.stats(SEMI),
		CAPACITY: 1, REMAINING_BULLETS: 1, COOLDOWN: 20,
		PROJECTILE_SPEED: 1200, PROJECTILE_GRAVITY: 50, PROJECTILE_MODEL: "semtex",
		GRENADE_FUSE: 80,  # 4 seconds
		EXPLOSION_RADIUS: 6, EXPLOSION_DAMAGE: 28, EXPLOSION_DECAY: 0.75,
	}
}

SMOKE_GRENADE: JsonDict = {
	"tactical": True,
	"stats": {
		GRENADE_TYPE: "smoke", **FireMode.stats(SEMI),
		CAPACITY: 1, REMAINING_BULLETS: 1, COOLDOWN: 20,
		PROJECTILE_SPEED: 1000, PROJECTILE_GRAVITY: 60, PROJECTILE_MODEL: "smoke_grenade",
		GRENADE_FUSE: 60,  # 3 seconds before activation
		GRENADE_DURATION: 60,  # 3 seconds of smoke
		GRENADE_EFFECT_RADIUS: 5,
	}
}

FLASH_GRENADE: JsonDict = {
	"tactical": True,
	"stats": {
		GRENADE_TYPE: "flash", **FireMode.stats(SEMI),
		CAPACITY: 1, REMAINING_BULLETS: 1, COOLDOWN: 20,
		PROJECTILE_SPEED: 1200, PROJECTILE_GRAVITY: 50, PROJECTILE_MODEL: "flash_grenade",
		GRENADE_FUSE: 60,  # 3 seconds before detonation
		GRENADE_DURATION: 100,  # 5 seconds of blindness
		GRENADE_EFFECT_RADIUS: 15,
	}
}

# Widow's Wine web grenade (zombies perk only, hotbar.7): webbing that roots and lightly damages nearby zombies.
# TODO: it reuses the frag art until a web-grenade texture exists.
WEB_GRENADE: JsonDict = {
	"stats": {
		GRENADE_TYPE: "web", **FireMode.stats(SEMI),
		BASE_WEAPON: "web_grenade",
		CAPACITY: 1, REMAINING_BULLETS: 1, COOLDOWN: 20,
		PROJECTILE_SPEED: 1500, PROJECTILE_GRAVITY: 60, PROJECTILE_MODEL: "frag_grenade",  # 1.5x throw motion
		GRENADE_FUSE: 40,  # 2 seconds
		GRENADE_EFFECT_RADIUS: 5,
	}
}

# Zombies-only tactical (hotbar.6): attracts zombies during the fuse, then explodes. "tactical" routes it to the tactical slot, like smoke and flash;
# base_weapon lets the mystery box duplicate check match it. Damage uses the BO to MC 2/15 conversion (BO ~1000, MC ~130), one-shotting the horde up to about round 10.
MONKEY_BOMB: JsonDict = {
	"tactical": True,
	"stats": {
		GRENADE_TYPE: "monkey_bomb", **FireMode.stats(SEMI),
		BASE_WEAPON: "monkey_bomb",
		CAPACITY: 1, REMAINING_BULLETS: 1, COOLDOWN: 20,
		PROJECTILE_SPEED: 800, PROJECTILE_GRAVITY: 60, PROJECTILE_MODEL: "monkey_bomb",
		GRENADE_FUSE: 180,  # 9 seconds (BO timing: lands, attracts ~7s, then detonates)
		EXPLOSION_RADIUS: 7, EXPLOSION_DAMAGE: 130, EXPLOSION_DECAY: 0.8,
	}
}

LETHAL_GRENADE_IDS: list[str] = ["frag_grenade", "semtex"]
""" Zombies lethal slot (hotbar.7, wallbuy kind 2), refilled with the bought type on round end, Max Ammo and recovery.

The order is the `{ns}.zb.lethal_type` enum, stored in live player scores: reordering renumbers them, and an index past the end refills frags.
"""
TACTICAL_GRENADE_IDS: list[str] = ["smoke_grenade", "flash_grenade", "monkey_bomb"]
""" Zombies tactical slot (hotbar.6), given back by Max Ammo once emptied.

`{ns}.zb.tactical_type` holds the index plus one, 0 for none: reordering renumbers live player scores.
"""

