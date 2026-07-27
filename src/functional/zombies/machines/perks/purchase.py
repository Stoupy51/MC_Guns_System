""" Buying a perk: the power, ownership and points guards, and the chip-in payment flow. """
# Imports
from stewbeet import Mem, write_versioned_function

from ....core.feedback import ZombiesFeedback
from ....helpers import MGS_TAG
from ...common import ZombiesCommon
from .definitions import PERK_DEFINITIONS


# Functions
def write_perk_purchase() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	deny_requires_power: str = ZombiesCommon.deny_cmd(ns, version, '{"text":"This perk machine requires power.","color":"red"}')
	deny_already_owned: str = ZombiesCommon.deny_cmd(ns, version, '{"text":"You already own this perk.","color":"yellow"}')
	deny_not_enough_points: str = ZombiesCommon.deny_not_enough_points_cmd(ns, version, "#pk_price")

	## Right-click handler (executor: "source" = player)
	write_versioned_function("zombies/perks/on_right_click", f"""
# Guard: game must be active
{ZombiesCommon.game_active_guard_cmd(ns)}

# Check power requirement. Quick Revive is exempt while solo (Black Ops rule).
execute store result score #pk_power {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.perk.power
execute store result score #qr_solo {ns}.data if entity @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator]
execute if score #pk_power {ns}.data matches 1 unless score #zb_power {ns}.data matches 1 unless entity @n[tag=bs.interaction.target,tag={ns}.pk_quick_revive] run return run {deny_requires_power}
execute if score #pk_power {ns}.data matches 1 unless score #zb_power {ns}.data matches 1 if entity @n[tag=bs.interaction.target,tag={ns}.pk_quick_revive] if score #qr_solo {ns}.data matches 2.. run return run {deny_requires_power}

# Look up perk_id
execute store result storage {ns}:temp _pk_buy.id int 1 run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.perk.id
function {ns}:v{version}/zombies/perks/lookup_perk with storage {ns}:temp _pk_buy

# Check if player already has this perk
function {ns}:v{version}/zombies/perks/check_owned with storage {ns}:temp _pk_data
execute if score #pk_owned {ns}.data matches 1 run return run {deny_already_owned}

# Get price and check points (chip-in machines charge one chunk per click)
function {ns}:v{version}/zombies/perks/read_price with storage {ns}:temp _pk_data
execute unless score @s {ns}.zb.points >= #pk_price {ns}.data run return run {deny_not_enough_points}

# Deduct points
scoreboard players operation @s {ns}.zb.points -= #pk_price {ns}.data

# Chip-in: progress is LOCAL, each player pays down their own perk. Stop here unless this
# payment was the one that completed it.
scoreboard players operation #pk_paid {ns}.data += #pk_price {ns}.data
execute if score #pk_partial {ns}.data matches 1.. run function {ns}:v{version}/zombies/perks/store_progress with storage {ns}:temp _pk_data
execute if score #pk_partial {ns}.data matches 1.. if score #pk_paid {ns}.data < #pk_total {ns}.data run return run function {ns}:v{version}/zombies/perks/announce_progress

# Apply perk effect (sets scoreboard + calls specific perk function)
function {ns}:v{version}/zombies/perks/apply with storage {ns}:temp _pk_data

# Signal
function #{ns}:zombies/on_new_perk

# Sound
{ZombiesFeedback.zb_sound('success')}
""")  # noqa: E501

	write_versioned_function("zombies/perks/lookup_perk", f"""
$data modify storage {ns}:temp _pk_data set from storage {ns}:zombies perk_data."$(id)"
""")

	hover_name_lines: str = "\n".join(
		f'execute unless data storage {ns}:temp _pk_data.name if data storage {ns}:temp _pk_data{{perk_id:"{perk_id}"}} run data modify storage {ns}:temp _pk_hover_name set value "{perk_data.display_name}"'  # noqa: E501
		for perk_id, perk_data in PERK_DEFINITIONS.items()
	)
	write_versioned_function("zombies/perks/get_hover_name", f"""
data modify storage {ns}:temp _pk_hover_name set value "Perk"
execute if data storage {ns}:temp _pk_data.name run data modify storage {ns}:temp _pk_hover_name set from storage {ns}:temp _pk_data.name
{hover_name_lines}
""")

	write_versioned_function("zombies/perks/check_owned", f"""
scoreboard players set #pk_owned {ns}.data 0
$execute if score @s {ns}.zb.perk.$(perk_id) matches 1 run scoreboard players set #pk_owned {ns}.data 1
""")

	# Price of the next click on the hovered machine; $(perk_id) selects the player's chip-in progress.
	# #pk_total is the full price, #pk_price what THIS click costs, #pk_paid the progress so far.
	write_versioned_function("zombies/perks/read_price", f"""
execute store result score #pk_price {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.perk.price
execute store result score #pk_partial {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.perk.partial
$execute store result score #pk_paid {ns}.data run scoreboard players get @s {ns}.zb.perkpaid.$(perk_id)
scoreboard players operation #pk_total {ns}.data = #pk_price {ns}.data

# Remaining, clamped at 0: solo Quick Revive rewrites the price live, so it can drop below the
# progress already paid. Clamping makes that last click free instead of refunding points.
scoreboard players operation #pk_left {ns}.data = #pk_total {ns}.data
scoreboard players operation #pk_left {ns}.data -= #pk_paid {ns}.data
execute if score #pk_left {ns}.data matches ..0 run scoreboard players set #pk_left {ns}.data 0

# Fixed chunks, last one is the remainder
execute if score #pk_partial {ns}.data matches 1.. run scoreboard players operation #pk_price {ns}.data = #pk_partial {ns}.data
execute if score #pk_partial {ns}.data matches 1.. run scoreboard players operation #pk_price {ns}.data < #pk_left {ns}.data
""")

	write_versioned_function("zombies/perks/store_progress", f"""
$scoreboard players operation @s {ns}.zb.perkpaid.$(perk_id) = #pk_paid {ns}.data
""")

	## Chip-in payment that didn't finish the perk (@s = paying player, _pk_data = the machine's perk)
	write_versioned_function("zombies/perks/announce_progress", f"""
function {ns}:v{version}/zombies/perks/get_hover_name
tellraw @s [{MGS_TAG},{{"text":"🥤 ","color":"dark_purple"}},{{"storage":"{ns}:temp","nbt":"_pk_hover_name","color":"light_purple","interpret":true}},{{"text":": ","color":"gray"}},{{"score":{{"name":"#pk_paid","objective":"{ns}.data"}},"color":"green"}},{{"text":"/","color":"gray"}},{{"score":{{"name":"#pk_total","objective":"{ns}.data"}},"color":"yellow"}},{{"text":" points paid","color":"gray"}}]
{ZombiesFeedback.zb_sound('refill')}
""")  # noqa: E501

