# Runs main
def main():
    ask = get_number()
    sum_result = half_digit(ask)
    check(sum_result, ask)


# Gets input
def get_number():
    while True:
        ask = int(input("Enter credit card number here: "))
        if ask > 0:
            return ask


# Calculate whether number is a valid card number
# Add every other number from right-left
def half_digit(ask):
    sum_result = 0
    second = False
    while ask > 0:
        end = ask % 10
        sum_result += times_two(end) if second else end
        second = not second
        ask //= 10
    return sum_result


# Multiply by 2
def times_two(end):
    multi = end * 2
    return sum(int(digit) for digit in str(multi))


# Checks if input number is a valid number
def check(sum_result, card_number):
    # Checks lenght of input number
    if sum_result % 10 == 0:
        card_str = str(card_number)
        length = len(card_str)
        # If valid lenght, determine what type of card
        if length == 15 and (int(card_str[:2]) == 34 or int(card_str[:2]) == 37):
            print("AMEX")
        elif (length == 13 and card_number // 10**12 == 4) or (length == 16 and card_number // 10**15 == 4):
            print("VISA")
        elif length == 16 and (51 <= int(card_str[:2]) <= 55):
            print("MASTERCARD")
        # If not valid card type
        else:
            print("INVALID")
    # If not valid lenght
    else:
        print("INVALID")


if __name__ == "__main__":
    main()
