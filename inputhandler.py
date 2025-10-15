from typing import Self
from datetime import date

class InputHandler:

	def input(self: Self) -> str | None:
		raise NotImplementedError("This method needs to be implemented in a subclass!")

	def input_while_none(self: Self, errorMessage: str) -> str:
		text: str | None = self.input()

		while text is None:
			print(errorMessage)
			text = self.input()

		return text

class MultiOptionInputHandler(InputHandler):
	
	def __init__(self: Self, options: set[str], caseSensitive = True) -> None:
		self.caseSensitive = caseSensitive
		self.options = options

	def input(self: Self) -> str | None:
		text = input()

		if self.caseSensitive:
			text = text.lower()

		for option in ([option.lower() for option in self.options] if self.caseSensitive else self.options):
			if text == option:
				return text
		
		return None
	
"""class FunctionBasedInputHandler(InputHandler):

	def __init__(self: Self, func: function, caseSensitive = True) -> None:
		self.caseSensitive = caseSensitive
		self.func = func

	def input(self: Self) -> str | None:
		text = input()

		if self.caseSensitive:
			text = text.lower()

		return (text if self.func(text) else None)"""
	
class DateInputHandler(InputHandler):

	def __init__(self: Self) -> None:
		pass
	
	def input(self: Self) -> str | None:
		try:
			return date.fromisoformat(input())
		except ValueError:
			return None
		
class IntInputHandler(InputHandler):

	def __init__(self: Self) -> None:
		pass
	
	def input(self: Self) -> str | None:
		try:
			return int(input())
		except ValueError:
			return None