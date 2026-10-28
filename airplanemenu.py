from os import system, name
from typing import Self
from sqlite3 import connect
from menu import *
from menupoint import *
from airplanemenupoint import *

class AirplaneMenu(Menu):
	def __init__(self: Self) -> None:
		database: Connection = connect("./airplanes.db3")
		menuPoints: set[MenuPoint] = [
			ListDatabaseInfoPoint(database),
			ListAllTableNamesPoint(database),
			ListAllTablesPoint(database),
			ListTableByNamePoint(database),
			# InsertRecordPoint(database),
			ListBoeingPlanesPoint(database),
			InsertPlaneRecordPoint(database),
			ReplaceBoiengPlanesPoint(database),
			SelectAirportByLocationPoint(database),
			SelectAirportByTimePoint(database),
			ExitPoint(database)
		]
		super().__init__(database, menuPoints)

	def create_options(self: Self) -> set[MenuPoint]:
		return self.menuPoints
	
	def run(self: Self) -> None:
		system('cls' if name == 'nt' else 'clear')

		self.manage_database()
		self.close_database()