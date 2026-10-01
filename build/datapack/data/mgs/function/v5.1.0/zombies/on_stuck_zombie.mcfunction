
#> mgs:v5.1.0/zombies/on_stuck_zombie
#
# @executed	as @e[tag=...,limit=24,sort=random] & at @s
#
# @within	mgs:v5.1.0/zombies/stuck_zombie_check
#			mgs:v5.1.0/zombies/escort/give_up
#

# Not for dogs: the escort freezes its passenger with an NBT write, which resets a wolf's MAX_HEALTH base to 8
# (TamableAnimal.setTame), and dogs outrun the trader anyway.
execute unless entity @s[tag=mgs.zb_dog] unless entity @s[tag=mgs.zb_escort_failed] if score #zb_escort_count mgs.data matches ..15 run return run function mgs:v5.1.0/zombies/escort/start


# Run as the stuck zombie: move it to a spawn near a player instead of killing it, back onto walkable ground.

# Dogs use their own markers: a zombie spawn may sit where only walkers belong, or outside the play bounds.
execute unless entity @s[tag=mgs.zb_dog] run function mgs:v5.1.0/zombies/tag_spawns_near_players
execute if entity @s[tag=mgs.zb_dog] run function mgs:v5.1.0/zombies/tag_special_spawns_near_players

# Never the spawn it last used, unless it is the only candidate.
scoreboard players operation #zb_last_sid mgs.data = @s mgs.zb.spawn.sid
execute as @e[tag=mgs.zb_near] if score @s mgs.zb.spawn.sid = #zb_last_sid mgs.data run tag @s add mgs.zb_near_prev
execute store result score #zb_near_alt mgs.data if entity @e[tag=mgs.zb_near,tag=!mgs.zb_near_prev]
execute if score #zb_near_alt mgs.data matches 1.. run tag @e[tag=mgs.zb_near_prev] remove mgs.zb_near
tag @e[tag=mgs.zb_near_prev] remove mgs.zb_near_prev

# The spawn nearest the player, not the enemy: from the enemy, a stranded one bounced between the same two far spawns.
execute if score #zb_near_found mgs.data matches 1.. at @p[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator] run function mgs:v5.1.0/zombies/rescue_tp
# Everyone downed: measure from the enemy instead.
execute if score #zb_near_found mgs.data matches 1.. unless entity @p[scores={mgs.zb.in_game=1,mgs.zb.downed=0},gamemode=!spectator] run function mgs:v5.1.0/zombies/rescue_tp
execute if score #zb_near_found mgs.data matches 1.. run tag @s add mgs.zb_rescued
tag @e[tag=mgs.zb_near] remove mgs.zb_near

# After a teleport a past escort failure no longer applies, so a later stuck timeout gets a trader again.
execute if score #zb_near_found mgs.data matches 1.. run tag @s remove mgs.zb_escort_failed

# Fresh stuck window from the new position.
scoreboard players set @s mgs.zb.stuck_dist 4
execute store result score @s mgs.zb.stuck_x run data get entity @s Pos[0]
execute store result score @s mgs.zb.stuck_z run data get entity @s Pos[2]
scoreboard players operation @s mgs.zb.stuck_ticks = #total_tick mgs.data

