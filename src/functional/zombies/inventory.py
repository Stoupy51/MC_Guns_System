
# Zombies Inventory Management
# Handles starting loadouts and weapon management during zombies games.
from stewbeet import Mem, write_versioned_function


def generate_zombies_inventory() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# ── Starting Loadout ──────────────────────────────────────────

	## Give starting loadout (clear inventory + give M1911)
	write_versioned_function("zombies/inventory/give_starting_loadout", f"""
# Clear existing inventory
clear @s

# Give starting weapon (M1911)
loot give @s loot {ns}:i/m1911
""")

	## Give respawn loadout (M1911 only, no clear — player may have picked up weapons)
	write_versioned_function("zombies/inventory/give_respawn_loadout", f"""
# Re-give M1911 on respawn
loot give @s loot {ns}:i/m1911
""")

