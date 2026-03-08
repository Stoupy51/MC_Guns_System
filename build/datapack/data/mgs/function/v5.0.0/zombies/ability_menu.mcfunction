
#> mgs:v5.0.0/zombies/ability_menu
#
# @executed	as @e[type=player,sort=random] & at @s
#
# @within	mgs:v5.0.0/zombies/perks/set_passive_1
#			mgs:v5.0.0/zombies/perks/set_passive_2
#

# Show the ability selection dialog
dialog show @s {type:"minecraft:multi_action",title:{translate: "mgs.zonweeb_ability",color:"dark_green"},body:{type:"minecraft:plain_message",contents:{translate: "mgs.choose_an_ability_for_this_game",color:"gray"}},columns:1,after_action:"close",exit_action:{label:"Skip"},actions:[{label:[{"text":"🏃 ","color":"yellow"},{"translate": "mgs.coward"}],tooltip:{translate: "mgs.tp_to_spawn_when_under_50_hp_1_round_cooldown"},action:{type:"run_command",command:"/trigger mgs.player.config set 8"}},{label:[{"text":"🛡 ","color":"green"},{"translate": "mgs.guardian"}],tooltip:{translate: "mgs.summon_an_iron_golem_ally_at_round_start_1_round_cooldown"},action:{type:"run_command",command:"/trigger mgs.player.config set 9"}}]}

