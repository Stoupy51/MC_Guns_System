
#> mgs:v5.1.0/actionbar/build_fire_mode_indicator
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.1.0/actionbar/show
#

data modify storage mgs:temp actionbar set value {list:[]}

data modify storage mgs:temp actionbar.list append value {"text":"","color":"#c24a17"}
data modify storage mgs:temp actionbar.list append value {"text":"[ ","color":"#c77e36"}

execute store result score #has_auto mgs.data if data storage mgs:gun all.stats.can_auto
execute store result score #has_burst mgs.data if data storage mgs:gun all.stats.can_burst

# auto and burst: [S | B | A]; auto only: [S | A]; burst only: [S | B]; neither: [S].

execute if data storage mgs:gun all.stats{fire_mode:"semi"} run data modify storage mgs:temp actionbar.list append value {"text":"S","color":"yellow","bold":true}
execute unless data storage mgs:gun all.stats{fire_mode:"semi"} run data modify storage mgs:temp actionbar.list append value {"text":"S"}

execute if score #has_burst mgs.data matches 1 run data modify storage mgs:temp actionbar.list append value {"text":" | "}

execute if score #has_burst mgs.data matches 1 if data storage mgs:gun all.stats{fire_mode:"burst"} run data modify storage mgs:temp actionbar.list append value {"text":"B","color":"yellow"}
execute if score #has_burst mgs.data matches 1 unless data storage mgs:gun all.stats{fire_mode:"burst"} run data modify storage mgs:temp actionbar.list append value {"text":"B"}

execute if score #has_auto mgs.data matches 1 run data modify storage mgs:temp actionbar.list append value {"text":" | "}

execute if score #has_auto mgs.data matches 1 if data storage mgs:gun all.stats{fire_mode:"auto"} run data modify storage mgs:temp actionbar.list append value {"text":"A","color":"yellow","bold":true}
execute if score #has_auto mgs.data matches 1 unless data storage mgs:gun all.stats{fire_mode:"auto"} run data modify storage mgs:temp actionbar.list append value {"text":"A"}

data modify storage mgs:temp actionbar.list append value {"text":" ] ","color":"#c77e36"}

