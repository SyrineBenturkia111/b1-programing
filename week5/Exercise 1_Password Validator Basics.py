# Part A - Individual validation functions
import string
import random

def check_min_length(password, min_len=8):
    """Return True if password length >= min_len, otherwise False"""
    return len(password) >= min_len

def has_uppercase(password):
    """Return True if password contains at least one uppercase letter"""
    return any(char.isupper() for char in password)

def has_lowercase(password):
    """Return True if password contains at least one lowercase letter"""
    return any(char.islower() for char in password)

def has_digit(password):
    """Return True if password contains at least one digit"""
    return any(char.isdigit() for char in password)

def has_special_char(password):
    """Return True if password contains at least one special character"""
    return any(char in string.punctuation for char in password)



# Part B - Master validation function
def validate_password(password):
    """
    Call all five validation functions and return a dictionary with:
    - individual check results (True/False)
    - overall 'is_valid' (True only if ALL checks pass)
    """
    length_ok = check_min_length(password)
    upper_ok = has_uppercase(password)
    lower_ok = has_lowercase(password)
    digit_ok = has_digit(password)
    special_ok = has_special_char(password)


    results = {
        "min_length": length_ok,
        "uppercase": upper_ok,
        "lowercase": lower_ok,
        "digit": digit_ok,
        "special_char": special_ok,
        "is_valid": all([length_ok, upper_ok, lower_ok, digit_ok, special_ok])
    }
    return results


# Part C - User Interface and Testing

def generate_hint(validation_result):
    """Return a hint based on which rules were not met"""
    missing = []
    if not validation_result["min_length"]:
        missing.append("at least 8 characters long")
    if not validation_result["uppercase"]:
        missing.append("an uppercase letter (A-Z)")
    if not validation_result["lowercase"]:
        missing.append("a lowercase letter (a-z)")
    if not validation_result["digit"]:
        missing.append("a digit (0-9)")
    if not validation_result["special_char"]:
        missing.append("a special character (!@#$%^&* etc)")
    
    if not missing:
        return "Password meets all criteria."
    elif len(missing) == 1:
        return f"Add {missing[0]}."
    else:
        hint = ", ".join(missing[:-1]) + " and " + missing[-1]
        return f"Add {hint}."

def main():
    print("=== Password Strength Validator ===")
    print("Rules: Minimum 8 characters, uppercase, lowercase, digit, special character.\n")

    user_password = input("Enter a password to validate: ")
    validation_result = validate_password(user_password)

    print("\n--- Validation Results ---")
    print(f"✓ Minimum length (≥8):      {'Met' if validation_result['min_length'] else 'Not met'}")
    print(f"✓ Uppercase letter:         {'Met' if validation_result['uppercase'] else 'Not met'}")
    print(f"✓ Lowercase letter:         {'Met' if validation_result['lowercase'] else 'Not met'}")
    print(f"✓ Digit:                    {'Met' if validation_result['digit'] else 'Not met'}")
    print(f"✓ Special character:        {'Met' if validation_result['special_char'] else 'Not met'}")

    if validation_result["is_valid"]:
        print("\n✓ Overall: STRONG password! Great job")
    else:
        print("\nX Overall: WEAK password")
        hint = generate_hint(validation_result)
        print(f"Hint: {hint}")

if __name__ == "__main__":
    main()