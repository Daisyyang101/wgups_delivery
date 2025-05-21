import csv
from hash_table import Hash
from package_data import Package

#reading and loading data from CSV file
class File:
    def __init__(self, file):
        self.file = file

    def parse_package_data(self):
        """Parses package CSV data and loads it into a Hash table."""
        row_count = self._count_rows() #total # of packages
        hash_table = Hash(row_count) #creates hash table

#open and reads CSV file
        with open(self.file, mode='r', encoding='utf-8-sig') as csv_data:
            reader = csv.reader(csv_data)
            for row in reader:
                package = Package(
                    #create package object for the rows
                    package_id=row[0],
                    address=row[1],
                    city=row[2],
                    state=row[3],
                    zipcode=row[4],
                    delivery_time=row[5],
                    weight=row[6],
                    status='At HUB', #ALL PACKAGES START AT THE HUB
                    notes=row[7]
                )

                hash_table.add(row[0], package) #aDDS PACKAGE TO THE HASH TABLE using pkg ID
        return hash_table

    def _count_rows(self):
        """Returns the number of rows in the file."""
        with open(self.file, mode='r', encoding='utf-8-sig') as f:
            return sum(1 for _ in f)

    def parse_distance_data(self):
        """Reads and cleans raw distance data from CSV."""
        raw_data = []
        with open(self.file, mode='r', encoding='utf-8-sig', newline='') as csv_data:
            reader = csv.reader(csv_data)
            for row in reader:
                if row[0] == '5383 S 900 East #104':
                    row[0] = '5383 South 900 East #104'
                raw_data.append(row)
        return raw_data
