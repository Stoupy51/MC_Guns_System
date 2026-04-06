
#> mgs:v5.0.0/zombies/revive/on_down
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/zombies/on_respawn
#

# Mark player as downed
scoreboard players set @s mgs.zb.downed 1
scoreboard players set @s mgs.zb.bleed 600
scoreboard players set @s mgs.zb.revive_p 0
tag @s add mgs.downed

# Slow down heavily + weakness (can't deal damage)
effect give @s slowness infinite 6 true
effect give @s weakness infinite 255 true
effect give @s mining_fatigue infinite 255 true

# Force crouch-like feel by lowering health to 1 heart
attribute @s minecraft:max_health base set 2
effect give @s instant_health 1 255 true

# Clear active weapon state to prevent shooting
scoreboard players set @s mgs.mp.death_count 0

# Announce
title @s title [{"text":"\u2620","color":"red"}]
title @s subtitle [{"translate":"mgs.you_are_down_wait_for_a_teammate_to_revive_you","color":"gray"}]
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"selector":"@s","color":"red"},[{"text":" ","color":"gray"}, {"translate":"mgs.is_down"}]]

