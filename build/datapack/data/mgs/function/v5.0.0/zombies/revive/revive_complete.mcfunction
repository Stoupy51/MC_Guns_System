
#> mgs:v5.0.0/zombies/revive/revive_complete
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/revive/progress_tick
#

# Remove downed state
scoreboard players set @s mgs.zb.downed 0
scoreboard players set @s mgs.zb.revive_p 0
tag @s remove mgs.downed

# Remove downed effects
effect clear @s slowness
effect clear @s weakness
effect clear @s mining_fatigue

# Restore max health (check for Juggernog perk)
execute if score @s mgs.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 40
execute unless score @s mgs.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 20

# Heal to full
effect give @s instant_health 1 255 true

# Announce
title @s title [{"text":"\u2764","color":"green"}]
title @s subtitle [{"translate":"mgs.you_have_been_revived","color":"green"}]
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"selector":"@s","color":"green"},[{"text":" ","color":"gray"}, {"translate":"mgs.has_been_revived"}]]

