
#> mgs:v5.1.0/actionbar/build_fire_mode_indicator
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/actionbar/show
#

data modify storage mgs:temp actionbar set value {list:[]}

data modify storage mgs:temp actionbar.list append value {"text":"","color":"#c24a17"}
data modify storage mgs:temp actionbar.list append value {"text":"[ ","color":"#c77e36"}
scoreboard players set #ab_modes mgs.data 0

execute store result score #has_mode mgs.data if data storage mgs:gun all.stats.fire_modes[{name:"pump"}]
execute if data storage mgs:gun all.stats{fire_mode:"pump"} run scoreboard players set #has_mode mgs.data 1
execute if score #has_mode mgs.data matches 1 if score #ab_modes mgs.data matches 1.. run data modify storage mgs:temp actionbar.list append value {"text":" | "}
execute if score #has_mode mgs.data matches 1 if data storage mgs:gun all.stats{fire_mode:"pump"} run data modify storage mgs:temp actionbar.list append value {"text":"P","color":"yellow","bold":true}
execute if score #has_mode mgs.data matches 1 unless data storage mgs:gun all.stats{fire_mode:"pump"} run data modify storage mgs:temp actionbar.list append value {"text":"P"}
execute if score #has_mode mgs.data matches 1 run scoreboard players add #ab_modes mgs.data 1

execute store result score #has_mode mgs.data if data storage mgs:gun all.stats.fire_modes[{name:"semi"}]
execute if data storage mgs:gun all.stats{fire_mode:"semi"} run scoreboard players set #has_mode mgs.data 1
execute if score #has_mode mgs.data matches 1 if score #ab_modes mgs.data matches 1.. run data modify storage mgs:temp actionbar.list append value {"text":" | "}
execute if score #has_mode mgs.data matches 1 if data storage mgs:gun all.stats{fire_mode:"semi"} run data modify storage mgs:temp actionbar.list append value {"text":"S","color":"yellow","bold":true}
execute if score #has_mode mgs.data matches 1 unless data storage mgs:gun all.stats{fire_mode:"semi"} run data modify storage mgs:temp actionbar.list append value {"text":"S"}
execute if score #has_mode mgs.data matches 1 run scoreboard players add #ab_modes mgs.data 1

execute store result score #has_mode mgs.data if data storage mgs:gun all.stats.fire_modes[{name:"burst"}]
execute if data storage mgs:gun all.stats{fire_mode:"burst"} run scoreboard players set #has_mode mgs.data 1
execute if score #has_mode mgs.data matches 1 if score #ab_modes mgs.data matches 1.. run data modify storage mgs:temp actionbar.list append value {"text":" | "}
execute if score #has_mode mgs.data matches 1 if data storage mgs:gun all.stats{fire_mode:"burst"} run data modify storage mgs:temp actionbar.list append value {"text":"B","color":"yellow","bold":true}
execute if score #has_mode mgs.data matches 1 unless data storage mgs:gun all.stats{fire_mode:"burst"} run data modify storage mgs:temp actionbar.list append value {"text":"B"}
execute if score #has_mode mgs.data matches 1 run scoreboard players add #ab_modes mgs.data 1

execute store result score #has_mode mgs.data if data storage mgs:gun all.stats.fire_modes[{name:"auto"}]
execute if data storage mgs:gun all.stats{fire_mode:"auto"} run scoreboard players set #has_mode mgs.data 1
execute if score #has_mode mgs.data matches 1 if score #ab_modes mgs.data matches 1.. run data modify storage mgs:temp actionbar.list append value {"text":" | "}
execute if score #has_mode mgs.data matches 1 if data storage mgs:gun all.stats{fire_mode:"auto"} run data modify storage mgs:temp actionbar.list append value {"text":"A","color":"yellow","bold":true}
execute if score #has_mode mgs.data matches 1 unless data storage mgs:gun all.stats{fire_mode:"auto"} run data modify storage mgs:temp actionbar.list append value {"text":"A"}
execute if score #has_mode mgs.data matches 1 run scoreboard players add #ab_modes mgs.data 1

data modify storage mgs:temp actionbar.list append value {"text":" ] ","color":"#c77e36"}

