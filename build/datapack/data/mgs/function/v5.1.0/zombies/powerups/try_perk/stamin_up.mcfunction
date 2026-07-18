
#> mgs:v5.1.0/zombies/powerups/try_perk/stamin_up
#
# @executed	at @s
#
# @within	mgs:v5.1.0/zombies/powerups/random_perk_iter
#

# Return early if the collecting player already owns this perk
execute if score @p[tag=mgs.pu_collecting] mgs.zb.perk.stamin_up matches 1 run return 0

# Apply the perk as the collecting player
execute as @p[tag=mgs.pu_collecting] run function mgs:v5.1.0/zombies/perks/apply {perk_id:"stamin_up"}

# Mark as applied so the iteration stops
scoreboard players set #pu_perk_applied mgs.data 1

