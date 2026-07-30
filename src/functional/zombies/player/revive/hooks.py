""" Resetting revive state on game start and stop. """
# Imports
from stewbeet import Mem, write_versioned_function


# Functions
def write_revive_hooks() -> None:
	ns: str = Mem.ctx.project_id

	# Hook: reset revive state on game start
	write_versioned_function("zombies/start", f"""
# Reset revive state
scoreboard players set @a {ns}.zb.downed 0
scoreboard players set @a {ns}.zb.bleed 0
scoreboard players set @a {ns}.zb.revive_p 0
scoreboard players set @a {ns}.zb.qr_uses 0
scoreboard players set @a {ns}.zb.downed_id 0
scoreboard players set #downed_id_next {ns}.data 0
tag @a remove {ns}.downed_spectator
tag @a remove {ns}.zb_qr_armed
kill @e[tag={ns}.downed_mannequin]
kill @e[tag={ns}.downed_hud]
kill @e[tag={ns}.downed_cam]
kill @e[tag={ns}.tombstone]
data modify storage {ns}:zombies tombstone_inv set value {{}}
""")

	## Hook: reset revive state on game stop
	write_versioned_function("zombies/stop", f"""
# Reset revive state
scoreboard players set @a {ns}.zb.downed 0
scoreboard players set @a {ns}.zb.bleed 0
scoreboard players set @a {ns}.zb.revive_p 0
scoreboard players set @a {ns}.zb.qr_uses 0
scoreboard players set @a {ns}.zb.downed_id 0
scoreboard players set #downed_id_next {ns}.data 0
tag @a remove {ns}.downed_spectator
tag @a remove {ns}.zb_qr_armed
kill @e[tag={ns}.downed_mannequin]
kill @e[tag={ns}.downed_hud]
kill @e[tag={ns}.downed_cam]
kill @e[tag={ns}.tombstone]
data modify storage {ns}:zombies tombstone_inv set value {{}}
""")

