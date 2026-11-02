
#> mgs:v5.3.0/maps/editor/summon_all
#
# @within	mgs:v5.3.0/maps/editor/enter 20t replace [ scheduled ]
#

execute unless entity @a[tag=mgs.map_editor] run return 0
scoreboard players set #ed_unloaded mgs.data 0
execute as @a[tag=mgs.map_editor,limit=1] run function mgs:v5.3.0/maps/editor/summon_in with storage mgs:temp map_edit.force
data remove storage mgs:temp map_edit.loading
execute if score #ed_unloaded mgs.data matches 1.. run data modify storage mgs:temp map_edit.unsafe set value 1b
execute if score #ed_unloaded mgs.data matches 1.. run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"score":{"name":"#ed_unloaded","objective":"mgs.data"},"color":"white"},{"translate":"mgs.elements_lie_more_than_112_blocks_from_the_base_and_could_not_be","fallback":" elements lie more than 112 blocks from the base and could not be loaded. Saving is off for this session, so they are not lost.","color":"red"}]

