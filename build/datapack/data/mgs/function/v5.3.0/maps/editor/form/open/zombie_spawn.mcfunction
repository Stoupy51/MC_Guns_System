
#> mgs:v5.3.0/maps/editor/form/open/zombie_spawn
#
# @executed	at @s & as @n[tag=mgs.map_element,distance=..10]
#
# @within	mgs:v5.3.0/maps/editor/show_element_config
#			mgs:v5.3.0/maps/editor/form/reopen
#

function mgs:v5.3.0/maps/editor/form/target
data modify storage mgs:temp dialog set value {"type": "minecraft:multi_action", "title": {"translate": "mgs.zombie_spawn","fallback": "Zombie Spawn", "color": "gold", "bold": true}, "body": [{"type": "minecraft:plain_message", "width": 400, "contents": "What spawns here, as SNBT: {entity:\"zombie\", gun:..., nbt:{...}, riders:[...]}\nentity: any entity id. nbt: merged into it, but the round still sets its health and speed.\ngun: absent = the round decides, false = never armed, {id:\"ak47\", level:2} = always armed\n(no id = a random non-explosive gun, no level = 1 with an id, else the round's tier).\nriders: mobs of the same format riding it; the whole stack counts once in the round.\nA plain zombie (no nbt, riders or gun) can still become a Zonweeb special type."}, {"type": "minecraft:plain_message", "width": 400, "contents": "Activation box: only spawns while a player stands in it, relative to the spawn. Empty: always."}], "inputs": [{"type": "minecraft:number_range", "key": "group_id", "label": "Group, opened by doors", "start": 0, "end": 64, "step": 1, "width": 300}, {"type": "minecraft:number_range", "key": "min_round", "label": "From round (0: the first)", "start": 0, "end": 100, "step": 1, "width": 300}, {"type": "minecraft:number_range", "key": "max_round", "label": "Until round (0: no end)", "start": 0, "end": 100, "step": 1, "width": 300}, {"type": "minecraft:single_option", "key": "arrival", "label": "Arrival", "width": 300, "options": [{"id": "floor", "display": "Floor"}, {"id": "ceiling", "display": "Ceiling"}, {"id": "portal", "display": "Portal"}, {"id": "instant", "display": "Instant"}]}, {"type": "minecraft:number_range", "key": "rise_ticks", "label": "Rise from the floor or ceiling, in ticks", "start": 1, "end": 100, "step": 1, "width": 300}, {"type": "minecraft:boolean", "key": "power", "label": "Only once the power is on", "initial": false, "on_true": "1", "on_false": "0"}, {"type": "minecraft:text", "key": "mob", "label": "Mob (SNBT, empty for the default)", "initial": "", "max_length": 4096, "width": 400}, {"type": "minecraft:text", "key": "activation_box", "label": "Activation box: x, y, z, dx, dy, dz", "initial": "", "max_length": 128, "width": 300}, {"type": "minecraft:text", "key": "walk_to", "label": "Walk to: x, y, z", "initial": "", "max_length": 64, "width": 300}], "actions": [{"label": {"translate": "mgs.save","fallback": "Save", "color": "green"}, "action": {"type": "dynamic/run_command", "template": "/function mgs:v5.3.0/maps/editor/form/spawn_apply {group_id:$(group_id),min_round:$(min_round),max_round:$(max_round),arrival:\"$(arrival)\",rise_ticks:$(rise_ticks),power:$(power),mob:[$(mob)],activation_box:[$(activation_box)],walk_to:[$(walk_to)],then:\"\"}"}}, {"label": "📐 Save, then draw the box", "tooltip": "Right-click two opposite corners with the Coord Stick", "action": {"type": "dynamic/run_command", "template": "/function mgs:v5.3.0/maps/editor/form/spawn_apply {group_id:$(group_id),min_round:$(min_round),max_round:$(max_round),arrival:\"$(arrival)\",rise_ticks:$(rise_ticks),power:$(power),mob:[$(mob)],activation_box:[$(activation_box)],walk_to:[$(walk_to)],then:\"box\"}"}}], "columns": 2, "exit_action": {"label": {"translate": "mgs.cancel","fallback": "Cancel", "color": "gray"}}}
execute store result score #ed_v mgs.data run data get entity @s data.group_id
execute if score #ed_v mgs.data matches ..-1 run scoreboard players set #ed_v mgs.data 0
execute if score #ed_v mgs.data matches 65.. run scoreboard players set #ed_v mgs.data 64
execute store result storage mgs:temp dialog.inputs[0].initial float 1 run scoreboard players get #ed_v mgs.data
execute store result score #ed_v mgs.data run data get entity @s data.min_round
execute if score #ed_v mgs.data matches ..-1 run scoreboard players set #ed_v mgs.data 0
execute if score #ed_v mgs.data matches 101.. run scoreboard players set #ed_v mgs.data 100
execute store result storage mgs:temp dialog.inputs[1].initial float 1 run scoreboard players get #ed_v mgs.data
execute store result score #ed_v mgs.data run data get entity @s data.max_round
execute if score #ed_v mgs.data matches ..-1 run scoreboard players set #ed_v mgs.data 0
execute if score #ed_v mgs.data matches 101.. run scoreboard players set #ed_v mgs.data 100
execute store result storage mgs:temp dialog.inputs[2].initial float 1 run scoreboard players get #ed_v mgs.data
execute store result score #ed_v mgs.data run data get entity @s data.rise_ticks
execute if score #ed_v mgs.data matches ..0 run scoreboard players set #ed_v mgs.data 1
execute if score #ed_v mgs.data matches 101.. run scoreboard players set #ed_v mgs.data 100
execute store result storage mgs:temp dialog.inputs[4].initial float 1 run scoreboard players get #ed_v mgs.data
execute if data entity @s data{arrival:"floor"} run data modify storage mgs:temp dialog.inputs[3].options[0].initial set value 1b
execute if data entity @s data{arrival:"ceiling"} run data modify storage mgs:temp dialog.inputs[3].options[1].initial set value 1b
execute if data entity @s data{arrival:"portal"} run data modify storage mgs:temp dialog.inputs[3].options[2].initial set value 1b
execute if data entity @s data{arrival:"instant"} run data modify storage mgs:temp dialog.inputs[3].options[3].initial set value 1b
data modify storage mgs:temp dialog.inputs[5].initial set from entity @s data.power

# The mob as SNBT, the lists without their brackets. A text holding a single quote breaks the macro, so the field stays empty and says so.
execute store result score #ed_texts mgs.data run function mgs:v5.3.0/maps/editor/form/open/zombie_spawn_texts with entity @s data
execute if score #ed_texts mgs.data matches 0 run data modify storage mgs:temp dialog.body append value {type:"minecraft:plain_message",contents:{translate:"mgs.this_mob_holds_a_quote_the_form_cannot_show_saving_would_reset_i",fallback:"This mob holds a quote the form cannot show: saving would reset it.",color:"red"}}
execute as @a[tag=mgs.ed_form_user] run function mgs:v5.3.0/multiplayer/show_dialog with storage mgs:temp

