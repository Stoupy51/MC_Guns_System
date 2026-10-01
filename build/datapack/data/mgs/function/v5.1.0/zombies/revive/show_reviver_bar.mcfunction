
#> mgs:v5.1.0/zombies/revive/show_reviver_bar
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/whos_who/owner_tick [ at @s ]
#			mgs:v5.1.0/zombies/revive/downed_tick [ at @s ]
#

# #rv_reviver_disp is the progress snapshotted in downed_tick: the reviver cannot select the downed player,
# who spectates a camera outside the revive range. Seconds = p / 20, tenths = (p % 20) / 2.
scoreboard players operation #rv_rev_sec mgs.data = #rv_reviver_disp mgs.data
scoreboard players operation #rv_rev_sec mgs.data /= #20 mgs.data
scoreboard players operation #rv_rev_tenth mgs.data = #rv_reviver_disp mgs.data
scoreboard players operation #rv_rev_tenth mgs.data %= #20 mgs.data
scoreboard players operation #rv_rev_tenth mgs.data /= #2 mgs.data

# revive_complete runs as the downed player and cannot select the revivers.
tag @s add mgs.zb_reviver

execute if entity @s[tag=mgs.perk.quick_revive] run function mgs:v5.1.0/zombies/revive/show_reviver_bar_quick
execute unless entity @s[tag=mgs.perk.quick_revive] run function mgs:v5.1.0/zombies/revive/show_reviver_bar_normal

