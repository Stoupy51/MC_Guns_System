
#> mgs:v5.1.0/zombies/wunderfizz/on_hover
#
# @executed	as @n[tag=mgs.wf_new]
#
# @within	mgs:v5.1.0/zombies/wunderfizz/setup_iter {run:"function mgs:v5.1.0/zombies/wunderfizz/on_hover",executor:"source"} [ as @n[tag=mgs.wf_new] ]
#

# If this player's perk is ready to collect here, prompt the pick-up (with the perk name) instead of the cost
execute at @n[tag=bs.interaction.target] if entity @n[type=item_display,tag=mgs.wunderfizz_orb,distance=..3,scores={mgs.zb.wf.anim=..0}] if score @s mgs.zb.wf_pid = @n[type=item_display,tag=mgs.wunderfizz_orb,distance=..3] mgs.zb.wf.buyer run return run function mgs:v5.1.0/zombies/wunderfizz/hover_result

execute store result score #wf_price mgs.data run scoreboard players get @n[tag=bs.interaction.target] mgs.zb.wf.price
data modify storage smithed.actionbar:input message set value {json:[[{"text":"🎰 ","color":"gold"}, {"translate":"mgs.der_wunderfizz"}],[{"text":" - ","color":"gray"}, {"translate":"mgs.cost_2"}],{"score":{"name":"#wf_price","objective":"mgs.data"},"color":"yellow"},[{"text":" ","color":"gray"}, {"translate":"mgs.points_random_perk"}]],priority:"conditional",freeze:5}
function #smithed.actionbar:message

