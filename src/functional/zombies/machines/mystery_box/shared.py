""" Move animation timings, the frame of a turned box and the owned-gun predicate. """
# Imports
import math
from collections.abc import Callable

from stewbeet import Mem

# Constants
MOVE_BEAR_TICKS: int = 30
""" Bear visible before ascend starts. """
MOVE_ASCEND_TICKS: int = 80
""" Ascend at old location. """
MOVE_WAIT_TICKS: int = 100
""" 5-second wait before descending. """
MOVE_DESCEND_TICKS: int = 70
""" Descend at new location. """
MOVE_TOTAL_TICKS: int = MOVE_BEAR_TICKS + MOVE_ASCEND_TICKS + MOVE_WAIT_TICKS + MOVE_DESCEND_TICKS
""" 280. """

MONKEY_BOMB_WEIGHT: int = 1
""" The monkey is not in the weapon catalog, so its box weight is set here, equal to every weapon's. """

RAY_GUN_DRY_PULLS: int = 5
""" Pulls without a Ray Gun after which it counts double, until round 25 (BO1 `default_ray_gun_weighting_func`). """

MB_SCALE: float = 2.4
""" Uniform scale of the two item_displays a presence box is made of.
The chest model is full-width, so 2.4 makes the box about 2.4 blocks across.
"""
LID_OPEN_ROTATION: tuple[float, float, float, float] = (-0.766, 0.0, 0.0, 0.643)
LID_OPEN_TRANSLATION: tuple[float, float, float] = (0.0, 0.415, -0.652)
""" The open lid, hinged about 100 degrees about X at its front-bottom edge, like a real chest opening toward the front.
An item_display rotates about the model centre, so the translation cancels that out to keep the hinge edge fixed
(T = p - R p, with p = (0, -0.15, -0.6) the hinge's scaled offset from the centre).
"""

ROLLS: int = 4
""" A box's roll is a whole number of quarter turns about its front axis, kept on its entities as mb.roll 0 to 3. """
QUARTER_TURNS: tuple[tuple[int, int], ...] = ((1, 0), (0, 1), (-1, 0), (0, -1))
""" Cosine and sine of each roll. """

PIVOT: str = "~ ~0.5 ~"
""" A box turns about the centre of the block of its map position, so a box flipped under a ceiling hangs from it. """
CENTER: tuple[float, float, float] = (0.0, 0.6, 0.3)
""" From that pivot to the centre of the box, in the box's frame. """
INTERACTION_LIFT: float = 0.9
""" The box's interaction stands this far above its centre, in world Y: interactions do not turn, so it straddles the box. """

PULL_DROP: float = 0.6
""" The pull display starts this far below the box's centre, inside the box, and floats up from there. """


# Functions
def box_offset(roll: int, x: float, y: float, z: float) -> str:
	""" Caret coordinates of a vector given in the frame of a box rolled by roll quarter turns.

	The execution rotation must be the box's yaw and pitch, since a display's own frame is the caret frame.

	>>> box_offset(1, 0.0, 1.1, 0.3)
	'^-1.1 ^ ^0.3'
	"""
	cos, sin = QUARTER_TURNS[roll]
	return " ".join(f"^{round(v, 4) + 0.0:g}" if v else "^" for v in (x * cos - y * sin, x * sin + y * cos, z))


def box_transformation(
	roll: int,
	translation: tuple[float, float, float] = (0.0, 0.0, 0.0),
	rotation: tuple[float, float, float, float] = (0.0, 0.0, 0.0, 1.0),
	scale: float = MB_SCALE,
) -> str:
	""" Transformation of a box part given in the frame of a box rolled by roll quarter turns, its roll folded in.

	>>> box_transformation(2, translation=(0.0, -0.6, 0.0), scale=0.4)
	'{left_rotation:[0f,0f,1f,0f],right_rotation:[0f,0f,0f,1f],translation:[0f,0.6f,0f],scale:[0.4f,0.4f,0.4f]}'
	"""
	cos, sin = QUARTER_TURNS[roll]
	half_sin, half_cos = math.sin(roll * math.pi / 4), math.cos(roll * math.pi / 4)
	x, y, z = translation
	qx, qy, qz, qw = rotation
	turned: tuple[float, ...] = (x * cos - y * sin, x * sin + y * cos, z)
	quaternion: tuple[float, ...] = (
		half_cos * qx - half_sin * qy, half_cos * qy + half_sin * qx, half_cos * qz + half_sin * qw, half_cos * qw - half_sin * qz,
	)
	def floats(values: tuple[float, ...]) -> str:
		return "[" + ",".join(f"{round(v, 4) + 0.0:g}f" for v in values) + "]"
	return (
		f"{{left_rotation:{floats(quaternion)},right_rotation:[0f,0f,0f,1f],"
		f"translation:{floats(turned)},scale:{floats((scale, scale, scale))}}}"
	)


def per_roll(command: Callable[[int], str]) -> str:
	""" One line per roll, running command(roll) as an entity whose mb.roll is that roll. """
	ns: str = Mem.ctx.project_id
	return "\n".join(f"execute if score @s {ns}.mb.roll matches {roll} run {command(roll)}" for roll in range(ROLLS))

def owned_gun_macro_cd(ns: str) -> str:
	""" Custom-data predicate matching any gun whose base weapon is the macro's $(weapon_id).

	Returns:
		str: The body of a `custom_data~` item predicate, braces included.

	>>> owned_gun_macro_cd("mgs")
	'{mgs:{gun:true,stats:{base_weapon:"$(weapon_id)"}}}'
	"""
	return "{" + ns + ':{gun:true,stats:{base_weapon:"$(weapon_id)"}}}'

