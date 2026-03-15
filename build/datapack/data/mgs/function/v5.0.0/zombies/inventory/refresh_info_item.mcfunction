
#> mgs:v5.0.0/zombies/inventory/refresh_info_item
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/inventory/give_starting_loadout
#			mgs:v5.0.0/zombies/inventory/recreate_critical_items
#

item replace entity @s hotbar.8 with minecraft:paper[custom_data={mgs:{zb_info:true}},item_name={"text":"\u2139 Player Info","color":"gold","italic":false},lore=[{"translate":"mgs.round_2","color":"gray","italic":false,"extra":[{"score":{"name":"#zb_round","objective":"mgs.data"},"color":"gold"}]},{"translate":"mgs.points_4","color":"gray","italic":false,"extra":[{"score":{"name":"@s","objective":"mgs.zb.points"},"color":"gold"}]},{"translate":"mgs.kills_2","color":"gray","italic":false,"extra":[{"score":{"name":"@s","objective":"mgs.zb.kills"},"color":"green"}]},{"translate":"mgs.downs","color":"gray","italic":false,"extra":[{"score":{"name":"@s","objective":"mgs.zb.downs"},"color":"red"}]},{"text":"","italic":false},{"translate":"mgs.passive","color":"gray","italic":false,"extra":[{"score":{"name":"@s","objective":"mgs.zb.passive"},"color":"aqua"}]},{"translate":"mgs.ability","color":"gray","italic":false,"extra":[{"score":{"name":"@s","objective":"mgs.zb.ability"},"color":"green"}]}]]
function mgs:v5.0.0/zombies/inventory/apply_slot_tag {slot:"hotbar.8",group:"hotbar",index:8}

