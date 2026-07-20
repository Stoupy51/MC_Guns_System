
#> mgs:v5.1.0/zombies/wallbuys/render_hover
#
# @executed	as @n[tag=mgs.wb_new]
#
# @within	mgs:v5.1.0/zombies/wallbuys/on_hover
#			mgs:v5.1.0/zombies/wallbuys/hover_knife
#			mgs:v5.1.0/zombies/wallbuys/hover_lethal
#			mgs:v5.1.0/zombies/wallbuys/hover_tactical
#

data modify storage smithed.actionbar:input message set value {json:[{"text":"🔫 ","color":"gold"},{"storage":"mgs:temp","nbt":"_wb_display_name","color":"yellow","interpret":true},[{"text":" - ","color":"gray"}, {"translate":"mgs.cost_2"}],{"score":{"name":"#wb_price","objective":"mgs.data"},"color":"yellow"},[{"text":" ","color":"gray"}, {"translate":"mgs.points_2"}],{"storage":"mgs:temp","nbt":"_wb_price_suffix","color":"gray","interpret":true}],priority:"conditional",freeze:5}
function #smithed.actionbar:message

