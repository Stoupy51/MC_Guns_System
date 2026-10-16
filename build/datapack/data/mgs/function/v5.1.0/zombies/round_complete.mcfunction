
#> mgs:v5.1.0/zombies/round_complete
#
# @within	mgs:v5.1.0/zombies/game_tick
#			mgs:zombies/recover
#

# -1 stops this from firing again every tick.
scoreboard players set #zb_to_spawn mgs.data -1

# No Max Ammo fallback here: it drops at the last hound's body (dog_death), never at a player.

function #mgs:zombies/on_round_end

# Split because only the roster earned the survival XP; the signal above set #xp_gain.
execute store result score #completed_round mgs.data run data get storage mgs:zombies game.round
tellraw @a[scores={mgs.zb.in_game=1}] ["",{"text":"","color":"dark_green","bold":true},"🧟 ",{"translate":"mgs.round_2","color":"green"},{"score":{"name":"#completed_round","objective":"mgs.data"},"color":"gold","bold":true},{"translate":"mgs.complete_next_round_in_5_seconds","color":"green"},[" ",{"text":"+","color":"gold"},{"score":{"name":"#xp_gain","objective":"mgs.data"},"color":"gold"},{"text":" XP","color":"gold"}]]
execute as @a[scores={mgs.zb.in_game=1}] at @s run playsound mgs:zombies/round_end_generic ambient @s ~ ~ ~ 0.3 1.0

# Counted down in game_tick, so a freeze or a suspension holds it.
scoreboard players set #zb_next_round mgs.data 100

function mgs:v5.1.0/zombies/revive/round_respawn

