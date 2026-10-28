from abc import ABC, abstractmethod
from typing import Self
from sqlite3 import Connection, OperationalError, Cursor, IntegrityError
from inputhandler import *

class MenuPoint(ABC):
	"""Customizable menu point for a menu."""

	def __init__(self: Self, databaseReference: Connection, name: str, summary: str) -> None:
		"""
		Constructs a MenuPoint.

		Parameters:
			databaseReference (Connection): The database of the menu point.
			name (str): The name of the menu point.
			summary (str): The summary of the menu point.
		"""

		self.databaseReference = databaseReference
		self.name = name.lower()
		self.summary = summary

	def getall_tablenames(self: Self) -> set[str]:
		"""Gets the tablenames in the database."""

		return [tableName[0] for tableName in self.databaseReference.cursor().execute("SELECT name FROM sqlite_master WHERE LOWER(type) LIKE 'table';")]

	def get_tablename(self: Self) -> str:
		"""
		Gets a tablename chosen by the user.
		
		Returns:
			str: The chosen tablename.
		"""

		print(f"{self.tostring_alltablenames()}The name of the table:")

		return MultiOptionInputHandler(self.getall_tablenames()).input_while_none("\nNo such table exists! Try again!")

	def sqlexecute(self: Self, sqlStatement: str) -> None | OperationalError:
		"""
		Executes the given SQL statement.

		Parameters:
			sqlStatement (str): The SQL statement.

		Raises:
			OperationalError: If the SQl statement raises an error.
		"""

		self.databaseReference.cursor().execute(sqlStatement)

	def sqlselect(self: Self, sqlStatement: str) -> tuple[list[str],list[tuple]] | OperationalError | TypeError:
		"""
		Executes the given SQL select statement and returns its result.

		Parameters:
			sqlStatement (str): The SQL statement.

		Raises:
			OperationalError: If the SQl statement raises an error.
			TypeError: If the SQl statement raises an error.
			
		Returns:
			tuple[list[str],list[tuple]]: The result of executing the SQL selection.
				The first item of the tuple is the header and the second is the selected records.
		"""

		c: Cursor = self.databaseReference.cursor().execute(sqlStatement)

		return ([description[0] for description in c.description], c.fetchall())
	
	def tostring_selected(self: Self, selected: tuple[list[str],list[tuple]], tableName: str | None = None) -> str:
		"""
		Converts the result of an SQL selection to a single string.

		Parameters:
			selected (tuple[list[str],list[tuple]]): The selection.
			tableName (str | None): The origin table of the SQL selection. (default is None)
			
		Returns:
			str: The result of an SQL selection as a single string.
		"""

		result: str = f"[\n\t{selected[0]}\n\n"
		for record in selected[1]:
			result = f"{result}\t{record}\n"
		
		return f"{f"{tableName}\n{"-" * len(tableName)}\n" if tableName is not None else ""}{result}]\n\n"
	
	def sql_selectandtostring(self: Self, sqlStatement: str) -> str | OperationalError | TypeError:
		"""
		Executes the given SQL select statement and returns its result as a single string.

		Parameters:
			sqlStatement (str): The SQL statement.
			
		Raises:
			OperationalError: If the SQl statement raises an error.
			TypeError: If the SQl statement raises an error.
			
		Returns:
			str: The result of an SQL selection as a single string.
		"""

		return self.tostring_selected(self.sqlselect(sqlStatement))

	def tostring_table(self: Self, tableName: str) -> str:
		"""
		Turns a table to string.

		Parameters:
			tableName (str): The name of the table.
			
		Returns:
			str: The table as a string.
		"""

		try:
			selected: tuple[list[str],list[tuple]] = self.sqlselect(f"SELECT * FROM {tableName};")
		except OperationalError:
			return "No such table exists!\n\n"

		return self.tostring_selected(selected, tableName)
	
	def tostring_alltablenames(self: Self) -> set[str]:
		"""
		Gets every table name.
			
		Returns:
			set[str]: The table names.
		"""

		return f"Tables\n------\n\t{self.getall_tablenames()}\n\n"
	
	def writetofile_selected(self: Self, selected: tuple[list[str],list[tuple]]) -> None:
		"""
		Converts the result of an SQL selection to a single string and writes it to a file.

		Parameters:
			selected (tuple[list[str],list[tuple]]): The selection.
		"""

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
			
	def writetofile_sqlselect(self: Self, sqlStatement: str, tableName: str | None = None) -> None:
		"""
		Executes the given SQL select selection, converts the result to a string and writes it to a file.

		Parameters:
			sqlStatement (str): The SQL statement.
			tableName (str | None): The origin table of the SQL selection. (default is None)
		"""

		try:
			selected: tuple[list[str],list[tuple]] = self.sqlselect(sqlStatement)
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
		"""
		Writes the content of a table to a file.

		Parameters:
			tableName (str): The name of the table.
		"""

		self.writetofile_sqlselect(f"SELECT * FROM {tableName};", tableName)
	
	def insert_record(self: Self, tableName: str, formats: dict[str, InputHandler] | None = None) -> None:
		"""
		Inserts a record into a table by a record format.
		
		Parameters:
			tableName (str): The name of the table.
			formats (dict[str, InputHandler] | None): The format of the record. (default is None)
		"""

		try:
			selected: tuple[list[str],list[tuple]] = self.sqlselect(f"SELECT * FROM {tableName}")
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
			self.sqlexecute(f"INSERT INTO {tableName} VALUES ({", ".join(values)});")
			print(f"\n{self.tostring_table(tableName)}")
		except IntegrityError as e:
			print(f"\n{e}. No changes were made.\n\n")

	@abstractmethod
	def run(self: Self) -> None:
		"""Runs this menu point."""

		pass

	def __hash__(self: Self) -> int:
		"""
		Returns the hash code of this menu point.

		Returns:
			int: The hash code.
		"""

		return self.name.__hash__()

	def __repr__(self: Self) -> str:
		"""
		Returns a string representation of this menu point.

		Returns:
			str: The string representation.
		"""

		return f"{type(self).__name__}({self.name}, {self.summary})"
 
	def __str__(self: Self) -> str:
		"""
		Returns a string representation of this menu point.

		Returns:
			str: The string representation.
		"""

		return f"|{self.name}| --> {self.summary}"
	
	def str_withpadding(self: Self, padding: int) -> str:
		"""
		Returns a string representation of this menu point with the given padding length.
		
		Parameters:
			padding (int): The length of the padding.

		Returns:
			str: The string representation.
		"""

		return f"|{self.name}| {padding * " "}--> {self.summary}"

class ListDatabaseInfoPoint(MenuPoint):
	"""A menu point for a menu that lists all information about the formats of the tables in the database."""

	def __init__(self: Self, databaseReference: Connection) -> None:
		"""
		Constructs a ListDatabaseInfoPoint.

		Parameters:
			databaseReference (Connection): The database of the menu point.
		"""

		super().__init__(databaseReference, "list_databaseinfo", "Lists all information about the formats of the tables in the database.")
		
	def run(self: Self) -> None:
		print(self.sql_selectandtostring("SELECT * FROM sqlite_master WHERE LOWER(type) LIKE 'table';"))

class ListAllTableNamesPoint(MenuPoint):
	"""A menu point for a menu that lists all tables of the database."""

	def __init__(self: Self, databaseReference: Connection) -> None:
		"""
		Constructs a ListDatabaseInfoPoint.

		Parameters:
			databaseReference (Connection): The database of the menu point.
		"""
		super().__init__(databaseReference, "list_tablenames", "Lists all tables of the database.")
		
	def run(self: Self) -> None:
		print(self.tostring_alltablenames())

class ListAllTablesPoint(MenuPoint):
	"""A menu point for a menu that lists all the tables and records of the database."""

	def __init__(self: Self, databaseReference: Connection) -> None:
		"""
		Constructs a ListDatabaseInfoPoint.

		Parameters:
			databaseReference (Connection): The database of the menu point.
		"""

		super().__init__(databaseReference, "list_everything", "Lists all the tables and records of the database.")
		
	def run(self: Self) -> None:
		print(self.tostring_alltablenames())

		for tablename in self.getall_tablenames():
			print(self.tostring_table(tablename))

class ListTableByNamePoint(MenuPoint):
	"""A menu point for a menu that lists a table by name."""

	def __init__(self: Self, databaseReference: Connection) -> None:
		"""
		Constructs a ListDatabaseInfoPoint.

		Parameters:
			databaseReference (Connection): The database of the menu point.
		"""

		super().__init__(databaseReference, "list_table", "Lists a table by name.")
		
	def run(self: Self) -> None:
		self.writetofile_table(self.get_tablename())

class InsertRecordPoint(MenuPoint):
	"""A menu point for a menu that inserts a new record into a given table."""

	def __init__(self: Self, databaseReference: Connection) -> None:
		"""
		Constructs a ListDatabaseInfoPoint.

		Parameters:
			databaseReference (Connection): The database of the menu point.
		"""

		super().__init__(databaseReference, "insert_table", "Inserts a new record into a given table.")
		
	def run(self: Self) -> None:
		tableName: str = self.get_tablename()
		print()
		self.insert_record(tableName)
		
class ExitPoint(MenuPoint):
	"""A menu point for a menu that exits from the current database."""

	def __init__(self: Self, databaseReference: Connection) -> None:
		"""
		Constructs a ListDatabaseInfoPoint.

		Parameters:
			databaseReference (Connection): The database of the menu point.
		"""

		super().__init__(databaseReference, "exit", "Exits from the current database.")
		
	def run(self: Self) -> None:
		pass