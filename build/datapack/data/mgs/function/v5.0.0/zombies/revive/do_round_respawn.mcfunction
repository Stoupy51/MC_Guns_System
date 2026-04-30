
#> mgs:v5.0.0/zombies/revive/do_round_respawn
#
# @executed	as @a[scores={mgs.zb.in_game=1},gamemode=spectator]
#
# @within	mgs:v5.0.0/zombies/revive/round_respawn [ as @a[scores={mgs.zb.in_game=1},gamemode=spectator] ]
#

# Restore adventure mode
spectate @s
gamemode adventure @s

# Teleport to random player spawn
function mgs:v5.0.0/zombies/respawn_tp

# Re-apply saturation and heal
effect give @s minecraft:saturation infinite 255 true
effect give @s minecraft:instant_health 1 255 true

# Restore max health (check for Juggernog perk)
execute if score @s mgs.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 40
execute unless score @s mgs.zb.perk.juggernog matches 1.. run attribute @s minecraft:max_health base set 20

# Re-give starting weapon on respawn
function mgs:v5.0.0/zombies/inventory/give_respawn_loadout

# Announce
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"selector":"@s","color":"green"},[{"text":" ","color":"gray"}, {"translate":"mgs.has_respawned"}]]

