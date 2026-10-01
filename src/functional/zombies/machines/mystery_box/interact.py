""" Right- and left-clicking a box: usability, sharing a pull and dispatching on its state. """
# Imports
from stewbeet import Mem, write_versioned_function

from ....core.feedback import ZombiesFeedback
from ....helpers import MGS_TAG
from ....helpers.text import Text
from ...common import ZombiesCommon


# Functions
def write_mystery_box_interaction() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	deny_moving: str = ZombiesCommon.deny_cmd(ns, version, '{"text":"The Mystery Box is moving...","color":"yellow"}')
	deny_already_in_use: str = ZombiesCommon.deny_cmd(ns, version, '{"text":"Mystery Box is already in use.","color":"red"}')
	deny_not_your_result: str = ZombiesCommon.deny_cmd(ns, version, '{"text":"Wait for the current player to collect their result.","color":"red"}')

	## Run as the player. Each box is an independent pull, so dispatch on the clicked box's state.
	write_versioned_function("zombies/mystery_box/on_right_click", f"""
# Usable: the active box, any box during a Fire Sale, or a box with a pull in progress (so a buyer can always collect).
scoreboard players set #mb_usable {ns}.data 0
execute if entity @e[tag=bs.interaction.target,tag={ns}.mystery_box_active] run scoreboard players set #mb_usable {ns}.data 1
execute if score #zb_fire_sale_timer {ns}.data matches 1.. if entity @e[tag=bs.interaction.target,tag={ns}.mb_fs_active] run scoreboard players set #mb_usable {ns}.data 1
execute at @n[tag=bs.interaction.target] if entity @n[tag={ns}.mb_display,distance=..3] run scoreboard players set #mb_usable {ns}.data 1
execute if score #mb_usable {ns}.data matches 0 run return fail

execute unless data storage {ns}:zombies game{{state:"active"}} run return fail

# The active box can be moving.
execute if score #mb_move_timer {ns}.data matches 1.. if entity @e[tag=bs.interaction.target,tag={ns}.mystery_box_active] run return run {deny_moving}

# Dispatched at the box position.
scoreboard players operation #cur_box {ns}.data = @n[tag=bs.interaction.target] {ns}.mb.box
execute at @n[tag=bs.interaction.target] run function {ns}:v{version}/zombies/mystery_box/box_click
""")

	## Shift + left click hands your finished pull to the team. Run as the player.
	write_versioned_function("zombies/mystery_box/on_left_click", f"""
# A plain left click is a normal swing.
execute unless predicate {ns}:v{version}/is_sneaking run return fail
execute unless data storage {ns}:zombies game{{state:"active"}} run return fail
execute at @n[tag=bs.interaction.target] run function {ns}:v{version}/zombies/mystery_box/share_at_box
""")

	## Run as the player, at the box.
	write_versioned_function("zombies/mystery_box/share_at_box", f"""
# A spinning pull has no weapon yet.
execute unless entity @n[tag={ns}.mb_display,distance=..3] run return fail
execute if entity @n[tag={ns}.mb_display,distance=..3,scores={{{ns}.mb.anim=1..}}] run return fail

# Sharing twice does nothing.
execute if entity @n[tag={ns}.mb_display,distance=..3,tag={ns}.mb_shared] run return fail

execute unless score @s {ns}.mb.pid = @n[tag={ns}.mb_display,distance=..3] {ns}.mb.buyer run return run {deny_not_your_result}

tag @n[tag={ns}.mb_display,distance=..3] add {ns}.mb_shared
{ZombiesFeedback.zb_sound('success')}
tellraw @a[scores={{{ns}.zb.in_game=1}}] [{MGS_TAG},{Text.player(ns, "@s", side="zb")},{{"text":" shared their Mystery Box weapon: anyone can take it!","color":"green"}}]
""")

	## Run as the player, at the box.
	write_versioned_function("zombies/mystery_box/box_click", f"""
execute if entity @n[tag={ns}.mb_display,distance=..3,scores={{{ns}.mb.anim=1..}}] run return run {deny_already_in_use}

# Shared by its buyer: anyone may collect.
execute if entity @n[tag={ns}.mb_display,distance=..3,tag={ns}.mb_shared] run return run function {ns}:v{version}/zombies/mystery_box/collect

# Ready: only its buyer may collect.
execute if entity @n[tag={ns}.mb_display,distance=..3] if score @s {ns}.mb.pid = @n[tag={ns}.mb_display,distance=..3] {ns}.mb.buyer run return run function {ns}:v{version}/zombies/mystery_box/collect
execute if entity @n[tag={ns}.mb_display,distance=..3] run return run {deny_not_your_result}

function {ns}:v{version}/zombies/mystery_box/try_use
""")

