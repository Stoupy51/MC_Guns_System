""" Buying from a wall: guns, knives, lethals and tacticals, each with its own guards. """
# ruff: noqa: E501
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

	## Right-click handler (executor: "source" = player)
	write_versioned_function("zombies/wallbuys/on_right_click", f"""
# Guard: game must be active
{ZombiesCommon.game_active_guard_cmd(ns)}

# Get wallbuy id + data first (used by dynamic price logic)
execute store result storage {ns}:temp _wb_buy.id int 1 run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.wb.id
function {ns}:v{version}/zombies/wallbuys/lookup_weapon with storage {ns}:temp _wb_buy
function {ns}:v{version}/zombies/wallbuys/get_display_name

# Read all possible prices from wallbuy entity
execute store result score #wb_buy_price {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.wb.price
execute store result score #wb_rfprice {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.wb.rfprice
execute store result score #wb_rfpap {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.wb.rfpap

# Non-gun wallbuys (knife / lethal grenade / tactical): dedicated purchase flows
execute if data storage {ns}:temp _wb_weapon{{kind:1}} run return run function {ns}:v{version}/zombies/wallbuys/buy_knife with storage {ns}:temp _wb_weapon
execute if data storage {ns}:temp _wb_weapon{{kind:2}} run return run function {ns}:v{version}/zombies/wallbuys/buy_lethal with storage {ns}:temp _wb_weapon
execute if data storage {ns}:temp _wb_weapon{{kind:3}} run return run function {ns}:v{version}/zombies/wallbuys/buy_tactical with storage {ns}:temp _wb_weapon

# Compute effective price for this interaction (buy vs refill vs PAP refill)
scoreboard players operation #wb_price {ns}.data = #wb_buy_price {ns}.data
function {ns}:v{version}/zombies/wallbuys/compute_effective_price with storage {ns}:temp _wb_weapon

# Check player has enough points
execute unless score @s {ns}.zb.points >= #wb_price {ns}.data run return run {deny_not_enough_points}

# Deduct points
scoreboard players operation @s {ns}.zb.points -= #wb_price {ns}.data

# Process buy by zombies inventory rules
function {ns}:v{version}/zombies/wallbuys/process_purchase with storage {ns}:temp _wb_weapon

execute if score #wb_purchase_mode {ns}.data matches 1 run function {ns}:v{version}/zombies/wallbuys/msg_purchased
execute if score #wb_purchase_mode {ns}.data matches 2 run function {ns}:v{version}/zombies/wallbuys/msg_refilled
execute if score #wb_purchase_mode {ns}.data matches 3 run function {ns}:v{version}/zombies/wallbuys/msg_replaced
execute if score #wb_purchase_mode {ns}.data matches 4 run scoreboard players operation @s {ns}.zb.points += #wb_price {ns}.data
execute if score #wb_purchase_mode {ns}.data matches 4 run function {ns}:v{version}/zombies/wallbuys/msg_refund_full

# Refresh the reserve-ammo HUD after a buy/refill/replace. reload_pair fills the magazines but
# the actionbar reads @s {ns}.reserve_ammo, which is otherwise only recomputed on reload/idle/
# weapon-switch — so without this the reserve count stayed stale until the next weapon swap.
execute if score #wb_purchase_mode {ns}.data matches 1..3 run function {ns}:v{version}/utils/copy_gun_data
execute if score #wb_purchase_mode {ns}.data matches 1..3 run function {ns}:v{version}/ammo/compute_reserve
""")

	## Knife wallbuy (kind 1): replaces hotbar.0, no refill concept (macro with _wb_weapon, @s = player)
	write_versioned_function("zombies/wallbuys/buy_knife", f"""
# Already own this exact knife: nothing to buy
$execute if items entity @s hotbar.0 *[custom_data~{{{ns}:{{$(weapon_id):true}}}}] run return run {deny_knife_owned}

# Full price
scoreboard players operation #wb_price {ns}.data = #wb_buy_price {ns}.data
execute unless score @s {ns}.zb.points >= #wb_price {ns}.data run return run {deny_not_enough_points}
scoreboard players operation @s {ns}.zb.points -= #wb_price {ns}.data

# Replace the knife slot and re-tag it for the zombies slot enforcement (inventory/check_slots)
$loot replace entity @s hotbar.0 loot {ns}:i/$(weapon_id)
function {ns}:v{version}/zombies/inventory/apply_slot_tag {{slot:"hotbar.0",group:"hotbar",index:0}}
function {ns}:v{version}/zombies/wallbuys/msg_purchased
""")

	## Equipment wallbuys: lethal grenades (hotbar.7, max 4) and tacticals (hotbar.6, max 3).
	## Same flow, generated per kind: same-item-in-slot -> refill at refill_price (deny when already full, BEFORE charging), otherwise full price for a fresh full stack of the bought type.
	for kind_name, eq_slot, eq_count in (("lethal", 7, 4), ("tactical", 6, 3)):
		widows_gate: str = ""
		record_line: str = ""
		if kind_name == "lethal":
			# Widow's Wine owners keep web grenades: any lethal buy refills webs instead of switching the bought type.
			# Reroute before the normal buy/refill flow (buy_lethal_web below).
			widows_gate = (
				f"execute if score @s {ns}.special.widows_wine matches 1 run "
				f"return run function {ns}:v{version}/zombies/wallbuys/buy_lethal_web with storage {ns}:temp _wb_weapon\n"
			)
			# Remember the bought lethal type so an emptied slot refills THIS type (not always frag) on round-end replenish / Max Ammo (inventory.py).
			# Not needed for tacticals (refill-only).
			record_line = f"function {ns}:v{version}/zombies/inventory/record_lethal_type\n"
		write_versioned_function(f"zombies/wallbuys/buy_{kind_name}", f"""
{widows_gate}# Same equipment already in the slot: refill flow
$execute if items entity @s hotbar.{eq_slot} *[custom_data~{{{ns}:{{$(weapon_id):true}}}}] run return run function {ns}:v{version}/zombies/wallbuys/refill_{kind_name} with storage {ns}:temp _wb_weapon

# New purchase (empty slot or different equipment type): full price for {eq_count} fresh ones
scoreboard players operation #wb_price {ns}.data = #wb_buy_price {ns}.data
execute unless score @s {ns}.zb.points >= #wb_price {ns}.data run return run {deny_not_enough_points}
scoreboard players operation @s {ns}.zb.points -= #wb_price {ns}.data
$loot replace entity @s hotbar.{eq_slot} loot {ns}:i/$(weapon_id)
item modify entity @s hotbar.{eq_slot} {ns}:v{version}/grenade/set_count_{eq_count}
function {ns}:v{version}/zombies/inventory/apply_slot_tag {{slot:"hotbar.{eq_slot}",group:"hotbar",index:{eq_slot}}}
{record_line}function {ns}:v{version}/zombies/wallbuys/msg_purchased
""")

		write_versioned_function(f"zombies/wallbuys/refill_{kind_name}", f"""
# Already at max: deny without charging (no points were deducted yet on this path)
execute store result score #wb_eq_count {ns}.data run data get entity @s Inventory[{{Slot:{eq_slot}b}}].count
execute if score #wb_eq_count {ns}.data matches {eq_count}.. run return run {deny_equipment_full}

# Refill price
scoreboard players operation #wb_price {ns}.data = #wb_rfprice {ns}.data
execute unless score @s {ns}.zb.points >= #wb_price {ns}.data run return run {deny_not_enough_points}
scoreboard players operation @s {ns}.zb.points -= #wb_price {ns}.data
item modify entity @s hotbar.{eq_slot} {ns}:v{version}/grenade/set_count_{eq_count}
function {ns}:v{version}/zombies/wallbuys/msg_refilled
""")

	## Widow's Wine lethal buy: refill/purchase web grenades regardless of the bought lethal type.
	## Already holding webs -> refill flow (deny if full); otherwise full price for 4 fresh webs.
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

	## Silent tactical give/refill (no pricing, no messages): shared by the Mystery Box collect flow (default_give/monkey_bomb) and any future scripted givers.
	## Sets the usual purchase flags so the box collect's retry logic sees a completed give.
	write_versioned_function("zombies/wallbuys/give_tactical", f"""
scoreboard players set #wb_purchase_done {ns}.data 1
scoreboard players set #wb_purchase_mode {ns}.data 2

# Already carrying the same tactical: top it back up to 3
$execute if items entity @s hotbar.6 *[custom_data~{{{ns}:{{$(weapon_id):true}}}}] run return run item modify entity @s hotbar.6 {ns}:v{version}/grenade/set_count_3

# Fresh give: 3 in the tactical slot (hotbar.6), tagged for the zombies slot enforcement
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

