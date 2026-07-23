
#> mgs:v5.1.0/zombies/wunderfizz/hover_result
#
# @executed	at @n[tag=bs.interaction.target]
#
# @within	mgs:v5.1.0/zombies/wunderfizz/on_hover [ at @n[tag=bs.interaction.target] ]
#

scoreboard players operation #wf_pick mgs.data = @n[type=item_display,tag=mgs.wunderfizz_orb,distance=..3] mgs.zb.wf.perk
execute if score #wf_pick mgs.data matches 0 run data modify storage smithed.actionbar:input message set value {json:[{"text":"🎰 ","color":"gold"},{"translate":"mgs.pick_up","color":"green"},{"translate":"mgs.juggernog","color":"red","bold":true}],priority:"conditional",freeze:5}
execute if score #wf_pick mgs.data matches 1 run data modify storage smithed.actionbar:input message set value {json:[{"text":"🎰 ","color":"gold"},{"translate":"mgs.pick_up","color":"green"},{"translate":"mgs.speed_cola","color":"green","bold":true}],priority:"conditional",freeze:5}
execute if score #wf_pick mgs.data matches 2 run data modify storage smithed.actionbar:input message set value {json:[{"text":"🎰 ","color":"gold"},{"translate":"mgs.pick_up","color":"green"},{"translate":"mgs.double_tap","color":"yellow","bold":true}],priority:"conditional",freeze:5}
execute if score #wf_pick mgs.data matches 3 run data modify storage smithed.actionbar:input message set value {json:[{"text":"🎰 ","color":"gold"},{"translate":"mgs.pick_up","color":"green"},{"translate":"mgs.quick_revive","color":"aqua","bold":true}],priority:"conditional",freeze:5}
execute if score #wf_pick mgs.data matches 4 run data modify storage smithed.actionbar:input message set value {json:[{"text":"🎰 ","color":"gold"},{"translate":"mgs.pick_up","color":"green"},{"translate":"mgs.mule_kick","color":"dark_green","bold":true}],priority:"conditional",freeze:5}
execute if score #wf_pick mgs.data matches 5 run data modify storage smithed.actionbar:input message set value {json:[{"text":"🎰 ","color":"gold"},{"translate":"mgs.pick_up","color":"green"},{"translate":"mgs.stamin_up","color":"gold","bold":true}],priority:"conditional",freeze:5}
execute if score #wf_pick mgs.data matches 6 run data modify storage smithed.actionbar:input message set value {json:[{"text":"🎰 ","color":"gold"},{"translate":"mgs.pick_up","color":"green"},{"translate":"mgs.phd_flopper","color":"dark_purple","bold":true}],priority:"conditional",freeze:5}
execute if score #wf_pick mgs.data matches 7 run data modify storage smithed.actionbar:input message set value {json:[{"text":"🎰 ","color":"gold"},{"translate":"mgs.pick_up","color":"green"},{"translate":"mgs.deadshot_daiquiri","color":"dark_green","bold":true}],priority:"conditional",freeze:5}
execute if score #wf_pick mgs.data matches 8 run data modify storage smithed.actionbar:input message set value {json:[{"text":"🎰 ","color":"gold"},{"translate":"mgs.pick_up","color":"green"},{"translate":"mgs.timeslip","color":"light_purple","bold":true}],priority:"conditional",freeze:5}
execute if score #wf_pick mgs.data matches 9 run data modify storage smithed.actionbar:input message set value {json:[{"text":"🎰 ","color":"gold"},{"translate":"mgs.pick_up","color":"green"},{"translate":"mgs.electric_cherry","color":"blue","bold":true}],priority:"conditional",freeze:5}
execute if score #wf_pick mgs.data matches 10 run data modify storage smithed.actionbar:input message set value {json:[{"text":"🎰 ","color":"gold"},{"translate":"mgs.pick_up","color":"green"},{"translate":"mgs.tombstone","color":"gold","bold":true}],priority:"conditional",freeze:5}
execute if score #wf_pick mgs.data matches 11 run data modify storage smithed.actionbar:input message set value {json:[{"text":"🎰 ","color":"gold"},{"translate":"mgs.pick_up","color":"green"},{"translate":"mgs.whos_who","color":"dark_aqua","bold":true}],priority:"conditional",freeze:5}
execute if score #wf_pick mgs.data matches 12 run data modify storage smithed.actionbar:input message set value {json:[{"text":"🎰 ","color":"gold"},{"translate":"mgs.pick_up","color":"green"},{"translate":"mgs.dying_wish","color":"blue","bold":true}],priority:"conditional",freeze:5}
execute if score #wf_pick mgs.data matches 13 run data modify storage smithed.actionbar:input message set value {json:[{"text":"🎰 ","color":"gold"},{"translate":"mgs.pick_up","color":"green"},{"translate":"mgs.widows_wine","color":"dark_red","bold":true}],priority:"conditional",freeze:5}
function #smithed.actionbar:message

