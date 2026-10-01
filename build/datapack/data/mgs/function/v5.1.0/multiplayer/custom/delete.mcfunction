
#> mgs:v5.1.0/multiplayer/custom/delete
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/player/config/process
#

# id = trigger - 40000
scoreboard players operation #loadout_id mgs.data = @s mgs.player.config
scoreboard players remove #loadout_id mgs.data 40000

data modify storage mgs:temp _del_src set from storage mgs:multiplayer custom_loadouts
data modify storage mgs:multiplayer custom_loadouts set value []

# Skips the entry matching both id and owner.
scoreboard players set #del_removed mgs.data 0
execute if data storage mgs:temp _del_src[0] run function mgs:v5.1.0/multiplayer/custom/delete_filter

# Reset the default and active class if they pointed at it.
scoreboard players operation #del_neg_id mgs.data = #loadout_id mgs.data
scoreboard players operation #del_neg_id mgs.data *= #minus_one mgs.data
execute if score #del_removed mgs.data matches 1 if score @s mgs.mp.default = #loadout_id mgs.data run scoreboard players set @s mgs.mp.default 0
execute if score #del_removed mgs.data matches 1 if score @s mgs.mp.class = #del_neg_id mgs.data run scoreboard players set @s mgs.mp.class 0

tellraw @s ["",[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],{"translate":"mgs.loadout_deleted","color":"red"}]

function mgs:v5.1.0/multiplayer/my_loadouts/browse

