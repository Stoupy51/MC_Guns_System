
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
AK47: dict = {"stats":{
    "capacity": 30,        # Magazine capacity (number of rounds)
    "reload": 70,          # Reload time in ticks
    "reload_end": 10,      # Additional ticks at the end of reload animation
    "cooldown": 2,         # Ticks between shots
    "burst": 3,            # Number of rounds fired in burst mode
    "damage": 15,          # Base damage per shot
    "decay": 4,            # Damage falloff over distance
    "acc_base": 150,       # Base accuracy (lower is more accurate)
    "acc_sneaky": 20,      # Accuracy modifier when sneaking
    "acc_walk": 500,       # Accuracy penalty when walking
    "acc_sprint": 1500,    # Accuracy penalty when sprinting
    "acc_jump": 1800,      # Accuracy penalty when jumping
    "switch": 25,          # Weapon switch time in ticks
    "kick": 2,             # Recoil intensity
    "casing_n": 200,       # Ejected casing normal vector (x)
    "casing_t": 50,        # Ejected casing tangent vector (y)
    "casing_b": -200       # Ejected casing binormal vector (z)
}}

