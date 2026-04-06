
#> mgs:v5.0.0/zombies/revive/do_round_respawn
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/revive/round_respawn [ at @s ]
#

# Stop spectating
spectate @s

# Teleport to random player spawn
function mgs:v5.0.0/zombies/respawn_tp

# Re-apply saturation
effect give @s saturation infinite 255 true

# Switch back to adventure
gamemode adventure @s

# Restore max health (check for Juggernog perk)
execute if score @s mgs.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 40
execute unless score @s mgs.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 20
effect give @s instant_health 1 255 true

# Re-give starting weapon on respawn
function mgs:v5.0.0/zombies/inventory/give_respawn_loadout

# Announce
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"selector":"@s","color":"green"},[{"text":" ","color":"gray"}, {"translate":"mgs.has_respawned"}]]

