""" Hitscan firing: accuracy groups, spread, and the raycast that resolves a shot.  """
# Imports
from .accuracy import write_accuracy
from .clicks import write_click_handling
from .hits import write_hit_resolution


# Functions
def main() -> None:
	write_click_handling()
	write_hit_resolution()
	write_accuracy()

