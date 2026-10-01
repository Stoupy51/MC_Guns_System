""" Buying from a wall: guns, knives, lethals and tacticals, each with its own guards. """
# Imports
from stewbeet import Mem, write_versioned_function

from ....core.feedback import ZombiesFeedback
from ....helpers import MGS_TAG
from ...common import ZombiesCommon


# Functions
def write_wallbuy_purchase() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	deny_not_enough_points: str = ZombiesCommon.deny_not_enough_points_cmd(ns, version, "#wb_price")
	deny_knife_owned: str = ZombiesCommon.deny_cmd(ns, version, '{"text":"You already own this knife.","color":"yellow"}')
	deny_equipment_full: str = ZombiesCommon.deny_cmd(ns, version, '{"text":"Your equipment is already full.","color":"yellow"}')

	## Run as the player.
	write_versioned_function("zombies/wallbuys/on_right_click", f"""
{ZombiesCommon.game_active_guard_cmd(ns)}

# Read first: the dynamic price needs them.
execute store result storage {ns}:temp _wb_buy.id int 1 run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.wb.id
function {ns}:v{version}/zombies/wallbuys/lookup_weapon with storage {ns}:temp _wb_buy
function {ns}:v{version}/zombies/wallbuys/get_display_name

execute store result score #wb_buy_price {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.wb.price
execute store result score #wb_rfprice {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.wb.rfprice
execute store result score #wb_rfpap {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.wb.rfpap

# Knife, lethal grenade and tactical have their own flows.
execute if data storage {ns}:temp _wb_weapon{{kind:1}} run return run function {ns}:v{version}/zombies/wallbuys/buy_knife with storage {ns}:temp _wb_weapon
execute if data storage {ns}:temp _wb_weapon{{kind:2}} run return run function {ns}:v{version}/zombies/wallbuys/buy_lethal with storage {ns}:temp _wb_weapon
execute if data storage {ns}:temp _wb_weapon{{kind:3}} run return run function {ns}:v{version}/zombies/wallbuys/buy_tactical with storage {ns}:temp _wb_weapon

# Buy, refill or PaP refill.
scoreboard players operation #wb_price {ns}.data = #wb_buy_price {ns}.data
function {ns}:v{version}/zombies/wallbuys/compute_effective_price with storage {ns}:temp _wb_weapon

execute unless score @s {ns}.zb.points >= #wb_price {ns}.data run return run {deny_not_enough_points}

scoreboard players operation @s {ns}.zb.points -= #wb_price {ns}.data

function {ns}:v{version}/zombies/wallbuys/process_purchase with storage {ns}:temp _wb_weapon

execute if score #wb_purchase_mode {ns}.data matches 1 run function {ns}:v{version}/zombies/wallbuys/msg_purchased
execute if score #wb_purchase_mode {ns}.data matches 2 run function {ns}:v{version}/zombies/wallbuys/msg_refilled
execute if score #wb_purchase_mode {ns}.data matches 3 run function {ns}:v{version}/zombies/wallbuys/msg_replaced
execute if score #wb_purchase_mode {ns}.data matches 4 run scoreboard players operation @s {ns}.zb.points += #wb_price {ns}.data
execute if score #wb_purchase_mode {ns}.data matches 4 run function {ns}:v{version}/zombies/wallbuys/msg_refund_full

# The actionbar reads reserve_ammo, which is otherwise only recomputed on reload, idle or weapon switch.
execute if score #wb_purchase_mode {ns}.data matches 1..3 run function {ns}:v{version}/utils/copy_gun_data
execute if score #wb_purchase_mode {ns}.data matches 1..3 run function {ns}:v{version}/ammo/compute_reserve
""")

	## Knife wallbuy (kind 1): replaces hotbar.0, no refill. Run as the player, with _wb_weapon.
	write_versioned_function("zombies/wallbuys/buy_knife", f"""
$execute if items entity @s hotbar.0 *[custom_data~{{{ns}:{{$(weapon_id):true}}}}] run return run {deny_knife_owned}

scoreboard players operation #wb_price {ns}.data = #wb_buy_price {ns}.data
execute unless score @s {ns}.zb.points >= #wb_price {ns}.data run return run {deny_not_enough_points}
scoreboard players operation @s {ns}.zb.points -= #wb_price {ns}.data

# Re-tagged for the zombies slot enforcement (inventory/check_slots).
$loot replace entity @s hotbar.0 loot {ns}:i/$(weapon_id)
function {ns}:v{version}/zombies/inventory/apply_slot_tag {{slot:"hotbar.0",group:"hotbar",index:0}}
function {ns}:v{version}/zombies/wallbuys/msg_purchased
""")

	## Lethal grenades (hotbar.7, max 4) and tacticals (hotbar.6, max 3): the same item refills at refill_price
	## (denied when full, before charging), anything else buys a full stack of the bought type.
	for kind_name, eq_slot, eq_count in (("lethal", 7, 4), ("tactical", 6, 3)):
		widows_gate: str = ""
		record_line: str = ""
		if kind_name == "lethal":
			# Widow's Wine owners keep web grenades: any lethal buy refills webs instead (buy_lethal_web).
			widows_gate = (
				f"execute if score @s {ns}.special.widows_wine matches 1 run "
				f"return run function {ns}:v{version}/zombies/wallbuys/buy_lethal_web with storage {ns}:temp _wb_weapon\n"
			)
			# An emptied lethal slot refills this type on round end and Max Ammo; tacticals are refill-only.
			record_line = f"function {ns}:v{version}/zombies/inventory/record_lethal_type\n"
		write_versioned_function(f"zombies/wallbuys/buy_{kind_name}", f"""
{widows_gate}# Same equipment already in the slot: refill flow
$execute if items entity @s hotbar.{eq_slot} *[custom_data~{{{ns}:{{$(weapon_id):true}}}}] run return run function {ns}:v{version}/zombies/wallbuys/refill_{kind_name} with storage {ns}:temp _wb_weapon

# Empty slot or another type: full price for {eq_count} fresh ones.
scoreboard players operation #wb_price {ns}.data = #wb_buy_price {ns}.data
execute unless score @s {ns}.zb.points >= #wb_price {ns}.data run return run {deny_not_enough_points}
scoreboard players operation @s {ns}.zb.points -= #wb_price {ns}.data
$loot replace entity @s hotbar.{eq_slot} loot {ns}:i/$(weapon_id)
item modify entity @s hotbar.{eq_slot} {ns}:v{version}/grenade/set_count_{eq_count}
function {ns}:v{version}/zombies/inventory/apply_slot_tag {{slot:"hotbar.{eq_slot}",group:"hotbar",index:{eq_slot}}}
{record_line}function {ns}:v{version}/zombies/wallbuys/msg_purchased
""")

		write_versioned_function(f"zombies/wallbuys/refill_{kind_name}", f"""
# Full: denied, and nothing was charged on this path.
execute store result score #wb_eq_count {ns}.data run data get entity @s Inventory[{{Slot:{eq_slot}b}}].count
execute if score #wb_eq_count {ns}.data matches {eq_count}.. run return run {deny_equipment_full}

scoreboard players operation #wb_price {ns}.data = #wb_rfprice {ns}.data
execute unless score @s {ns}.zb.points >= #wb_price {ns}.data run return run {deny_not_enough_points}
scoreboard players operation @s {ns}.zb.points -= #wb_price {ns}.data
item modify entity @s hotbar.{eq_slot} {ns}:v{version}/grenade/set_count_{eq_count}
function {ns}:v{version}/zombies/wallbuys/msg_refilled
""")

	## Widow's Wine: refill webs (denied when full), otherwise 4 fresh webs at full price.
	write_versioned_function("zombies/wallbuys/buy_lethal_web", f"""
execute if items entity @s hotbar.7 *[custom_data~{{{ns}:{{stats:{{grenade_type:"web"}}}}}}] run return run function {ns}:v{version}/zombies/wallbuys/refill_lethal with storage {ns}:temp _wb_weapon
scoreboard players operation #wb_price {ns}.data = #wb_buy_price {ns}.data
execute unless score @s {ns}.zb.points >= #wb_price {ns}.data run return run {deny_not_enough_points}
scoreboard players operation @s {ns}.zb.points -= #wb_price {ns}.data
loot replace entity @s hotbar.7 loot {ns}:i/web_grenade
item modify entity @s hotbar.7 {ns}:v{version}/grenade/set_count_4
function {ns}:v{version}/zombies/inventory/apply_slot_tag {{slot:"hotbar.7",group:"hotbar",index:7}}
function {ns}:v{version}/zombies/wallbuys/msg_purchased
""")

	## Silent tactical give or refill, for the Mystery Box (default_give/monkey_bomb).
	## Sets the purchase flags its retry logic reads.
	write_versioned_function("zombies/wallbuys/give_tactical", f"""
scoreboard players set #wb_purchase_done {ns}.data 1
scoreboard players set #wb_purchase_mode {ns}.data 2

# Same tactical: back to 3.
$execute if items entity @s hotbar.6 *[custom_data~{{{ns}:{{$(weapon_id):true}}}}] run return run item modify entity @s hotbar.6 {ns}:v{version}/grenade/set_count_3

# Tagged for the zombies slot enforcement.
$loot replace entity @s hotbar.6 loot {ns}:i/$(weapon_id)
item modify entity @s hotbar.6 {ns}:v{version}/grenade/set_count_3
function {ns}:v{version}/zombies/inventory/apply_slot_tag {{slot:"hotbar.6",group:"hotbar",index:6}}
scoreboard players set #wb_purchase_mode {ns}.data 1
""")

	write_versioned_function("zombies/wallbuys/msg_purchased", f"""
tellraw @s [{MGS_TAG},{{"text":"You bought ","color":"green"}},{{"storage":"{ns}:temp","nbt":"_wb_display_name","color":"gold","interpret":true}},{{"text":" for ","color":"green"}},{{"score":{{"name":"#wb_price","objective":"{ns}.data"}},"color":"yellow"}},{{"text":" points.","color":"green"}}]
{ZombiesFeedback.zb_sound('success')}
""")

	write_versioned_function("zombies/wallbuys/msg_refilled", f"""
tellraw @s [{MGS_TAG},{{"text":"Ammo refilled for ","color":"gold"}},{{"score":{{"name":"#wb_price","objective":"{ns}.data"}},"color":"yellow"}},{{"text":" points.","color":"gold"}}]
{ZombiesFeedback.zb_sound('refill')}
""")

	write_versioned_function("zombies/wallbuys/msg_replaced", f"""
tellraw @s [{MGS_TAG},{{"text":"Swapped your selected weapon for ","color":"yellow"}},{{"storage":"{ns}:temp","nbt":"_wb_display_name","color":"gold","interpret":true}},{{"text":" (","color":"yellow"}},{{"score":{{"name":"#wb_price","objective":"{ns}.data"}},"color":"yellow"}},{{"text":" points).","color":"yellow"}}]
{ZombiesFeedback.zb_sound('replace')}
""")

	write_versioned_function("zombies/wallbuys/msg_refund_full", f"""
tellraw @s [{MGS_TAG},{{"text":"Ammo is already full. Refunded ","color":"red"}},{{"score":{{"name":"#wb_price","objective":"{ns}.data"}},"color":"yellow"}},{{"text":" points.","color":"red"}}]
{ZombiesFeedback.zb_sound('deny')}
""")

