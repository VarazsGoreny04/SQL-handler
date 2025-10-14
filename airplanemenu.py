from os import system, name
from sqlite3 import connect
from menu import *
from menupoint import *
from airplanemenupoint import *

class AirplaneMenu(Menu):

	def __init__(self) -> None:
		database = connect("./airplanes.db3")
		menuPoints = [
			ListAllTableNamesPoint(database),
			ListAllTablesPoint(database),
			ListTableByNamePoint(database),
			InsertRecordPoint(database),
			ListBoeingPlanesPoint(database),
			InsertPlaneRecordPoint(database),
			SelectAirportByLocationPoint(database),
			ExitPoint(database)
		]
		super().__init__(database, menuPoints)

	def create_options(self) -> set[MenuPoint]:
		return self.menuPoints
	
	def run(self: Menu):
		system('cls' if name == 'nt' else 'clear')
		self.manage_database()
		self.close_database()