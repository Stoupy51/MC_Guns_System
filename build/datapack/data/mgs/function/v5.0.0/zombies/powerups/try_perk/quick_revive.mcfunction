
#> mgs:v5.0.0/zombies/powerups/try_perk/quick_revive
#
# @executed	as @e[tag=mgs.pu_item] & at @s
#
# @within	mgs:v5.0.0/zombies/powerups/random_perk_iter
#

# Return early if the collecting player already owns this perk
execute if score @p[tag=mgs.pu_collecting] mgs.zb.perk.quick_revive matches 1 run return 0

# Apply the perk as the collecting player
execute as @p[tag=mgs.pu_collecting] run function mgs:v5.0.0/zombies/perks/apply {perk_id:"quick_revive"}

# Mark as applied so the iteration stops
scoreboard players set #pu_perk_applied mgs.data 1

