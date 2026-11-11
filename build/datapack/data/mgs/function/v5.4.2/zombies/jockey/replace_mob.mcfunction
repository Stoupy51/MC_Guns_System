
#> mgs:v5.4.2/zombies/jockey/replace_mob
#
# @within	mgs:v5.4.2/dialog/close_then
#			mgs:v5.4.2/zombies/do_spawn
#

execute unless data storage mgs:temp _mob{entity:"zombie"} unless data storage mgs:temp _mob{entity:"minecraft:zombie"} run return 0
execute if data storage mgs:temp _mob.nbt run return 0
execute if data storage mgs:temp _mob.riders[0] run return 0
execute if data storage mgs:temp _mob.gun run return 0
data modify storage mgs:temp _mob merge value {entity:"minecraft:chicken",jockey:"mount",nbt:{IsChickenJockey:1b},riders:[{entity:"minecraft:zombie",jockey:"rider",nbt:{IsBaby:1b,active_effects:[{id:"minecraft:invisibility",amplifier:0b,duration:-1,show_particles:0b,show_icon:0b}]}}]}

