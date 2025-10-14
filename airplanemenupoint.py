from menupoint import MenuPoint

# Készíts egy python funkciót arra, hogy az adatbázisból kilistázza az összes „Boeing” gyártmányú repülőgépet.
class ListBoeingPlanesPoint(MenuPoint):

	def __init__(self, databaseReference) -> None:
		super().__init__(databaseReference, "list_boeings", "Lists all Boeing type airplanes from Plane.")
		
	def run(self) -> None:
		print(f"The location to search for: ")
		print(f"\nPlane\n--------\n{self.sql_selector(f"SELECT * FROM Plane WHERE Plane.plane_make LIKE 'Boieng'")}")

# Készíts egy python funkciót, amelynek segítésével a felhasználó új repülőket vihet be az adatbázisba.
class InsertPlaneRecordPoint(MenuPoint):

	def __init__(self, databaseReference) -> None:
		super().__init__(databaseReference, "insert_plane", "Inserts a new record into the Plane table.")
		
	def run(self) -> None:
		print(f"\n{self.insert_record("Plane")}")

# Készíts egy olyan python funkciót amely segítségével kilistázható bármely, a user által megadott városban (location) található repülőtér.
class SelectAirportByLocationPoint(MenuPoint):

	def __init__(self, databaseReference) -> None:
		super().__init__(databaseReference, "select_airport", "Selects all airports at the given location.")
		
	def run(self) -> None:
		print(f"The location to search for: ")
		print(f"\nAirport\n--------\n{self.sql_selector(f"SELECT * FROM Airport WHERE Airport.location LIKE '{input()}'")}")