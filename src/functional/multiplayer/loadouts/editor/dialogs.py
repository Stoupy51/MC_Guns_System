""" The shared submenu skeleton every static action list is poured into. """
# Imports
from stewbeet import Mem, write_versioned_function

from ..catalogs import PICK10_TOTAL, TRIG_HUB


# Functions
def write_editor_dialog_base() -> None:
	ns: str = Mem.ctx.project_id

	## Shared dialog builder (static action lists, points in body, Back → hub) One shared skeleton for all thirteen "points line + static action list" submenus.
	## Title and hint ride in as whole text components inside single-quoted SNBT so they substitute raw and auto.lang_file still lifts their English out.
	## The action list stays a literal in each caller: its tooltips contain \n and \uXXXX escapes that a nested SNBT string would eat.
	write_versioned_function("multiplayer/editor/show_static_dialog", f"""$data modify storage {ns}:temp dialog set value {{\
type:"minecraft:multi_action",\
title:$(title),\
body:[{{\
type:"minecraft:plain_message",\
contents:["",["",{{"text":"Points remaining"}},": "],{{"text":"$(pts)","color":"gold","bold":true}},{{"text":" / {PICK10_TOTAL}","color":"dark_gray"}}]\
}},{{\
type:"minecraft:plain_message",\
contents:$(hint)\
}}],\
actions:[],\
columns:$(columns),\
after_action:"close",\
exit_action:{{label:"Back",action:{{type:"run_command",command:"/trigger {ns}.player.config set {TRIG_HUB}"}}}}\
}}
""")

