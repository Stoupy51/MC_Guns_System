
#> mgs:v5.4.2/zombies/jockey/kill_mate
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/jockey/link
#

execute if entity @s[tag=mgs.zb_jockey_linked] run return 0
tag @s add mgs.zb_jockey_linked
scoreboard players operation @s mgs.zb.player_hit > #zb_jk_hit mgs.data

# Unattributed: the player's kill count only grew for the part they hit.
kill @s

