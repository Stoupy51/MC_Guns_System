
#> mgs:v5.1.0/zombies/round_complete
#
# @within	mgs:v5.1.0/zombies/game_tick
#			mgs:zombies/recover
#

# Guard: prevent re-triggering every tick
scoreboard players set #zb_to_spawn mgs.data -1

# Dog rounds always end with a Max Ammo. Normally the last hound already dropped it as it died;
# this only covers the cases where that path didn't fire.
execute if score #zb_dog_round mgs.data matches 1 if score #zb_dog_ammo_done mgs.data matches 0 run function mgs:v5.1.0/zombies/dog_max_ammo_fallback

# Signal round end
function #mgs:zombies/on_round_end

# Announce
execute store result score #completed_round mgs.data run data get storage mgs:zombies game.round
tellraw @a ["",{"text":"","color":"dark_green","bold":true},"🧟 ",{"translate":"mgs.round","color":"green"},{"score":{"name":"#completed_round","objective":"mgs.data"},"color":"gold","bold":true},{"translate":"mgs.complete_next_round_in_5_seconds","color":"green"}]
execute as @a[scores={mgs.zb.in_game=1}] at @s run playsound mgs:zombies/round_end_generic ambient @s ~ ~ ~ 0.3 1.0

# Schedule next round after 5 seconds
schedule function mgs:v5.1.0/zombies/start_round 5s

# Respawn all bled-out (spectator) players for the next round
function mgs:v5.1.0/zombies/revive/round_respawn

