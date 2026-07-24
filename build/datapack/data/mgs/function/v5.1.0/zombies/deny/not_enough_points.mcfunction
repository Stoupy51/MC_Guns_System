
#> mgs:v5.1.0/zombies/deny/not_enough_points
#
# @executed	at @n[tag=bs.interaction.target]
#
# @within	mgs:v5.1.0/zombies/mystery_box/try_use {score:"#zb_mystery_box_price",obj:"mgs.config"}
#			mgs:v5.1.0/zombies/pap/on_right_click {score:"#pap_price",obj:"mgs.data"}
#			mgs:v5.1.0/zombies/doors/on_right_click {score:"#door_price",obj:"mgs.data"}
#			mgs:v5.1.0/zombies/wallbuys/on_right_click {score:"#wb_price",obj:"mgs.data"}
#			mgs:v5.1.0/zombies/wallbuys/buy_knife {score:"#wb_price",obj:"mgs.data"}
#			mgs:v5.1.0/zombies/wallbuys/buy_lethal {score:"#wb_price",obj:"mgs.data"}
#			mgs:v5.1.0/zombies/wallbuys/refill_lethal {score:"#wb_price",obj:"mgs.data"}
#			mgs:v5.1.0/zombies/wallbuys/buy_tactical {score:"#wb_price",obj:"mgs.data"}
#			mgs:v5.1.0/zombies/wallbuys/refill_tactical {score:"#wb_price",obj:"mgs.data"}
#			mgs:v5.1.0/zombies/wallbuys/buy_lethal_web {score:"#wb_price",obj:"mgs.data"}
#			mgs:v5.1.0/zombies/perks/on_right_click {score:"#pk_price",obj:"mgs.data"}
#			mgs:v5.1.0/zombies/wunderfizz/try_use {score:"#wf_price",obj:"mgs.data"}
#			mgs:v5.1.0/zombies/traps/on_right_click {score:"#trap_price",obj:"mgs.data"}
#
# @args		score (string)
#			obj (string)
#

$tellraw @s [[{"text":"","color":"gold"},"[",{"translate":"mgs"},"] "],[{"translate":"mgs.you_dont_have_enough_points","color":"red"}, " ("],{"score":{"name":"$(score)","objective":"$(obj)"},"color":"yellow"},[{"text":" ","color":"red"}, {"translate":"mgs.needed"}, ")."]]
playsound minecraft:entity.villager.no ambient @s ~ ~ ~ 0.8 1.0

