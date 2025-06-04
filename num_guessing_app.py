from random import randint

random_num = randint(1, 101)
c = 0  

while True:
    guess = int(input("Enter your guess number from 1-100: "))
    c += 1
    if guess < random_num:
        print("Too Low!")
    elif guess > random_num:
        print("Too High!")
    else:
        print(f"You guessed it right at {c} attempts!")
        break
