""" Item registration: the add_item() builder and the model loading it depends on. """
# Imports
import json
from typing import Any

import stouputils as stp
from stewbeet import CUSTOM_ITEM_VANILLA, Item, JsonDict, Mem


# Classes
class ItemBuilder:
	""" Items helpers. """

	# Constants
	SRC_ROOT: str = stp.get_root_path(__file__, go_up=2)
	""" The src/ directory. Two levels up from config/stats/items.py. """
	ITEM_MODELS_PATH: str = f"{SRC_ROOT}/database/models"
	ALL_SLOTS: tuple[str, ...] = (
		*[f"hotbar.{i}" for i in range(9)],
		"weapon.offhand",
		*[f"inventory.{i}" for i in range(3*9)],
		"player.cursor",
		*[f"player.crafting.{i}" for i in range(4)],
	)

	# Functions
	# Utility functions
	@staticmethod
	def json_dump(x: Any) -> str: return stp.json_dump(x, max_level=-1)
	@staticmethod
	def get_model_path(model_name: str) -> str: return f"{ItemBuilder.ITEM_MODELS_PATH}/{model_name}.json"
	@staticmethod
	def load_model(path: str) -> JsonDict:
		return json.loads(stp.read_file(path).replace("mgs:item", f"{Mem.ctx.project_id}:item"))

	@staticmethod
	def add_item(id: str, stats: JsonDict | None = None, model_path: str | None = None, max_stack_size: int = 1, **kwargs: Any) -> Item:
		if model_path == "auto":
			model_path = ItemBuilder.get_model_path(id)
		ns: str = Mem.ctx.project_id
		components: JsonDict = {
			"max_stack_size": max_stack_size,
			"custom_data": {ns: {"gun":True, **stats} if stats else {"casing":True}},
			"rarity": "common",
		}
		if stats:
			# Left-click detection (functional/weapon/left_click.py): a zero-reach piercing_weapon makes every swing fire the enchantment's post_piercing_attack effect, even at air.
			# That effect is what toggles fire mode.
			# The enchantment is hidden from the tooltip and its glint suppressed, so it stays an implementation detail.
			components |= {
				"piercing_weapon": {"min_reach": 0.0, "max_reach": 0.0, "hitbox_margin": 0.0},
				"enchantments": {f"{ns}:left_click": 1},
				"enchantment_glint_override": False,
				"tooltip_display": {"hidden_components": ["minecraft:enchantments"]},
			}
		return Item(
			id=id,
			base_item="minecraft:poisonous_potato" if stats else CUSTOM_ITEM_VANILLA,
			components=components,
			override_model=(ItemBuilder.load_model(model_path) if model_path else None),
			**kwargs
		)

