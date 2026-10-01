""" The shared submenu skeleton every static action list is poured into. """
# Imports
from stewbeet import Mem, write_versioned_function

from .....config.catalogs import PICK10_TOTAL, TRIG_HUB


# Functions
def write_editor_dialog_base() -> None:
	ns: str = Mem.ctx.project_id

	## One skeleton for the thirteen "points line + static actions" submenus. Title and hint are whole components in single-quoted SNBT,
	## so auto.lang_file still translates them; the action list stays literal, since its \n and \uXXXX escapes would not survive nesting.
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

