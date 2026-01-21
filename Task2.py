import random

def choose_difficulty():
    print("\nChoose Difficulty Level")
    print("1. Easy (1 to 10)")
    print("2. Medium (1 to 50)")
    print("3. Hard (1 to 100)")

    while True:
        choice = input("Enter your choice (1-3): ")
        if choice == "1":
            return 10
        elif choice == "2":
            return 50
        elif choice == "3":
            return 100
        else:
            print("Invalid choice. Try again.")


def play_game(best_score):
    max_range = choose_difficulty()
    secret_number = random.randint(1, max_range)
    attempts = 0

    print(f"\nI have chosen a number between 1 and {max_range}. Try to guess it!")

    while True:
        try:
            guess = int(input("Enter your guess: "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        attempts += 1

        if guess < secret_number:
            print("Too low! Try again.")
        elif guess > secret_number:
            print("Too high! Try again.")
        else:
            print(f"Correct! You guessed it in {attempts} attempts.")
            break

    if best_score is None or attempts < best_score:
        print(" New best score!")
        return attempts
    else:
        return best_score


def number_guessing_game():
    best_score = None

    while True:
        best_score = play_game(best_score)

        print(f"Best Attempts So Far: {best_score}")

        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again != "yes":
            print("Thanks for playing! 👋")
            break


# ----- Start the Game -----
number_guessing_game()
