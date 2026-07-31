""" The round-result announce, shared by both bomb modes.

Search & Destroy and Demolition both close a round the same way: name the side that took it, and pay both
sides — more to the winners, never nothing to the losers. Only the wording differs, so the four win functions
across the two modes all come through here.
"""
# Imports
from ....helpers import MGS_TAG
from ....progression import Xp

# Constants
TEAMS: dict[int, tuple[str, str]] = {1: ("Red", "red"), 2: ("Blue", "blue")}
""" Team score value mapped to its display name and colour. """


# Classes
class RoundXp:
	""" The result announce for one closed bomb round. """

	# Functions
	@staticmethod
	def result_lines(ns: str, attackers_score: str, attackers_won: bool, note: str) -> str:
		""" Return the announce and XP for a round, branching on which side was attacking.

		Args:
			ns              (str):  Project namespace.
			attackers_score (str):  Fake player holding the attacking team, ex: "#snd_attackers".
			attackers_won   (bool): True when the attacking side took the round.
			note            (str):  Text after the team name, ex: "destroyed both sites!".
		Returns:
			str: Four commands per attacking side, so eight lines.

		Examples:
			>>> len(RoundXp.result_lines("mgs", "#snd_attackers", True, "win!").splitlines())
			8
		"""
		blocks: list[str] = []
		for attacker_id in TEAMS:
			winner_id: int = attacker_id if attackers_won else 3 - attacker_id
			name, color = TEAMS[winner_id]
			blocks.append(Xp.announce_teams(
				side="mp",
				body=f'{MGS_TAG},{{"text":"{name}","color":"{color}"}},{{"text":" {note}","color":"yellow"}}',
				win_key="round_win",
				winners=f"@a[scores={{{ns}.mp.team={winner_id},{ns}.mp.in_game=1}}]",
				loss_key="round_loss",
				losers=f"@a[scores={{{ns}.mp.team={3 - winner_id},{ns}.mp.in_game=1}}]",
				guard=f"if score {attackers_score} {ns}.data matches {attacker_id}",
			))
		return "\n".join(blocks)
