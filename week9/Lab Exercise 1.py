# Lab Task 1: Building a School Management System
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def introduce(self):
        return f"Hi, my name is {self.name} and I am {self.age} years old."


class Student(Person):
    def __init__(self, name, age, student_id):
        super().__init__(name, age)
        self.student_id = student_id

    def introduce(self):
        basic_intro = super().introduce()
        return f"{basic_intro} My student ID is {self.student_id}."


class Teacher(Person):
    def __init__(self, name, age, subject):
        super().__init__(name, age)
        self.subject = subject

    def introduce(self):
        basic_intro = super().introduce()
        return f"{basic_intro} I teach {self.subject}."


#Test
if __name__ == "__main__":
    alice = Student("Alice", 18, "s56001")
    mr_mueller = Teacher("Mr. Müller", 50, "Math")

    print(alice.introduce())
    print(mr_mueller.introduce())