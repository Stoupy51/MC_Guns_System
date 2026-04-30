
# Imports
import json
from typing import Any, cast

import stouputils as stp
from stewbeet import Item, JsonDict, Mem

# Constants
SRC_ROOT: str = stp.get_root_path(__file__, go_up=1)
ITEM_MODELS_PATH: str = f"{SRC_ROOT}/database/models"
ALL_SLOTS: tuple[str, ...] = (
    *[f"hotbar.{i}" for i in range(9)],
    "weapon.offhand",
    *[f"inventory.{i}" for i in range(3*9)],
    "player.cursor",
    *[f"player.crafting.{i}" for i in range(4)],
)

# Color constants
START_HEX: str = "c24a17"
END_HEX: str = "c77e36"

# Utility functions
def json_dump(x: Any) -> str: return stp.json_dump(x, max_level=-1)
def get_model_path(model_name: str) -> str: return f"{ITEM_MODELS_PATH}/{model_name}.json"

# Function
def add_item(id: str, stats: JsonDict | None = None, model_path: str | None = None, **kwargs: Any) -> Item:
    if model_path == "auto":
        model_path = get_model_path(id)
    return Item(
        id=id,
        base_item="minecraft:poisonous_potato" if stats else Item.base_item,
        components={
            "max_stack_size": 1,
            "custom_data": {Mem.ctx.project_id: {"gun":True, **stats} if stats else {"casing":True}},
            "rarity": "common",
        },
        override_model=(
            json.loads(stp.read_file(model_path).replace("mgs:item", f"{Mem.ctx.project_id}:item"))
            if model_path else None
        ),
        **kwargs
    )


# Mandatory constants
CAPACITY: str = "capacity"
""" Maximum number of bullets that can be loaded into the weapon's magazine. """
REMAINING_BULLETS: str = "remaining_bullets"
""" Current number of bullets remaining in the weapon's magazine.
This value is updated when firing and reloading the weapon. """
RELOAD_TIME: str = "reload_time"
""" Time required to reload the weapon, measured in game ticks. """
RELOAD_END: str = "reload_end"
""" Additional time in ticks after the reload animation completes.
Used to create a smoother transition between reloading and being able to fire again. """
RELOAD_MID: str = "reload_mid"
""" Time in ticks at which the reload sound effect is triggered during the reload sequence.
This parameter is optional and primarily used for weapons with longer reload animations. """
COOLDOWN: str = "cooldown"
""" Delay between consecutive shots, measured in game ticks.
Controls the weapon's rate of fire. Lower values result in faster firing rates. """
BURST: str = "burst"
""" Number of rounds automatically fired when in burst fire mode.
A value of 1 indicates semi-automatic, while 3 would be a three-round burst. """
CAN_BURST: str = "can_burst"
""" Boolean flag indicating whether the weapon supports burst fire mode.
If true, players can toggle between auto and burst fire modes by dropping the weapon. """
CAN_AUTO: str = "can_auto"
""" Boolean flag indicating whether the weapon supports automatic fire mode.
If true, players can hold right-click to continuously fire. All weapons support semi-auto. """
FIRE_MODE: str = "fire_mode"
""" Current firing mode of the weapon: 'auto' for automatic fire or 'burst' for burst fire.
In auto mode, holding right-click continuously fires. In burst mode, each click fires a fixed burst. """
PELLET_COUNT: str = "pellet_count"
""" Number of projectiles fired per shot (usually for shotguns). """
DAMAGE: str = "damage"
""" Base damage inflicted by each bullet at close range.
This value may be reduced at longer distances based on the decay parameter. """
DECAY: str = "decay"
""" Rate at which damage decreases over distance using multiplication.
For instance, a value of 0.95 means damage decreases to 59.9% damage at 10 blocks distance. """
ACCURACY_BASE: str = "acc_base"
""" Base accuracy of the weapon when standing still.
Lower values indicate better accuracy (smaller spread of bullets). """
ACCURACY_SNEAK: str = "acc_sneak"
""" Accuracy modifier applied when the player is sneaking/crouching.
Typically improves accuracy (reduces spread) when value is lower than base accuracy. """
ACCURACY_WALK: str = "acc_walk"
""" Accuracy penalty applied when the player is walking.
Higher values result in decreased accuracy (wider bullet spread). """
ACCURACY_SPRINT: str = "acc_sprint"
""" Accuracy penalty applied when the player is sprinting.
Significantly increases bullet spread, making the weapon less accurate. """
ACCURACY_JUMP: str = "acc_jump"
""" Accuracy penalty applied when the player is jumping or in mid-air.
Creates the largest reduction in accuracy, simulating the difficulty of shooting while airborne. """
SWITCH: str = "switch"
""" Time required to switch to this weapon, measured in game ticks.
Controls how quickly the player can change weapons in combat. """
KICK: str = "kick"
""" Intensity of the weapon's recoil effect.
Higher values create stronger visual kick when firing. """
CASING_MODEL: str = "casing_model"
""" Type of bullet casing ejected when firing.
Determines the visual model and properties of the ejected casing. """
CASING_OFFSET: str = "casing_offset"
""" Relative position to the player to use when summoning the casing.
The value is modified in setup_database.py according to the zoom type. """
CASING_NORMAL: str = "casing_n"
""" Vertical (Y-axis) component of the ejected casing's direction vector.
Controls the upward force applied to the casing during ejection. """
CASING_TANGENT: str = "casing_t"
""" Forward/backward (Z-axis) component of the ejected casing's direction vector.
Determines how far the casing is pushed forward or backward, with added randomness for realism. """
CASING_BINORMAL: str = "casing_b"
""" Sideways (X-axis) component of the ejected casing's direction vector.
Controls the horizontal offset of the casing, contributing to its full 3D trajectory. """
BASE_WEAPON: str = "base_weapon"
""" Identifier for the base weapon model.
Determines which weapon model and animations to use as a foundation.
Used for weapons that share the same base model but have different stats or attachments. """
WEIGHT: str = "weight"
""" Mystery box weight determining how frequently this weapon can appear.
Higher values mean more common (scale 1-10: 1=very rare, 10=very common). """


# Projectile constants (for slow-traveling bullets like RPG rockets, grenades, etc.)
PROJECTILE_SPEED: str = "proj_speed"
""" Speed of the projectile in thousandths of blocks/tick (e.g. 1500 = 1.5 blocks/tick).
If present in a weapon's stats, the weapon fires a slow projectile instead of an instant raycast. """
PROJECTILE_GRAVITY: str = "proj_gravity"
""" Gravity applied to the projectile each tick in thousandths of blocks/tick² (e.g. 50 = 0.05 blocks/tick²).
Set to 0 for straight-line travel. Configurable per weapon for arcing projectiles like grenades. """
PROJECTILE_LIFETIME: str = "proj_lifetime"
""" Maximum lifetime of the projectile in game ticks before it auto-explodes.
Prevents orphaned projectiles from existing forever. """
PROJECTILE_MODEL: str = "proj_model"
""" Item model identifier for the visible projectile entity (item_display).
Determines the visual appearance of the projectile in flight. """
EXPLOSION_RADIUS: str = "expl_radius"
""" Radius of the explosion effect in blocks.
Entities within this radius will take damage with distance-based falloff. """
EXPLOSION_DAMAGE: str = "expl_damage"
""" Base damage dealt at the center of the explosion.
Damage decreases with distance based on the explosion decay parameter. """
EXPLOSION_DECAY: str = "expl_decay"
""" Rate at which explosion damage decreases per block of distance from impact center.
Uses the formula: damage *= pow(decay, distance). Lower values = faster falloff. """

# Grenade constants
GRENADE_TYPE: str = "grenade_type"
""" Type of grenade: 'frag', 'semtex', 'smoke', or 'flash'.
If present, the weapon is treated as a throwable grenade instead of a gun. """
GRENADE_FUSE: str = "grenade_fuse"
""" Time in game ticks before the grenade detonates after being thrown. """
GRENADE_DURATION: str = "grenade_duration"
""" Duration of the grenade effect in ticks (for smoke/flash grenades). """
GRENADE_EFFECT_RADIUS: str = "grenade_effect_radius"
""" Radius of the grenade effect in blocks (for smoke/flash grenades). """

# Stats field
STATS_FIELDS: tuple[str, ...] = (
	CAPACITY,
	REMAINING_BULLETS,
	RELOAD_TIME,
	RELOAD_END,
	RELOAD_MID,
	COOLDOWN,
	BURST,
	PELLET_COUNT,
	DAMAGE,
	DECAY,
	ACCURACY_BASE,
	ACCURACY_SNEAK,
	ACCURACY_WALK,
	ACCURACY_SPRINT,
	ACCURACY_JUMP,
	SWITCH,
	KICK,
	WEIGHT,
	PROJECTILE_SPEED,
	PROJECTILE_GRAVITY,
	PROJECTILE_LIFETIME,
	EXPLOSION_RADIUS,
	EXPLOSION_DAMAGE,
	EXPLOSION_DECAY,
	FIRE_MODE,
	CAN_AUTO,
	CAN_BURST,
)

# Optional constants
MODELS: str = "models"
""" Models to use to switch between normal and zoom modes. """
IS_ZOOM: str = "is_zoom"
""" Indicates whether the weapon is currently in zoom mode """
WEAPON_ID: str = "weapon_id"
""" Dynamic unique identifier assigned to each weapon item when selected from the hotbar.
Used to track weapon switching and manage weapon-specific systems and states."""
PAP_STATS: str = "pap_stats"
""" Pack-a-Punch stat overrides applied when a weapon is upgraded.
Any PAP stat value can be a scalar or a list. Scalars are treated like a list with one value. """
PAP_NAME: str = "pap_name"
""" Optional Pack-a-Punch display name entry inside PAP_STATS.
Can be a scalar string or a list of strings (one per PAP level). """


def get_pap_max_level(weapon_stats: JsonDict) -> int:
    """ Return max PAP level based on the longest PAP stat list for this weapon. """
    pap_stats_any: Any = weapon_stats.get(PAP_STATS)
    if not isinstance(pap_stats_any, dict) or not pap_stats_any:
        return 0
    pap_stats = cast(dict[str, Any], pap_stats_any)

    max_level: int = 0
    for value in pap_stats.values():
        if isinstance(value, (list, tuple)):
            pap_values = cast(list[Any] | tuple[Any, ...], value)
            max_level = max(max_level, len(pap_values))
        else:
            max_level = max(max_level, 1)
    return max_level


def resolve_pap_overrides(weapon_stats: JsonDict, pap_level: int) -> JsonDict:
    """ Resolve PAP overrides for a given level.

    For list values, this clamps to the last value when pap_level exceeds list length.
    For scalar values, the same value is used at every PAP level.
    """
    pap_stats_any: Any = weapon_stats.get(PAP_STATS)
    if not isinstance(pap_stats_any, dict) or pap_level <= 0:
        return {}
    pap_stats = cast(dict[str, Any], pap_stats_any)

    resolved: JsonDict = {}
    value_index: int = pap_level - 1
    for stat_key, value in pap_stats.items():
        if isinstance(value, (list, tuple)):
            pap_values = cast(list[Any] | tuple[Any, ...], value)
            if not pap_values:
                continue
            resolved[stat_key] = pap_values[min(value_index, len(pap_values) - 1)]
        else:
            resolved[stat_key] = value
    return resolved


def resolve_pap_name(weapon_stats: JsonDict, pap_level: int, default_name: str) -> str:
    """ Resolve PAP display name for a given level.

    Reads PAP_STATS[PAP_NAME] as scalar or list and clamps list indexing to the last value.
    Falls back to default_name when PAP name is missing or invalid.
    """
    pap_stats_any: Any = weapon_stats.get(PAP_STATS)
    if not isinstance(pap_stats_any, dict) or pap_level <= 0:
        return default_name
    pap_stats = cast(dict[str, Any], pap_stats_any)

    pap_name: Any = pap_stats.get(PAP_NAME)
    if isinstance(pap_name, str):
        return pap_name
    if isinstance(pap_name, (list, tuple)):
        pap_names = cast(list[Any] | tuple[Any, ...], pap_name)
        if not pap_names:
            return default_name
        idx: int = min(pap_level - 1, len(pap_names) - 1)
        picked = pap_names[idx]
        return picked if isinstance(picked, str) else default_name
    return default_name



# Casing types
CASING_762X39MM = "762x39mm"
CASING_762X51MM = "762x51mm"
CASING_762X54MM = "762x54mm"
CASING_9X18MM = "9x18mm"
CASING_9X19MM = "9x19mm"
CASING_12GA3IN = "12ga3in"
CASING_12GA275IN = "12ga275in"
CASING_32ACP = "32acp"
CASING_45ACP = "45acp"
CASING_46X30MM = "46x30mm"
CASING_50AE = "50ae"
CASING_50BMG = "50bmg"
CASING_338LAPUA = "338lapua"
CASING_556X45MM = "556x45mm"
CASING_762X25MM = "762x25mm"


## Gun stats
# Rifles
M16A4: JsonDict = {
    "stats": {
        BASE_WEAPON: "m16a4", FIRE_MODE: "auto",
        CAPACITY: 30, RELOAD_TIME: 60, RELOAD_END: 10, COOLDOWN: 2, BURST: 3, CAN_BURST: True, CAN_AUTO: True, DAMAGE: 14, DECAY: 0.95, WEIGHT: 7,
        ACCURACY_BASE: 100, ACCURACY_SNEAK: 7, ACCURACY_WALK: 450, ACCURACY_SPRINT: 1000, ACCURACY_JUMP: 1500,
        SWITCH: 20, KICK: 2, CASING_MODEL: CASING_556X45MM, CASING_NORMAL: 150, CASING_TANGENT: -75, CASING_BINORMAL: -200,
        CASING_OFFSET: {"normal": (-0.4, -0.35, 0.7), "zoom": (-0.05, -0.25, 0.5)},
        PAP_STATS: {
            PAP_NAME: "Skullpiercer",
            CAPACITY: 40,
            REMAINING_BULLETS: 40,
            RELOAD_TIME: 50,
            RELOAD_END: 8,
            ACCURACY_BASE: 85,
            ACCURACY_WALK: 360,
            ACCURACY_SPRINT: 850,
            ACCURACY_JUMP: 1200,
            SWITCH: 16,
            DAMAGE: [28, 31, 35, 39, 44],
        },
    },
    "sounds": {
        "fire": "m16a4/fire",
        "reload": "m16a4/reload",
        "playerbegin": "m16a4/playerbegin",
        "playerend": "m16a4/playerend",
        "crack": "medium"
    }
}

AK47: JsonDict = {
    "stats": {
        BASE_WEAPON: "ak47", FIRE_MODE: "auto",
        CAPACITY: 30, RELOAD_TIME: 70, RELOAD_END: 10, COOLDOWN: 2, BURST: 3, CAN_BURST: True, CAN_AUTO: True, DAMAGE: 15, DECAY: 0.90, WEIGHT: 7,
        ACCURACY_BASE: 150, ACCURACY_SNEAK: 20, ACCURACY_WALK: 500, ACCURACY_SPRINT: 1500, ACCURACY_JUMP: 1800,
        SWITCH: 25, KICK: 2, CASING_MODEL: CASING_762X39MM, CASING_NORMAL: 200, CASING_TANGENT: 50, CASING_BINORMAL: -200,
        CASING_OFFSET: {"normal": (-0.35, -0.3, 0.7), "zoom": (-0.05, -0.25, 0.5)},
        PAP_STATS: {
            PAP_NAME: "Reznov's Revenge",
            CAPACITY: 40,
            REMAINING_BULLETS: 40,
            RELOAD_TIME: 58,
            RELOAD_END: 8,
            ACCURACY_BASE: 120,
            ACCURACY_WALK: 420,
            ACCURACY_SPRINT: 1000,
            ACCURACY_JUMP: 1500,
            SWITCH: 20,
            DAMAGE: [30, 34, 38, 43, 48],
        },
    },
    "sounds": {
        "fire": "ak47/fire",
        "reload": "ak47/reload",
        "playerbegin": "ak47/playerbegin",
        "playerend": "ak47/playerend",
        "crack": "medium"
    }
}

FNFAL: JsonDict = {
    "stats": {
        BASE_WEAPON: "fnfal", FIRE_MODE: "auto",
        CAPACITY: 20, RELOAD_TIME: 80, RELOAD_END: 20, COOLDOWN: 3, BURST: 2, CAN_BURST: True, CAN_AUTO: True, DAMAGE: 22, DECAY: 0.92, WEIGHT: 7,
        ACCURACY_BASE: 200, ACCURACY_SNEAK: 10, ACCURACY_WALK: 600, ACCURACY_SPRINT: 1800, ACCURACY_JUMP: 2500,
        SWITCH: 35, KICK: 3, CASING_MODEL: CASING_762X51MM, CASING_NORMAL: 125, CASING_TANGENT: 25, CASING_BINORMAL: -200,
        CASING_OFFSET: {"normal": (-0.3, -0.25, 0.7), "zoom": (-0.05, -0.2, 0.5)},
        PAP_STATS: {
            PAP_NAME: "WN",
            CAPACITY: 30,
            REMAINING_BULLETS: 30,
            RELOAD_TIME: 65,
            RELOAD_END: 14,
            COOLDOWN: 2,
            ACCURACY_BASE: 140,
            ACCURACY_WALK: 460,
            ACCURACY_SPRINT: 1200,
            ACCURACY_JUMP: 1500,
            SWITCH: 28,
            DAMAGE: [44, 49, 55, 62, 70],
        },
    },
    "sounds": {
        "fire": "fnfal/fire",
        "reload": "fnfal/reload",
        "playerbegin": "fnfal/playerbegin",
        "playerend": "fnfal/playerend",
        "crack": "large"
    }
}

AUG: JsonDict = {
    "stats": {
        BASE_WEAPON: "aug", FIRE_MODE: "auto",
        CAPACITY: 30, RELOAD_TIME: 80, RELOAD_MID: 40, RELOAD_END: 10, COOLDOWN: 2, BURST: 2, CAN_BURST: True, CAN_AUTO: True, DAMAGE: 13, DECAY: 0.95, WEIGHT: 6,
        ACCURACY_BASE: 100, ACCURACY_SNEAK: 12, ACCURACY_WALK: 350, ACCURACY_SPRINT: 800, ACCURACY_JUMP: 1200,
        SWITCH: 15, KICK: 2, CASING_MODEL: CASING_556X45MM, CASING_NORMAL: 125, CASING_TANGENT: -100, CASING_BINORMAL: -125,
        CASING_OFFSET: {"normal": (-0.45, -0.4, 0.4), "zoom": (-0.05, -0.3, 0.3)},
        PAP_STATS: {
            PAP_NAME: "AUG-50M3",
            CAPACITY: 42,
            REMAINING_BULLETS: 42,
            RELOAD_TIME: 60,
            RELOAD_MID: 30,
            RELOAD_END: 8,
            ACCURACY_BASE: 80,
            ACCURACY_WALK: 260,
            ACCURACY_SPRINT: 650,
            ACCURACY_JUMP: 1000,
            SWITCH: 12,
            DAMAGE: [26, 30, 34, 39, 44],
        },
    },
    "sounds": {
        "fire": "aug/fire",
        "reload": "aug/reload",
        "playerbegin": "aug/playerbegin",
        "playerend": "aug/playerend",
        "playermid": "aug/playermid",
        "crack": "medium"
    }
}

M4A1: JsonDict = {
    "stats": {
        BASE_WEAPON: "m4a1", FIRE_MODE: "auto",
        CAPACITY: 30, RELOAD_TIME: 50, RELOAD_END: 14, COOLDOWN: 2, BURST: 3, CAN_BURST: True, CAN_AUTO: True, DAMAGE: 13, DECAY: 0.92, WEIGHT: 7,
        ACCURACY_BASE: 110, ACCURACY_SNEAK: 15, ACCURACY_WALK: 400, ACCURACY_SPRINT: 900, ACCURACY_JUMP: 1400,
        SWITCH: 17, KICK: 2, CASING_MODEL: CASING_556X45MM, CASING_NORMAL: 150, CASING_TANGENT: -75, CASING_BINORMAL: -200,
        CASING_OFFSET: {"normal": (-0.4, -0.35, 0.7), "zoom": (-0.05, -0.25, 0.5)},
        PAP_STATS: {
            PAP_NAME: "M4-Annihilator",
            CAPACITY: 42,
            REMAINING_BULLETS: 42,
            RELOAD_TIME: 42,
            RELOAD_END: 10,
            ACCURACY_BASE: 90,
            ACCURACY_WALK: 320,
            ACCURACY_SPRINT: 760,
            ACCURACY_JUMP: 1200,
            SWITCH: 14,
            DAMAGE: [26, 29, 33, 38, 43],
        },
    },
    "sounds": {
        "fire": "m4a1/fire",
        "reload": "m4a1/reload",
        "playerbegin": "m4a1/playerbegin",
        "playerend": "m4a1/playerend",
        "crack": "medium"
    }
}

G3A3: JsonDict = {
    "stats": {
        BASE_WEAPON: "g3a3", FIRE_MODE: "auto",
        CAPACITY: 20, RELOAD_TIME: 80, RELOAD_END: 17, COOLDOWN: 3, BURST: 2, CAN_BURST: True, CAN_AUTO: True, DAMAGE: 20, DECAY: 0.92, WEIGHT: 6,
        ACCURACY_BASE: 180, ACCURACY_SNEAK: 6, ACCURACY_WALK: 600, ACCURACY_SPRINT: 1800, ACCURACY_JUMP: 2500,
        SWITCH: 30, KICK: 3, CASING_MODEL: CASING_762X51MM, CASING_NORMAL: 200, CASING_TANGENT: 100, CASING_BINORMAL: -300,
        CASING_OFFSET: {"normal": (-0.32, -0.3, 0.7), "zoom": (-0.05, -0.25, 0.5)},
        PAP_STATS: {
            PAP_NAME: "Great Dane",
            CAPACITY: 30,
            REMAINING_BULLETS: 30,
            RELOAD_TIME: 62,
            RELOAD_END: 12,
            COOLDOWN: 2,
            ACCURACY_BASE: 130,
            ACCURACY_WALK: 450,
            ACCURACY_SPRINT: 1200,
            ACCURACY_JUMP: 1800,
            SWITCH: 24,
            DAMAGE: [40, 45, 51, 58, 66],
        },
    },
    "sounds": {
        "fire": "g3a3/fire",
        "reload": "g3a3/reload",
        "playerbegin": "g3a3/playerbegin",
        "playerend": "g3a3/playerend",
        "crack": "large"
    }
}

FAMAS: JsonDict = {
    "stats": {
        BASE_WEAPON: "famas", FIRE_MODE: "auto",
        CAPACITY: 25, RELOAD_TIME: 80, RELOAD_MID: 40, RELOAD_END: 10, COOLDOWN: 2, BURST: 2, CAN_BURST: True, CAN_AUTO: True, DAMAGE: 13, DECAY: 0.95, WEIGHT: 5,
        ACCURACY_BASE: 110, ACCURACY_SNEAK: 15, ACCURACY_WALK: 400, ACCURACY_SPRINT: 900, ACCURACY_JUMP: 1400,
        SWITCH: 13, KICK: 2, CASING_MODEL: CASING_556X45MM, CASING_NORMAL: 150, CASING_TANGENT: -150, CASING_BINORMAL: -225,
        CASING_OFFSET: {"normal": (-0.45, -0.35, 0.3), "zoom": (-0.05, -0.3, 0.3)},
        PAP_STATS: {
            PAP_NAME: "G16-GL35",
            CAPACITY: 38,
            REMAINING_BULLETS: 38,
            RELOAD_TIME: 60,
            RELOAD_MID: 28,
            RELOAD_END: 8,
            ACCURACY_BASE: 90,
            ACCURACY_WALK: 300,
            ACCURACY_SPRINT: 700,
            ACCURACY_JUMP: 1200,
            SWITCH: 10,
            DAMAGE: [26, 30, 34, 39, 45],
        },
    },
    "sounds": {
        "fire": "famas/fire",
        "reload": "famas/reload",
        "playerbegin": "famas/playerbegin",
        "playerend": "famas/playerend",
        "playermid": "famas/playermid",
        "crack": "medium"
    }
}

SCAR17: JsonDict = {
    "stats": {
        BASE_WEAPON: "scar17", FIRE_MODE: "auto",
        CAPACITY: 20, RELOAD_TIME: 60, RELOAD_END: 15, COOLDOWN: 3, BURST: 2, CAN_BURST: True, CAN_AUTO: True, DAMAGE: 18, DECAY: 0.92, WEIGHT: 5,
        ACCURACY_BASE: 140, ACCURACY_SNEAK: 5, ACCURACY_WALK: 500, ACCURACY_SPRINT: 1500, ACCURACY_JUMP: 2300,
        SWITCH: 30, KICK: 3, CASING_MODEL: CASING_762X51MM, CASING_NORMAL: 50, CASING_TANGENT: -75, CASING_BINORMAL: -300,
        CASING_OFFSET: {"normal": (-0.32, -0.3, 0.7), "zoom": (-0.05, -0.25, 0.5)},
        PAP_STATS: {
            PAP_NAME: "Agarthan Reaper",
            CAPACITY: 30,
            REMAINING_BULLETS: 30,
            RELOAD_TIME: 48,
            RELOAD_END: 10,
            COOLDOWN: 2,
            ACCURACY_BASE: 110,
            ACCURACY_WALK: 380,
            ACCURACY_SPRINT: 1000,
            ACCURACY_JUMP: 1500,
            SWITCH: 24,
            DAMAGE: [36, 41, 47, 54, 62],
        },
    },
    "sounds": {
        "fire": "scar17/fire",
        "reload": "scar17/reload",
        "playerbegin": "scar17/playerbegin",
        "playerend": "scar17/playerend",
        "crack": "large"
    }
}

# Pistols
M1911: JsonDict = {
    "stats": {
        BASE_WEAPON: "m1911", FIRE_MODE: "semi",
        CAPACITY: 7, RELOAD_TIME: 45, RELOAD_END: 10, DAMAGE: 11, DECAY: 0.88, WEIGHT: 0,
        ACCURACY_BASE: 165, ACCURACY_SNEAK: 105, ACCURACY_WALK: 250, ACCURACY_SPRINT: 450, ACCURACY_JUMP: 800,
        SWITCH: 10, KICK: 4, CASING_MODEL: CASING_45ACP, CASING_NORMAL: 250, CASING_TANGENT: 0, CASING_BINORMAL: -150,
        CASING_OFFSET: {"normal": (-0.33, -0.25, 0.5), "zoom": (-0.05, -0.05, 0.4)},
        PAP_STATS: {
            PAP_NAME: "Mustang and Sally",
            CAPACITY: 12,
            REMAINING_BULLETS: 12,
            RELOAD_TIME: 32,
            RELOAD_END: 8,
            ACCURACY_BASE: 120,
            ACCURACY_WALK: 190,
            ACCURACY_SPRINT: 340,
            SWITCH: 8,
            DAMAGE: [22, 26, 31, 37, 44],
        },
    },
    "sounds": {
        "fire": "m1911/fire",
        "reload": "m1911/reload",
        "playerbegin": "m1911/playerbegin",
        "playerend": "m1911/playerend",
        "crack": "tiny"
    }
}

M9: JsonDict = {
    "stats": {
        BASE_WEAPON: "m9", FIRE_MODE: "semi",
        CAPACITY: 15, RELOAD_TIME: 60, RELOAD_END: 15, DAMAGE: 9, DECAY: 0.92, WEIGHT: 6,
        ACCURACY_BASE: 130, ACCURACY_SNEAK: 75, ACCURACY_WALK: 160, ACCURACY_SPRINT: 400, ACCURACY_JUMP: 800,
        SWITCH: 10, KICK: 3, CASING_MODEL: CASING_9X19MM, CASING_NORMAL: 100, CASING_TANGENT: -75, CASING_BINORMAL: -150,
        CASING_OFFSET: {"normal": (-0.35, -0.25, 0.5), "zoom": (-0.05, -0.1, 0.4)},
        PAP_STATS: {
            PAP_NAME: "Beretta M9",
            CAPACITY: 21,
            REMAINING_BULLETS: 21,
            RELOAD_TIME: 45,
            RELOAD_END: 10,
            ACCURACY_BASE: 100,
            ACCURACY_WALK: 130,
            ACCURACY_SPRINT: 300,
            ACCURACY_JUMP: 600,
            SWITCH: 8,
            DAMAGE: [18, 21, 25, 30, 36],
        },
    },
    "sounds": {
        "fire": "m9/fire",
        "reload": "m9/reload",
        "playerbegin": "m9/playerbegin",
        "playerend": "m9/playerend",
        "crack": "tiny"
    }
}

DEAGLE: JsonDict = {
    "stats": {
        BASE_WEAPON: "deagle", FIRE_MODE: "semi",
        CAPACITY: 7, RELOAD_TIME: 70, RELOAD_END: 15, COOLDOWN: 3, DAMAGE: 17, DECAY: 0.90, WEIGHT: 6,
        ACCURACY_BASE: 220, ACCURACY_SNEAK: 50, ACCURACY_WALK: 400, ACCURACY_SPRINT: 1000, ACCURACY_JUMP: 2000,
        SWITCH: 15, KICK: 5, CASING_MODEL: CASING_50AE, CASING_NORMAL: 250, CASING_TANGENT: -75, CASING_BINORMAL: -100,
        CASING_OFFSET: {"normal": (-0.3, -0.2, 0.5), "zoom": (-0.05, -0.05, 0.4)},
        PAP_STATS: {
            PAP_NAME: "Space Eagle",
            CAPACITY: 10,
            REMAINING_BULLETS: 10,
            RELOAD_TIME: 55,
            RELOAD_END: 10,
            COOLDOWN: 2,
            ACCURACY_BASE: 170,
            ACCURACY_WALK: 280,
            ACCURACY_SPRINT: 650,
            ACCURACY_JUMP: 1200,
            SWITCH: 12,
            DAMAGE: [34, 40, 47, 55, 64],
        },
    },
    "sounds": {
        "fire": "deagle/fire",
        "reload": "deagle/reload",
        "playerbegin": "deagle/playerbegin",
        "playerend": "deagle/playerend",
        "crack": "tiny"
    }
}

MAKAROV: JsonDict = {
    "stats": {
        BASE_WEAPON: "makarov", FIRE_MODE: "semi",
        CAPACITY: 8, RELOAD_TIME: 40, RELOAD_END: 10, DAMAGE: 9, DECAY: 0.90, WEIGHT: 6,
        ACCURACY_BASE: 120, ACCURACY_SNEAK: 65, ACCURACY_WALK: 130, ACCURACY_SPRINT: 350, ACCURACY_JUMP: 800,
        SWITCH: 8, KICK: 2, CASING_MODEL: CASING_9X18MM, CASING_NORMAL: 250, CASING_TANGENT: -100, CASING_BINORMAL: -75,
        CASING_OFFSET: {"normal": (-0.3, -0.25, 0.5), "zoom": (-0.05, -0.05, 0.4)},
        PAP_STATS: {
            PAP_NAME: "Mak-A-Roar",
            CAPACITY: 12,
            REMAINING_BULLETS: 12,
            RELOAD_TIME: 30,
            RELOAD_END: 8,
            ACCURACY_BASE: 95,
            ACCURACY_WALK: 105,
            ACCURACY_SPRINT: 250,
            ACCURACY_JUMP: 500,
            SWITCH: 6,
            DAMAGE: [18, 21, 25, 30, 36],
        },
    },
    "sounds": {
        "fire": "makarov/fire",
        "reload": "makarov/reload",
        "playerbegin": "makarov/playerbegin",
        "playerend": "makarov/playerend",
        "crack": "tiny"
    }
}

GLOCK17: JsonDict = {
    "stats": {
        BASE_WEAPON: "glock17", FIRE_MODE: "semi",
        CAPACITY: 17, RELOAD_TIME: 60, RELOAD_END: 16, DAMAGE: 9, DECAY: 0.92, WEIGHT: 6,
        ACCURACY_BASE: 150, ACCURACY_SNEAK: 90, ACCURACY_WALK: 170, ACCURACY_SPRINT: 400, ACCURACY_JUMP: 800,
        SWITCH: 8, KICK: 3, CASING_MODEL: CASING_9X19MM, CASING_NORMAL: 225, CASING_TANGENT: -100, CASING_BINORMAL: -75,
        CASING_OFFSET: {"normal": (-0.35, -0.27, 0.5), "zoom": (-0.05, 0.0, 0.4)},
        PAP_STATS: {
            PAP_NAME: "Glock 'n' Load",
            CAPACITY: 24,
            REMAINING_BULLETS: 24,
            RELOAD_TIME: 44,
            RELOAD_END: 10,
            ACCURACY_BASE: 110,
            ACCURACY_WALK: 130,
            ACCURACY_SPRINT: 280,
            ACCURACY_JUMP: 500,
            SWITCH: 6,
            DAMAGE: [18, 21, 25, 30, 36],
        },
    },
    "sounds": {
        "fire": "glock17/fire",
        "reload": "glock17/reload",
        "playerbegin": "glock17/playerbegin",
        "playerend": "glock17/playerend",
        "crack": "tiny"
    }
}

GLOCK18: JsonDict = {
    "stats": {
        BASE_WEAPON: "glock18", FIRE_MODE: "auto",
        CAPACITY: 19, RELOAD_TIME: 70, RELOAD_END: 16, COOLDOWN: 1, BURST: 4, CAN_BURST: True, CAN_AUTO: True, DAMAGE: 9, DECAY: 0.92, WEIGHT: 5,
        ACCURACY_BASE: 180, ACCURACY_SNEAK: 140, ACCURACY_WALK: 300, ACCURACY_SPRINT: 400, ACCURACY_JUMP: 800,
        SWITCH: 10, KICK: 3, CASING_MODEL: CASING_9X19MM, CASING_NORMAL: 225, CASING_TANGENT: -100, CASING_BINORMAL: -75,
        CASING_OFFSET: {"normal": (-0.35, -0.27, 0.5), "zoom": (-0.05, 0.0, 0.4)},
        PAP_STATS: {
            PAP_NAME: "The Panic Button",
            CAPACITY: 28,
            REMAINING_BULLETS: 28,
            RELOAD_TIME: 52,
            RELOAD_END: 10,
            ACCURACY_BASE: 130,
            ACCURACY_WALK: 220,
            ACCURACY_SPRINT: 280,
            ACCURACY_JUMP: 500,
            SWITCH: 8,
            DAMAGE: [18, 21, 25, 30, 36],
        },
    },
    "sounds": {
        "fire": "glock18/fire",
        "reload": "glock18/reload",
        "playerbegin": "glock18/playerbegin",
        "playerend": "glock18/playerend",
        "crack": "tiny"
    }
}

VZ61: JsonDict = {
    "stats": {
        BASE_WEAPON: "vz61", FIRE_MODE: "auto",
        CAPACITY: 20, RELOAD_TIME: 70, RELOAD_END: 14, COOLDOWN: 2, BURST: 2, CAN_BURST: True, CAN_AUTO: True, DAMAGE: 8, DECAY: 0.92, WEIGHT: 7,
        ACCURACY_BASE: 150, ACCURACY_SNEAK: 80, ACCURACY_WALK: 290, ACCURACY_SPRINT: 400, ACCURACY_JUMP: 800,
        SWITCH: 12, KICK: 2, CASING_MODEL: CASING_32ACP, CASING_NORMAL: 300, CASING_TANGENT: 25, CASING_BINORMAL: 0,
        CASING_OFFSET: {"normal": (-0.23, -0.1, 0.5), "zoom": (0, 0.05, 0.4)},
        PAP_STATS: {
            PAP_NAME: "Skorpitron",
            CAPACITY: 28,
            REMAINING_BULLETS: 28,
            RELOAD_TIME: 52,
            RELOAD_END: 10,
            COOLDOWN: 1,
            ACCURACY_BASE: 120,
            ACCURACY_WALK: 210,
            ACCURACY_SPRINT: 280,
            ACCURACY_JUMP: 500,
            SWITCH: 8,
            DAMAGE: [16, 19, 23, 28, 34],
        },
    },
    "sounds": {
        "fire": "vz61/fire",
        "reload": "vz61/reload",
        "playerbegin": "vz61/playerbegin",
        "playerend": "vz61/playerend",
        "crack": "tiny"
    }
}

RAY_GUN: JsonDict = {
    "stats": {
        BASE_WEAPON: "ray_gun", FIRE_MODE: "auto",
        CAPACITY: 20, RELOAD_TIME: 60, RELOAD_END: 14, COOLDOWN: 11, CAN_AUTO: True, DAMAGE: 24, DECAY: 0.92, WEIGHT: 2,
        ACCURACY_BASE: 150, ACCURACY_SNEAK: 80, ACCURACY_WALK: 290, ACCURACY_SPRINT: 400, ACCURACY_JUMP: 800,
        SWITCH: 12, KICK: 5,
        PROJECTILE_SPEED: 3000, PROJECTILE_GRAVITY: 0, PROJECTILE_LIFETIME: 200, PROJECTILE_MODEL: "ray_gun",
        EXPLOSION_RADIUS: 3.5, EXPLOSION_DAMAGE: 32, EXPLOSION_DECAY: 0.80,
        PAP_STATS: {
            PAP_NAME: "Porter's X2 Ray Gun",
            CAPACITY: 30,
            REMAINING_BULLETS: 30,
            RELOAD_TIME: 45,
            RELOAD_END: 10,
            COOLDOWN: 9,
            ACCURACY_BASE: 110,
            ACCURACY_WALK: 210,
            ACCURACY_SPRINT: 280,
            ACCURACY_JUMP: 500,
            SWITCH: 9,
            PROJECTILE_SPEED: 3400,
            EXPLOSION_DAMAGE: 40,
            DAMAGE: [48, 56, 66, 78, 92],
        },
    },
    "sounds": {
        "fire": "ray_gun/fire",
        "reload": "ray_gun/reload",
        "playerbegin": "ray_gun/playerbegin",
        "playerend": "ray_gun/playerend",
        "playermid": "ray_gun/playermid"
    }
}

# SMGS
MP5: JsonDict = {
    "stats": {
        BASE_WEAPON: "mp5", FIRE_MODE: "auto",
        CAPACITY: 30, RELOAD_TIME: 60, RELOAD_MID: 25, RELOAD_END: 5, COOLDOWN: 2, BURST: 2, CAN_BURST: True, CAN_AUTO: True, DAMAGE: 10, DECAY: 0.92, WEIGHT: 6,
        ACCURACY_BASE: 100, ACCURACY_SNEAK: 60, ACCURACY_WALK: 200, ACCURACY_SPRINT: 450, ACCURACY_JUMP: 1000,
        SWITCH: 15, KICK: 1, CASING_MODEL: CASING_9X19MM, CASING_NORMAL: 225, CASING_TANGENT: 10, CASING_BINORMAL: -275,
        CASING_OFFSET: {"normal": (-0.38, -0.35, 0.7), "zoom": (-0.05, -0.25, 0.5)},
        PAP_STATS: {
            PAP_NAME: "MP115 Kollider",
            CAPACITY: 42,
            REMAINING_BULLETS: 42,
            RELOAD_TIME: 45,
            RELOAD_MID: 20,
            RELOAD_END: 4,
            COOLDOWN: 1,
            ACCURACY_BASE: 80,
            ACCURACY_WALK: 150,
            ACCURACY_SPRINT: 320,
            ACCURACY_JUMP: 500,
            SWITCH: 11,
            DAMAGE: [20, 23, 27, 32, 38],
        },
    },
    "sounds": {
        "fire": "mp5/fire",
        "reload": "mp5/reload",
        "playerbegin": "mp5/playerbegin",
        "playerend": "mp5/playerend",
        "playermid": "mp5/playermid",
        "crack": "tiny"
    }
}

MAC10: JsonDict = {
    "stats": {
        BASE_WEAPON: "mac10", FIRE_MODE: "auto",
        CAPACITY: 30, RELOAD_TIME: 50, RELOAD_MID: 38, RELOAD_END: 10, COOLDOWN: 1, BURST: 4, CAN_BURST: True, CAN_AUTO: True, DAMAGE: 11, DECAY: 0.88, WEIGHT: 6,
        ACCURACY_BASE: 220, ACCURACY_SNEAK: 150, ACCURACY_WALK: 330, ACCURACY_SPRINT: 400, ACCURACY_JUMP: 800,
        SWITCH: 10, KICK: 2, CASING_MODEL: CASING_45ACP, CASING_NORMAL: 125, CASING_TANGENT: -25, CASING_BINORMAL: -175,
        CASING_OFFSET: {"normal": (-0.4, -0.35, 0.7), "zoom": (-0.05, -0.25, 0.5)},
        PAP_STATS: {
            PAP_NAME: "Mac Attack",
            CAPACITY: 45,
            REMAINING_BULLETS: 45,
            RELOAD_TIME: 40,
            RELOAD_MID: 28,
            RELOAD_END: 8,
            ACCURACY_BASE: 165,
            ACCURACY_WALK: 250,
            ACCURACY_SPRINT: 300,
            ACCURACY_JUMP: 500,
            SWITCH: 8,
            DAMAGE: [22, 25, 29, 34, 40],
        },
    },
    "sounds": {
        "fire": "mac10/fire",
        "reload": "mac10/reload",
        "playerbegin": "mac10/playerbegin",
        "playerend": "mac10/playerend",
        "playermid": "mac10/playermid",
        "crack": "tiny"
    }
}

MP7: JsonDict = {
    "stats": {
        BASE_WEAPON: "mp7", FIRE_MODE: "auto",
        CAPACITY: 40, RELOAD_TIME: 55, RELOAD_END: 15, COOLDOWN: 2, BURST: 3, CAN_BURST: True, CAN_AUTO: True, DAMAGE: 12, DECAY: 0.95, WEIGHT: 6,
        ACCURACY_BASE: 150, ACCURACY_SNEAK: 50, ACCURACY_WALK: 250, ACCURACY_SPRINT: 480, ACCURACY_JUMP: 1500,
        SWITCH: 20, KICK: 2, CASING_MODEL: CASING_46X30MM, CASING_NORMAL: 10, CASING_TANGENT: -50, CASING_BINORMAL: -275,
        CASING_OFFSET: {"normal": (-0.45, -0.4, 0.7), "zoom": (-0.05, -0.4, 0.5)},
        PAP_STATS: {
            PAP_NAME: "MP-Heaven",
            CAPACITY: 55,
            REMAINING_BULLETS: 55,
            RELOAD_TIME: 42,
            RELOAD_END: 10,
            COOLDOWN: 1,
            ACCURACY_BASE: 110,
            ACCURACY_WALK: 180,
            ACCURACY_SPRINT: 330,
            ACCURACY_JUMP: 1200,
            SWITCH: 14,
            DAMAGE: [24, 28, 32, 37, 43],
        },
    },
    "sounds": {
        "fire": "mp7/fire",
        "reload": "mp7/reload",
        "playerbegin": "mp7/playerbegin",
        "playerend": "mp7/playerend",
        "crack": "small"
    }
}

PPSH41: JsonDict = {
    "stats": {
        BASE_WEAPON: "ppsh41", FIRE_MODE: "auto",
        CAPACITY: 71, RELOAD_TIME: 100, RELOAD_MID: 70, RELOAD_END: 16, COOLDOWN: 1, BURST: 4, CAN_BURST: True, CAN_AUTO: True, DAMAGE: 10, DECAY: 0.92, WEIGHT: 5,
        ACCURACY_BASE: 175, ACCURACY_SNEAK: 125, ACCURACY_WALK: 400, ACCURACY_SPRINT: 700, ACCURACY_JUMP: 1500,
        SWITCH: 40, KICK: 2, CASING_MODEL: CASING_762X25MM, CASING_NORMAL: 300, CASING_TANGENT: -50, CASING_BINORMAL: -25,
        CASING_OFFSET: {"normal": (-0.38, -0.2, 0.7), "zoom": (0.0, 0.0, 0.5)},
        PAP_STATS: {
            PAP_NAME: "The Reaper",
            CAPACITY: 90,
            REMAINING_BULLETS: 90,
            RELOAD_TIME: 75,
            RELOAD_MID: 48,
            RELOAD_END: 12,
            ACCURACY_BASE: 135,
            ACCURACY_WALK: 290,
            ACCURACY_SPRINT: 500,
            ACCURACY_JUMP: 1200,
            SWITCH: 30,
            DAMAGE: [20, 23, 27, 32, 38],
        },
    },
    "sounds": {
        "fire": "ppsh41/fire",
        "reload": "ppsh41/reload",
        "playerbegin": "ppsh41/playerbegin",
        "playerend": "ppsh41/playerend",
        "playermid": "ppsh41/playermid",
        "crack": "tiny"
    }
}

STEN: JsonDict = {
    "stats": {
        BASE_WEAPON: "sten", FIRE_MODE: "auto",
        CAPACITY: 32, RELOAD_TIME: 58, RELOAD_MID: 40, RELOAD_END: 10, COOLDOWN: 3, BURST: 2, CAN_BURST: True, CAN_AUTO: True, DAMAGE: 11, DECAY: 0.92, WEIGHT: 7,
        ACCURACY_BASE: 200, ACCURACY_SNEAK: 100, ACCURACY_WALK: 400, ACCURACY_SPRINT: 800, ACCURACY_JUMP: 1500,
        SWITCH: 25, KICK: 3, CASING_MODEL: CASING_9X19MM, CASING_NORMAL: 200, CASING_TANGENT: -50, CASING_BINORMAL: -200,
        CASING_OFFSET: {"normal": (-0.4, -0.35, 0.7), "zoom": (-0.05, -0.25, 0.5)},
        PAP_STATS: {
            PAP_NAME: "Sten & Deliver",
            CAPACITY: 45,
            REMAINING_BULLETS: 45,
            RELOAD_TIME: 44,
            RELOAD_MID: 28,
            RELOAD_END: 8,
            COOLDOWN: 2,
            ACCURACY_BASE: 150,
            ACCURACY_WALK: 280,
            ACCURACY_SPRINT: 520,
            ACCURACY_JUMP: 1200,
            SWITCH: 18,
            DAMAGE: [22, 26, 30, 35, 41],
        },
    },
    "sounds": {
        "fire": "sten/fire",
        "reload": "sten/reload",
        "playerbegin": "sten/playerbegin",
        "playerend": "sten/playerend",
        "playermid": "sten/playermid",
        "crack": "tiny"
    }
}

# Shotguns
SPAS12: JsonDict = {
    "stats": {
        BASE_WEAPON: "spas12", FIRE_MODE: "semi",
        CAPACITY: 8, RELOAD_TIME: 20, COOLDOWN: 16, PELLET_COUNT: 3, DAMAGE: 13, DECAY: 0.82, WEIGHT: 5,
        ACCURACY_BASE: 230, ACCURACY_SNEAK: 190, ACCURACY_WALK: 300, ACCURACY_SPRINT: 800, ACCURACY_JUMP: 1500,
        SWITCH: 25, KICK: 6, CASING_MODEL: CASING_12GA275IN, CASING_NORMAL: 25, CASING_TANGENT: 100, CASING_BINORMAL: -200,
        CASING_OFFSET: {"normal": (-0.35, -0.3, 0.7), "zoom": (-0.1, -0.3, 0.6)},
        PAP_STATS: {
            PAP_NAME: "SPAZ-24",
            CAPACITY: 12,
            REMAINING_BULLETS: 12,
            RELOAD_TIME: 14,
            COOLDOWN: 12,
            PELLET_COUNT: 4,
            ACCURACY_BASE: 170,
            ACCURACY_WALK: 220,
            ACCURACY_SPRINT: 550,
            ACCURACY_JUMP: 1200,
            SWITCH: 18,
            DAMAGE: [26, 31, 37, 44, 52],
        },
    },
    "sounds": {
        "fire": "spas12/fire",
        "fire_alt": "spas12/fire_alt",
        "reload": "spas12/reload",
        "pump": "spas12/pump",
        "crack": "largest"
    }
}

M500: JsonDict = {
    "stats": {
        BASE_WEAPON: "m500", FIRE_MODE: "semi",
        CAPACITY: 5, RELOAD_TIME: 22, COOLDOWN: 18, PELLET_COUNT: 3, DAMAGE: 14, DECAY: 0.82, WEIGHT: 4,
        ACCURACY_BASE: 250, ACCURACY_SNEAK: 200, ACCURACY_WALK: 350, ACCURACY_SPRINT: 900, ACCURACY_JUMP: 1600,
        SWITCH: 20, KICK: 7, CASING_MODEL: CASING_12GA3IN, CASING_NORMAL: 25, CASING_TANGENT: 100, CASING_BINORMAL: -200,
        CASING_OFFSET: {"normal": (-0.35, -0.3, 0.7), "zoom": (-0.1, -0.3, 0.6)},
        PAP_STATS: {
            PAP_NAME: "Voice of Justice",
            CAPACITY: 8,
            REMAINING_BULLETS: 8,
            RELOAD_TIME: 16,
            COOLDOWN: 14,
            PELLET_COUNT: 4,
            ACCURACY_BASE: 180,
            ACCURACY_WALK: 240,
            ACCURACY_SPRINT: 600,
            ACCURACY_JUMP: 1200,
            SWITCH: 15,
            DAMAGE: [28, 33, 39, 46, 54],
        },
    },
    "sounds": {
        "fire": "m500/fire",
        "reload": "m500/reload",
        "pump": "m500/pump",
        "crack": "largest"
    }
}

M590: JsonDict = {
    "stats": {
        BASE_WEAPON: "m590", FIRE_MODE: "semi",
        CAPACITY: 8, RELOAD_TIME: 22, COOLDOWN: 19, PELLET_COUNT: 3, DAMAGE: 14, DECAY: 0.82, WEIGHT: 4,
        ACCURACY_BASE: 210, ACCURACY_SNEAK: 175, ACCURACY_WALK: 325, ACCURACY_SPRINT: 800, ACCURACY_JUMP: 1500,
        SWITCH: 35, KICK: 5, CASING_MODEL: CASING_12GA3IN, CASING_NORMAL: 50, CASING_TANGENT: 80, CASING_BINORMAL: -220,
        CASING_OFFSET: {"normal": (-0.35, -0.27, 0.7), "zoom": (-0.1, -0.25, 0.6)},
        PAP_STATS: {
            PAP_NAME: "The Conversation Ender",
            CAPACITY: 12,
            REMAINING_BULLETS: 12,
            RELOAD_TIME: 16,
            COOLDOWN: 14,
            PELLET_COUNT: 4,
            ACCURACY_BASE: 155,
            ACCURACY_WALK: 220,
            ACCURACY_SPRINT: 520,
            ACCURACY_JUMP: 1200,
            SWITCH: 26,
            DAMAGE: [28, 33, 39, 46, 54],
        },
    },
    "sounds": {
        "fire": "m590/fire",
        "reload": "m590/reload",
        "pump": "m590/pump",
        "crack": "largest"
    }
}

# Snipers
SVD: JsonDict = {
    "stats": {
        BASE_WEAPON: "svd", FIRE_MODE: "semi",
        CAPACITY: 10, RELOAD_TIME: 73, RELOAD_MID: 40, RELOAD_END: 10, COOLDOWN: 5, DAMAGE: 27, DECAY: 0.95, WEIGHT: 6,
        ACCURACY_BASE: 350, ACCURACY_SNEAK: 5, ACCURACY_WALK: 700, ACCURACY_SPRINT: 1500, ACCURACY_JUMP: 3000,
        SWITCH: 40, KICK: 4, CASING_MODEL: CASING_762X54MM, CASING_NORMAL: 150, CASING_TANGENT: -150, CASING_BINORMAL: -175,
        CASING_OFFSET: {"normal": (-0.3, -0.27, 0.7), "zoom": (-0.05, -0.25, 0.5)},
        PAP_STATS: {
            PAP_NAME: "Sudden Violence Device",
            CAPACITY: 14,
            REMAINING_BULLETS: 14,
            RELOAD_TIME: 55,
            RELOAD_MID: 30,
            RELOAD_END: 8,
            COOLDOWN: 4,
            ACCURACY_BASE: 250,
            ACCURACY_WALK: 450,
            ACCURACY_SPRINT: 1000,
            ACCURACY_JUMP: 2000,
            SWITCH: 30,
            DAMAGE: [54, 62, 72, 84, 98],
        },
    },
    "sounds": {
        "fire": "svd/fire",
        "reload": "svd/reload",
        "playerbegin": "svd/playerbegin",
        "playerend": "svd/playerend",
        "playermid": "svd/playermid",
        "crack": "large"
    }
}

M82: JsonDict = {
    "stats": {
        BASE_WEAPON: "m82", FIRE_MODE: "semi",
        CAPACITY: 10, RELOAD_TIME: 80, RELOAD_MID: 50, RELOAD_END: 15, COOLDOWN: 10, DAMAGE: 55, DECAY: 0.90, WEIGHT: 3,
        ACCURACY_BASE: 450, ACCURACY_SNEAK: 12, ACCURACY_WALK: 800, ACCURACY_SPRINT: 1500, ACCURACY_JUMP: 3000,
        SWITCH: 50, KICK: 5, CASING_MODEL: CASING_50BMG, CASING_NORMAL: 50, CASING_TANGENT: -25, CASING_BINORMAL: -225,
        CASING_OFFSET: {"normal": (-0.28, -0.3, 0.7), "zoom": (-0.1, -0.25, 0.6)},
        PAP_STATS: {
            PAP_NAME: "Macro Annihilator",
            CAPACITY: 12,
            REMAINING_BULLETS: 12,
            RELOAD_TIME: 62,
            RELOAD_MID: 38,
            RELOAD_END: 10,
            COOLDOWN: 8,
            ACCURACY_BASE: 320,
            ACCURACY_WALK: 500,
            ACCURACY_SPRINT: 1100,
            ACCURACY_JUMP: 2000,
            SWITCH: 38,
            DAMAGE: [110, 126, 144, 165, 190],
        },
    },
    "sounds": {
        "fire": "m82/fire",
        "reload": "m82/reload",
        "playerbegin": "m82/playerbegin",
        "playerend": "m82/playerend",
        "playermid": "m82/playermid",
        "crack": "largest"
    }
}

MOSIN: JsonDict = {
    "stats": {
        BASE_WEAPON: "mosin", FIRE_MODE: "semi",
        CAPACITY: 5, RELOAD_TIME: 20, RELOAD_MID: 15, COOLDOWN: 40, DAMAGE: 29, DECAY: 0.95, WEIGHT: 4,
        ACCURACY_BASE: 150, ACCURACY_SNEAK: 3, ACCURACY_WALK: 175, ACCURACY_SPRINT: 1000, ACCURACY_JUMP: 1500,
        SWITCH: 25, KICK: 4, CASING_MODEL: CASING_762X54MM, CASING_NORMAL: 100, CASING_TANGENT: -50, CASING_BINORMAL: -100,
        CASING_OFFSET: {"normal": (-0.35, -0.2, 0.6), "zoom": (-0.05, -0.2, 0.4)},
        PAP_STATS: {
            PAP_NAME: "Marksmen's Old Silent Infantry",
            CAPACITY: 7,
            REMAINING_BULLETS: 7,
            RELOAD_TIME: 14,
            RELOAD_MID: 10,
            COOLDOWN: 28,
            ACCURACY_BASE: 110,
            ACCURACY_WALK: 130,
            ACCURACY_SPRINT: 700,
            ACCURACY_JUMP: 1200,
            SWITCH: 18,
            DAMAGE: [58, 68, 80, 94, 111],
        },
    },
    "sounds": {
        "fire": "mosin/fire",
        "reload": "mosin/reload",
        "playerbegin": "mosin/playerbegin",
        "playerend": "mosin/playerend",
        "cycle": "mosin/cycle",
        "crack": "large"
    }
}

M24: JsonDict = {
    "stats": {
        BASE_WEAPON: "m24", FIRE_MODE: "semi",
        CAPACITY: 5, RELOAD_TIME: 25, RELOAD_MID: 14, COOLDOWN: 45, DAMAGE: 36, DECAY: 0.92, WEIGHT: 4,
        ACCURACY_BASE: 350, ACCURACY_SNEAK: 1, ACCURACY_WALK: 700, ACCURACY_SPRINT: 1500, ACCURACY_JUMP: 3000,
        SWITCH: 39, KICK: 4, CASING_MODEL: CASING_338LAPUA, CASING_NORMAL: 100, CASING_TANGENT: -50, CASING_BINORMAL: -100,
        CASING_OFFSET: {"normal": (-0.35, -0.2, 0.6), "zoom": (-0.05, -0.2, 0.4)},
        PAP_STATS: {
            PAP_NAME: "Isolator of Judgment",
            CAPACITY: 7,
            REMAINING_BULLETS: 7,
            RELOAD_TIME: 18,
            RELOAD_MID: 10,
            COOLDOWN: 32,
            ACCURACY_BASE: 250,
            ACCURACY_WALK: 420,
            ACCURACY_SPRINT: 1000,
            ACCURACY_JUMP: 2000,
            SWITCH: 28,
            DAMAGE: [72, 84, 98, 114, 132],
        },
    },
    "sounds": {
        "fire": "m24/fire",
        "reload": "m24/reload",
        "playerbegin": "m24/playerbegin",
        "playerend": "m24/playerend",
        "cycle": "m24/cycle",
        "crack": "largest"
    }
}


# Special
RPG7: JsonDict = {
    "stats": {
        BASE_WEAPON: "rpg7", FIRE_MODE: "semi",
        CAPACITY: 1, RELOAD_TIME: 110, RELOAD_END: 20, COOLDOWN: 10, DAMAGE: 30, DECAY: 1.00, WEIGHT: 4,
        ACCURACY_BASE: 250, ACCURACY_SNEAK: 100, ACCURACY_WALK: 300, ACCURACY_SPRINT: 300, ACCURACY_JUMP: 300,
        SWITCH: 55, KICK: 6,
        PROJECTILE_SPEED: 1500, PROJECTILE_GRAVITY: 0, PROJECTILE_LIFETIME: 200, PROJECTILE_MODEL: "rpg7_rocket",
        EXPLOSION_RADIUS: 6, EXPLOSION_DAMAGE: 30, EXPLOSION_DECAY: 0.80,
        PAP_STATS: {
            PAP_NAME: "Rocket Propelled Grievance",
            FIRE_MODE: "auto",
            CAN_AUTO: True,
            CAPACITY: 8,
            RELOAD_TIME: 80,
            RELOAD_END: 14,
            COOLDOWN: 5,
            SWITCH: 40,
            PROJECTILE_SPEED: 1800,
            EXPLOSION_RADIUS: 7,
            EXPLOSION_DAMAGE: 42,
            DAMAGE: [60, 75, 93, 113],
        },
    },
    "sounds": {
        "fire": "rpg7/fire",
        "reload": "rpg7/reload",
        "playerbegin": "rpg7/playerbegin",
        "playerend": "rpg7/playerend",
        "handling_endgrab": "rpg7/handling/rpg7_endgrab",
        "handling_fetch": "rpg7/handling/rpg7_fetch",
        "handling_load": "rpg7/handling/rpg7_load",
        "crack": "rocket"
    }
}

RPK: JsonDict = {
    "stats": {
        BASE_WEAPON: "rpk", FIRE_MODE: "auto",
        CAPACITY: 75, RELOAD_TIME: 115, RELOAD_MID: 60, RELOAD_END: 20, COOLDOWN: 2, BURST: 2, CAN_BURST: True, CAN_AUTO: True, DAMAGE: 15, DECAY: 0.90, WEIGHT: 3,
        ACCURACY_BASE: 470, ACCURACY_SNEAK: 80, ACCURACY_WALK: 900, ACCURACY_SPRINT: 1500, ACCURACY_JUMP: 3000,
        SWITCH: 55, KICK: 3, CASING_MODEL: CASING_762X39MM, CASING_NORMAL: 200, CASING_TANGENT: 50, CASING_BINORMAL: -200,
        CASING_OFFSET: {"normal": (-0.35, -0.28, 0.7), "zoom": (-0.05, -0.25, 0.5)},
        PAP_STATS: {
            PAP_NAME: "R115 Resonator",
            CAPACITY: 100,
            REMAINING_BULLETS: 100,
            RELOAD_TIME: 84,
            RELOAD_MID: 45,
            RELOAD_END: 14,
            COOLDOWN: 1,
            ACCURACY_BASE: 320,
            ACCURACY_WALK: 650,
            ACCURACY_SPRINT: 1100,
            ACCURACY_JUMP: 2000,
            SWITCH: 40,
            DAMAGE: [30, 34, 39, 45, 52],
        },
    },
    "sounds": {
        "fire": "rpk/fire",
        "reload": "rpk/reload",
        "playerbegin": "rpk/playerbegin",
        "playerend": "rpk/playerend",
        "playermid": "rpk/playermid",
        "crack": "medium"
    }
}

M249: JsonDict = {
    "stats": {
        BASE_WEAPON: "m249", FIRE_MODE: "auto",
        CAPACITY: 150, RELOAD_TIME: 175, RELOAD_MID: 110, RELOAD_END: 30, COOLDOWN: 2, BURST: 2, CAN_BURST: True, CAN_AUTO: True, DAMAGE: 13, DECAY: 0.92, WEIGHT: 3,
        ACCURACY_BASE: 300, ACCURACY_SNEAK: 60, ACCURACY_WALK: 1500, ACCURACY_SPRINT: 2500, ACCURACY_JUMP: 4000,
        SWITCH: 70, KICK: 2, CASING_MODEL: CASING_556X45MM, CASING_NORMAL: -50, CASING_TANGENT: 0, CASING_BINORMAL: -250,
        CASING_OFFSET: {"normal": (-0.35, -0.34, 0.7), "zoom": (0.0, -0.3, 0.7)},
        PAP_STATS: {
            PAP_NAME: "Endless Barrage",
            CAPACITY: 180,
            REMAINING_BULLETS: 180,
            RELOAD_TIME: 120,
            RELOAD_MID: 70,
            RELOAD_END: 20,
            COOLDOWN: 1,
            ACCURACY_BASE: 240,
            ACCURACY_WALK: 900,
            ACCURACY_SPRINT: 1500,
            ACCURACY_JUMP: 3000,
            SWITCH: 50,
            DAMAGE: [26, 30, 35, 41, 48],
        },
    },
    "sounds": {
        "fire": "m249/fire",
        "reload": "m249/reload",
        "playerbegin": "m249/playerbegin",
        "playerend": "m249/playerend",
        "playermid": "m249/playermid",
        "crack": "medium"
    }
}


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
        GRENADE_DURATION: 200,  # 10 seconds of smoke
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

