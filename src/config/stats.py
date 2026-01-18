
# Imports
import json
from typing import Any

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
        base_item="minecraft:warped_fungus_on_a_stick" if stats else Item.base_item,
        components={
            "custom_data": {Mem.ctx.project_id: {"gun":True, **stats} if stats else {"casing":True}},
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
CRACK_TYPE: str = "crack_type"
""" Type of crack sound effect played when firing the weapon.
Available types: tiny, small, medium, large, largest, rocket. """


# Optional constants
MODELS: str = "models"
""" Models to use to switch between normal and zoom modes. """
IS_ZOOM: str = "is_zoom"
""" Indicates whether the weapon is currently in zoom mode """
WEAPON_ID: str = "weapon_id"
""" Dynamique unique identifier assigned to each weapon item when selected from the hotbar.
Used to track weapon switching and manage weapon-specific systems and states."""



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
M16A4: JsonDict = {"stats": {
    BASE_WEAPON: "m16a4", CRACK_TYPE: "medium",
    CAPACITY: 30, RELOAD_TIME: 60, RELOAD_END: 10, COOLDOWN: 2, BURST: 3, DAMAGE: 14, DECAY: 0.95,
    ACCURACY_BASE: 100, ACCURACY_SNEAK: 7, ACCURACY_WALK: 450, ACCURACY_SPRINT: 1000, ACCURACY_JUMP: 1500,
    SWITCH: 20, KICK: 2, CASING_MODEL: CASING_556X45MM, CASING_NORMAL: 150, CASING_TANGENT: -75, CASING_BINORMAL: -200,
    CASING_OFFSET: {"normal": (-0.4, -0.35, 0.7), "zoom": (-0.05, -0.25, 0.5)},
}}

AK47: JsonDict = {"stats": {
    BASE_WEAPON: "ak47", CRACK_TYPE: "medium",
    CAPACITY: 30, RELOAD_TIME: 70, RELOAD_END: 10, COOLDOWN: 2, BURST: 3, DAMAGE: 15, DECAY: 0.90,
    ACCURACY_BASE: 150, ACCURACY_SNEAK: 20, ACCURACY_WALK: 500, ACCURACY_SPRINT: 1500, ACCURACY_JUMP: 1800,
    SWITCH: 25, KICK: 2, CASING_MODEL: CASING_762X39MM, CASING_NORMAL: 200, CASING_TANGENT: 50, CASING_BINORMAL: -200,
    CASING_OFFSET: {"normal": (-0.35, -0.3, 0.7), "zoom": (-0.05, -0.25, 0.5)},
}}

FNFAL: JsonDict = {"stats": {
    BASE_WEAPON: "fnfal", CRACK_TYPE: "large",
    CAPACITY: 20, RELOAD_TIME: 80, RELOAD_END: 20, COOLDOWN: 3, BURST: 2, DAMAGE: 22, DECAY: 0.92,
    ACCURACY_BASE: 200, ACCURACY_SNEAK: 10, ACCURACY_WALK: 600, ACCURACY_SPRINT: 1800, ACCURACY_JUMP: 2500,
    SWITCH: 35, KICK: 3, CASING_MODEL: CASING_762X51MM, CASING_NORMAL: 125, CASING_TANGENT: 25, CASING_BINORMAL: -200,
    CASING_OFFSET: {"normal": (-0.3, -0.25, 0.7), "zoom": (-0.05, -0.2, 0.5)},
}}

AUG: JsonDict = {"stats": {
    BASE_WEAPON: "aug", CRACK_TYPE: "medium",
    CAPACITY: 30, RELOAD_TIME: 80, RELOAD_MID: 40, RELOAD_END: 10, COOLDOWN: 2, BURST: 2, DAMAGE: 13, DECAY: 0.95,
    ACCURACY_BASE: 100, ACCURACY_SNEAK: 12, ACCURACY_WALK: 350, ACCURACY_SPRINT: 800, ACCURACY_JUMP: 1200,
    SWITCH: 15, KICK: 2, CASING_MODEL: CASING_556X45MM, CASING_NORMAL: 125, CASING_TANGENT: -100, CASING_BINORMAL: -125,
    CASING_OFFSET: {"normal": (-0.45, -0.4, 0.4), "zoom": (-0.05, -0.3, 0.3)},
}}

M4A1: JsonDict = {"stats": {
    BASE_WEAPON: "m4a1", CRACK_TYPE: "medium",
    CAPACITY: 30, RELOAD_TIME: 50, RELOAD_END: 14, COOLDOWN: 2, BURST: 3, DAMAGE: 13, DECAY: 0.92,
    ACCURACY_BASE: 110, ACCURACY_SNEAK: 15, ACCURACY_WALK: 400, ACCURACY_SPRINT: 900, ACCURACY_JUMP: 1400,
    SWITCH: 17, KICK: 2, CASING_MODEL: CASING_556X45MM, CASING_NORMAL: 150, CASING_TANGENT: -75, CASING_BINORMAL: -200,
    CASING_OFFSET: {"normal": (-0.4, -0.35, 0.7), "zoom": (-0.05, -0.25, 0.5)},
}}

G3A3: JsonDict = {"stats": {
    BASE_WEAPON: "g3a3", CRACK_TYPE: "large",
    CAPACITY: 20, RELOAD_TIME: 80, RELOAD_END: 17, COOLDOWN: 3, BURST: 2, DAMAGE: 20, DECAY: 0.92,
    ACCURACY_BASE: 180, ACCURACY_SNEAK: 6, ACCURACY_WALK: 600, ACCURACY_SPRINT: 1800, ACCURACY_JUMP: 2500,
    SWITCH: 30, KICK: 3, CASING_MODEL: CASING_762X51MM, CASING_NORMAL: 200, CASING_TANGENT: 100, CASING_BINORMAL: -300,
    CASING_OFFSET: {"normal": (-0.32, -0.3, 0.7), "zoom": (-0.05, -0.25, 0.5)},
}}

FAMAS: JsonDict = {"stats": {
    BASE_WEAPON: "famas", CRACK_TYPE: "medium",
    CAPACITY: 25, RELOAD_TIME: 80, RELOAD_MID: 40, RELOAD_END: 10, COOLDOWN: 2, BURST: 2, DAMAGE: 13, DECAY: 0.95,
    ACCURACY_BASE: 110, ACCURACY_SNEAK: 15, ACCURACY_WALK: 400, ACCURACY_SPRINT: 900, ACCURACY_JUMP: 1400,
    SWITCH: 13, KICK: 2, CASING_MODEL: CASING_556X45MM, CASING_NORMAL: 150, CASING_TANGENT: -150, CASING_BINORMAL: -225,
    CASING_OFFSET: {"normal": (-0.45, -0.35, 0.3), "zoom": (-0.05, -0.3, 0.3)},
}}

SCAR17: JsonDict = {"stats": {
    BASE_WEAPON: "scar17", CRACK_TYPE: "large",
    CAPACITY: 20, RELOAD_TIME: 60, RELOAD_END: 15, COOLDOWN: 3, BURST: 2, DAMAGE: 18, DECAY: 0.92,
    ACCURACY_BASE: 140, ACCURACY_SNEAK: 5, ACCURACY_WALK: 500, ACCURACY_SPRINT: 1500, ACCURACY_JUMP: 2300,
    SWITCH: 30, KICK: 3, CASING_MODEL: CASING_762X51MM, CASING_NORMAL: 50, CASING_TANGENT: -75, CASING_BINORMAL: -300,
    CASING_OFFSET: {"normal": (-0.32, -0.3, 0.7), "zoom": (-0.05, -0.25, 0.5)},
}}

# Pistols
M1911: JsonDict = {"stats": {
    BASE_WEAPON: "m1911", CRACK_TYPE: "tiny",
    CAPACITY: 7, RELOAD_TIME: 45, RELOAD_END: 10, DAMAGE: 11, DECAY: 0.88,
    ACCURACY_BASE: 165, ACCURACY_SNEAK: 105, ACCURACY_WALK: 250, ACCURACY_SPRINT: 450, ACCURACY_JUMP: 800,
    SWITCH: 10, KICK: 4, CASING_MODEL: CASING_45ACP, CASING_NORMAL: 250, CASING_TANGENT: 0, CASING_BINORMAL: -150,
    CASING_OFFSET: {"normal": (-0.33, -0.25, 0.5), "zoom": (-0.05, -0.05, 0.4)},
}}

M9: JsonDict = {"stats": {
    BASE_WEAPON: "m9", CRACK_TYPE: "tiny",
    CAPACITY: 15, RELOAD_TIME: 60, RELOAD_END: 15, DAMAGE: 9, DECAY: 0.92,
    ACCURACY_BASE: 130, ACCURACY_SNEAK: 75, ACCURACY_WALK: 160, ACCURACY_SPRINT: 400, ACCURACY_JUMP: 800,
    SWITCH: 10, KICK: 3, CASING_MODEL: CASING_9X19MM, CASING_NORMAL: 100, CASING_TANGENT: -75, CASING_BINORMAL: -150,
    CASING_OFFSET: {"normal": (-0.35, -0.25, 0.5), "zoom": (-0.05, -0.1, 0.4)},
}}

DEAGLE: JsonDict = {"stats": {
    BASE_WEAPON: "deagle", CRACK_TYPE: "tiny",
    CAPACITY: 7, RELOAD_TIME: 70, RELOAD_END: 15, COOLDOWN: 3, DAMAGE: 17, DECAY: 0.90,
    ACCURACY_BASE: 220, ACCURACY_SNEAK: 50, ACCURACY_WALK: 400, ACCURACY_SPRINT: 1000, ACCURACY_JUMP: 2000,
    SWITCH: 15, KICK: 5, CASING_MODEL: CASING_50AE, CASING_NORMAL: 250, CASING_TANGENT: -75, CASING_BINORMAL: -100,
    CASING_OFFSET: {"normal": (-0.3, -0.2, 0.5), "zoom": (-0.05, -0.05, 0.4)},
}}

MAKAROV: JsonDict = {"stats": {
    BASE_WEAPON: "makarov", CRACK_TYPE: "tiny",
    CAPACITY: 8, RELOAD_TIME: 40, RELOAD_END: 10, DAMAGE: 9, DECAY: 0.90,
    ACCURACY_BASE: 120, ACCURACY_SNEAK: 65, ACCURACY_WALK: 130, ACCURACY_SPRINT: 350, ACCURACY_JUMP: 800,
    SWITCH: 8, KICK: 2, CASING_MODEL: CASING_9X18MM, CASING_NORMAL: 250, CASING_TANGENT: -100, CASING_BINORMAL: -75,
    CASING_OFFSET: {"normal": (-0.3, -0.25, 0.5), "zoom": (-0.05, -0.05, 0.4)},
}}

GLOCK17: JsonDict = {"stats": {
    BASE_WEAPON: "glock17", CRACK_TYPE: "tiny",
    CAPACITY: 17, RELOAD_TIME: 60, RELOAD_END: 16, DAMAGE: 9, DECAY: 0.92,
    ACCURACY_BASE: 150, ACCURACY_SNEAK: 90, ACCURACY_WALK: 170, ACCURACY_SPRINT: 400, ACCURACY_JUMP: 800,
    SWITCH: 8, KICK: 3, CASING_MODEL: CASING_9X19MM, CASING_NORMAL: 225, CASING_TANGENT: -100, CASING_BINORMAL: -75,
    CASING_OFFSET: {"normal": (-0.35, -0.27, 0.5), "zoom": (-0.05, 0.0, 0.4)},
}}

GLOCK18: JsonDict = {"stats": {
    BASE_WEAPON: "glock18", CRACK_TYPE: "tiny",
    CAPACITY: 19, RELOAD_TIME: 70, RELOAD_END: 16, COOLDOWN: 1, BURST: 4, DAMAGE: 9, DECAY: 0.92,
    ACCURACY_BASE: 180, ACCURACY_SNEAK: 140, ACCURACY_WALK: 300, ACCURACY_SPRINT: 400, ACCURACY_JUMP: 800,
    SWITCH: 10, KICK: 3, CASING_MODEL: CASING_9X19MM, CASING_NORMAL: 225, CASING_TANGENT: -100, CASING_BINORMAL: -75,
    CASING_OFFSET: {"normal": (-0.35, -0.27, 0.5), "zoom": (-0.05, 0.0, 0.4)},
}}

VZ61: JsonDict = {"stats": {
    BASE_WEAPON: "vz61", CRACK_TYPE: "tiny",
    CAPACITY: 20, RELOAD_TIME: 70, RELOAD_END: 14, COOLDOWN: 2, BURST: 2, DAMAGE: 8, DECAY: 0.92,
    ACCURACY_BASE: 150, ACCURACY_SNEAK: 80, ACCURACY_WALK: 290, ACCURACY_SPRINT: 400, ACCURACY_JUMP: 800,
    SWITCH: 12, KICK: 2, CASING_MODEL: CASING_32ACP, CASING_NORMAL: 300, CASING_TANGENT: 25, CASING_BINORMAL: 0,
    CASING_OFFSET: {"normal": (-0.23, -0.1, 0.5), "zoom": (0, 0.05, 0.4)},
}}

# SMGS
MP5: JsonDict = {"stats": {
    BASE_WEAPON: "mp5", CRACK_TYPE: "tiny",
    CAPACITY: 30, RELOAD_TIME: 60, RELOAD_MID: 25, RELOAD_END: 5, COOLDOWN: 2, BURST: 2, DAMAGE: 10, DECAY: 0.92,
    ACCURACY_BASE: 100, ACCURACY_SNEAK: 60, ACCURACY_WALK: 200, ACCURACY_SPRINT: 450, ACCURACY_JUMP: 1000,
    SWITCH: 15, KICK: 1, CASING_MODEL: CASING_9X19MM, CASING_NORMAL: 225, CASING_TANGENT: 10, CASING_BINORMAL: -275,
    CASING_OFFSET: {"normal": (-0.38, -0.35, 0.7), "zoom": (-0.05, -0.25, 0.5)},
}}

MAC10: JsonDict = {"stats": {
    BASE_WEAPON: "mac10", CRACK_TYPE: "tiny",
    CAPACITY: 30, RELOAD_TIME: 50, RELOAD_MID: 38, RELOAD_END: 10, COOLDOWN: 1, BURST: 4, DAMAGE: 11, DECAY: 0.88,
    ACCURACY_BASE: 220, ACCURACY_SNEAK: 150, ACCURACY_WALK: 330, ACCURACY_SPRINT: 400, ACCURACY_JUMP: 800,
    SWITCH: 10, KICK: 2, CASING_MODEL: CASING_45ACP, CASING_NORMAL: 125, CASING_TANGENT: -25, CASING_BINORMAL: -175,
    CASING_OFFSET: {"normal": (-0.4, -0.35, 0.7), "zoom": (-0.1, -0.15, 0.5)},
}}

MP7: JsonDict = {"stats": {
    BASE_WEAPON: "mp7", CRACK_TYPE: "small",
    CAPACITY: 40, RELOAD_TIME: 55, RELOAD_END: 15, COOLDOWN: 2, BURST: 3, DAMAGE: 12, DECAY: 0.95,
    ACCURACY_BASE: 150, ACCURACY_SNEAK: 50, ACCURACY_WALK: 250, ACCURACY_SPRINT: 480, ACCURACY_JUMP: 1500,
    SWITCH: 20, KICK: 2, CASING_MODEL: CASING_46X30MM, CASING_NORMAL: 10, CASING_TANGENT: -50, CASING_BINORMAL: -275,
    CASING_OFFSET: {"normal": (-0.45, -0.4, 0.7), "zoom": (-0.05, -0.4, 0.5)},
}}

PPSH41: JsonDict = {"stats": {
    BASE_WEAPON: "ppsh41", CRACK_TYPE: "tiny",
    CAPACITY: 71, RELOAD_TIME: 100, RELOAD_MID: 70, RELOAD_END: 16, COOLDOWN: 1, BURST: 4, DAMAGE: 10, DECAY: 0.92,
    ACCURACY_BASE: 175, ACCURACY_SNEAK: 125, ACCURACY_WALK: 400, ACCURACY_SPRINT: 700, ACCURACY_JUMP: 1500,
    SWITCH: 40, KICK: 2, CASING_MODEL: CASING_762X25MM, CASING_NORMAL: 300, CASING_TANGENT: -50, CASING_BINORMAL: -25,
    CASING_OFFSET: {"normal": (-0.38, -0.2, 0.7), "zoom": (0.0, 0.0, 0.5)},
}}

STEN: JsonDict = {"stats": {
    BASE_WEAPON: "sten", CRACK_TYPE: "tiny",
    CAPACITY: 32, RELOAD_TIME: 58, RELOAD_MID: 40, RELOAD_END: 10, COOLDOWN: 3, BURST: 2, DAMAGE: 11, DECAY: 0.92,
    ACCURACY_BASE: 150, ACCURACY_SNEAK: 100, ACCURACY_WALK: 300, ACCURACY_SPRINT: 400, ACCURACY_JUMP: 800,
    SWITCH: 20, KICK: 1, CASING_MODEL: CASING_9X19MM, CASING_NORMAL: 20, CASING_TANGENT: 0, CASING_BINORMAL: -125,
    CASING_OFFSET: {"normal": (-0.38, -0.35, 0.7), "zoom": (-0.1, -0.12, 0.5)},
}}

# Shotguns
SPAS12: JsonDict = {"stats": {
    BASE_WEAPON: "spas12", CRACK_TYPE: "largest",
    CAPACITY: 8, RELOAD_TIME: 20, COOLDOWN: 16, DAMAGE: 13, DECAY: 0.82,
    ACCURACY_BASE: 230, ACCURACY_SNEAK: 190, ACCURACY_WALK: 300, ACCURACY_SPRINT: 800, ACCURACY_JUMP: 1500,
    SWITCH: 25, KICK: 6, CASING_MODEL: CASING_12GA275IN, CASING_NORMAL: 25, CASING_TANGENT: 100, CASING_BINORMAL: -200,
    CASING_OFFSET: {"normal": (-0.35, -0.3, 0.7), "zoom": (-0.1, -0.3, 0.6)},
}}

M500: JsonDict = {"stats": {
    BASE_WEAPON: "m500", CRACK_TYPE: "largest",
    CAPACITY: 5, RELOAD_TIME: 22, COOLDOWN: 18, DAMAGE: 14, DECAY: 0.82,
    ACCURACY_BASE: 190, ACCURACY_SNEAK: 160, ACCURACY_WALK: 350, ACCURACY_SPRINT: 800, ACCURACY_JUMP: 1500,
    SWITCH: 30, KICK: 5, CASING_MODEL: CASING_12GA3IN, CASING_NORMAL: 50, CASING_TANGENT: 75, CASING_BINORMAL: -200,
    CASING_OFFSET: {"normal": (-0.35, -0.27, 0.7), "zoom": (-0.1, -0.25, 0.6)},
}}

M590: JsonDict = {"stats": {
    BASE_WEAPON: "m590", CRACK_TYPE: "largest",
    CAPACITY: 8, RELOAD_TIME: 22, COOLDOWN: 19, DAMAGE: 14, DECAY: 0.82,
    ACCURACY_BASE: 210, ACCURACY_SNEAK: 175, ACCURACY_WALK: 325, ACCURACY_SPRINT: 800, ACCURACY_JUMP: 1500,
    SWITCH: 35, KICK: 5, CASING_MODEL: CASING_12GA3IN, CASING_NORMAL: 50, CASING_TANGENT: 80, CASING_BINORMAL: -220,
    CASING_OFFSET: {"normal": (-0.35, -0.27, 0.7), "zoom": (-0.1, -0.25, 0.6)},
}}

# Snipers
SVD: JsonDict = {"stats": {
    BASE_WEAPON: "svd", CRACK_TYPE: "large",
    CAPACITY: 10, RELOAD_TIME: 73, RELOAD_MID: 40, RELOAD_END: 10, COOLDOWN: 5, DAMAGE: 27, DECAY: 0.95,
    ACCURACY_BASE: 350, ACCURACY_SNEAK: 5, ACCURACY_WALK: 700, ACCURACY_SPRINT: 1500, ACCURACY_JUMP: 3000,
    SWITCH: 40, KICK: 4, CASING_MODEL: CASING_762X54MM, CASING_NORMAL: 150, CASING_TANGENT: -150, CASING_BINORMAL: -175,
    CASING_OFFSET: {"normal": (-0.3, -0.27, 0.7), "zoom": (-0.05, -0.25, 0.5)},
}}

M82: JsonDict = {"stats": {
    BASE_WEAPON: "m82", CRACK_TYPE: "largest",
    CAPACITY: 10, RELOAD_TIME: 80, RELOAD_MID: 50, RELOAD_END: 15, COOLDOWN: 10, DAMAGE: 55, DECAY: 0.90,
    ACCURACY_BASE: 450, ACCURACY_SNEAK: 12, ACCURACY_WALK: 800, ACCURACY_SPRINT: 1500, ACCURACY_JUMP: 3000,
    SWITCH: 50, KICK: 5, CASING_MODEL: CASING_50BMG, CASING_NORMAL: 50, CASING_TANGENT: -25, CASING_BINORMAL: -225,
    CASING_OFFSET: {"normal": (-0.28, -0.3, 0.7), "zoom": (-0.1, -0.25, 0.6)},
}}

MOSIN: JsonDict = {"stats": {
    BASE_WEAPON: "mosin", CRACK_TYPE: "large",
    CAPACITY: 5, RELOAD_TIME: 20, RELOAD_MID: 15, COOLDOWN: 40, DAMAGE: 29, DECAY: 0.95,
    ACCURACY_BASE: 150, ACCURACY_SNEAK: 3, ACCURACY_WALK: 175, ACCURACY_SPRINT: 1000, ACCURACY_JUMP: 1500,
    SWITCH: 25, KICK: 4, CASING_MODEL: CASING_762X54MM, CASING_NORMAL: 100, CASING_TANGENT: -50, CASING_BINORMAL: -100,
    CASING_OFFSET: {"normal": (-0.35, -0.2, 0.6), "zoom": (-0.05, -0.2, 0.4)},
}}

M24: JsonDict = {"stats": {
    BASE_WEAPON: "m24", CRACK_TYPE: "largest",
    CAPACITY: 5, RELOAD_TIME: 25, RELOAD_MID: 14, COOLDOWN: 45, DAMAGE: 36, DECAY: 0.92,
    ACCURACY_BASE: 350, ACCURACY_SNEAK: 1, ACCURACY_WALK: 700, ACCURACY_SPRINT: 1500, ACCURACY_JUMP: 3000,
    SWITCH: 39, KICK: 4, CASING_MODEL: CASING_338LAPUA, CASING_NORMAL: 100, CASING_TANGENT: -50, CASING_BINORMAL: -100,
    CASING_OFFSET: {"normal": (-0.35, -0.2, 0.6), "zoom": (-0.05, -0.2, 0.4)},
}}


# Special
RPG7: JsonDict = {"stats": {
    BASE_WEAPON: "rpg7", CRACK_TYPE: "rocket",
    CAPACITY: 1, RELOAD_TIME: 110, RELOAD_END: 20, COOLDOWN: 10, DAMAGE: 30, DECAY: 1.00,
    ACCURACY_BASE: 250, ACCURACY_SNEAK: 100, ACCURACY_WALK: 300, ACCURACY_SPRINT: 300, ACCURACY_JUMP: 300,
    SWITCH: 55, KICK: 6,
}}

RPK: JsonDict = {"stats": {
    BASE_WEAPON: "rpk", CRACK_TYPE: "medium",
    CAPACITY: 75, RELOAD_TIME: 115, RELOAD_MID: 60, RELOAD_END: 20, COOLDOWN: 2, BURST: 2, DAMAGE: 15, DECAY: 0.90,
    ACCURACY_BASE: 470, ACCURACY_SNEAK: 80, ACCURACY_WALK: 900, ACCURACY_SPRINT: 1500, ACCURACY_JUMP: 3000,
    SWITCH: 55, KICK: 3, CASING_MODEL: CASING_762X39MM, CASING_NORMAL: 200, CASING_TANGENT: 50, CASING_BINORMAL: -200,
    CASING_OFFSET: {"normal": (-0.35, -0.28, 0.7), "zoom": (-0.05, -0.25, 0.5)},
}}

M249: JsonDict = {"stats": {
    BASE_WEAPON: "m249", CRACK_TYPE: "medium",
    CAPACITY: 150, RELOAD_TIME: 175, RELOAD_MID: 110, RELOAD_END: 30, COOLDOWN: 2, BURST: 2, DAMAGE: 13, DECAY: 0.92,
    ACCURACY_BASE: 300, ACCURACY_SNEAK: 60, ACCURACY_WALK: 1500, ACCURACY_SPRINT: 2500, ACCURACY_JUMP: 4000,
    SWITCH: 70, KICK: 2, CASING_MODEL: CASING_556X45MM, CASING_NORMAL: -50, CASING_TANGENT: 0, CASING_BINORMAL: -250,
    CASING_OFFSET: {"normal": (-0.35, -0.34, 0.7), "zoom": (0.0, -0.3, 0.7)},
}}

