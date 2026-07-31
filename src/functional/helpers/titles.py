""" How long each kind of title stays on screen.

`title <player> times` is per-player STATE, not part of the message: it persists until something sets it
again. A title that omits it therefore inherits whatever the previous one used — which is how a death notice
ended up wearing the GAME OVER banner's four-second stay, and how a per-tick hover tooltip ended up fading in
over half a second and smearing.

So every site that *displays* a title sets its timing first. Sites that only update a subtitle do not: a
subtitle packet does not re-trigger the display, so the timing belongs to the title that opened it — see
`RESPAWN`, whose stay is sized to outlast the countdown that writes into it.
"""
# Imports
from dataclasses import dataclass


# Classes
@dataclass(frozen=True)
class TitleTiming:
	""" One `title times` triple, in ticks.

	Examples:
		>>> TitleTimes.HOVER.cmd()
		'title @s times 0 10 0'
		>>> TitleTimes.BANNER.cmd("@a[tag=mgs.x]")
		'title @a[tag=mgs.x] times 10 80 20'
	"""
	fade_in: int
	stay: int
	fade_out: int
	note: str

	def cmd(self, selector: str = "@s") -> str:
		""" Return the `title ... times` command for this timing.

		Args:
			selector (str): Who it applies to.
		Returns:
			str: One command.
		"""
		return f"title {selector} times {self.fade_in} {self.stay} {self.fade_out}"


class TitleTimes:
	""" Every title timing in the project, named by what the title is for rather than by its numbers. """

	# Constants
	HOVER: TitleTiming = TitleTiming(fade_in=0, stay=10, fade_out=0, note=(
		"Re-sent every tick while looking at something. No fade at either end: a fade-in never completes "
		"before the next packet replaces it, and a fade-out would leave the tooltip hanging after you look "
		"away. The 0.5s stay is what makes it vanish promptly instead of flickering between ticks."
	))
	HIT_DIRECTION: TitleTiming = TitleTiming(fade_in=0, stay=8, fade_out=6, note=(
		"The arc glyph flashed around the crosshair when you are hit. Instant, then gone in ~0.7s — any "
		"fade-in would land after the shot that caused it."
	))
	RESPAWN: TitleTiming = TitleTiming(fade_in=0, stay=70, fade_out=10, note=(
		"The death skull, whose subtitle the respawn countdown then rewrites second by second. The stay has "
		"to outlast that whole countdown (60 ticks) or the title fades out from under it."
	))
	BAD_NEWS: TitleTiming = TitleTiming(fade_in=0, stay=60, fade_out=20, note=(
		"Going down, bleeding out, falling out of the world. No fade-in: you already know it happened, and "
		"half a second of fade is half a second of not reading why."
	))
	EVENT: TitleTiming = TitleTiming(fade_in=5, stay=40, fade_out=15, note=(
		"Something good or notable happened to you — revived, gear recovered, a perk saved your life. Short "
		"fade-in is affordable here because nothing is urgent about it."
	))
	AFTERMATH: TitleTiming = TitleTiming(fade_in=3, stay=25, fade_out=10, note=(
		"The quiet follow-up to an EVENT, like Dying Wish ending. Deliberately briefer than what it follows "
		"so it reads as a footnote rather than a second announcement."
	))
	FREEZE: TitleTiming = TitleTiming(fade_in=5, stay=60, fade_out=10, note=(
		"The admin freeze overlay, re-sent while the freeze holds."
	))
	BANNER: TitleTiming = TitleTiming(fade_in=10, stay=80, fade_out=20, note=(
		"End of a game. The only place a long stay is right: there is nothing left to look at behind it."
	))
	FLASH_FULL: TitleTiming = TitleTiming(fade_in=5, stay=40, fade_out=20, note=(
		"A flashbang at close range. The fade-out IS the effect wearing off, so it is the longest here."
	))
	FLASH_WEAK: TitleTiming = TitleTiming(fade_in=2, stay=10, fade_out=10, note=(
		"A flashbang caught at the edge of its radius, or through a turned head."
	))
