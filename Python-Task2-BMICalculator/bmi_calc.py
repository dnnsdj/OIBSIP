try:
    weight = float(input("Enter your weight in kg: "))
except ValueError:
    print("Error: Please enter a number for your weight.")
    raise SystemExit(1)

if weight <= 0:
    print("Error: Weight cannot be negative.")
    raise SystemExit(1)

try:
    height = float(input("Enter your height in metres: "))
except ValueError:
    print("Error: Please enter a number for your height.")
    raise SystemExit(1)

if height <= 0:
    print("Error: Height must be greater than zero.")
    raise SystemExit(1)

# BMI is weight divided by height squared.
bmi = weight / (height * height)

print(f"Your BMI is: {bmi:.2f}")

if bmi < 18.5:
    print("Underweight")
elif bmi < 25:
    print("Normal")
elif bmi < 30:
    print("Overweight")
else:
    print("Obese")