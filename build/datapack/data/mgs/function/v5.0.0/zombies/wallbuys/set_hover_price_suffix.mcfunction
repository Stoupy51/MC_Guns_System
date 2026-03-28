
#> mgs:v5.0.0/zombies/wallbuys/set_hover_price_suffix
#
# @within	mgs:v5.0.0/zombies/wallbuys/on_hover
#

data modify storage mgs:temp _wb_price_suffix set value ""
execute if score #wb_price_mode mgs.data matches 1 run data modify storage mgs:temp _wb_price_suffix set value " (Refill)"
execute if score #wb_price_mode mgs.data matches 2 run data modify storage mgs:temp _wb_price_suffix set value " (PAP Refill)"

