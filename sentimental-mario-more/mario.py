# Runs main
def main():
    height = get_height()
    print_hills(height)


# Gets input between 1-8
def get_height():
    while True:
        try:
            h = int(input("How high should we build, sir?: "))
            if 1 <= h <= 8:
                return h
            # Loops until a valid number is input
            else:
                print("Input number between 1 and 8.")
        except ValueError:
            print("Please enter a valid number.")


# Prins "#" or " " depending on the value
def print_hills(h):
    for i in range(h):
        print(" " * (h - i - 1) + "#" * (i + 1) + "  " + "#" * (i + 1))


if __name__ == "__main__":
    main()
