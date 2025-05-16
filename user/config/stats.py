
# Imports
from python_datapack.constants import CUSTOM_ITEM_VANILLA, OVERRIDE_MODEL


# Function
def get_data(ns: str, stats: dict = {}, override_model: dict = {}) -> dict:  # noqa: B006
    return {
        "id": "minecraft:warped_fungus_on_a_stick" if stats else CUSTOM_ITEM_VANILLA,
        "custom_data": {ns: {"gun":True, **stats} if stats else {"casing":True}},
        **({OVERRIDE_MODEL: override_model} if override_model else {})
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
The value is modified in setup_database.py according to the zoom type.
"""
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


# Gun stats
AK47: dict = {"stats": {
    BASE_WEAPON: "ak47",
    CAPACITY: 30, RELOAD: 70, RELOAD_END: 10, COOLDOWN: 2, BURST: 3, DAMAGE: 15, DECAY: 0.99,
    ACCURACY_BASE: 150, ACCURACY_SNEAK: 20, ACCURACY_WALK: 500, ACCURACY_SPRINT: 1500, ACCURACY_JUMP: 1800,
    SWITCH: 25, KICK: 2, CASING_MODEL: CASING_762X39MM, CASING_NORMAL: 200, CASING_TANGENT: 50, CASING_BINORMAL: -200,
    CASING_OFFSET: {"normal": (-0.35, -0.3, 0.7), "zoom": (-0.05, -0.25, 0.5)},
}}
# scoreboard players set ak47_mag S 30           # TODO: Not Implemented
# scoreboard players set ak47_reload S 70        # TODO: Not Implemented
# scoreboard players set ak47_reload_end S 10    # TODO: Not Implemented
# scoreboard players set ak47_cooldown S 2
# scoreboard players set ak47_burst S 3          ## TODO: Not Implemented
# scoreboard players set ak47_damage S 15
# scoreboard players set ak47_decay S 4
# scoreboard players set ak47_acc_base S 150
# scoreboard players set ak47_acc_sneaky S 20
# scoreboard players set ak47_acc_walk S 500
# scoreboard players set ak47_acc_sprint S 1500
# scoreboard players set ak47_acc_jump S 1800
# scoreboard players set ak47_switch S 25        ## TODO: Not Implemented
# scoreboard players set ak47_kick S 2
# scoreboard players set ak47_casing_n S 200
# scoreboard players set ak47_casing_t S 50
# scoreboard players set ak47_casing_b S -200

