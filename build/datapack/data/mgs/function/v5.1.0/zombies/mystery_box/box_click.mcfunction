
#> mgs:v5.1.0/zombies/mystery_box/box_click
#
# @executed	at @n[tag=bs.interaction.target]
#
# @within	mgs:v5.1.0/zombies/mystery_box/on_right_click [ at @n[tag=bs.interaction.target] ]
#

execute if entity @n[tag=mgs.mb_display,distance=..3,scores={mgs.mb.anim=1..}] run return run function mgs:v5.1.0/zombies/deny/message {msg:'{"translate":"mgs.mystery_box_is_already_in_use","color":"red"}'}

# Shared by its buyer: anyone may collect.
execute if entity @n[tag=mgs.mb_display,distance=..3,tag=mgs.mb_shared] run return run function mgs:v5.1.0/zombies/mystery_box/collect

# Ready: only its buyer may collect.
execute if entity @n[tag=mgs.mb_display,distance=..3] if score @s mgs.mb.pid = @n[tag=mgs.mb_display,distance=..3] mgs.mb.buyer run return run function mgs:v5.1.0/zombies/mystery_box/collect
execute if entity @n[tag=mgs.mb_display,distance=..3] run return run function mgs:v5.1.0/zombies/deny/message {msg:'{"translate":"mgs.wait_for_the_current_player_to_collect_their_result","color":"red"}'}

function mgs:v5.1.0/zombies/mystery_box/try_use

