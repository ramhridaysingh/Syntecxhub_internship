# ----- Calculation Functions -----

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Error: Cannot divide by zero"
    return a / b


# ----- Calculator Menu -----

def calculator():
    while True:
        print("\n--- Simple Calculator ---")
        print("1. Add (+)")
        print("2. Subtract (-)")
        print("3. Multiply (*)")
        print("4. Divide (/)")
        print("5. Clear")
        print("6. Exit")

        choice = input("Choose an option (1-6): ")

        if choice == "6":
            print("Exiting calculator. Goodbye!")
            break

        if choice == "5":
            print("Calculator cleared.")
            continue

        if choice not in ["1", "2", "3", "4"]:
            print("Invalid choice. Try again.")
            continue

        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
        except ValueError:
            print("Invalid number input.")
            continue

        if choice == "1":
            result = add(num1, num2)
        elif choice == "2":
            result = subtract(num1, num2)
        elif choice == "3":
            result = multiply(num1, num2)
        elif choice == "4":
            result = divide(num1, num2)

        print("Result:", result)


# ----- Run Calculator -----
calculator()
