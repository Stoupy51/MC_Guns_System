
#> mgs:v5.0.0/zombies/passive_ability_menu
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/player/config/process
#			mgs:v5.0.0/zombies/preload_complete [ as @a[scores={mgs.zb.in_game=1}] ]
#

# Show the passive selection dialog (ability dialog is shown after)
dialog show @s {type:"minecraft:multi_action",title:{translate:"mgs.zonweeb_passive",color:"dark_green"},body:{type:"minecraft:plain_message",contents:{translate:"mgs.choose_a_passive_effect_for_this_game",color:"gray"}},columns:1,after_action:"close",exit_action:{label:"Skip"},actions:[{label:[{"text":"💰 ","color":"gold"},{"translate":"mgs.x1_2_points"}],tooltip:{translate:"mgs.earn_20_more_points_from_kills_permanent"},action:{type:"run_command",command:"/trigger mgs.player.config set 6"}},{label:[{"text":"⏱ ","color":"aqua"},{"translate":"mgs.x1_5_powerups"}],tooltip:{translate:"mgs.all_powerup_durations_last_50_longer"},action:{type:"run_command",command:"/trigger mgs.player.config set 7"}}]}

