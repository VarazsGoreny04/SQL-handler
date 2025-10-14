from sqlite3 import Connection, OperationalError

class MenuPoint:

	def __init__(self, databaseReference: Connection, name: str, summary: str) -> None:
		self.databaseReference = databaseReference
		self.name = name.lower()
		self.summary = summary

	def sql_selector(self, sql_statement: str) -> set[str] | OperationalError:
		c = self.databaseReference.cursor()

		c.execute(sql_statement)

		result = f"[\n\t{[description[0] for description in c.description]}\n\n"
		for record in c.fetchall():
			result = f"{result}\t{record}\n"
		
		return f"{result}]\n\n"

	def lookup_all_tablenames(self) -> set[str]:
		return [tablename[0] for tablename in self.databaseReference.cursor().execute("SELECT name FROM sqlite_master WHERE sqlite_master.type LIKE 'table';")]

	def lookup_table(self, name: str) -> str:
		try:
			return f"{name}\n{"-" * len(name)}\n{self.sql_selector(f"SELECT * FROM {name};")}"
		except OperationalError:
			return "No such table exists!\n\n"

	
	def insert_record(self, table_name: str) -> str:
		c = self.databaseReference.cursor()
		try:
			c.execute(f"SELECT * FROM {table_name}")
		except OperationalError:
			return "No such table exists!\n\n"
		
		print("Add the values to insert!")

		values = []
		for header_label in [description[0] for description in c.description]:
			print(f"{header_label}: ", end="")
			values.append(f"\'{input()}\'")

		return f"{", ".join(values)}\n"
		#c.execute(f"INSERT INTO {table_name} VALUES ({", ".join(values)});")

		#return self.lookup_table(table_name)

	def run(self) -> None:
		NotImplementedError()

	def __hash__(self) -> int:
		return self.name.__hash__()

	def __repr__(self) -> str:
		return f"{type(self).__name__}({self.name}, {self.summary})"
 
	def __str__(self) -> str:
		return f"|{self.name}| --> {self.summary}"

class ListAllTableNamesPoint(MenuPoint):

	def __init__(self, databaseReference: Connection) -> None:
		super().__init__(databaseReference, "list_tablenames", "Lists all tables of the database.")
		
	def run(self) -> None:
		print(f"Tables\n------\n\t{self.lookup_all_tablenames()}\n")

class ListAllTablesPoint(MenuPoint):

	def __init__(self, databaseReference: Connection) -> None:
		super().__init__(databaseReference, "list_everything", "Lists all the tables and records of the database.")
		
	def run(self) -> None:
		print(f"Tables\n------\n\t{self.lookup_all_tablenames()}\n")

		for tablename in self.lookup_all_tablenames():
			print(self.lookup_table(tablename))

class ListTableByNamePoint(MenuPoint):

	def __init__(self, databaseReference: Connection) -> None:
		super().__init__(databaseReference, "list_table", "Lists a table by name.")
		
	def run(self) -> None:
		print(f"Tables\n------\n\t{self.lookup_all_tablenames()}\n\nThe name of the table: ")
		print(f"\n{self.lookup_table(input())}")

class InsertRecordPoint(MenuPoint):

	def __init__(self, databaseReference: Connection) -> None:
		super().__init__(databaseReference, "insert_table", "Inserts a new record into a given table.")
		
	def run(self) -> None:
		print(f"Tables\n------\n\t{self.lookup_all_tablenames()}\n\nThe name of the table: ")
		print(f"\n{self.insert_record(input())}")
		
class ExitPoint(MenuPoint):

	def __init__(self, databaseReference: Connection) -> None:
		super().__init__(databaseReference, "exit", "Exits from the current database.")
		
	def run(self) -> None:
		pass