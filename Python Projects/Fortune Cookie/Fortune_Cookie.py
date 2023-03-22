import random

lucky_number = random.randint(1, 100)

fortune_number = random.randint(1, 3)

fortune_text = ""

if fortune_number == 1:
    fortune_text = "You will have a great day!"
elif fortune_number == 2:
    fortune_text = "Today will be tough... but worth it."
else:
    fortune_text = "You will get married this year!"

print(f"{fortune_text} Your lucky number is: {lucky_number}")
