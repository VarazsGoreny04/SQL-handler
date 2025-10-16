from typing import Self, Callable
from datetime import date

class InputHandler:
	
	def __init__(self: Self) -> None:
		raise NotImplementedError("This method needs to be implemented in a subclass!")

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

		if not self.caseSensitive:
			text = text.lower()

		for option in self.options:
			if (option if self.caseSensitive else option.lower()) == text:
				return option
		
		return None
	
class YesNoInputHandler(MultiOptionInputHandler):

	def __init__(self: Self) -> None:
		super().__init__(["yes", "no"], False)
	
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
	
class FunctionBasedInputHandler(InputHandler):

	def __init__(self: Self, func: Callable[[str], bool]) -> None:
		self.func = func

	def input(self: Self) -> str | None:
		text = input()

		return (text if self.func(text) else None)
	
class StringWithExactLengthInputHandler(FunctionBasedInputHandler):

	def __init__(self: Self, length: int) -> None:
		super().__init__(lambda text: len(text) == length)
		
class StringWithRangeLengthInputHandler(FunctionBasedInputHandler):

	def __init__(self: Self, minLength: int, maxLength: int) -> None:
		super().__init__(lambda text: minLength <= len(text) <= maxLength)