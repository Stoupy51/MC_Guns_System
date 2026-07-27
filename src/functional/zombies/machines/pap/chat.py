""" The detailed upgrade summary printed in chat, one lore line at a time. """
# ruff: noqa: E501
# Imports
from stewbeet import Mem, write_versioned_function

from ....helpers import MGS_TAG


# Functions
def write_pap_chat() -> None:
	ns: str = Mem.ctx.project_id
	version: str = Mem.ctx.project_version

	# Macro: send one lore-line compound as a tellraw text component (with prefix).
	write_versioned_function("zombies/pap/pap_chat_lore_line", """$tellraw @s [{"text":"- ","color":"gray"},$(line)]\n""")

	# Macro: copy lore[$(index)] to _pap_lore_line.line and display if non-empty.
	write_versioned_function("zombies/pap/pap_chat_lore_iter", f"""
$data modify storage {ns}:temp _pap_lore_line.line set from storage {ns}:temp _pap_extract.lore[$(index)]
execute if data storage {ns}:temp _pap_lore_line.line unless data storage {ns}:temp _pap_lore_line.line{{text:""}} run function {ns}:v{version}/zombies/pap/pap_chat_lore_line with storage {ns}:temp _pap_lore_line
""")

	# Loop: iterates indices 0 .. #pap_lore_len-1, calling pap_chat_lore_iter each step.
	write_versioned_function("zombies/pap/pap_chat_lore_loop", f"""
execute store result storage {ns}:temp _pap_lore_idx.index int 1 run scoreboard players get #pap_li {ns}.data
function {ns}:v{version}/zombies/pap/pap_chat_lore_iter with storage {ns}:temp _pap_lore_idx
scoreboard players add #pap_li {ns}.data 1
execute if score #pap_li {ns}.data < #pap_lore_len {ns}.data run function {ns}:v{version}/zombies/pap/pap_chat_lore_loop
""")

	# Detailed PAP upgrade chat message.
	pap_chat_lines: list[str] = [
		f'tellraw @s [{MGS_TAG},{{"text":"Machine: ","color":"gray"}},{{"storage":"{ns}:temp","nbt":"_pap_machine.name","color":"gold","italic":false,"interpret":true}},{{"text":"\\nLevel: ","color":"gray"}},{{"score":{{"name":"#pap_next","objective":"{ns}.data"}},"color":"aqua"}},{{"text":"/","color":"dark_gray"}},{{"score":{{"name":"#pap_max","objective":"{ns}.data"}},"color":"aqua"}},{{"text":"  Cost: -","color":"gray"}},{{"score":{{"name":"#pap_price","objective":"{ns}.data"}},"color":"yellow"}},{{"text":" points","color":"gray"}}]',
		'tellraw @s [{"text":"Weapon stats:","color":"gray","italic":true}]',
		# Compute (len - 2) to skip the last 2 entries (switch time + empty separator)
		f'execute store result score #pap_lore_len {ns}.data run data get storage {ns}:temp _pap_extract.lore',
		f'scoreboard players remove #pap_lore_len {ns}.data 2',
		f'scoreboard players set #pap_li {ns}.data 0',
		f'execute if score #pap_li {ns}.data < #pap_lore_len {ns}.data run function {ns}:v{version}/zombies/pap/pap_chat_lore_loop',
	]
	write_versioned_function("zombies/pap/pap_chat_message", "\n".join(pap_chat_lines))

