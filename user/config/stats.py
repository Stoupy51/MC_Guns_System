
# Imports
from python_datapack.constants import OVERRIDE_MODEL


# Function
def get_data(ns: str, stats: dict, override_model: dict) -> dict:
    return {
        "id": "minecraft:warped_fungus_on_a_stick",
        "custom_data": {ns: {"gun":True, **stats}},
        OVERRIDE_MODEL: override_model
    }

# Constants
CAPACITY: str = "capacity"
""" Magazine capacity (number of rounds) """
RELOAD: str = "reload"
""" Reload time in ticks """
RELOAD_END: str = "reload_end"
""" Additional ticks at the end of reload animation """
COOLDOWN: str = "cooldown"
""" Ticks between shots """
BURST: str = "burst"
""" Number of rounds fired in burst mode """
DAMAGE: str = "damage"
""" Base damage per shot """
DECAY: str = "decay"
""" Damage falloff over distance """
ACCURACY: str = "acc_base"
""" Base accuracy (lower is more accurate) """
ACCURACY_SNEAKY: str = "acc_sneaky"
""" Accuracy modifier when sneaking """
ACCURACY_WALK: str = "acc_walk"
""" Accuracy penalty when walking """
ACCURACY_SPRINT: str = "acc_sprint"
""" Accuracy penalty when sprinting """
ACCURACY_JUMP: str = "acc_jump"
""" Accuracy penalty when jumping """
SWITCH: str = "switch"
""" Weapon switch time in ticks """
KICK: str = "kick"
""" Recoil intensity """
CASING_N: str = "casing_n"
""" Ejected casing normal vector (x) """
CASING_T: str = "casing_t"
""" Ejected casing tangent vector (y) """
CASING_B: str = "casing_b"
""" Ejected casing binormal vector (z) """


# Gun stats
AK47: dict = {
    "base_weapon": "ak47",
    "stats":{
    CAPACITY: 30, RELOAD: 70, RELOAD_END: 10, COOLDOWN: 2, BURST: 3, DAMAGE: 15, DECAY: 4,
    ACCURACY: 150, ACCURACY_SNEAKY: 20, ACCURACY_WALK: 500, ACCURACY_SPRINT: 1500, ACCURACY_JUMP: 1800,
    SWITCH: 25, KICK: 2, CASING_N: 200, CASING_T: 50, CASING_B: -200
}}

