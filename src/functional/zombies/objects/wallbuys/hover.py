""" The hover actionbar and the preload hook. """
# Imports
from stewbeet import Mem, write_versioned_function


# Functions
def write_wallbuy_hover() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	wallbuy_hover_message: str = (
		f'[{{"text":"🔫 "}},'
		f'{{"storage":"{ns}:temp","nbt":"_wb_display_name","color":"yellow","interpret":true}},'
		f'{{"text":" - Cost: ","color":"gray"}},'
		f'{{"score":{{"name":"#wb_price","objective":"{ns}.data"}},"color":"yellow"}},'
		f'{{"text":" points","color":"gray"}},'
		f'{{"storage":"{ns}:temp","nbt":"_wb_price_suffix","color":"gray","interpret":true}}]'
	)

	## Run as the player.
	write_versioned_function("zombies/wallbuys/get_hover_name", f"""
$data modify storage {ns}:temp _wb_weapon set from storage {ns}:zombies wallbuy_data."$(id)"
""")

	write_versioned_function("zombies/wallbuys/on_hover", f"""
execute store result storage {ns}:temp _wb_hover.id int 1 run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.wb.id
function {ns}:v{version}/zombies/wallbuys/get_hover_name with storage {ns}:temp _wb_hover
function {ns}:v{version}/zombies/wallbuys/get_display_name

# Buy, refill or PaP refill.
execute store result score #wb_buy_price {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.wb.price
execute store result score #wb_rfprice {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.wb.rfprice
execute store result score #wb_rfpap {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.wb.rfpap
scoreboard players operation #wb_price {ns}.data = #wb_buy_price {ns}.data
data modify storage {ns}:temp _wb_price_suffix set value ""

execute if data storage {ns}:temp _wb_weapon{{kind:1}} run return run function {ns}:v{version}/zombies/wallbuys/hover_knife with storage {ns}:temp _wb_weapon
execute if data storage {ns}:temp _wb_weapon{{kind:2}} run return run function {ns}:v{version}/zombies/wallbuys/hover_lethal with storage {ns}:temp _wb_weapon
execute if data storage {ns}:temp _wb_weapon{{kind:3}} run return run function {ns}:v{version}/zombies/wallbuys/hover_tactical with storage {ns}:temp _wb_weapon

function {ns}:v{version}/zombies/wallbuys/compute_effective_price with storage {ns}:temp _wb_weapon
function {ns}:v{version}/zombies/wallbuys/set_hover_price_suffix
function {ns}:v{version}/zombies/wallbuys/render_hover
""")

	## The caller prepares the title, #wb_price and the suffix.
	write_versioned_function("zombies/wallbuys/render_hover", f"""
data modify storage smithed.actionbar:input message set value {{json:{wallbuy_hover_message},priority:"conditional",freeze:5}}
function #smithed.actionbar:message
""")

	## Run as the player, with _wb_weapon.
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

	write_versioned_function("zombies/preload_complete", f"""
execute if data storage {ns}:zombies game.map.wallbuys[0] run function {ns}:v{version}/zombies/wallbuys/setup
""")

