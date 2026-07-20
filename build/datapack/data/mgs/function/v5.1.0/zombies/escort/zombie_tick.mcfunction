
#> mgs:v5.1.0/zombies/escort/zombie_tick
#
# @executed	as @e[tag=mgs.zb_escorted] & at @s
#
# @within	mgs:v5.1.0/zombies/game_tick [ as @e[tag=mgs.zb_escorted] & at @s ]
#

# Trader gone (killed externally)? Unfreeze; normal stuck detection takes over again
execute unless entity @n[type=minecraft:wandering_trader,tag=mgs.zb_escort,distance=..8] run return run function mgs:v5.1.0/zombies/escort/detach

# Glue the zombie exactly onto the trader (same position AND rotation): always a path-valid
# spot, and the horde's pushOtherTeams collision rule keeps the overlap from pushing the trader
execute at @n[type=minecraft:wandering_trader,tag=mgs.zb_escort,distance=..8] run tp @s ~ ~ ~ ~ ~

# Monkey-bomb lure (monkey_bomb.py): while the trader is flagged, this escort pulls the zombie to
# a thrown monkey. Drop the flag once every monkey is gone (revert to a normal player escort);
# otherwise ride toward the monkey and release on arrival, ignoring the player releases below.
execute if entity @n[type=minecraft:wandering_trader,tag=mgs.zb_escort,tag=mgs.zb_escort_monkey,distance=..8] unless entity @e[tag=mgs.monkey_bomb] run tag @n[type=minecraft:wandering_trader,tag=mgs.zb_escort,distance=..8] remove mgs.zb_escort_monkey
execute if entity @n[type=minecraft:wandering_trader,tag=mgs.zb_escort,tag=mgs.zb_escort_monkey,distance=..8] run return run function mgs:v5.1.0/zombies/escort/monkey_ride

# PaP-room lure active: release once the zombie reaches the theatre centre (no player will be
# nearby there to trigger the player-based releases below)
execute if score #zb_lure mgs.data matches 1 if entity @e[tag=mgs.lure_center,distance=..8] run return run function mgs:v5.1.0/zombies/escort/release

# Point-blank → release NOW, no line-of-sight needed: the visibility check below aims at the
# player's feet and corner/slab geometry can fail it forever while the taxi orbits the player
execute if entity @p[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,distance=..6] run return run function mgs:v5.1.0/zombies/escort/release

# Hand off to vanilla AI once a player is close AND in the zombie's line of sight: a player
# 3 blocks above through a floor is "close" but the zombie still can't path there — keep riding
scoreboard players set #zb_esc_see mgs.data 0
execute positioned as @p[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator,distance=..10] store result score #zb_esc_see mgs.data run function #bs.view:can_see_ata {with:{}}
execute if score #zb_esc_see mgs.data matches 1 run return run function mgs:v5.1.0/zombies/escort/release

# Ride tail: TTL fallback + periodic retarget/watchdog (shared with the monkey-bomb ride below)
function mgs:v5.1.0/zombies/escort/escort_tail

