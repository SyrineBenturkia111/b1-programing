# Exercise 2: Student Grade Analyzer

# Part A: Data Collection
student_records = []   # list of tuples (name, score)
stats = {}             # dictionary for highest, lowest, average score
unique_scores = set()  # set for unique scores
grade_distribution = {} # dictionary for frequency of each score

# Collect data for 6 students
print("Enter student names and scores:\n")
for i in range(1, 7):
    name = input(f"Student {i} name: ")
    score = int(input(f"Score for {name}: "))   # convert to int
    student_records.append((name, score))
    print()

# Part B: Statistics
# Extract all scores into a list
scores_list = [score for (_, score) in student_records]

stats['highest'] = max(scores_list)
stats['lowest'] = min(scores_list)
stats['average'] = sum(scores_list) / len(scores_list)

# Part C: Unique Scores
unique_scores = set(scores_list)

# Part D: Grade Distribution
for score in scores_list:
    grade_distribution[score] = grade_distribution.get(score, 0) + 1

# Results
print("\n==== STUDENT RECORDS ====")
for idx, (name, score) in enumerate(student_records, start=1):
    print(f"{idx}. {name}: {score}")

print("\n==== CLASS STATISTICS ====")
print(f"Highest Score: {stats['highest']}")
print(f"Lowest Score: {stats['lowest']}")
print(f"Average Score: {stats['average']:.2f}")

print("\n==== UNIQUE SCORES ====")
print(unique_scores)
print(f"Total unique scores: {len(unique_scores)}")

print("\n==== GRADE DISTRIBUTION ====")
for score in sorted(grade_distribution.keys()):
    print(f"Score {score}: {grade_distribution[score]} students")

# Challenge Extensions
import json
from collections import Counter
import statistics

# Median score
median_score = statistics.median(scores_list)

# Letter grade assignment
def get_letter_grade(score):
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'

letter_grades = [get_letter_grade(score) for (_, score) in student_records]
letter_grade_counts = Counter(letter_grades)

# Students above/below average
average_score = sum(scores_list) / len(scores_list)
above_avg = [(name, score) for name, score in student_records if score > average_score]
below_avg = [(name, score) for name, score in student_records if score < average_score]

# Grade distribution
grade_distribution = Counter(scores_list)

# Save all results to JSON file
output_data = {
    "student_records": [{"name": n, "score": s} for n, s in student_records],
    "statistics": {
        "highest": max(scores_list),
        "lowest": min(scores_list),
        "average": average_score,
        "median": median_score
    },
    "unique_scores": list(set(scores_list)),
    "grade_distribution": dict(grade_distribution),
    "letter_grade_counts": dict(letter_grade_counts),
    "above_average": [{"name": n, "score": s} for n, s in above_avg],
    "below_average": [{"name": n, "score": s} for n, s in below_avg]
}

with open("student_grade_report.json", "w") as json_file:
    json.dump(output_data, json_file, indent=4)

print("Data saved to 'student_grade_report.json'")