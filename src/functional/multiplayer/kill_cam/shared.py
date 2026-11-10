""" The kill cam's tunables and the probe that both recording and playback move around. """
# Imports
import uuid

# Constants
CHAIN_GAP: int = 80
""" Longest pause between two kills of one streak, in ticks (4 s). """
MAX_CHAIN: int = 6
""" Most kills a replay shows: the window opens this many kills short of the score limit. """
PRE_ROLL: int = 40
""" Ticks shown before the first kill of the chain. """
POST_ROLL: int = 30
""" Ticks shown after the final kill, holding the last frame once the frames run out. """
RECORD_TICKS: int = PRE_ROLL + (MAX_CHAIN - 1) * CHAIN_GAP
""" Frames the buffer keeps, the longest stretch a chain can need. """
INTRO_TICKS: int = 20
""" Ticks the first frame holds under the titles, the length of a mannequin's death animation:
the copies `multiplayer/death_animation` leaves cannot be selected, and are gone once it ends. """
EYE_HEIGHT: float = 1.62
""" Camera height above the killer's recorded feet. """
SNEAK_EYE_HEIGHT: float = 1.27
""" Camera height above the killer's recorded feet while they sneak. """
PROBE_UUID: str = "006d6773-0000-0000-0000-000000006b63"
""" The probe marker's fixed UUID, so a sample reaches it without a selector scan. """
PROBE_UUID_NBT: str = "[I;" + ",".join(str(int.from_bytes(uuid.UUID(PROBE_UUID).bytes[i:i + 4], signed=True)) for i in range(0, 16, 4)) + "]"
""" The same UUID as the int array `summon` takes.

>>> PROBE_UUID_NBT
'[I;7169907,0,0,27491]'
"""

