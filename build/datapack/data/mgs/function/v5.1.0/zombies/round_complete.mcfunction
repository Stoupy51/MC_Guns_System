
#> mgs:v5.1.0/zombies/round_complete
#
# @within	mgs:v5.1.0/zombies/game_tick
#			mgs:zombies/recover
#

# Guard: prevent re-triggering every tick
scoreboard players set #zb_to_spawn mgs.data -1

# NOTE: no Max Ammo fallback here on purpose. The drop belongs at the last hound's body, so it is
# only ever spawned by dog_death. A round that ends without one (Nuke, death watch missed) simply
# doesn't get it — better than granting it at a player, which reads as an automatic refill.

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

