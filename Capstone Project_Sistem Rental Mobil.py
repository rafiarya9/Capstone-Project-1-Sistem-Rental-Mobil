from tabulate import tabulate
from colorama import Fore, Back, Style, init
import pyinputplus as pyip
from datetime import datetime

# Inisialisasi colorama
init()

# Data dummy untuk menyimpan data mobil dan rental
cars = [
    {'name': 'Toyota Innova Zenix', 'plat': 'Ganjil', 'price': 1150000, 'quantity': 5},
    {'name': 'Wuling Air EV', 'plat': 'Gage', 'price': 850000, 'quantity': 3},
    {'name': 'Honda CRV RS Hybrid', 'plat': 'Genap', 'price': 3400000, 'quantity': 4},
    {'name': 'Suzuki XL7 Hybrid', 'plat': 'Genap', 'price': 550000, 'quantity': 6},
    {'name': 'Hyundai Santa Fe', 'plat': 'Ganjil', 'price': 2100000, 'quantity': 1},
    {'name': 'BYD Seal', 'plat': 'Gage', 'price': 3000000, 'quantity': 1},
    {'name': 'Mazda CX5', 'plat': 'Ganjil', 'price': 2800000, 'quantity': 2},
    {'name': 'Toyota Calya', 'plat': 'Genap', 'price': 300000, 'quantity': 12}
]

rental_records = []

# Data login untuk admin dan customer
admin_credentials = {'username': 'admin', 'password': 'admin123'}
customer_credentials = {'username': 'customer', 'password': 'cust123'}

# ANSI escape sequences for colors
HEADER_COLOR = '\033[93m'
END_COLOR = '\033[0m'
RED_COLOR = '\033[91m'
GREEN_COLOR = '\033[92m'
BLUE_COLOR = '\033[94m'
YELLOW_COLOR = '\033[93m'

# Fungsi untuk login
def login(role):
    print(BLUE_COLOR + "\n→→→ Login ←←←" + END_COLOR)
    username = input("Masukkan username: ")
    password = pyip.inputPassword(prompt="Masukkan password: ")
    
    if role == 'admin':
        if username == admin_credentials['username'] and password == admin_credentials['password']:
            print(GREEN_COLOR + "Login berhasil sebagai Admin!" + END_COLOR)
            return True
        else:
            print(RED_COLOR + "Username atau password Admin salah." + END_COLOR)
            return False
    elif role == 'customer':
        if username == customer_credentials['username'] and password == customer_credentials['password']:
            print(GREEN_COLOR + "Login berhasil sebagai Customer!" + END_COLOR)
            return True
        else:
            print(RED_COLOR + "Username atau password Customer salah." + END_COLOR)
            return False

# Fungsi untuk menampilkan daftar mobil dalam bentuk tabel
def view_cars_table(cars_list, is_customer=False):
    print("\nDaftar Mobil:")
    if not cars_list:
        print("Maaf, tidak ada mobil yang sesuai dengan kriteria.")
    else:
        table_data = []
        for index, car in enumerate(cars_list):
            no_color = BLUE_COLOR + str(index+1) + END_COLOR
            if car['quantity'] == 0:
                row = [no_color,
                       RED_COLOR + car['name'] + END_COLOR,
                       RED_COLOR + car['plat'] + END_COLOR,
                       RED_COLOR + f"Rp{car['price']:,}".replace(",", ".") + END_COLOR,
                       RED_COLOR + str(car['quantity']) + END_COLOR]
            else:
                if is_customer:
                    row = [no_color, car['name'], car['plat'], f"Rp{car['price']:,}".replace(",", ".")]
                else:
                    row = [no_color, car['name'], car['plat'], f"Rp{car['price']:,}".replace(",", "."), car['quantity']]
            table_data.append(row)
        
        headers = [HEADER_COLOR + "No" + END_COLOR, 
                   HEADER_COLOR + "Nama Mobil" + END_COLOR, 
                   HEADER_COLOR + "Plat" + END_COLOR, 
                   HEADER_COLOR + "Harga/Hari" + END_COLOR]
        
        if not is_customer:
            headers.append(HEADER_COLOR + "Quantity" + END_COLOR)
        
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

# Fungsi untuk membuat dan menampilkan invoice
def view_invoice():
    print("\nInvoice Penyewaan Mobil:")
    if not rental_records:
        print(RED_COLOR + "Belum ada riwayat penyewaan." + END_COLOR)
    else:
        table_data = []
        for index, record in enumerate(rental_records):
            no_color = BLUE_COLOR + str(index+1) + END_COLOR
            table_data.append([
                no_color, 
                record['car'], 
                record['start_date'],   # Waktu Awal Sewa
                record['end_date'],     # Waktu Akhir Sewa
                record['days'], 
                f"Rp{record['total_price']:,}".replace(",", ".")
            ])
        
        headers = [
            HEADER_COLOR + "No" + END_COLOR,
            HEADER_COLOR + "Nama Mobil" + END_COLOR,
            HEADER_COLOR + "Waktu Awal Sewa" + END_COLOR,
            HEADER_COLOR + "Waktu Akhir Sewa" + END_COLOR,
            HEADER_COLOR + "Jumlah Hari" + END_COLOR,
            HEADER_COLOR + "Total Biaya" + END_COLOR
        ]
        
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

# Fitur 1: Create - Admin menambahkan mobil baru dengan notifikasi berwarna
def add_car():
    while True:
        name = input("Masukkan nama mobil: ")
        if name.isdigit() or name.strip() == "":
            print(RED_COLOR + "Nama mobil tidak boleh kosong atau hanya berupa angka. Silakan masukkan nama mobil yang valid." + END_COLOR)
        else:
            break
    
    while True:
        plat = input("Masukkan jenis plat (Ganjil/Genap/Gage): ").lower()
        if plat in ['ganjil', 'genap', 'gage']:
            plat = plat.capitalize()
            break
        else:
            print(RED_COLOR + "Jenis plat hanya bisa 'Ganjil', 'Genap', atau 'Gage'. Silakan coba lagi." + END_COLOR)
    
    while True:
        try:
            price = int(input("Masukkan harga sewa mobil per hari: Rp "))
            if price <= 0:
                print(RED_COLOR + "Harga harus lebih dari 0. Silakan coba lagi." + END_COLOR)
            else:
                break
        except ValueError:
            print(RED_COLOR + "Harga harus berupa angka. Silakan coba lagi." + END_COLOR)
    
    while True:
        try:
            quantity = int(input("Masukkan jumlah mobil yang tersedia: "))
            if quantity <= 0:  # Memastikan quantity harus lebih dari 0
                print(RED_COLOR + "Jumlah tidak boleh 0 atau negatif. Silakan coba lagi." + END_COLOR)
            else:
                break
        except ValueError:
            print(RED_COLOR + "Jumlah harus berupa angka. Silakan coba lagi." + END_COLOR)
    cars.append({'name': name, 'plat': plat, 'price': price, 'quantity': quantity})
    print(GREEN_COLOR + f"Mobil {name} berhasil ditambahkan!" + END_COLOR)

# Fitur 2: Read - Admin melihat daftar mobil rental
def view_cars_admin():
    view_cars_table(cars)
    print(RED_COLOR + "Note : Data mobil dengan warna merah belum tersedia untuk saat ini" + END_COLOR)

# Fitur 2: Read - Customer melihat daftar seluruh mobil
def view_all_cars():
    view_cars_table(cars, is_customer=True)
    print(RED_COLOR + "Note : Data mobil dengan warna merah belum tersedia untuk saat ini" + END_COLOR)

# Fitur 3: Update - Admin mengubah informasi mobil
def update_car():
    view_cars_admin()  # Fungsi untuk menampilkan daftar mobil
    try:
        car_index = int(input("\nPilih nomor mobil yang ingin diupdate: ")) - 1
        if 0 <= car_index < len(cars):  # Memastikan indeks mobil yang dipilih valid
            while True:
                name = input("Masukkan nama mobil baru: ")
                if name.isdigit() or name.strip() == "":
                    print(RED_COLOR + "Nama mobil tidak boleh kosong atau hanya berupa angka. Silakan masukkan nama mobil yang valid." + END_COLOR)
                else:
                    break
            
            while True:
                plat = input("Masukkan jenis plat (Ganjil/Genap/Gage): ").lower()
                if plat in ['ganjil', 'genap', 'gage']:
                    plat = plat.capitalize()
                    break
                else:
                    print(RED_COLOR + "Jenis plat hanya bisa 'Ganjil', 'Genap', atau 'Gage'. Silakan coba lagi." + END_COLOR)
            
            while True:
                try:
                    price = int(input("Masukkan harga sewa mobil baru per hari: Rp "))
                    if price <= 0:
                        print(RED_COLOR + "Harga harus lebih dari 0. Silakan coba lagi." + END_COLOR)
                    else:
                        break
                except ValueError:
                    print(RED_COLOR + "Harga harus berupa angka. Silakan coba lagi." + END_COLOR)
            
            while True:
                try:
                    quantity = int(input("Masukkan jumlah mobil yang tersedia: "))
                    if quantity <= 0:
                        print(RED_COLOR + "Jumlah tidak boleh 0 atau negatif. Silakan coba lagi." + END_COLOR)
                        continue  # Mengulangi input quantity
                    else:
                        break
                except ValueError:
                    print(RED_COLOR + "Jumlah harus berupa angka. Silakan coba lagi." + END_COLOR)
                    continue  # Mengulangi input jika salah

            # Update informasi mobil
            cars[car_index] = {'name': name, 'plat': plat, 'price': price, 'quantity': quantity}
            print(GREEN_COLOR + "Informasi mobil berhasil diupdate!" + END_COLOR)
        else:
            print(RED_COLOR + "Mobil tidak ditemukan." + END_COLOR)
    except ValueError:
        print(RED_COLOR + "Input tidak valid." + END_COLOR)


# Fitur 4: Delete - Admin menghapus mobil
def delete_car():
    view_cars_admin()
    try:
        car_index = int(input("\nPilih nomor mobil yang ingin dihapus: ")) - 1
        if 0 <= car_index < len(cars):
            deleted_car = cars.pop(car_index)
            print(GREEN_COLOR + f"Mobil {deleted_car['name']} berhasil dihapus!" + END_COLOR)
        else:
            print(RED_COLOR + "Mobil tidak ditemukan." + END_COLOR)
    except ValueError:
        print(RED_COLOR + "Input tidak valid." + END_COLOR)

# Fitur 5: Menyewa mobil - Customer menyewa mobil
from datetime import datetime

def is_car_available(car_index, start_date, end_date):
    # Cek apakah mobil sudah dipesan pada rentang waktu yang sama
    for record in rental_records:
        if (record['car'] == cars[car_index]['name'] and
            not (end_date <= datetime.strptime(record['start_date'], '%d-%m-%Y').date() or
                 start_date >= datetime.strptime(record['end_date'], '%d-%m-%Y').date())):
            return False, record['end_date']  # Return False and the end_date of the existing rental
    return True, None

def rent_car():
    view_all_cars()
    try:
        car_index = int(input("\nPilih nomor mobil yang ingin disewa: ")) - 1
        if 0 <= car_index < len(cars):
            while True:
                start_date_str = input("Masukkan waktu mulai sewa (DD-MM-YYYY): ")
                try:
                    start_date = datetime.strptime(start_date_str, '%d-%m-%Y').date()

                    if start_date < datetime.now().date():
                        print(RED_COLOR + "Waktu mulai sewa tidak bisa sebelum tanggal hari ini." + END_COLOR)
                    else:
                        # Cek ketersediaan mobil untuk rentang tanggal yang diberikan
                        available, end_date_str = is_car_available(car_index, start_date, start_date)
                        if not available:
                            print(RED_COLOR + f"Mobil ini sudah dipesan hingga {end_date_str}. Silakan pilih tanggal mulai sewa setelah {end_date_str}." + END_COLOR)
                        else:
                            # Masukkan waktu akhir sewa
                            while True:
                                end_date_str = input("Masukkan waktu akhir sewa (DD-MM-YYYY): ")
                                try:
                                    end_date = datetime.strptime(end_date_str, '%d-%m-%Y').date()
                                    if end_date <= start_date:
                                        print(RED_COLOR + "Waktu akhir sewa harus setelah waktu mulai sewa." + END_COLOR)
                                    else:
                                        available_end, _ = is_car_available(car_index, start_date, end_date)
                                        if not available_end:
                                            print(RED_COLOR + f"Mobil ini sudah dipesan hingga {end_date_str}. Silakan pilih tanggal mulai sewa setelah {end_date_str}." + END_COLOR)
                                            break
                                        else:
                                            days = (end_date - start_date).days
                                            if days <= 0:
                                                print(RED_COLOR + "Jumlah hari sewa harus lebih dari 0." + END_COLOR)
                                            else:
                                                total_price = days * cars[car_index]['price']
                                                car_name = cars[car_index]['name']
                                                rental_records.append({'car': car_name, 'start_date': start_date_str, 'end_date': end_date_str, 'days': days, 'total_price': total_price})
                                                cars[car_index]['quantity'] -= 1
                                                print(GREEN_COLOR + f"Mobil {car_name} berhasil disewa! Total biaya: Rp{total_price:,}".replace(",", ".") + END_COLOR)
                                                view_invoice()
                                                return
                                except ValueError:
                                    print(RED_COLOR + "Format waktu tidak valid. Gunakan format DD-MM-YYYY." + END_COLOR)
                except ValueError:
                    print(RED_COLOR + "Format waktu tidak valid. Gunakan format DD-MM-YYYY." + END_COLOR)
        else:
            print(RED_COLOR + "Nomor mobil tidak valid." + END_COLOR)
    except ValueError:
        print(RED_COLOR + "Input tidak valid. Silakan masukkan nomor yang benar." + END_COLOR)



# Fitur 6: Melihat riwayat sewa - Admin melihat daftar mobil yang disewa
def view_rental_records():
    print("\nRiwayat Penyewaan Mobil:")
    if not rental_records:
        print(RED_COLOR + "Belum ada riwayat penyewaan." + END_COLOR)
    else:
        table_data = []
        for index, record in enumerate(rental_records):
            no_color = BLUE_COLOR + str(index+1) + END_COLOR
            table_data.append([
                no_color, 
                record['car'], 
                record['start_date'],   # Waktu Awal Sewa
                record['end_date'],     # Waktu Akhir Sewa
                record['days'], 
                f"Rp{record['total_price']:,}".replace(",", ".")
            ])
        
        headers = [HEADER_COLOR + "No" + END_COLOR,
                   HEADER_COLOR + "Nama Mobil" + END_COLOR,
                   HEADER_COLOR + "Waktu Awal Sewa" + END_COLOR,
                   HEADER_COLOR + "Waktu Akhir Sewa" + END_COLOR,
                   HEADER_COLOR + "Jumlah Hari" + END_COLOR,
                   HEADER_COLOR + "Total Biaya" + END_COLOR]
        
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

# Fitur 7: Urutkan dan Filter - Customer mengurutkan dan memfilter daftar mobil
def sort_and_filter_cars():
    while True:  # Tambahkan loop agar tetap berada di sub-menu
        print(YELLOW_COLOR + "\n→→→ Urutkan dan Filter Mobil ←←←" + END_COLOR)
        print(YELLOW_COLOR + "1. Urutkan berdasarkan harga" + END_COLOR)
        print(YELLOW_COLOR + "2. Urutkan berdasarkan nama" + END_COLOR)
        print(YELLOW_COLOR + "3. Filter berdasarkan jenis plat" + END_COLOR)
        print(RED_COLOR + "4. Kembali ke Customer Main Menu" + END_COLOR)  # Tambahkan opsi untuk kembali ke main menu
        choice = input("Pilih opsi: ")

        if choice == '1':
            sorted_cars = sorted(cars, key=lambda x: x['price'])
            view_cars_table(sorted_cars, is_customer=True)
            print(RED_COLOR + "Note : Data mobil dengan warna merah belum tersedia untuk saat ini" + END_COLOR)
        elif choice == '2':
            sorted_cars = sorted(cars, key=lambda x: x['name'])
            view_cars_table(sorted_cars, is_customer=True)
            print(RED_COLOR + "Note : Data mobil dengan warna merah belum tersedia untuk saat ini" + END_COLOR)
        elif choice == '3':
            plat_filter = input("Masukkan jenis plat (Ganjil/Genap/Gage): ").capitalize()
            filtered_cars = [car for car in cars if car['plat'] == plat_filter]
            view_cars_table(filtered_cars, is_customer=True)
            print(RED_COLOR + "Note : Data mobil dengan warna merah belum tersedia untuk saat ini" + END_COLOR)
        elif choice == '4':
            break  # Keluar dari loop dan kembali ke main menu
        else:
            print(RED_COLOR + "Opsi tidak valid." + END_COLOR)

# Fungsi utama untuk menjalankan program dengan peran admin atau customer
def main():
    while True:
        header_line = "═══════════════════════════════"
        print(f"{Fore.BLUE}{Back.BLACK}{Style.BRIGHT}{header_line}{Style.RESET_ALL}")
        print(f"{Fore.BLUE}{Back.BLACK}{Style.BRIGHT}    WELCOME TO BOB'S GARAGE    {Style.RESET_ALL}")
        print(f"{Fore.BLUE}{Back.BLACK}{Style.BRIGHT}{header_line}{Style.RESET_ALL}")
        print(YELLOW_COLOR + "1. Login sebagai Admin" + END_COLOR)
        print(YELLOW_COLOR + "2. Login sebagai Customer" + END_COLOR)
        print(RED_COLOR + "3. Keluar" + END_COLOR)
        role = input("Pilih opsi: ")

        if role == '1':
            if login('admin'):
                while True:
                    header_line = "═══════════════════════════════"
                    print(f"{Fore.BLUE}{Back.BLACK}{Style.BRIGHT}{header_line}{Style.RESET_ALL}")
                    print(f"{Fore.BLUE}{Back.BLACK}{Style.BRIGHT}        ADMIN DASHBOARD        {Style.RESET_ALL}")
                    print(f"{Fore.BLUE}{Back.BLACK}{Style.BRIGHT}{header_line}{Style.RESET_ALL}")
                    print(YELLOW_COLOR + "1. Tambah Data Mobil" + END_COLOR)
                    print(YELLOW_COLOR + "2. Lihat Data Mobil" + END_COLOR)
                    print(YELLOW_COLOR + "3. Edit Data Mobil" + END_COLOR)
                    print(YELLOW_COLOR + "4. Hapus Data Mobil" + END_COLOR)
                    print(YELLOW_COLOR + "5. Lihat Riwayat Penyewaan" + END_COLOR)
                    print(RED_COLOR + "6. Kembali ke Menu Utama" + END_COLOR)
                    admin_choice = input("Pilih opsi: ")

                    if admin_choice == '1':
                        add_car()
                    elif admin_choice == '2':
                        view_cars_admin()
                    elif admin_choice == '3':
                        update_car()
                    elif admin_choice == '4':
                        delete_car()
                    elif admin_choice == '5':
                        view_rental_records()
                    elif admin_choice == '6':
                        break
                    else:
                        print(RED_COLOR + "Opsi tidak valid, coba lagi." + END_COLOR)
            else:
                print(RED_COLOR + "Gagal login sebagai Admin." + END_COLOR)

        elif role == '2':
            if login('customer'):
                while True:
                    header_line = "═══════════════════════════════"
                    print(f"{Fore.BLUE}{Back.BLACK}{Style.BRIGHT}{header_line}{Style.RESET_ALL}")
                    print(f"{Fore.BLUE}{Back.BLACK}{Style.BRIGHT}      CUSTOMER MAIN MENU       {Style.RESET_ALL}")
                    print(f"{Fore.BLUE}{Back.BLACK}{Style.BRIGHT}{header_line}{Style.RESET_ALL}")
                    print(YELLOW_COLOR + "1. Lihat Semua Mobil" + END_COLOR)
                    print(YELLOW_COLOR + "2. Urutkan dan Filter Mobil" + END_COLOR)
                    print(YELLOW_COLOR + "3. Sewa Mobil" + END_COLOR)
                    print(RED_COLOR + "4. Kembali ke Menu Utama" + END_COLOR)
                    customer_choice = input("Pilih opsi: ")

                    if customer_choice == '1':
                        view_all_cars()
                    elif customer_choice == '2':
                        sort_and_filter_cars()
                    elif customer_choice == '3':
                        rent_car()
                    elif customer_choice == '4':
                        break
                    else:
                        print(RED_COLOR + "Opsi tidak valid, coba lagi." + END_COLOR)
            else:
                print(RED_COLOR + "Gagal login sebagai Customer." + END_COLOR)

        elif role == '3':
            message = [["Terima kasih telah berkunjung ke Bob's Garage!"]]
            print(tabulate(message, tablefmt="grid"))
            break

        else:
            print(RED_COLOR + "Opsi tidak valid, coba lagi." + END_COLOR)

# Menjalankan program
main()
