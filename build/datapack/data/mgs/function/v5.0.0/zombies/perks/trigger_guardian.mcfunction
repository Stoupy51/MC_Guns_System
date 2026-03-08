
#> mgs:v5.0.0/zombies/perks/trigger_guardian
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/perks/check_guardian [ at @s ]
#

# Summon an Iron Golem ally near the player
summon minecraft:iron_golem ~ ~ ~ {Tags:["mgs.guardian_golem","mgs.gm_entity"],PlayerCreated:0b,CustomName:'"\u00a72Guardian"'}

# Set cooldown (1 round)
scoreboard players set @s mgs.zb.ability_cd 1

# Announce
title @s actionbar [{"translate": "mgs.guardian_activated_iron_golem_summoned","color":"green"}]

