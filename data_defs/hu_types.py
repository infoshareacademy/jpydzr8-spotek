HU_TYPES = [
    "Paleta Homo",
    "Paleta Mix",
    "Box",
    "Kontener"

]

def choose_hu_types():
    print("\n📦 Wybierz typ dostawy:")
    for i, t in enumerate(HU_TYPES, start=1):
        print(f"{i}. {t}")
    while True:
        choice = input("Nr opcji (1-4): ").strip()
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(HU_TYPES):
                return HU_TYPES[idx - 1]
        print("⚠️  Nieprawidłowa opcja, spróbuj ponownie.")