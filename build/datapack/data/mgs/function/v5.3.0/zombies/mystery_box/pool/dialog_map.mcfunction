
#> mgs:v5.3.0/zombies/mystery_box/pool/dialog_map
#
# @executed	as the player & at current position
#
# @within	mgs:v5.3.0/zombies/mystery_box/pool/edit_map
#

data modify storage mgs:temp dialog set value {type:"minecraft:multi_action",title:{translate:"mgs.mystery_box_pool_of_the_map",fallback:"Mystery Box Pool of the Map",color:"light_purple",bold:true},body:[{type:"minecraft:plain_message",contents:{translate:"mgs.weight_of_each_weapon_in_the_box_0_leaves_it_out",fallback:"Weight of each weapon in the box, 0 leaves it out","color":"gray"}}],inputs:[],actions:[{label:{translate:"mgs.save",fallback:"Save",color:"green"},action:{type:"minecraft:dynamic/run_command",template:"function mgs:v5.3.0/zombies/mystery_box/pool/save_map {ak47:$(ak47),m16a4:$(m16a4),famas:$(famas),aug:$(aug),m4a1:$(m4a1),fnfal:$(fnfal),g3a3:$(g3a3),scar17:$(scar17),mp5:$(mp5),mp7:$(mp7),mac10:$(mac10),ppsh41:$(ppsh41),sten:$(sten),m249:$(m249),rpk:$(rpk),svd:$(svd),m82:$(m82),mosin:$(mosin),m24:$(m24),spas12:$(spas12),m500:$(m500),m590:$(m590),rpg7:$(rpg7),m1911:$(m1911),m9:$(m9),deagle:$(deagle),makarov:$(makarov),glock17:$(glock17),glock18:$(glock18),vz61:$(vz61),ray_gun:$(ray_gun),monkey_bomb:$(monkey_bomb)}"}}],columns:1,exit_action:{label:{translate:"gui.cancel"}}}
data modify storage mgs:temp dialog.inputs append value {type:"minecraft:number_range",key:"ak47",label:"AK-47",start:0,end:20,step:1,initial:0}
data modify storage mgs:temp dialog.inputs[-1].initial set from storage mgs:temp _mb_cur[{weapon_id:"ak47"}].weight
data modify storage mgs:temp dialog.inputs append value {type:"minecraft:number_range",key:"m16a4",label:"M16A4",start:0,end:20,step:1,initial:0}
data modify storage mgs:temp dialog.inputs[-1].initial set from storage mgs:temp _mb_cur[{weapon_id:"m16a4"}].weight
data modify storage mgs:temp dialog.inputs append value {type:"minecraft:number_range",key:"famas",label:"FAMAS",start:0,end:20,step:1,initial:0}
data modify storage mgs:temp dialog.inputs[-1].initial set from storage mgs:temp _mb_cur[{weapon_id:"famas"}].weight
data modify storage mgs:temp dialog.inputs append value {type:"minecraft:number_range",key:"aug",label:"AUG",start:0,end:20,step:1,initial:0}
data modify storage mgs:temp dialog.inputs[-1].initial set from storage mgs:temp _mb_cur[{weapon_id:"aug"}].weight
data modify storage mgs:temp dialog.inputs append value {type:"minecraft:number_range",key:"m4a1",label:"M4A1",start:0,end:20,step:1,initial:0}
data modify storage mgs:temp dialog.inputs[-1].initial set from storage mgs:temp _mb_cur[{weapon_id:"m4a1"}].weight
data modify storage mgs:temp dialog.inputs append value {type:"minecraft:number_range",key:"fnfal",label:"FN FAL",start:0,end:20,step:1,initial:0}
data modify storage mgs:temp dialog.inputs[-1].initial set from storage mgs:temp _mb_cur[{weapon_id:"fnfal"}].weight
data modify storage mgs:temp dialog.inputs append value {type:"minecraft:number_range",key:"g3a3",label:"G3A3",start:0,end:20,step:1,initial:0}
data modify storage mgs:temp dialog.inputs[-1].initial set from storage mgs:temp _mb_cur[{weapon_id:"g3a3"}].weight
data modify storage mgs:temp dialog.inputs append value {type:"minecraft:number_range",key:"scar17",label:"SCAR-17",start:0,end:20,step:1,initial:0}
data modify storage mgs:temp dialog.inputs[-1].initial set from storage mgs:temp _mb_cur[{weapon_id:"scar17"}].weight
data modify storage mgs:temp dialog.inputs append value {type:"minecraft:number_range",key:"mp5",label:"MP5",start:0,end:20,step:1,initial:0}
data modify storage mgs:temp dialog.inputs[-1].initial set from storage mgs:temp _mb_cur[{weapon_id:"mp5"}].weight
data modify storage mgs:temp dialog.inputs append value {type:"minecraft:number_range",key:"mp7",label:"MP7",start:0,end:20,step:1,initial:0}
data modify storage mgs:temp dialog.inputs[-1].initial set from storage mgs:temp _mb_cur[{weapon_id:"mp7"}].weight
data modify storage mgs:temp dialog.inputs append value {type:"minecraft:number_range",key:"mac10",label:"MAC-10",start:0,end:20,step:1,initial:0}
data modify storage mgs:temp dialog.inputs[-1].initial set from storage mgs:temp _mb_cur[{weapon_id:"mac10"}].weight
data modify storage mgs:temp dialog.inputs append value {type:"minecraft:number_range",key:"ppsh41",label:"PPSh-41",start:0,end:20,step:1,initial:0}
data modify storage mgs:temp dialog.inputs[-1].initial set from storage mgs:temp _mb_cur[{weapon_id:"ppsh41"}].weight
data modify storage mgs:temp dialog.inputs append value {type:"minecraft:number_range",key:"sten",label:"Sten",start:0,end:20,step:1,initial:0}
data modify storage mgs:temp dialog.inputs[-1].initial set from storage mgs:temp _mb_cur[{weapon_id:"sten"}].weight
data modify storage mgs:temp dialog.inputs append value {type:"minecraft:number_range",key:"m249",label:"M249",start:0,end:20,step:1,initial:0}
data modify storage mgs:temp dialog.inputs[-1].initial set from storage mgs:temp _mb_cur[{weapon_id:"m249"}].weight
data modify storage mgs:temp dialog.inputs append value {type:"minecraft:number_range",key:"rpk",label:"RPK",start:0,end:20,step:1,initial:0}
data modify storage mgs:temp dialog.inputs[-1].initial set from storage mgs:temp _mb_cur[{weapon_id:"rpk"}].weight
data modify storage mgs:temp dialog.inputs append value {type:"minecraft:number_range",key:"svd",label:"SVD",start:0,end:20,step:1,initial:0}
data modify storage mgs:temp dialog.inputs[-1].initial set from storage mgs:temp _mb_cur[{weapon_id:"svd"}].weight
data modify storage mgs:temp dialog.inputs append value {type:"minecraft:number_range",key:"m82",label:"M82",start:0,end:20,step:1,initial:0}
data modify storage mgs:temp dialog.inputs[-1].initial set from storage mgs:temp _mb_cur[{weapon_id:"m82"}].weight
data modify storage mgs:temp dialog.inputs append value {type:"minecraft:number_range",key:"mosin",label:"Mosin-Nagant",start:0,end:20,step:1,initial:0}
data modify storage mgs:temp dialog.inputs[-1].initial set from storage mgs:temp _mb_cur[{weapon_id:"mosin"}].weight
data modify storage mgs:temp dialog.inputs append value {type:"minecraft:number_range",key:"m24",label:"M24",start:0,end:20,step:1,initial:0}
data modify storage mgs:temp dialog.inputs[-1].initial set from storage mgs:temp _mb_cur[{weapon_id:"m24"}].weight
data modify storage mgs:temp dialog.inputs append value {type:"minecraft:number_range",key:"spas12",label:"SPAS-12",start:0,end:20,step:1,initial:0}
data modify storage mgs:temp dialog.inputs[-1].initial set from storage mgs:temp _mb_cur[{weapon_id:"spas12"}].weight
data modify storage mgs:temp dialog.inputs append value {type:"minecraft:number_range",key:"m500",label:"M500",start:0,end:20,step:1,initial:0}
data modify storage mgs:temp dialog.inputs[-1].initial set from storage mgs:temp _mb_cur[{weapon_id:"m500"}].weight
data modify storage mgs:temp dialog.inputs append value {type:"minecraft:number_range",key:"m590",label:"M590",start:0,end:20,step:1,initial:0}
data modify storage mgs:temp dialog.inputs[-1].initial set from storage mgs:temp _mb_cur[{weapon_id:"m590"}].weight
data modify storage mgs:temp dialog.inputs append value {type:"minecraft:number_range",key:"rpg7",label:"RPG-7",start:0,end:20,step:1,initial:0}
data modify storage mgs:temp dialog.inputs[-1].initial set from storage mgs:temp _mb_cur[{weapon_id:"rpg7"}].weight
data modify storage mgs:temp dialog.inputs append value {type:"minecraft:number_range",key:"m1911",label:"M1911",start:0,end:20,step:1,initial:0}
data modify storage mgs:temp dialog.inputs[-1].initial set from storage mgs:temp _mb_cur[{weapon_id:"m1911"}].weight
data modify storage mgs:temp dialog.inputs append value {type:"minecraft:number_range",key:"m9",label:"M9",start:0,end:20,step:1,initial:0}
data modify storage mgs:temp dialog.inputs[-1].initial set from storage mgs:temp _mb_cur[{weapon_id:"m9"}].weight
data modify storage mgs:temp dialog.inputs append value {type:"minecraft:number_range",key:"deagle",label:"Deagle",start:0,end:20,step:1,initial:0}
data modify storage mgs:temp dialog.inputs[-1].initial set from storage mgs:temp _mb_cur[{weapon_id:"deagle"}].weight
data modify storage mgs:temp dialog.inputs append value {type:"minecraft:number_range",key:"makarov",label:"Makarov",start:0,end:20,step:1,initial:0}
data modify storage mgs:temp dialog.inputs[-1].initial set from storage mgs:temp _mb_cur[{weapon_id:"makarov"}].weight
data modify storage mgs:temp dialog.inputs append value {type:"minecraft:number_range",key:"glock17",label:"Glock 17",start:0,end:20,step:1,initial:0}
data modify storage mgs:temp dialog.inputs[-1].initial set from storage mgs:temp _mb_cur[{weapon_id:"glock17"}].weight
data modify storage mgs:temp dialog.inputs append value {type:"minecraft:number_range",key:"glock18",label:"Glock 18",start:0,end:20,step:1,initial:0}
data modify storage mgs:temp dialog.inputs[-1].initial set from storage mgs:temp _mb_cur[{weapon_id:"glock18"}].weight
data modify storage mgs:temp dialog.inputs append value {type:"minecraft:number_range",key:"vz61",label:"VZ-61",start:0,end:20,step:1,initial:0}
data modify storage mgs:temp dialog.inputs[-1].initial set from storage mgs:temp _mb_cur[{weapon_id:"vz61"}].weight
data modify storage mgs:temp dialog.inputs append value {type:"minecraft:number_range",key:"ray_gun",label:"Ray Gun",start:0,end:20,step:1,initial:0}
data modify storage mgs:temp dialog.inputs[-1].initial set from storage mgs:temp _mb_cur[{weapon_id:"ray_gun"}].weight
data modify storage mgs:temp dialog.inputs append value {type:"minecraft:number_range",key:"monkey_bomb",label:"Monkey Bomb",start:0,end:20,step:1,initial:0}
data modify storage mgs:temp dialog.inputs[-1].initial set from storage mgs:temp _mb_cur[{weapon_id:"monkey_bomb"}].weight
function mgs:v5.3.0/multiplayer/show_dialog with storage mgs:temp

