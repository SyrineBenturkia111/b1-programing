# Lab Exercise 1: Grade Calculator
score_input = input("Enter a numerical score between 0 and 100:")

if score_input is None or score_input =="":
    print("Format is invalid. Please provide an actual number between 0 and 100")
else:
    score = int(score_input)

if score >= 90:
    grade = "A"
    print("Excellent work!")
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"
    
print(f"Your grade is: {grade}")

# Lab Exercise 2: Limited Login Attempts
correct_pin = "1234"
attempts = 0
max_attempts = 3
login_successful = False

while attempts < max_attempts:
    print(f"Attempt {attempts+1} of {max_attempts}")
    entered_pin = input("Enter your PIN:")
    if entered_pin == correct_pin:
        print("PIN accepted! Welcome.")
        login_successful = True
        break #exits the loop if PIN is correct
    else:
        print("Incorrect PIN.")
        attempts +=1
if not login_successful:
    print("Too many incorrect attempts. Account locked.")

# Lab Exercise 3: Filtering Even Numbers
for number in range(11):
    if number % 2 != 0:
        continue
    elif number == 0:
        continue
    else:
        print(number)