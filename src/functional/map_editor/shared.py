""" The chat rule and the zombies element subset. """
# Imports
from ..map_editor_defs import ALL_ELEMENTS, ElementDef

# Constants
SEP: str = '{"text":"============================================","color":"dark_gray"}'
""" The horizontal rule every editor chat panel is framed with. """
ZB_ELEMENTS: dict[str, ElementDef] = {etype: einfo for etype, einfo in ALL_ELEMENTS.items() if einfo.save_type == "zb_object"}
""" The zombies elements, which share one placement handler and one compound layout in storage. """
GROUP_ID_ELEMENTS: tuple[str, ...] = ("zombie_spawn", "player_spawn_zb", "special_spawn")
""" The only elements carrying a group_id, the spawn group a door opens.
A door's link_id is its front-room group and back_group_id its back room; nothing else reads one. """

