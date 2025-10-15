from typing import Self
from sqlite3 import Connection, OperationalError
from menupoint import MenuPoint
from inputhandler import *

# Készíts egy python funkciót arra, hogy az adatbázisból kilistázza az összes „Boeing” gyártmányú repülőgépet.
class ListBoeingPlanesPoint(MenuPoint):

	def __init__(self: Self, databaseReference: Connection) -> None:
		super().__init__(databaseReference, "list_boeings", "Lists all Boeing type airplanes from Plane.")
		
	def run(self: Self) -> None:
		print(f"Plane\n-----\n{self.sql_selectandwrite(f"SELECT * FROM Plane WHERE Plane.plane_make LIKE 'Boeing'")}")

# Készíts egy python funkciót, amelynek segítésével a felhasználó új repülőket vihet be az adatbázisba.
class InsertPlaneRecordPoint(MenuPoint):

	def __init__(self: Self, databaseReference: Connection) -> None:
		super().__init__(databaseReference, "insert_plane", "Inserts a new record into the Plane table.")
		
	def run(self: Self) -> None:
		print(f"\n{self.insert_record("Plane")}")

# Az egyik kollégánk véletlen elrontott valamit és az adatbázisba importálás közben nem „Boeing”-ként vitette fel a repülögépek gyártmányát, hanem „Boieng”-ként. 
# Írj egy funkciót amely kijavítja a hibát. A hiba kijavítása előtt listázza ki magukat a változtatandó sorokat vagy azok darabszámát, 
# majd a program tegye fel a kérdést a folytatásra. Amennyiben a felhasznló nem-el válaszol, úgy ne történjen semmilyen módosítás.
class ReplaceBoiengPlanesPoint(MenuPoint):

	def __init__(self: Self, databaseReference: Connection) -> None:
		super().__init__(databaseReference, "replace_boiengs", "Lists all Boieng type airplanes from Plane and replaces them with Boeing.")
		
	def run(self: Self) -> None:
		print(f"Records to change:\n\nPlane\n-----\n{self.sql_selectandwrite(f"SELECT * FROM Plane WHERE plane_make LIKE 'Boieng'")}")
		print("Are you sure you want to change them? |yes| or |no|?")

		text: str = MultiOptionInputHandler(["yes", "no"], False).input_while_none("\nIncorrect input! |yes| or |no|?")

		if text == "yes":
			try:
				self.sql_execute(f"UPDATE Plane SET plane_make = 'Boeing' WHERE plane_make LIKE 'Boieng'")
			except OperationalError:
				text = "no"
			
		if text == "yes":
			print(f"\nPlane\n-----\n{self.sql_selectandwrite(f"SELECT * FROM Plane")}")
		else:
			print("\nNo changes were made.\n\n")

# Készíts egy olyan python funkciót amely segítségével kilistázható bármely, a user által megadott városban (location) található repülőtér.
class SelectAirportByLocationPoint(MenuPoint):

	def __init__(self: Self, databaseReference: Connection) -> None:
		super().__init__(databaseReference, "select_bylocation", "Selects all airports at the given location.")
		
	def run(self: Self) -> None:
		locationNames: list[str] = [location[0] for location in self.sql_select("SELECT DISTINCT location FROM Airport")]
		print(f"Airport locations\n-----------------\n\t{locationNames}\n\nThe location to search for:")
		
		locationName =  MultiOptionInputHandler(locationNames).input_while_none("\nNo such location exists! Try again!")

		print(f"\nAirport\n--------\n{self.sql_selectandwrite(f"SELECT * FROM Airport WHERE location LIKE '{locationName}'")}")

# Készíts egy python funkciót amely segítésével a felhasználó lekérdezheti, hogy a két megadott dátum között (arrival, departure) melyik repülőtereken volt 
# legalább egy Boeing típusú repülőgép. Minden repülőtér csak egyszer szerepeljen a felsorolásban. A funkció elkészítése közben igyekezz a lehető legtöbb szűrést 
# az adatbázison végezni. Mit gondolsz miért fontos ez? Írd le a választ a kommentként (angolul vagy magyarul) a funkció definíciója fölé.
class SelectAirportByTimePoint(MenuPoint):

	def __init__(self: Self, databaseReference: Connection) -> None:
		super().__init__(databaseReference, "select_bytime", "Selects all airports where there was at least one Boeing between the given times.")
		
	def run(self: Self) -> None:
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
				WHERE plane_make LIKE 'Boieng' AND date_of_creation <= {end}
			)
		)
		"""

		print(f"\nAirport\n--------\n{self.sql_selectandwrite(sql)}")