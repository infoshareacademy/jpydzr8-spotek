
import csv

class Delivery:
        def __init__(self,id, login, company,  delivery_date, delivery_type, unit_type):
            self.id = id
            self.login = login
            self.company = company

            self.delivery_date = delivery_date
            self.delivery_type = delivery_type
            self.unit_type = unit_type




        def save_to_file(self, path):

                with open(path, mode='a', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter=';')
                    writer.writerow([
                        self.id,
                        self.login,
                        self.company,
                        self.delivery_date,
                        self.delivery_type,
                        self.unit_type,

                    ])


                    print("✅ Awizacja zapisana do pliku.")


