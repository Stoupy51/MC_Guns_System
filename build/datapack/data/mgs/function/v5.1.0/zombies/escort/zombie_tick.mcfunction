
#> mgs:v5.1.0/zombies/escort/zombie_tick
#
# @executed	as @e[tag=mgs.zb_escorted] & at @s
#
# @within	mgs:v5.1.0/zombies/game_tick [ as @e[tag=mgs.zb_escorted] & at @s ]
#

# Trader killed externally: unfreeze, normal stuck detection takes over.
execute unless entity @n[type=minecraft:wandering_trader,tag=mgs.zb_escort,distance=..8] run return run function mgs:v5.1.0/zombies/escort/detach

# Same position and rotation as the trader: always path-valid, and pushOtherTeams stops the overlap from pushing it.
execute at @n[type=minecraft:wandering_trader,tag=mgs.zb_escort,distance=..8] run tp @s ~ ~ ~ ~ ~

# Monkey-bomb lure: once every monkey is gone the escort reverts to a player escort;
# otherwise ride to the monkey and ignore the player releases below.
execute if entity @n[type=minecraft:wandering_trader,tag=mgs.zb_escort,tag=mgs.zb_escort_monkey,distance=..8] unless entity @e[tag=mgs.monkey_bomb] run tag @n[type=minecraft:wandering_trader,tag=mgs.zb_escort,distance=..8] remove mgs.zb_escort_monkey
execute if entity @n[type=minecraft:wandering_trader,tag=mgs.zb_escort,tag=mgs.zb_escort_monkey,distance=..8] run return run function mgs:v5.1.0/zombies/escort/monkey_ride

# Walk-to spawn: skip the player releases, which would fire at once (spawns are within 32 blocks of a player)
# and drop the zombie back at its spawn.
execute if entity @n[type=minecraft:wandering_trader,tag=mgs.zb_escort,tag=mgs.zb_escort_walk,distance=..8] run return run function mgs:v5.1.0/zombies/escort/walk_ride

# PaP-room lure: release at the theatre centre, where no player is near to trigger the releases below.
execute if score #zb_lure mgs.data matches 1 if entity @e[tag=mgs.lure_center,distance=..8] run return run function mgs:v5.1.0/zombies/escort/release

# Point-blank: release without line of sight, which corner and slab geometry can fail forever.
execute if entity @p[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,distance=..6] run return run function mgs:v5.1.0/zombies/escort/release

# Release once a player is close and visible: a player above a floor is close but unreachable.
scoreboard players set #zb_esc_see mgs.data 0
execute positioned as @p[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,distance=..10] store result score #zb_esc_see mgs.data run function #bs.view:can_see_ata {with:{}}
execute if score #zb_esc_see mgs.data matches 1 run return run function mgs:v5.1.0/zombies/escort/release

# Shared with the monkey ride.
function mgs:v5.1.0/zombies/escort/escort_tail

