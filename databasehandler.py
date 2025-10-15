from menu import *
from airplanemenu import *

def main():
	menu: Menu = AirplaneMenu()
	menu.run()

if __name__ == "__main__":
	main()

"""
Todo lista:
- InsertPlaneRecordPoint -> Plane táblára szabni és ellenőrizni a típusokat
- 7. feladat elkészítése
- Adatbázis bezárásnál kell commit?
- Ha egy funkció kéri egy tábla létezését, de nem létezik -> hozd létre a táblát
- Absztrakt osztályok használata
- Leírások elkészításe
- list_databaseinfo nevének kiírása
"""