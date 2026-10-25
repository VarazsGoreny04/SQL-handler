from abc import ABC, abstractmethod
from typing import Self, Callable
from datetime import date

class InputHandler(ABC):
	"""An abstract class for input handling."""

	@abstractmethod
	def __init__(self: Self) -> None:
		"""Creates an InputHandler."""
		
		pass

	@abstractmethod
	def input(self: Self) -> str | None:
		"""
		Asks for an input.

		Returns:
			str | None: The input.
		"""

		pass

	def input_while_none(self: Self, errorMessage: str) -> str:
		"""
		Asks for an input until it is a string.

		Returns:
			str: The input.
		"""

		text: str | None = self.input()

		while text is None:
			print(errorMessage)
			text = self.input()

		return text

class MultiOptionInputHandler(InputHandler):
	"""A class for multi-option input handling."""

	def __init__(self: Self, options: set[str], caseSensitive: bool = True) -> None:
		"""
		Creates a MultiOptionInputHandler.

		Parameters:
			options (set[str]): The input options.
			caseSensitive (bool): The case sensitivity of the input. (default is True)
		"""

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
	"""A class for yes/no input handling."""

	def __init__(self: Self) -> None:
		"""Creates a YesNoInputHandler."""

		super().__init__(["yes", "no"], False)
	
class DateInputHandler(InputHandler):
	"""A class for date input handling."""

	def __init__(self: Self) -> None:
		"""Creates a DateInputHandler."""

		pass
	
	def input(self: Self) -> str | None:
		try:
			return date.fromisoformat(input())
		except ValueError:
			return None
		
class IntInputHandler(InputHandler):
	"""A class for integer input handling."""

	def __init__(self: Self) -> None:
		"""Creates a IntInputHandler."""

		pass
	
	def input(self: Self) -> str | None:
		try:
			return int(input())
		except ValueError:
			return None
	
class FunctionBasedInputHandler(InputHandler):
	"""A class for function-based input handling."""

	def __init__(self: Self, func: Callable[[str], bool]) -> None:
		"""
		Creates a FunctionBasedInputHandler.

		Parameters:
			func (Callable[[str], bool]): A predicate that decides weather the input is correct or not.
		"""

		self.func = func

	def input(self: Self) -> str | None:
		text = input()

		return (text if self.func(text) else None)
	
class StringWithExactLengthInputHandler(FunctionBasedInputHandler):
	"""A class for string input handling with a predetermined size."""

	def __init__(self: Self, length: int) -> None:
		"""
		Creates a StringWithExactLengthInputHandler.

		Parameters:
			length (int): The length of the input.
		"""

		super().__init__(lambda text: len(text) == length)
		
class StringWithRangeLengthInputHandler(FunctionBasedInputHandler):

	def __init__(self: Self, minLength: int, maxLength: int) -> None:
		"""
		Creates a StringWithExactLengthInputHandler.

		Parameters:
			length (int): The length of the input.
		"""
		
		super().__init__(lambda text: minLength <= len(text) <= maxLength)