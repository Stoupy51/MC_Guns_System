
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
""" Maximum number of bullets that can be loaded into the weapon's magazine. """
RELOAD: str = "reload"
""" Time required to reload the weapon, measured in game ticks. """
RELOAD_END: str = "reload_end"
""" Additional time in ticks after the reload animation completes.
Used to create a smoother transition between reloading and being able to fire again. """
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
ACCURACY: str = "acc_base"
""" Base accuracy of the weapon when standing still.
Lower values indicate better accuracy (smaller spread of bullets). """
ACCURACY_SNEAKY: str = "acc_sneaky"
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
CASING_N: str = "casing_n"
""" X-component of the ejected bullet casing's direction vector.
Controls the direction in which spent casings are ejected from the weapon. """
CASING_T: str = "casing_t"
""" Y-component of the ejected bullet casing's direction vector.
Controls the vertical trajectory of ejected casings. """
CASING_B: str = "casing_b"
""" Z-component of the ejected bullet casing's direction vector.
Works with the other components to determine the full 3D trajectory of ejected casings. """


# Gun stats
AK47: dict = {
    "base_weapon": "ak47",
    "stats": {
    CAPACITY: 30, RELOAD: 70, RELOAD_END: 10, COOLDOWN: 2, BURST: 3, DAMAGE: 15, DECAY: 0.95,
    ACCURACY: 150, ACCURACY_SNEAKY: 20, ACCURACY_WALK: 500, ACCURACY_SPRINT: 1500, ACCURACY_JUMP: 1800,
    SWITCH: 25, KICK: 2, CASING_N: 200, CASING_T: 50, CASING_B: -200
}}

# scoreboard players set ak47_mag S 30           # TODO: Not Implemented
# scoreboard players set ak47_reload S 70        # TODO: Not Implemented
# scoreboard players set ak47_reload_end S 10    # TODO: Not Implemented
# scoreboard players set ak47_cooldown S 2       # TODO: Not Implemented
# scoreboard players set ak47_burst S 3          # TODO: Not Implemented
# scoreboard players set ak47_damage S 15
# scoreboard players set ak47_decay S 4
# scoreboard players set ak47_acc_base S 150     # TODO: Not Implemented
# scoreboard players set ak47_acc_sneaky S 20    # TODO: Not Implemented
# scoreboard players set ak47_acc_walk S 500     # TODO: Not Implemented
# scoreboard players set ak47_acc_sprint S 1500  # TODO: Not Implemented
# scoreboard players set ak47_acc_jump S 1800    # TODO: Not Implemented
# scoreboard players set ak47_switch S 25        # TODO: Not Implemented
# scoreboard players set ak47_kick S 2           # TODO: Not Implemented
# scoreboard players set ak47_casing_n S 200     # TODO: Not Implemented
# scoreboard players set ak47_casing_t S 50      # TODO: Not Implemented
# scoreboard players set ak47_casing_b S -200    # TODO: Not Implemented

