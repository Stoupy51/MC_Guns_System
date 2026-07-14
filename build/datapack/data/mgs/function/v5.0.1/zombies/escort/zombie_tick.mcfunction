
#> mgs:v5.0.1/zombies/escort/zombie_tick
#
# @executed	as @e[tag=mgs.zb_escorted] & at @s
#
# @within	mgs:v5.0.1/zombies/game_tick [ as @e[tag=mgs.zb_escorted] & at @s ]
#

# Trader gone (killed externally)? Unfreeze; normal stuck detection takes over again
execute unless entity @n[type=minecraft:wandering_trader,tag=mgs.zb_escort,distance=..8] run return run function mgs:v5.0.1/zombies/escort/detach

# Glue the zombie exactly onto the trader (same position AND rotation): always a path-valid
# spot, and the horde's pushOtherTeams collision rule keeps the overlap from pushing the trader
execute at @n[type=minecraft:wandering_trader,tag=mgs.zb_escort,distance=..8] run tp @s ~ ~ ~ ~ ~

# Point-blank → release NOW, no line-of-sight needed: the visibility check below aims at the
# player's feet and corner/slab geometry can fail it forever while the taxi orbits the player
execute if entity @p[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,distance=..6] run return run function mgs:v5.0.1/zombies/escort/release

# Hand off to vanilla AI once a player is close AND in the zombie's line of sight: a player
# 3 blocks above through a floor is "close" but the zombie still can't path there — keep riding
scoreboard players set #zb_esc_see mgs.data 0
execute positioned as @p[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,distance=..10] store result score #zb_esc_see mgs.data run function #bs.view:can_see_ata {with:{}}
execute if score #zb_esc_see mgs.data matches 1 run return run function mgs:v5.0.1/zombies/escort/release

# TTL countdown; the trader could not reach anyone in time -> teleport-rescue fallback
scoreboard players remove @s mgs.zb.escort_ttl 1
execute if score @s mgs.zb.escort_ttl matches ..0 run return run function mgs:v5.0.1/zombies/escort/give_up

# Re-aim the trader at the nearest alive player every second
scoreboard players operation #zb_esc_mod mgs.data = @s mgs.zb.escort_ttl
scoreboard players operation #zb_esc_mod mgs.data %= #20 mgs.data
execute if score #zb_esc_mod mgs.data matches 0 as @n[type=minecraft:wandering_trader,tag=mgs.zb_escort,distance=..8] at @s run function mgs:v5.0.1/zombies/escort/retarget

# Watchdog every second: a trader that can't move is caught in 5s, not 45s
execute if score #zb_esc_mod mgs.data matches 0 run function mgs:v5.0.1/zombies/escort/watchdog

