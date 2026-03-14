
#> mgs:v5.0.0/zombies/perks/trigger_coward
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/perks/check_coward
#

# Teleport to a player spawn point
function mgs:v5.0.0/zombies/respawn_tp

# Set cooldown (1 round)
scoreboard players set @s mgs.zb.ability_cd 1

# Effects
effect give @s speed 5 1 true
effect give @s regeneration 5 1 true

# Announce
title @s actionbar [[{"text":"🏃 ","color":"yellow"}, {"translate":"mgs.coward_activated_teleported_to_safety"}]]

