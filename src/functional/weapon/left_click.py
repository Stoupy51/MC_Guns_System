
# Imports
from beet import Enchantment
from stewbeet import Mem, write_versioned_function

from ...config.stats import CAN_AUTO, CAN_BURST

# Left-click detection.
#
# Minecraft has no "player swung" event, but an enchantment's `post_piercing_attack` effect fires a
# function on every piercing attack, and a `piercing_weapon` component with zero reach makes the
# attack connect with nothing while still firing the effect. Combining the two turns any left click
# — including a swing at empty air — into a function call. Right click is already taken by firing
# (the `using_item` advancement in common.py), so left click drives the fire-mode toggle. Reload
# lives on the hand-swap key instead (player/offhand_swap_check in common.py).
#
# The two halves live in different places: the enchantment + function are here, while the item
# components that arm it are attached to every gun in config/stats.py (see add_item).
#
# Named for the input it detects, not the action it currently performs: the ID is baked into every
# gun item stack, and changing it later would need another world restart to re-register (enchantments
# live in WORLD_REGISTRIES, which /reload does not touch).
ENCHANTMENT_ID: str = "left_click"


def main() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# The enchantment is deliberately NOT versioned: gun item stacks persist in player inventories
	# and in the world across pack updates, so the ID they embed has to stay valid. Only the function
	# it points at is versioned, and that is rewritten on every build.
	Mem.ctx.data[ns].enchantments[ENCHANTMENT_ID] = Enchantment({
		"description": "",
		"max_level": 1,
		"slots": ["hand"],
		"supported_items": [],
		"weight": 1,
		"anvil_cost": 0,
		"min_cost": {"base": 0, "per_level_above_first": 0},
		"max_cost": {"base": 0, "per_level_above_first": 0},
		"effects": {
			"minecraft:post_piercing_attack": [
				{"effect": {"type": "run_function", "function": f"{ns}:v{version}/weapon/left_click"}}
			]
		},
	})

	# Runs as the attacking player.
	write_versioned_function("weapon/left_click", f"""
# The enchantment only sits on our guns, but a player can left-click mid-swap: re-check the mainhand
# so a click landing on the frame the weapon changes can't retarget whatever is held now.
execute unless items entity @s weapon.mainhand *[custom_data~{{{ns}:{{gun:true}}}}] run return 0

function {ns}:v{version}/utils/copy_gun_data

# Only weapons that actually have a second mode respond. Throwables carry a fire_mode too, so
# without this the toggle would pointlessly rewrite the item and fire the change signal on grenades.
execute unless data storage {ns}:gun all.stats.{CAN_AUTO} unless data storage {ns}:gun all.stats.{CAN_BURST} run return 0

# Cycle the mode (auto -> semi -> burst -> auto, narrowed to whatever the weapon supports).
function {ns}:v{version}/switch/do_toggle_fire_mode
""")
