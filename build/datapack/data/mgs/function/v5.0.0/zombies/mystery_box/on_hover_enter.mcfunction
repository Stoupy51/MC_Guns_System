
#> mgs:v5.0.0/zombies/mystery_box/on_hover_enter
#
# @within	???
#

execute unless entity @e[tag=bs.interaction.target,tag=mgs.mystery_box_active] run return fail
execute unless data storage mgs:zombies game{state:"active"} run return fail
execute if data storage mgs:zombies mystery_box{ready:true} run return run title @s actionbar [{"translate": "mgs.mystery_box","color":"light_purple"},{"text":" - ","color":"gray"},{"translate": "mgs.click_to_collect","color":"green"}]
execute if data storage mgs:zombies mystery_box{spinning:true} run return run title @s actionbar [{"translate": "mgs.mystery_box","color":"light_purple"},{"text":" - ","color":"gray"},{"translate": "mgs.spinning","color":"yellow"}]
title @s actionbar [{"translate": "mgs.mystery_box","color":"light_purple"},{"text":" - ","color":"gray"},{"translate": "mgs.950_points","color":"gold"}]

