""" Buying a perk: the power, ownership and points guards, and the chip-in payment flow. """
# Imports
from stewbeet import Mem, write_versioned_function

from ....core.feedback import ZombiesFeedback
from ....helpers import MGS_TAG
from ...common import ZombiesCommon
from ...player.revive.shared import SOLO_QR_MAX
from .definitions import PERK_DEFINITIONS


# Functions
def write_perk_purchase() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	deny_requires_power: str = ZombiesCommon.deny_cmd(ns, version, '{"text":"This perk machine requires power.","color":"red"}')
	deny_already_owned: str = ZombiesCommon.deny_cmd(ns, version, '{"text":"You already own this perk.","color":"yellow"}')
	deny_qr_exhausted: str = ZombiesCommon.deny_cmd(ns, version, f'{{"text":"Quick Revive is spent ({SOLO_QR_MAX}/{SOLO_QR_MAX} self-revives used this game).","color":"yellow"}}')
	deny_not_enough_points: str = ZombiesCommon.deny_not_enough_points_cmd(ns, version, "#pk_price")

	## Run as the player.
	write_versioned_function("zombies/perks/on_right_click", f"""
{ZombiesCommon.game_active_guard_cmd(ns)}

# Quick Revive needs no power while solo (Black Ops rule).
execute store result score #pk_power {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.perk.power
execute store result score #qr_solo {ns}.data if entity @a[scores={{{ns}.zb.in_game=1}},gamemode=!spectator]
execute if score #pk_power {ns}.data matches 1 unless score #zb_power {ns}.data matches 1 unless entity @n[tag=bs.interaction.target,tag={ns}.pk_quick_revive] run return run {deny_requires_power}
execute if score #pk_power {ns}.data matches 1 unless score #zb_power {ns}.data matches 1 if entity @n[tag=bs.interaction.target,tag={ns}.pk_quick_revive] if score #qr_solo {ns}.data matches 2.. run return run {deny_requires_power}

execute store result storage {ns}:temp _pk_buy.id int 1 run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.perk.id
function {ns}:v{version}/zombies/perks/lookup_perk with storage {ns}:temp _pk_buy

function {ns}:v{version}/zombies/perks/check_owned with storage {ns}:temp _pk_data
execute if score #pk_owned {ns}.data matches 1 run return run {deny_already_owned}

# At most {SOLO_QR_MAX} solo self-revives per game, counted on qr_uses.
execute if entity @n[tag=bs.interaction.target,tag={ns}.pk_quick_revive] if score @s {ns}.zb.qr_uses matches {SOLO_QR_MAX}.. run return run {deny_qr_exhausted}

# Chip-in machines charge one chunk per click.
function {ns}:v{version}/zombies/perks/read_price with storage {ns}:temp _pk_data
execute unless score @s {ns}.zb.points >= #pk_price {ns}.data run return run {deny_not_enough_points}

scoreboard players operation @s {ns}.zb.points -= #pk_price {ns}.data

# Chip-in progress is per player: stop unless this payment completed it.
scoreboard players operation #pk_paid {ns}.data += #pk_price {ns}.data
execute if score #pk_partial {ns}.data matches 1.. run function {ns}:v{version}/zombies/perks/store_progress with storage {ns}:temp _pk_data
execute if score #pk_partial {ns}.data matches 1.. if score #pk_paid {ns}.data < #pk_total {ns}.data run return run function {ns}:v{version}/zombies/perks/announce_progress

function {ns}:v{version}/zombies/perks/apply with storage {ns}:temp _pk_data

function #{ns}:zombies/on_new_perk

{ZombiesFeedback.zb_sound('success')}
""")

	write_versioned_function("zombies/perks/lookup_perk", f"""
$data modify storage {ns}:temp _pk_data set from storage {ns}:zombies perk_data."$(id)"
""")

	hover_name_lines: str = "\n".join(
		f'execute unless data storage {ns}:temp _pk_data.name if data storage {ns}:temp _pk_data{{perk_id:"{perk_id}"}} run data modify storage {ns}:temp _pk_hover_name set value "{perk_data.display_name}"'
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

	# Price of the next click: $(perk_id) selects the player's chip-in progress. #pk_total full price, #pk_price this click, #pk_paid the progress.
	write_versioned_function("zombies/perks/read_price", f"""
execute store result score #pk_price {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.perk.price
execute store result score #pk_partial {ns}.data run scoreboard players get @n[tag=bs.interaction.target] {ns}.zb.perk.partial
$execute store result score #pk_paid {ns}.data run scoreboard players get @s {ns}.zb.perkpaid.$(perk_id)
scoreboard players operation #pk_total {ns}.data = #pk_price {ns}.data

# Clamped at 0: solo Quick Revive changes the price live, so it can fall below the progress; the last click is then free.
scoreboard players operation #pk_left {ns}.data = #pk_total {ns}.data
scoreboard players operation #pk_left {ns}.data -= #pk_paid {ns}.data
execute if score #pk_left {ns}.data matches ..0 run scoreboard players set #pk_left {ns}.data 0

execute if score #pk_partial {ns}.data matches 1.. run scoreboard players operation #pk_price {ns}.data = #pk_partial {ns}.data
execute if score #pk_partial {ns}.data matches 1.. run scoreboard players operation #pk_price {ns}.data < #pk_left {ns}.data
""")

	write_versioned_function("zombies/perks/store_progress", f"""
$scoreboard players operation @s {ns}.zb.perkpaid.$(perk_id) = #pk_paid {ns}.data
""")

	## Run as the paying player, when the chunk did not finish the perk.
	write_versioned_function("zombies/perks/announce_progress", f"""
function {ns}:v{version}/zombies/perks/get_hover_name
tellraw @s [{MGS_TAG},{{"text":"🥤 ","color":"white"}},{{"storage":"{ns}:temp","nbt":"_pk_hover_name","color":"light_purple","interpret":true}},{{"text":": ","color":"gray"}},{{"score":{{"name":"#pk_paid","objective":"{ns}.data"}},"color":"green"}},{{"text":"/","color":"gray"}},{{"score":{{"name":"#pk_total","objective":"{ns}.data"}},"color":"yellow"}},{{"text":" points paid","color":"gray"}}]
{ZombiesFeedback.zb_sound('refill')}
""")

