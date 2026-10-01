""" Left-click detection.

Minecraft has no "player swung" event, but a zero-reach `piercing_weapon` plus a `post_piercing_attack` enchantment turns any left click (even at air) into a function call.
Left click is the reload key here; fire mode is on the drop key (switch).
The enchantment and its function live here; the item components that arm it are added to every gun in config/stats/items (add_item).
"""
# Imports
from beet import Enchantment
from stewbeet import Mem, write_versioned_function

from ....config.stats.keys import RELOAD_TIME

# Constants
ENCHANTMENT_ID: str = "left_click"
""" Named for the input it detects, not the action it performs: the ID is baked into every gun item
stack, and changing it needs a world restart to re-register (enchantments live in WORLD_REGISTRIES,
which /reload does not touch). """

# Functions
def main() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Not versioned: gun stacks persist across pack updates, so the embedded id must stay valid; only the function it points at is versioned.
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

	# Run as the attacking player.
	write_versioned_function("weapon/left_click", f"""
# A left click can land on the frame the weapon changes, so the main hand is checked again.
execute unless items entity @s weapon.mainhand *[custom_data~{{{ns}:{{gun:true}}}}] run return 0

function {ns}:v{version}/utils/copy_gun_data

# Throwables and knives have no {RELOAD_TIME}: ammo/reload would set a garbage cooldown and lock the item.
execute unless data storage {ns}:gun all.stats.{RELOAD_TIME} run return 0

# ammo/reload fails while reloading or full, so spamming is safe.
function {ns}:v{version}/ammo/reload
""")

