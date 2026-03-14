
#> mgs:v5.0.0/zombies/inventory/refresh_info_item
#
# @executed	at @s
#
# @within	mgs:v5.0.0/zombies/inventory/give_starting_loadout
#			mgs:v5.0.0/zombies/inventory/fix_info
#

# Build a player info item with current stats in lore
item replace entity @s hotbar.8 with minecraft:paper[custom_data={mgs:{zb_info:true}},item_name={"text":"\u2139 Player Info","color":"gold","italic":false},lore=[{"translate":"mgs.round","color":"gray","italic":false,"extra":[{"score":{"name":"#zb_round","objective":"mgs.data"},"color":"gold"}]},{"translate":"mgs.points_3","color":"gray","italic":false,"extra":[{"score":{"name":"@s","objective":"mgs.zb.points"},"color":"gold"}]},{"translate":"mgs.kills","color":"gray","italic":false,"extra":[{"score":{"name":"@s","objective":"mgs.zb.kills"},"color":"green"}]},{"translate":"mgs.downs","color":"gray","italic":false,"extra":[{"score":{"name":"@s","objective":"mgs.zb.downs"},"color":"red"}]},{"text":"","italic":false},{"translate":"mgs.passive","color":"gray","italic":false,"extra":[{"score":{"name":"@s","objective":"mgs.zb.passive"},"color":"aqua"}]},{"translate":"mgs.ability","color":"gray","italic":false,"extra":[{"score":{"name":"@s","objective":"mgs.zb.ability"},"color":"green"}]}]]

