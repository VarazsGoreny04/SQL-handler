from os import system, name
from sqlite3 import Connection, connect
from menupoint import *

class Menu:

	def __init__(self, database: Connection | None = None, menuPoints: set[MenuPoint] | None = None) -> None:
		self.database = database
		self.menuPoints = menuPoints

	def create_options(self) -> set[MenuPoint]:
		return [
			ListAllTableNamesPoint(self.database),
			ListAllTablesPoint(self.database),
			ListTableByNamePoint(self.database),
			InsertRecordPoint(self.database),
			ExitPoint(self.database)
		]

	def open_database(self) -> None:
		print("Give the file path of the .db file: ")
		file_path = input()
		print("\n")

		self.database = connect(file_path)

	def manage_database(self) -> None:
		if self.database is None:
			return
		
		self.menuPoints = self.create_options()
		
		text = ""
		while text != "exit":
			print("What would you like to do?")
			for menuPoint in self.menuPoints:
				print(menuPoint.__str__())

			text = input()
			print("\n")

			for menuPoint in self.menuPoints:
				if menuPoint.name == text:
					menuPoint.run()

	def close_database(self) -> None:
		self.menuPoints = None
		self.database = self.database.close()

	def run(self) -> None:
		system('cls' if name == 'nt' else 'clear')

		text = "open"
		while text != "exit":
			if (text == "open"):
				self.open_database()	
				self.manage_database()
				self.close_database()

			print("Would you like to |open| another database, or do you want to |exit|?")
			text = input()
			print("\n")