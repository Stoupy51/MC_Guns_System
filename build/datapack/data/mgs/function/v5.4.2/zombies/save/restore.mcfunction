
#> mgs:v5.4.2/zombies/save/restore
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/preload_complete
#

# start_round adds one: the next round is the one after the saved round.
data modify storage mgs:zombies game.round set from storage mgs:zombies_saves loading.round
execute store result score #zb_round mgs.data run data get storage mgs:zombies_saves loading.round
data modify storage mgs:temp _sv_missing set value []

execute if data storage mgs:zombies_saves loading.map{power:1b} run function mgs:v5.4.2/zombies/power/turn_on

# Opening a door unlocks its spawn groups. anim 1 removes the block without the break effect.
data modify storage mgs:temp _sv_iter set from storage mgs:zombies_saves loading.map.opened
execute if data storage mgs:temp _sv_iter[0] run function mgs:v5.4.2/zombies/save/restore_door_open

data modify storage mgs:temp _sv_iter set from storage mgs:zombies_saves loading.map.doors
execute if data storage mgs:temp _sv_iter[0] run function mgs:v5.4.2/zombies/save/restore_doors
data modify storage mgs:temp _sv_iter set from storage mgs:zombies_saves loading.map.barricades
execute if data storage mgs:temp _sv_iter[0] run function mgs:v5.4.2/zombies/save/restore_barricades
data modify storage mgs:temp _sv_iter set from storage mgs:zombies_saves loading.map.traps
execute if data storage mgs:temp _sv_iter[0] run function mgs:v5.4.2/zombies/save/restore_traps
execute as @e[type=minecraft:block_display,tag=mgs.barricade_display,scores={mgs.zb.barricade.state=1}] run function mgs:v5.4.2/zombies/barricades/break

execute store result score #mb_pulls mgs.data run data get storage mgs:zombies_saves loading.map.box_pulls
execute store result score #mb_dry_ray_gun mgs.data run data get storage mgs:zombies_saves loading.map.box_dry_ray_gun
execute if data storage mgs:zombies_saves loading.map.box run function mgs:v5.4.2/zombies/save/restore_box
execute store result score #wf_uses mgs.data run data get storage mgs:zombies_saves loading.map.wunderfizz_uses
execute if data storage mgs:zombies_saves loading.map.wunderfizz run function mgs:v5.4.2/zombies/save/restore_wunderfizz

execute as @a[scores={mgs.zb.in_game=1}] at @s run function mgs:v5.4.2/zombies/save/restore_player

execute if data storage mgs:temp _sv_missing[0] run tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.map_elements_of_the_save_missing_from_this_map_skipped","fallback":"Map elements of the save missing from this map, skipped: ","color":"gold"},{"storage":"mgs:temp","nbt":"_sv_missing[]","color":"yellow"}]
data remove storage mgs:temp _sv_missing
data remove storage mgs:temp _sv_iter
tellraw @a[scores={mgs.zb.in_game=1}] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.save_2","fallback":"Save ","color":"green"},{"storage":"mgs:zombies_saves","nbt":"loading.name","color":"gold"},[{"text":" ","color":"green"}, {"translate":"mgs.loaded_round","fallback":"loaded. Round "}],{"score":{"name":"#zb_round","objective":"mgs.data"},"color":"gold"},{"translate":"mgs.is_over_the_next_one_starts_in_10_seconds","fallback":" is over, the next one starts in 10 seconds!","color":"green"}]
data remove storage mgs:zombies_saves loading

