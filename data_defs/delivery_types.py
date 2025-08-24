DELIVERY_TYPES = [
    "Dostawa paczka",
    "Dostawa luz",
    "Dostawa kontener",
    "Dostawa palety",
]

def choose_delivery_type():
    print("\n📦 Wybierz typ dostawy:")
    for i, t in enumerate(DELIVERY_TYPES, start=1):
        print(f"{i}. {t}")
    while True:
        choice = input("Nr opcji (1-4): ").strip()
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(DELIVERY_TYPES):
                return DELIVERY_TYPES[idx - 1]
        print("⚠️  Nieprawidłowa opcja, spróbuj ponownie.")