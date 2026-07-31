""" The hover actionbar and the preload hook. """
# Imports
from stewbeet import Mem, write_versioned_function

from ....helpers.titles import TitleTimes


# Functions
def write_wallbuy_hover() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	wallbuy_hover_message: str = (
		f'[{{"text":"🔫 ","color":"gold"}},'
		f'{{"storage":"{ns}:temp","nbt":"_wb_display_name","color":"yellow","interpret":true}},'
		f'{{"text":" - Cost: ","color":"gray"}},'
		f'{{"score":{{"name":"#wb_price","objective":"{ns}.data"}},"color":"yellow"}},'
		f'{{"text":" points","color":"gray"}},'
		f'{{"storage":"{ns}:temp","nbt":"_wb_price_suffix","color":"gray","interpret":true}}]'
	)

	## Hover events (executor: "source" = player)
	write_versioned_function("zombies/wallbuys/get_hover_name", f"""
$data modify storage {ns}:temp _wb_weapon set from storage {ns}:zombies wallbuy_data."$(id)"
""")

	write_versioned_function("zombies/wallbuys/render_hover_title", f"""
{TitleTimes.HOVER.cmd()}
title @s title ["","🔫 ",{{"storage":"{ns}:temp","nbt":"_wb_weapon.item_name","color":"gold","interpret":true}}]
""")

	write_versioned_function("zombies/wallbuys/on_hover", f"""
execute store result storage {ns}:temp _wb_hover.id int 1 run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.wb.id
function {ns}:v{version}/zombies/wallbuys/get_hover_name with storage {ns}:temp _wb_hover
function {ns}:v{version}/zombies/wallbuys/get_display_name

# Dynamic hover price (buy, refill, or PAP refill)
execute store result score #wb_buy_price {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.wb.price
execute store result score #wb_rfprice {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.wb.rfprice
execute store result score #wb_rfpap {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.wb.rfpap
scoreboard players operation #wb_price {ns}.data = #wb_buy_price {ns}.data
data modify storage {ns}:temp _wb_price_suffix set value ""

# Non-gun wallbuys: kind-specific effective price + suffix
execute if data storage {ns}:temp _wb_weapon{{kind:1}} run return run function {ns}:v{version}/zombies/wallbuys/hover_knife with storage {ns}:temp _wb_weapon
execute if data storage {ns}:temp _wb_weapon{{kind:2}} run return run function {ns}:v{version}/zombies/wallbuys/hover_lethal with storage {ns}:temp _wb_weapon
execute if data storage {ns}:temp _wb_weapon{{kind:3}} run return run function {ns}:v{version}/zombies/wallbuys/hover_tactical with storage {ns}:temp _wb_weapon

function {ns}:v{version}/zombies/wallbuys/compute_effective_price with storage {ns}:temp _wb_weapon
function {ns}:v{version}/zombies/wallbuys/set_hover_price_suffix
function {ns}:v{version}/zombies/wallbuys/render_hover
""")

	## Shared actionbar render (title + effective #wb_price + suffix, all prepared by the caller)
	write_versioned_function("zombies/wallbuys/render_hover", f"""
data modify storage smithed.actionbar:input message set value {{json:{wallbuy_hover_message},priority:"conditional",freeze:5}}
function #smithed.actionbar:message
""")

	## Kind-specific hovers (macro with _wb_weapon, @s = player)
	write_versioned_function("zombies/wallbuys/hover_knife", f"""
$execute if items entity @s hotbar.0 *[custom_data~{{{ns}:{{$(weapon_id):true}}}}] run data modify storage {ns}:temp _wb_price_suffix set value " (Owned)"
function {ns}:v{version}/zombies/wallbuys/render_hover
""")

	for kind_name, eq_slot in (("lethal", 7), ("tactical", 6)):
		write_versioned_function(f"zombies/wallbuys/hover_{kind_name}", f"""
$execute if items entity @s hotbar.{eq_slot} *[custom_data~{{{ns}:{{$(weapon_id):true}}}}] run scoreboard players operation #wb_price {ns}.data = #wb_rfprice {ns}.data
$execute if items entity @s hotbar.{eq_slot} *[custom_data~{{{ns}:{{$(weapon_id):true}}}}] run data modify storage {ns}:temp _wb_price_suffix set value " (Refill)"
function {ns}:v{version}/zombies/wallbuys/render_hover
""")

	## Hook into preload_complete: setup wallbuys
	write_versioned_function("zombies/preload_complete", f"""
# Setup wallbuys
execute if data storage {ns}:zombies game.map.wallbuys[0] run function {ns}:v{version}/zombies/wallbuys/setup
""")

