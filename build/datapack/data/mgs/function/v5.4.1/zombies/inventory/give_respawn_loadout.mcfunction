
#> mgs:v5.4.1/zombies/inventory/give_respawn_loadout
#
# @within	mgs:v5.4.1/dialog/close_then
#			mgs:v5.4.1/zombies/whos_who/on_down
#			mgs:v5.4.1/zombies/revive/do_round_respawn
#

function mgs:v5.4.1/zombies/inventory/give_starting_loadout

# Bleed-out respawns are lighter: knife, M1911 and 2 frags; bought knives, grenade types and tacticals are lost.
item modify entity @s hotbar.7 mgs:v5.4.1/grenade/set_count_2

