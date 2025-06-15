
import csv

class Delivery:
        def __init__(self,id, login, company, ship_date, delivery_date, delivery_type, unit_type, order_number,
                     driver_name=None, vehicle_number=None, trailer_number=None, phone_number=None):
            self.id = id
            self.login = login
            self.company = company
            self.ship_date = ship_date
            self.delivery_date = delivery_date
            self.delivery_type = delivery_type
            self.unit_type = unit_type
            self.order_number = order_number
            self.driver_name = driver_name
            self.vehicle_number = vehicle_number
            self.trailer_number = trailer_number
            self.phone_number = phone_number



        def save_to_file(self, path):

                with open(path, mode='a', newline='', encoding='utf-8') as csvfile:
                    # Użyj writer z separatorem średnikowym (;) aby dane były zgodne z resztą aplikacji
                    writer = csv.writer(csvfile, delimiter=';')

                    # Zapisz wszystkie pola w odpowiedniej kolejności jako nowy wiersz
                    writer.writerow([
                        self.id,
                        self.login,
                        self.company,
                        self.ship_date,
                        self.delivery_date,
                        self.delivery_type,
                        self.unit_type,
                        self.order_number,
                        self.driver_name or "",  # jeśli brak danych, zapisz pusty string
                        self.vehicle_number or "",
                        self.trailer_number or "",
                        self.phone_number or ""
                    ])

                    # Możesz dodać print, by potwierdzić zapis (do testów)
                    print("✅ Awizacja zapisana do pliku.")

        def save_to_file(self, path):
            for target_path in [path, "archiwum/awizacje_backup.csv"]:
                with open(target_path, mode='a', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile, delimiter=';')
                    writer.writerow([
                        self.id,
                        self.login,
                        self.company,
                        self.ship_date,
                        self.delivery_date,
                        self.delivery_type,
                        self.unit_type,
                        self.order_number,
                        self.driver_name or "",
                        self.vehicle_number or "",
                        self.trailer_number or "",
                        self.phone_number or ""
                    ])
            print("✅ Awizacja zapisana do głównego pliku i kopii zapasowej.")
