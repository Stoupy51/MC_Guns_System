
#> mgs:v5.4.0/maps/editor/summon_report
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/maps/editor/summon_all
#			mgs:v5.4.0/maps/editor/summon_retry
#

execute if score #ed_unloaded mgs.data matches 0 run data remove storage mgs:temp map_edit.unsafe
execute if score #ed_unloaded mgs.data matches 1.. run data modify storage mgs:temp map_edit.unsafe set value 1b
execute if score #ed_unloaded mgs.data matches 1.. run tellraw @a[tag=mgs.map_editor] [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"score":{"name":"#ed_unloaded","objective":"mgs.data"},"color":"white"},{"translate":"mgs.elements_lie_more_than_112_blocks_from_the_base_and_could_not_be","fallback":" elements lie more than 112 blocks from the base and could not be loaded. Saving is off for this session, so they are not lost. ","color":"red"},[{"text": "[", "color": "gold", "click_event": {"action": "run_command", "command": "/function mgs:v5.4.0/maps/editor/summon_retry"}, "hover_event": {"action": "show_text", "value": "Load them again, once the chunks are loaded"}}, "Retry", "]"]]

