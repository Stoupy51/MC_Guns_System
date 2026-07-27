""" Throwable stat tables and the zombies lethal-slot ordering. """
# Imports
from stewbeet import JsonDict

from ..keys import (
	BASE_WEAPON,
	CAPACITY,
	COOLDOWN,
	EXPLOSION_DAMAGE,
	EXPLOSION_DECAY,
	EXPLOSION_RADIUS,
	FIRE_MODE,
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
# Grenades
FRAG_GRENADE: JsonDict = {
	"stats": {
		GRENADE_TYPE: "frag", FIRE_MODE: "semi",
		CAPACITY: 1, REMAINING_BULLETS: 1, COOLDOWN: 20,
		PROJECTILE_SPEED: 1000, PROJECTILE_GRAVITY: 60, PROJECTILE_MODEL: "frag_grenade",
		GRENADE_FUSE: 80,  # 4 seconds
		EXPLOSION_RADIUS: 6, EXPLOSION_DAMAGE: 25, EXPLOSION_DECAY: 0.75,
	}
}

SEMTEX: JsonDict = {
	"stats": {
		GRENADE_TYPE: "semtex", FIRE_MODE: "semi",
		CAPACITY: 1, REMAINING_BULLETS: 1, COOLDOWN: 20,
		PROJECTILE_SPEED: 1200, PROJECTILE_GRAVITY: 50, PROJECTILE_MODEL: "semtex",
		GRENADE_FUSE: 80,  # 4 seconds
		EXPLOSION_RADIUS: 6, EXPLOSION_DAMAGE: 28, EXPLOSION_DECAY: 0.75,
	}
}

SMOKE_GRENADE: JsonDict = {
	"stats": {
		GRENADE_TYPE: "smoke", FIRE_MODE: "semi",
		CAPACITY: 1, REMAINING_BULLETS: 1, COOLDOWN: 20,
		PROJECTILE_SPEED: 1000, PROJECTILE_GRAVITY: 60, PROJECTILE_MODEL: "smoke_grenade",
		GRENADE_FUSE: 60,  # 3 seconds before activation
		GRENADE_DURATION: 60,  # 3 seconds of smoke
		GRENADE_EFFECT_RADIUS: 5,
	}
}

FLASH_GRENADE: JsonDict = {
	"stats": {
		GRENADE_TYPE: "flash", FIRE_MODE: "semi",
		CAPACITY: 1, REMAINING_BULLETS: 1, COOLDOWN: 20,
		PROJECTILE_SPEED: 1200, PROJECTILE_GRAVITY: 50, PROJECTILE_MODEL: "flash_grenade",
		GRENADE_FUSE: 60,  # 3 seconds before detonation
		GRENADE_DURATION: 100,  # 5 seconds of blindness
		GRENADE_EFFECT_RADIUS: 15,
	}
}

# Widow's Wine web grenade (zombies perk-exclusive, hotbar.7).
# Bursts into webbing that roots and lightly damages nearby zombies.
# PROJECTILE_MODEL/model reuse the frag grenade art as a placeholder until a dedicated web-grenade texture exists (README task 5 = HUMAN art follow-up).
WEB_GRENADE: JsonDict = {
	"stats": {
		GRENADE_TYPE: "web", FIRE_MODE: "semi",
		BASE_WEAPON: "web_grenade",
		CAPACITY: 1, REMAINING_BULLETS: 1, COOLDOWN: 20,
		PROJECTILE_SPEED: 1500, PROJECTILE_GRAVITY: 60, PROJECTILE_MODEL: "frag_grenade",  # 1.5x throw motion
		GRENADE_FUSE: 40,  # 2 seconds
		GRENADE_EFFECT_RADIUS: 5,
	}
}

# Zombies-exclusive tactical (hotbar.6): attracts zombies during the fuse, then explodes.
# "tactical": True keeps it out of the camo pipeline and lets wallbuys/inventory route it to the tactical slot. base_weapon is set so the mystery box duplicate check can match it in hotbar.6.
# Damage follows the BO->MC 2/15 HP conversion used by calc_zombie_hp (BO ~1000 -> MC ~130), so the blast one-shots the horde up to roughly round 10 like the original.
MONKEY_BOMB: JsonDict = {
	"tactical": True,
	"stats": {
		GRENADE_TYPE: "monkey_bomb", FIRE_MODE: "semi",
		BASE_WEAPON: "monkey_bomb",
		CAPACITY: 1, REMAINING_BULLETS: 1, COOLDOWN: 20,
		PROJECTILE_SPEED: 800, PROJECTILE_GRAVITY: 60, PROJECTILE_MODEL: "monkey_bomb",
		GRENADE_FUSE: 180,  # 9 seconds (BO timing: lands, attracts ~7s, then detonates)
		EXPLOSION_RADIUS: 7, EXPLOSION_DAMAGE: 130, EXPLOSION_DECAY: 0.8,
	}
}

# Lethal grenades occupy the zombies lethal slot (hotbar.7, wallbuy kind 2).
# Their order here defines the per-player {ns}.zb.lethal_type enum, indexed from 0 = frag_grenade.
# That lets an EMPTY slot be refilled with the type the player actually bought, rather than always frag.
# Applies on round-end replenish, Max Ammo, and item recovery; see zombies/inventory.py.
LETHAL_GRENADE_IDS: list[str] = ["frag_grenade", "semtex", "smoke_grenade", "flash_grenade"] # TODO: smoke and flash should be tactical instead (like monkeys)

