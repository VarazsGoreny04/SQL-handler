from typing import Self
from sqlite3 import Connection, OperationalError, Cursor, IntegrityError
from inputhandler import *

class MenuPoint:

	def __init__(self: Self, databaseReference: Connection, name: str, summary: str) -> None:
		self.databaseReference = databaseReference
		self.name = name.lower()
		self.summary = summary

	def get_alltablenames(self: Self) -> set[str]:
		return [tableName[0] for tableName in self.databaseReference.cursor().execute("SELECT name FROM sqlite_master WHERE LOWER(type) LIKE 'table';")]

	def get_tablename(self: Self) -> str:
		print(f"{self.tostring_all_tablenames()}The name of the table:")

		return MultiOptionInputHandler(self.get_alltablenames()).input_while_none("\nNo such table exists! Try again!")

	def sql_execute(self: Self, sqlStatement: str) -> None | OperationalError:
		self.databaseReference.cursor().execute(sqlStatement)

	def sql_select(self: Self, sqlStatement: str) -> tuple[list[str],list[tuple]] | OperationalError | TypeError:
		c: Cursor = self.databaseReference.cursor().execute(sqlStatement)

		return ([description[0] for description in c.description], c.fetchall())
	
	def tostring_selected(self: Self, selected: tuple[list[str],list[tuple]], tableName: str | None = None) -> str:
		result: str = f"[\n\t{selected[0]}\n\n"
		for record in selected[1]:
			result = f"{result}\t{record}\n"
		
		return f"{f"{tableName}\n{"-" * len(tableName)}\n" if tableName is not None else ""}{result}]\n\n"
	
	def sql_selectandtostring(self: Self, sqlStatement: str) -> str | OperationalError | TypeError:
		return self.tostring_selected(self.sql_select(sqlStatement))

	def tostring_table(self: Self, tableName: str) -> str:
		try:
			selected: tuple[list[str],list[tuple]] = self.sql_select(f"SELECT * FROM {tableName};")
		except OperationalError:
			return "No such table exists!\n\n"

		return self.tostring_selected(selected, tableName)
	
	def tostring_all_tablenames(self: Self) -> set[str]:
		return f"Tables\n------\n\t{self.get_alltablenames()}\n\n"
	
	def writetofile_selected(self: Self, selected: tuple[list[str],list[tuple]]) -> None:
		print("\nGive the file path of the .csv file: ")

		try:
			with open(StringWithRangeLengthInputHandler(1, 1024).input_while_none("\nIncorrect format! Try again!"), "a", encoding="utf-8") as f:
				f.write(f"{";".join(selected[0])}\n")

				for record in selected[1]:
					f.write(f"{";".join(record)}\n")

				f.write("\n")

			print("\nData has been written out.\n\n")
		except IOError as e:
			print(f"\n{e}. File access aborted.\n\n")
			
	def writetofile_sql_select(self: Self, sqlStatement: str, tableName: str | None = None) -> None:
		try:
			selected: tuple[list[str],list[tuple]] = self.sql_select(sqlStatement)
		except OperationalError:
			return "\nNo such table exists!\n\n"

		print(f"\n{self.tostring_selected(selected, tableName)}")

		print("Do you want to write it out into a file? |yes| or |no|?")
		text: str = YesNoInputHandler().input_while_none("\nIncorrect input! |yes| or |no|?")

		if (text == "yes"):
			self.writetofile_selected(selected)
		else:
			print("\nAcknowledged.\n\n")
	
	def writetofile_table(self: Self, tableName: str) -> None:
		self.writetofile_sql_select(f"SELECT * FROM {tableName};", tableName)
	
	def insert_record(self: Self, tableName: str, formats: dict[str, InputHandler] | None = None) -> None:
		try:
			selected: tuple[list[str],list[tuple]] = self.sql_select(f"SELECT * FROM {tableName}")
		except OperationalError:
			return "No such table exists!\n\n"
		
		if formats is None:
			formats = {}
		
		print("Add the values to insert!")

		formatKeys = formats.keys()
		values: list[str] = []

		for headerLabel in selected[0]:
			print(f"{headerLabel}: ", end="")

			text: InputHandler = formats[headerLabel].input_while_none("\nIncorrect format! Try again!") if headerLabel in formatKeys else \
				StringWithRangeLengthInputHandler(1, 1024).input_while_none("\nIncorrect format! Try again!")

			values.append(f"\'{text}\'")

		try:
			self.sql_execute(f"INSERT INTO {tableName} VALUES ({", ".join(values)});")
			print(f"\n{self.tostring_table(tableName)}")
		except IntegrityError as e:
			print(f"\n{e}. No changes were made.\n\n")

	def run(self: Self) -> None:
		raise NotImplementedError("This method needs to be implemented in a subclass!")

	def __hash__(self: Self) -> int:
		return self.name.__hash__()

	def __repr__(self: Self) -> str:
		return f"{type(self).__name__}({self.name}, {self.summary})"
 
	def __str__(self: Self) -> str:
		return f"|{self.name}| --> {self.summary}"
	
	def str_withpadding(self: Self, padding: int) -> str:
		return f"|{self.name}| {padding * " "}--> {self.summary}"

class ListDatabaseInfoPoint(MenuPoint):

	def __init__(self: Self, databaseReference: Connection) -> None:
		super().__init__(databaseReference, "list_databaseinfo", "Lists all information about the formats of the tables in the database.")
		
	def run(self: Self) -> None:
		print(self.sql_selectandtostring("SELECT * FROM sqlite_master WHERE LOWER(type) LIKE 'table';"))

class ListAllTableNamesPoint(MenuPoint):

	def __init__(self: Self, databaseReference: Connection) -> None:
		super().__init__(databaseReference, "list_tablenames", "Lists all tables of the database.")
		
	def run(self: Self) -> None:
		print(self.tostring_all_tablenames())

class ListAllTablesPoint(MenuPoint):

	def __init__(self: Self, databaseReference: Connection) -> None:
		super().__init__(databaseReference, "list_everything", "Lists all the tables and records of the database.")
		
	def run(self: Self) -> None:
		print(self.tostring_all_tablenames())

		for tablename in self.get_alltablenames():
			print(self.tostring_table(tablename))

class ListTableByNamePoint(MenuPoint):

	def __init__(self: Self, databaseReference: Connection) -> None:
		super().__init__(databaseReference, "list_table", "Lists a table by name.")
		
	def run(self: Self) -> None:
		self.writetofile_table(self.get_tablename())

class InsertRecordPoint(MenuPoint):

	def __init__(self: Self, databaseReference: Connection) -> None:
		super().__init__(databaseReference, "insert_table", "Inserts a new record into a given table.")
		
	def run(self: Self) -> None:
		tableName: str = self.get_tablename()
		print()
		self.insert_record(tableName)
		
class ExitPoint(MenuPoint):

	def __init__(self: Self, databaseReference: Connection) -> None:
		super().__init__(databaseReference, "exit", "Exits from the current database.")
		
	def run(self: Self) -> None:
		pass