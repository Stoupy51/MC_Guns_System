
# FIXME:
- Pap:
	# FIXME, use this Timeline instead (no rotation or size changes):
	#   240-> 211 (30t): GOING IN   — slide horizontally from ahead to center (beware of waiting 2 ticks after summon before starting interpolation to avoid information not being synced to client)
	#   210-> 151 (60t): INSIDE     — particles + periodic sound
	#   150-> 121 (30t): COMING OUT — slide horizontally from center to ahead
	#   120:             TRIGGER RETREAT — glowing weapon, starts retreat timer and allows collection
	#   119→ 1 (118t):   RETREAT   — weapon retreats back, still collectible
	#   0:               RETREAT FINISH — weapon destroyed (lost) (sound)

- When loosing weapon with pap, while having 3 weapons in inventory, we end up with 2.
In case the loose slot is between gun 1 and 3, when we get a new weapon it believes we have 2 guns (slot 1 and 2) and it replaces the third weapon even tho it's slot 2 that is empty

- Inventory:
  - If I swap gun 1 and 2 by pressing hotbar keys in inventory, then gun 1 will disappear (also the magazines) and gun 2 will be replaced to its expected position. We are effectively loosing a gun and its magazines.
  - Same issue apply with other items, if I swap the Player Info item with anything in the inventory, the item will be lost but not the Player Info item itself.

