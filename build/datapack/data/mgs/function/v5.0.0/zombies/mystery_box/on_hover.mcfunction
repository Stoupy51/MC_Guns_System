
#> mgs:v5.0.0/zombies/mystery_box/on_hover
#
# @within	???
#

execute unless entity @e[tag=bs.interaction.target,tag=mgs.mystery_box_active] run return fail
execute unless data storage mgs:zombies game{state:"active"} run return fail
execute if data storage mgs:zombies mystery_box{ready:true} run return run function mgs:v5.0.0/zombies/mystery_box/hud_ready
execute if data storage mgs:zombies mystery_box{spinning:true} run return run function mgs:v5.0.0/zombies/mystery_box/hud_spinning
function mgs:v5.0.0/zombies/mystery_box/hud_price

