
#> mgs:v5.3.0/zombies/perks/tombstone_on_respawn
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.3.0/zombies/revive/do_round_respawn
#

scoreboard players operation #my_downed_id mgs.data = @s mgs.zb.downed_id
execute unless entity @e[tag=mgs.tombstone,predicate=mgs:v5.3.0/zombies/revive/downed_id_match] run return 0
scoreboard players set @e[tag=mgs.tombstone,predicate=mgs:v5.3.0/zombies/revive/downed_id_match] mgs.zb.ts.state 1
scoreboard players set @e[tag=mgs.tombstone,predicate=mgs:v5.3.0/zombies/revive/downed_id_match] mgs.zb.ts.timer 1200
title @s times 5 40 15
title @s title ["🪦"]
title @s subtitle [{"translate":"mgs.return_to_your","fallback":"Return to your ","color":"gold"},{"text":"🪦","color":"white"},{"translate":"mgs.within_60s_to_recover_your_gear","fallback":" within 60s to recover your gear!","color":"gold"}]

