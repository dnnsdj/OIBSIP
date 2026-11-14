import secrets
import string


CHARACTER_TYPES = {
    "u": ("uppercase letters", string.ascii_uppercase),
    "l": ("lowercase letters", string.ascii_lowercase),
    "n": ("numbers", string.digits),
    "s": ("symbols", "!@#$%^&*()-_=+[]{};:,.?/"),
}
MIN_PASSWORD_LENGTH = 8


def get_character_types():
    print("Choose at least two character types:")
    print("  u - uppercase letters")
    print("  l - lowercase letters")
    print("  n - numbers")
    print("  s - symbols")

    while True:
        selected = input("Enter the letters for your choices (for example, uln): ").lower()
        selected_types = []
        valid_selection = True
        for choice in selected:
            if choice not in CHARACTER_TYPES:
                print("Invalid choice. Use only u, l, n, and s.")
                valid_selection = False
                break
            if choice not in selected_types:
                selected_types.append(choice)

        if not valid_selection:
            continue
        if len(selected_types) < 2:
            print("Select at least two different character types.")
            continue
        return selected_types


def get_password_length(minimum_length):
    while True:
        try:
            length = int(input("Enter the desired password length: "))
        except ValueError:
            print("Invalid length. Enter a whole number.")
            continue

        if length < minimum_length:
            print(f"Invalid length. Choose at least {minimum_length} characters.")
            continue
        return length


def generate_password(length, selected_types):
    password_characters = []
    all_characters = ""

    for choice in selected_types:
        character_pool = CHARACTER_TYPES[choice][1]
        password_characters.append(secrets.choice(character_pool))
        all_characters += character_pool

    while len(password_characters) < length:
        password_characters.append(secrets.choice(all_characters))

    secrets.SystemRandom().shuffle(password_characters)
    return "".join(password_characters)


def main():
    selected_types = get_character_types()
    minimum_length = MIN_PASSWORD_LENGTH
    if len(selected_types) > minimum_length:
        minimum_length = len(selected_types)
    length = get_password_length(minimum_length)

    while True:
        print("Generated password:", generate_password(length, selected_types))
        again = input(
            "Generate another password with the same criteria? (y/n): "
        ).strip().lower()
        if again not in ("y", "yes"):
            break


if __name__ == "__main__":
    main()
