""" Shared helpers for the functional generators, one class per concern.

Each submodule owns one class: [scores.SpecialScores], [lifecycle.GameLifecycle], [content.SharedContent],
[ranked.RankedStats], [text.Text] and [dialogs.Dialogs].
"""
# Constants
MGS_TAG: str = r'[{"text":"","color":"gold"},"[",{"text":"MGS"},"] "]'
""" The [MGS] chat prefix as a nested list component, gold and lang-safe.

Use it inside a tellraw array: tellraw @s ["",{MGS_TAG},...].
The brackets and the trailing space are raw strings so the lang plugin never matches them, while {"text":"MGS"} becomes {"translate":"mgs"} resolving to "MGS".
"""
