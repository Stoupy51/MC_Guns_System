
#> mgs:v5.1.0/zombies/inventory/give_respawn_loadout
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/zombies/whos_who/on_down
#			mgs:v5.1.0/zombies/revive/do_round_respawn
#

function mgs:v5.1.0/zombies/inventory/give_starting_loadout

# Bleed-out respawns come back lighter than a fresh game start: knife + M1911 + only 2 frags.
# The starting-loadout clear also strips any bought knife/grenade-type/tactical (intended).
item modify entity @s hotbar.7 mgs:v5.1.0/grenade/set_count_2

