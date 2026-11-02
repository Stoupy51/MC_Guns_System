
#> mgs:v5.3.0/maps/editor/form/perk_apply
#
# @within	string in mgs:v5.3.0/maps/editor/form/open/perk_machine {name:\"$(name)\",price:$(price),partial_price:$(partial_price),power:$(power),perk:\"\"}
#			string in mgs:v5.3.0/maps/editor/form/open/perk_machine {name:\"$(name)\",price:$(price),partial_price:$(partial_price),power:$(power),perk:\"juggernog\"}
#			string in mgs:v5.3.0/maps/editor/form/open/perk_machine {name:\"$(name)\",price:$(price),partial_price:$(partial_price),power:$(power),perk:\"speed_cola\"}
#			string in mgs:v5.3.0/maps/editor/form/open/perk_machine {name:\"$(name)\",price:$(price),partial_price:$(partial_price),power:$(power),perk:\"double_tap\"}
#			string in mgs:v5.3.0/maps/editor/form/open/perk_machine {name:\"$(name)\",price:$(price),partial_price:$(partial_price),power:$(power),perk:\"quick_revive\"}
#			string in mgs:v5.3.0/maps/editor/form/open/perk_machine {name:\"$(name)\",price:$(price),partial_price:$(partial_price),power:$(power),perk:\"mule_kick\"}
#			string in mgs:v5.3.0/maps/editor/form/open/perk_machine {name:\"$(name)\",price:$(price),partial_price:$(partial_price),power:$(power),perk:\"stamin_up\"}
#			string in mgs:v5.3.0/maps/editor/form/open/perk_machine {name:\"$(name)\",price:$(price),partial_price:$(partial_price),power:$(power),perk:\"phd_flopper\"}
#			string in mgs:v5.3.0/maps/editor/form/open/perk_machine {name:\"$(name)\",price:$(price),partial_price:$(partial_price),power:$(power),perk:\"deadshot\"}
#			string in mgs:v5.3.0/maps/editor/form/open/perk_machine {name:\"$(name)\",price:$(price),partial_price:$(partial_price),power:$(power),perk:\"timeslip\"}
#			string in mgs:v5.3.0/maps/editor/form/open/perk_machine {name:\"$(name)\",price:$(price),partial_price:$(partial_price),power:$(power),perk:\"electric_cherry\"}
#			string in mgs:v5.3.0/maps/editor/form/open/perk_machine {name:\"$(name)\",price:$(price),partial_price:$(partial_price),power:$(power),perk:\"tombstone\"}
#			string in mgs:v5.3.0/maps/editor/form/open/perk_machine {name:\"$(name)\",price:$(price),partial_price:$(partial_price),power:$(power),perk:\"whos_who\"}
#			string in mgs:v5.3.0/maps/editor/form/open/perk_machine {name:\"$(name)\",price:$(price),partial_price:$(partial_price),power:$(power),perk:\"dying_wish\"}
#			string in mgs:v5.3.0/maps/editor/form/open/perk_machine {name:\"$(name)\",price:$(price),partial_price:$(partial_price),power:$(power),perk:\"widows_wine\"}
#
# @args		name (string)
#			price (unknown)
#			partial_price (unknown)
#			power (unknown)
#			perk (string)
#

execute unless entity @n[type=minecraft:marker,tag=mgs.ed_form_target] run return run tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.the_element_being_edited_is_gone","fallback":"The element being edited is gone.","color":"red"}]
$data modify storage mgs:temp _form set value {title:"$(name)",price:$(price),partial_price:$(partial_price),power:$(power)b}
$data modify storage mgs:temp _form.perk_id set value "$(perk)"
execute if data storage mgs:temp _form{perk_id:""} run data remove storage mgs:temp _form.perk_id
execute as @n[type=minecraft:marker,tag=mgs.ed_form_target] run data modify entity @s data merge from storage mgs:temp _form
tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs","fallback":"MGS"},"] "],{"translate":"mgs.perk_machine_saved","fallback":"Perk machine saved: ","color":"green"},{"entity":"@n[type=minecraft:marker,tag=mgs.ed_form_target]","nbt":"data.perk_id","color":"light_purple"}]

