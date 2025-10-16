from os import system, name
from typing import Self
from sqlite3 import Connection, connect
from menupoint import *

class Menu:

	def __init__(self: Self, database: Connection | None = None, menuPoints: set[MenuPoint] | None = None) -> None:
		self.database = database
		self.menuPoints = menuPoints

	def create_options(self: Self) -> set[MenuPoint]:
		return [
			ListDatabaseInfoPoint(self.database),
			ListAllTableNamesPoint(self.database),
			ListAllTablesPoint(self.database),
			ListTableByNamePoint(self.database),
			InsertRecordPoint(self.database),
			ExitPoint(self.database)
		]

	def open_database(self: Self) -> None:
		print("Give the file path of the .db file: ")
		file_path: str = StringWithRangeLengthInputHandler(1, 1024).input_while_none("\nIncorrect format! Try again!")
		print("\n")

		self.database = connect(file_path)

	def manage_database(self: Self) -> None:
		if self.database is None:
			return
		
		self.menuPoints = self.create_options()
		options: set[str] = [menuPoint.name for menuPoint in self.menuPoints]
		longestOption = max([len(option) for option in options])
		
		text: str = ""
		while text != "exit":
			print("What would you like to do?")
			for menuPoint in self.menuPoints:
				print(menuPoint.str_withpadding(longestOption - len(menuPoint.name)))

			text = MultiOptionInputHandler(options, False).input_while_none("\nNo such menu point exists! Try again!")
			print("\n")

			for menuPoint in self.menuPoints:
				if menuPoint.name == text:
					menuPoint.run()

	def close_database(self: Self) -> None:
		self.menuPoints = None

		self.database.commit()
		self.database = self.database.close()

	def run(self: Self) -> None:
		system('cls' if name == 'nt' else 'clear')

		text: str = "open"
		while text != "exit":
			self.open_database()	
			self.manage_database()
			self.close_database()

			print("Would you like to |open| another database, or do you want to |exit|?")
			text = MultiOptionInputHandler(["open", "exit"], False).input_while_none("\nIncorrect input! |open| or |exit|?")
			print("\n")