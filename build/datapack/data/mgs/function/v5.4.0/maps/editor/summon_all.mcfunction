
#> mgs:v5.4.0/maps/editor/summon_all
#
# @within	mgs:v5.4.0/dialog/close_then
#			mgs:v5.4.0/maps/editor/enter 40t replace [ scheduled ]
#

execute unless entity @a[tag=mgs.map_editor] run return 0
scoreboard players set #ed_unloaded mgs.data 0
scoreboard players set #ed_retry mgs.data 0
data modify storage mgs:temp map_edit.missed set value []
data modify storage mgs:temp map_edit.kept set value []
execute as @a[tag=mgs.map_editor,limit=1] run function mgs:v5.4.0/maps/editor/summon_in with storage mgs:temp map_edit.force
data remove storage mgs:temp map_edit.loading
function mgs:v5.4.0/maps/editor/summon_report

