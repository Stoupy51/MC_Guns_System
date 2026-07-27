""" The tuning constants behind the escort: its caps, radii and timeouts. """
# Constants
MAX_ESCORTS: int = 16
""" Max simultaneous escorts; stuck zombies beyond this use the teleport rescue instead. """

ESCORT_TTL: int = 900
""" Escort lifetime in ticks before the teleport-rescue fallback. Hard cap only: a trader that is
itself stuck is caught much earlier by the watchdog. """

WATCHDOG_GIVE_UP: int = 5
""" Seconds without leaving the current block before the escort gives up early. """

PATHFINDING_RANGE: int = 96
""" Escort trader follow_range. The budget scales live with this attribute (Mob.java
onAttributeUpdated): max A* nodes = value*16, region radius = value+8. The default 16 cannot afford
stair detours, so a trader whose target is on another floor hugs the closest point below it. """

RELEASE_RADIUS: int = 10
""" Hand back to vanilla zombie AI once an alive player is within this radius AND visible. """

PAP_ROOM_RADIUS: int = 14
LURE_RELEASE: int = 8
""" PaP-room lure: when every alive player is within PAP_ROOM_RADIUS of a PaP machine, escorts aim
at the map-defined lure centre instead of a player, spreading the horde to the middle of the map.
The centre is opt-in via the #<ns>:zombies/setup_lure tag; a map that registers nothing stays
inert. A lured zombie is released within LURE_RELEASE of the centre marker. """

RELEASE_RADIUS_CLOSE: int = 6
""" Release unconditionally within this radius: vanilla AI handles it even around corners, and the
visibility check aims at the player's FEET, which slabs or stairs can fail forever. """

TRADER_REACH_GUARD: int = 6
""" Radius of the "a trader must never be right-clickable" safeguard. Do NOT lower: reach is the
minecraft:entity_interaction_range attribute, which zombies raises to 5 (game.py), so the vanilla 3
does not apply. Monkey-bomb traders are exempt; their eaten click is recovered by the
right_click_entity advancement (weapon/common.py). """

MONKEY_RELEASE: int = 4
""" A monkey-escorted zombie stops riding and HOLDS within this many blocks of the thrown monkey,
so zombies spread along their approach paths instead of stacking — well inside the 7-block blast. """

