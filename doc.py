import csv
import lxml
import os
import inspect
from xml_template import *

class Modeling():
    def __init__(self):
        self.path = os.path.dirname(inspect.getfile(self.__class__))
        self.filename = f'{self.path}/sql.csv'
        self.xmlFull = xmlTemplate

    def read_csv(self):
        try:
            with open(self.filename, mode='r') as input_file:
                csv_file = csv.reader(input_file)
                csv_dict = {rows[0]: rows[1] for rows in csv_file}

            del csv_dict['column_name']
            if "id" in csv_dict:
                del csv_dict['id']
            return csv_dict

        except Exception as error:
            print(f"ERROR!\n {error}")

    def generate_diagram(self):
        csv_file = self.read_csv()
        columns_with_type = []
        

        for i in csv_file:
            if csv_file[i] == "character varying":
                csv_file[i] = "VARCHAR (255)"

            elif csv_file[i] == "boolean":
                csv_file[i] = "BOOLEAN"

            elif csv_file[i] == "timestamp without time zone":
                csv_file[i] = "TIMESTAMP"

            elif csv_file[i] == "double":
                csv_file[i] = "DOUBLE PRECISION"

            elif csv_file[i] == "integer":
                csv_file[i] = "INTEGER"

            elif csv_file[i] == "bigint":
                csv_file[i] = "BIGINT"   
        
        for i in csv_file:
            concatColumnType = (i+" "+ csv_file[i]) 
            columns_with_type.append(concatColumnType)

        data = {f"name{n}":f"{columns_with_type[n]}" for n in range(len(columns_with_type))}
        return data

    def save_xml(self):
        try:
            diagram = self.generate_diagram()
            size = 100-(100 - len(diagram))
            data_null = {f"name{n}":"null" for n in range(size, 101)}
            diagram.update(data_null)
            open(f'{self.path}/demofile.xml','a+').write(self.xmlFull%diagram)
        except Exception as error:
            print(f"ERROR!\n {error}")

def main():
    Modeling().save_xml()

if __name__ == "__main__":
    main()
