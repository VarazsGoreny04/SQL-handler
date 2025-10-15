from typing import Self
from sqlite3 import Connection, OperationalError, Cursor
from inputhandler import *

class MenuPoint:

	def __init__(self: Self, databaseReference: Connection, name: str, summary: str) -> None:
		self.databaseReference = databaseReference
		self.name = name.lower()
		self.summary = summary

	def sql_select(self: Self, sqlStatement: str) -> list[tuple] | OperationalError | TypeError:
		return self.databaseReference.cursor().execute(sqlStatement).fetchall()
	
	def sql_selectandwrite(self: Self, sqlStatement: str) -> str | OperationalError | TypeError:
		c: Cursor = self.databaseReference.cursor()

		c.execute(sqlStatement)

		result: str = f"[\n\t{[description[0] for description in c.description]}\n\n"
		for record in c.fetchall():
			result = f"{result}\t{record}\n"
		
		return f"{result}]\n\n"

	def sql_execute(self: Self, sql_statement: str) -> None | OperationalError:
		self.databaseReference.cursor().execute(sql_statement)

	def lookup_all_tablenames(self) -> set[str]:
		return [tablename[0] for tablename in self.databaseReference.cursor().execute("SELECT name FROM sqlite_master WHERE sqlite_master.type LIKE 'table';")]

	def lookup_table(self: Self, name: str) -> str:
		try:
			return f"{name}\n{"-" * len(name)}\n{self.sql_selectandwrite(f"SELECT * FROM {name};")}"
		except OperationalError:
			return "No such table exists!\n\n"
	
	def insert_record(self: Self, table_name: str) -> str:	# todo le kell kérdezni a rekord elemeinek formátumát és olyat kell bekérni
		c: Cursor = self.databaseReference.cursor()

		try:
			c.execute(f"SELECT * FROM {table_name}")
		except OperationalError:
			return "No such table exists!\n\n"
		
		print("Add the values to insert!")

		values: list[str] = []
		for header_label in [description[0] for description in c.description]:
			print(f"{header_label}: ", end="")
			values.append(f"\'{input()}\'")

		#return f"({", ".join(values)})\n\n"
		c.execute(f"INSERT INTO {table_name} VALUES ({", ".join(values)});")

		return self.lookup_table(table_name)

	def get_tablenames(self) -> str:
		tableNames: set[str] = self.lookup_all_tablenames()
		print(f"Tables\n------\n\t{tableNames}\n\nThe name of the table:")

		return MultiOptionInputHandler(tableNames).input_while_none("\nNo such table exists! Try again!")

	def run(self) -> None:
		raise NotImplementedError("This method needs to be implemented in a subclass!")

	def __hash__(self) -> int:
		return self.name.__hash__()

	def __repr__(self) -> str:
		return f"{type(self).__name__}({self.name}, {self.summary})"
 
	def __str__(self) -> str:
		return f"|{self.name}| --> {self.summary}"

class ListDatabaseInfoPoint(MenuPoint):

	def __init__(self: Self, databaseReference: Connection) -> None:
		super().__init__(databaseReference, "list_databaseinfo", "Lists all information about the formats of the tables in the database.")
		
	def run(self) -> None:
		print(self.sql_selectandwrite("SELECT * FROM sqlite_master WHERE sqlite_master.type LIKE 'table';"))

class ListAllTableNamesPoint(MenuPoint):

	def __init__(self: Self, databaseReference: Connection) -> None:
		super().__init__(databaseReference, "list_tablenames", "Lists all tables of the database.")
		
	def run(self) -> None:
		print(f"Tables\n------\n\t{self.lookup_all_tablenames()}\n")

class ListAllTablesPoint(MenuPoint):

	def __init__(self: Self, databaseReference: Connection) -> None:
		super().__init__(databaseReference, "list_everything", "Lists all the tables and records of the database.")
		
	def run(self) -> None:
		print(f"Tables\n------\n\t{self.lookup_all_tablenames()}\n")

		for tablename in self.lookup_all_tablenames():
			print(self.lookup_table(tablename))

class ListTableByNamePoint(MenuPoint):

	def __init__(self: Self, databaseReference: Connection) -> None:
		super().__init__(databaseReference, "list_table", "Lists a table by name.")
		
	def run(self) -> None:
		print(f"\n{self.lookup_table(self.get_tablenames())}")

class InsertRecordPoint(MenuPoint):

	def __init__(self: Self, databaseReference: Connection) -> None:
		super().__init__(databaseReference, "insert_table", "Inserts a new record into a given table.")
		
	def run(self) -> None:
		print(f"\n{self.insert_record(self.get_tablenames())}")
		
class ExitPoint(MenuPoint):

	def __init__(self: Self, databaseReference: Connection) -> None:
		super().__init__(databaseReference, "exit", "Exits from the current database.")
		
	def run(self) -> None:
		pass