from typing import Self
from sqlite3 import Connection, OperationalError
from menupoint import MenuPoint
from inputhandler import *

class AirplaneMenuPoint(MenuPoint):
	def __init__(self: Self, databaseReference: Connection, name: str, summary: str) -> None:
		super().__init__(databaseReference, name, summary)
	
	def create_table_if_does_not_exists(self: Self, name: str, sql: str) -> None:
		if (name not in self.get_alltablenames()):
			self.sql_execute(sql)

	def create_plane_table_if_does_not_exists(self: Self) -> None:
		self.create_table_if_does_not_exists("Plane", "CREATE TABLE Plane (plane_id TEXT PRIMARY KEY, name TEXT, plane_make TEXT, date_of_creation TEXT)")
		
	def create_airport_table_if_does_not_exists(self: Self) -> None:
		self.create_table_if_does_not_exists("Airport", "CREATE TABLE Airport (airport_id TEXT PRIMARY KEY, location TEXT, name TEXT, country_code TEXT, 'coordinates')")
		
	def create_schedule_table_if_does_not_exists(self: Self) -> None:
		self.create_table_if_does_not_exists("Schedule", "CREATE TABLE Schedule (plane_id TEXT, aiport_id TEXT, time_of_departure TEXT, time_of_arrival TEXT, " \
			"FOREIGN KEY(plane_id) REFERENCES Plane(plane_id), FOREIGN KEY(aiport_id) REFERENCES Airport(airport_id))")

# Készíts egy python funkciót arra, hogy az adatbázisból kilistázza az összes „Boeing” gyártmányú repülőgépet.
class ListBoeingPlanesPoint(AirplaneMenuPoint):

	def __init__(self: Self, databaseReference: Connection) -> None:
		super().__init__(databaseReference, "list_boeings", "Lists all Boeing type airplanes from Plane.")
		
	def run(self: Self) -> None:
		self.create_plane_table_if_does_not_exists()

		self.writetofile_sql_select(f"SELECT * FROM Plane WHERE Plane.plane_make LIKE 'Boeing';", "Plane")

# Készíts egy python funkciót, amelynek segítésével a felhasználó új repülőket vihet be az adatbázisba.
class InsertPlaneRecordPoint(AirplaneMenuPoint):

	def __init__(self: Self, databaseReference: Connection) -> None:
		super().__init__(databaseReference, "insert_plane", "Inserts a new record into the Plane table.")
		
	def run(self: Self) -> None:
		self.create_plane_table_if_does_not_exists()

		formats: dict[str, InputHandler] = {
			"plane_id": StringWithRangeLengthInputHandler(1, 4),
			"date_of_creation": DateInputHandler()
		}
		
		self.insert_record("Plane", formats)

# Az egyik kollégánk véletlen elrontott valamit és az adatbázisba importálás közben nem „Boeing”-ként vitette fel a repülögépek gyártmányát, hanem „Boieng”-ként. 
# Írj egy funkciót amely kijavítja a hibát. A hiba kijavítása előtt listázza ki magukat a változtatandó sorokat vagy azok darabszámát, 
# majd a program tegye fel a kérdést a folytatásra. Amennyiben a felhasznló nem-el válaszol, úgy ne történjen semmilyen módosítás.
class ReplaceBoiengPlanesPoint(AirplaneMenuPoint):

	def __init__(self: Self, databaseReference: Connection) -> None:
		super().__init__(databaseReference, "replace_boiengs", "Lists all Boieng type airplanes from Plane and replaces them with Boeing.")
		
	def run(self: Self) -> None:
		self.create_plane_table_if_does_not_exists()

		print(f"Records to change:\n\nPlane\n-----\n{self.sql_selectandtostring(f"SELECT * FROM Plane WHERE plane_make LIKE 'Boieng';")}")
		print("Are you sure you want to change them? |yes| or |no|?")

		text: str = YesNoInputHandler().input_while_none("\nIncorrect input! |yes| or |no|?")

		if text == "yes":
			try:
				self.sql_execute(f"UPDATE Plane SET plane_make = 'Boeing' WHERE plane_make LIKE 'Boieng';")
				self.writetofile_sql_select("SELECT * FROM Plane;", "Plane")
			except OperationalError as e:
				print(f"\n{e}. An problem occoured while updating the table. No changes were made.\n\n")
		else:
			print("\nNo changes were made.\n\n")
		

# Készíts egy olyan python funkciót amely segítségével kilistázható bármely, a user által megadott városban (location) található repülőtér.
class SelectAirportByLocationPoint(AirplaneMenuPoint):

	def __init__(self: Self, databaseReference: Connection) -> None:
		super().__init__(databaseReference, "select_bylocation", "Selects all airports at the given location.")
		
	def run(self: Self) -> None:
		self.create_airport_table_if_does_not_exists()
		
		locationNames: list[str] = [location[0] for location in self.sql_select("SELECT DISTINCT location FROM Airport;")[1]]
		print(f"Airport locations\n-----------------\n\t{locationNames}\n\nThe location to search for:")
		
		locationName =  MultiOptionInputHandler(locationNames).input_while_none("\nNo such location exists! Try again!")

		self.writetofile_sql_select(f"SELECT * FROM Airport WHERE location LIKE '{locationName}';", "Airport")

# Készíts egy python funkciót amely segítésével a felhasználó lekérdezheti, hogy a két megadott dátum között (arrival, departure) melyik repülőtereken volt 
# legalább egy Boeing típusú repülőgép. Minden repülőtér csak egyszer szerepeljen a felsorolásban. A funkció elkészítése közben igyekezz a lehető legtöbb szűrést 
# az adatbázison végezni. Mit gondolsz miért fontos ez? Írd le a választ a kommentként (angolul vagy magyarul) a funkció definíciója fölé.
# Válasz:
# Hogy minél előbb minimalizáljuk a lekérdezés közben keletkezett táblák méretét. Ennek több előnye is van:
# -> A legfontosabb, hogy a további számítások során már csak kisebb táblákkal kell számolni, így csökkentve a futásidőt. 
# -> Ugyanúgy a tábla méretének köszönhetően, csökken az újonnan keletkező adat mennyisége, ami csökkenti a lekérdezés memóriaigényét.
class SelectAirportByTimePoint(AirplaneMenuPoint):

	def __init__(self: Self, databaseReference: Connection) -> None:
		super().__init__(databaseReference, "select_bytime", "Selects all airports where there was at least one Boeing between the given times.")
		
	def run(self: Self) -> None:
		self.create_plane_table_if_does_not_exists()
		self.create_airport_table_if_does_not_exists()
		self.create_schedule_table_if_does_not_exists()

		handler: InputHandler = DateInputHandler()

		print("The starting date of the search:")
		start: str = f"\'{handler.input_while_none("\nNot a valid date format! Try again!")}\'"
		print("\nThe ending date of the search:")
		end: str = f"\'{handler.input_while_none("\nNot a valid date format! Try again!")}\'"

		sql: str = f"""
		SELECT *
		FROM Airport
		WHERE airport_id IN (
			SELECT DISTINCT aiport_id
			FROM Schedule
			WHERE {start} <= time_of_departure AND {end} >= time_of_arrival AND plane_id IN (
				SELECT plane_id
				FROM Plane 
				WHERE plane_make LIKE 'Boeing' AND date_of_creation <= {end}
			)
		);
		"""

		self.writetofile_sql_select(sql, "Airport")