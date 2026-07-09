"""
CareerPath Application Tracker

This program helps users track job and internship applications.
Users can add applications, view saved applications, filter by status,
update application statuses, delete applications, and see a simple
priority score.

Applications are saved to and loaded from a JSON file.
"""

import json
from datetime import datetime, date


DATA_FILE = "applications.json"

VALID_STATUSES = [
    "Interested",
    "Applied",
    "Interviewing",
    "Rejected",
    "Accepted",
    "Need Follow-Up"
]


class Application:
    """Represents one job or internship application."""

    def __init__(
        self,
        company,
        role,
        deadline,
        status,
        required_skills,
        user_skills,
        interest_level,
        notes
    ):
        self.company = company
        self.role = role
        self.deadline = deadline
        self.status = status
        self.required_skills = required_skills
        self.user_skills = user_skills
        self.interest_level = interest_level
        self.notes = notes

    def calculate_priority_score(self):
        """
        Calculates a priority score out of 100.

        Score is based on:
        - interest level
        - skill match
        - deadline urgency
        """

        interest_score = self.interest_level * 10

        if len(self.required_skills) > 0:
            matching_skills = 0

            for skill in self.required_skills:
                if skill in self.user_skills:
                    matching_skills += 1

            skill_score = int((matching_skills / len(self.required_skills)) * 30)
        else:
            skill_score = 0

        today = date.today()
        days_until_deadline = (self.deadline - today).days

        if days_until_deadline < 0:
            deadline_score = 0
        elif days_until_deadline <= 7:
            deadline_score = 20
        elif days_until_deadline <= 14:
            deadline_score = 15
        elif days_until_deadline <= 30:
            deadline_score = 10
        else:
            deadline_score = 5

        return interest_score + skill_score + deadline_score

    def get_missing_skills(self):
        """Returns a list of required skills that the user does not have."""

        missing_skills = []

        for skill in self.required_skills:
            if skill not in self.user_skills:
                missing_skills.append(skill)

        return missing_skills

    def to_dict(self):
        """Converts an Application object into a dictionary."""

        return {
            "company": self.company,
            "role": self.role,
            "deadline": self.deadline.strftime("%Y-%m-%d"),
            "status": self.status,
            "required_skills": self.required_skills,
            "user_skills": self.user_skills,
            "interest_level": self.interest_level,
            "notes": self.notes
        }

    def display(self):
        """Displays the application information."""

        print("\n----------------------------------------")
        print(f"Company: {self.company}")
        print(f"Role: {self.role}")
        print(f"Deadline: {self.deadline}")
        print(f"Status: {self.status}")
        print(f"Required Skills: {', '.join(self.required_skills)}")
        print(f"Your Skills: {', '.join(self.user_skills)}")
        print(f"Interest Level: {self.interest_level}/5")
        print(f"Priority Score: {self.calculate_priority_score()}/100")

        missing_skills = self.get_missing_skills()

        if len(missing_skills) > 0:
            print(f"Missing Skills: {', '.join(missing_skills)}")
        else:
            print("Missing Skills: None")

        print(f"Notes: {self.notes}")
        print("----------------------------------------")


def display_menu():
    """Displays the main menu."""

    print("\nCareerPath Application Tracker")
    print("1. Add application")
    print("2. View all applications")
    print("3. Filter applications by status")
    print("4. Update application status")
    print("5. Delete application")
    print("6. Quit")


def get_non_empty_input(prompt):
    """Keeps asking the user for input until they enter something."""

    user_input = input(prompt).strip()

    while user_input == "":
        print("Input cannot be blank. Please try again.")
        user_input = input(prompt).strip()

    return user_input


def get_deadline():
    """Gets and validates the application deadline."""

    while True:
        deadline_input = input("Enter deadline (YYYY-MM-DD): ").strip()

        try:
            deadline = datetime.strptime(deadline_input, "%Y-%m-%d").date()
            return deadline
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")


def get_status():
    """Gets and validates the application status."""

    print("\nStatus Options:")

    for index, status in enumerate(VALID_STATUSES, start=1):
        print(f"{index}. {status}")

    while True:
        choice = input("Choose a status number: ").strip()

        if choice.isdigit():
            choice = int(choice)

            if 1 <= choice <= len(VALID_STATUSES):
                return VALID_STATUSES[choice - 1]

        print("Invalid choice. Please choose a valid status number.")


def get_interest_level():
    """Gets and validates the user's interest level."""

    while True:
        interest_input = input("Enter interest level (1-5): ").strip()

        if interest_input.isdigit():
            interest_level = int(interest_input)

            if 1 <= interest_level <= 5:
                return interest_level

        print("Invalid interest level. Please enter a number from 1 to 5.")


def get_skills(prompt):
    """
    Gets a list of skills from the user.

    Example input:
    Python, SQL, Excel
    """

    skills_input = input(prompt).strip()

    if skills_input == "":
        return []

    skills = skills_input.split(",")
    cleaned_skills = []

    for skill in skills:
        cleaned_skills.append(skill.strip().lower())

    return cleaned_skills


def save_applications(applications):
    """Saves all applications to a JSON file."""

    application_data = []

    for application in applications:
        application_data.append(application.to_dict())

    with open(DATA_FILE, "w") as file:
        json.dump(application_data, file, indent=4)

    print("Applications saved.")


def load_applications():
    """Loads applications from a JSON file."""

    applications = []

    try:
        with open(DATA_FILE, "r") as file:
            application_data = json.load(file)

            for item in application_data:
                deadline = datetime.strptime(
                    item["deadline"],
                    "%Y-%m-%d"
                ).date()

                application = Application(
                    item["company"],
                    item["role"],
                    deadline,
                    item["status"],
                    item["required_skills"],
                    item["user_skills"],
                    item["interest_level"],
                    item["notes"]
                )

                applications.append(application)

    except FileNotFoundError:
        pass

    except json.JSONDecodeError:
        print("Saved file could not be read. Starting with an empty tracker.")

    return applications


def add_application(applications):
    """Adds a new job or internship application."""

    print("\nAdd New Application")

    company = get_non_empty_input("Enter company name: ")
    role = get_non_empty_input("Enter role title: ")
    deadline = get_deadline()
    status = get_status()

    required_skills = get_skills(
        "Enter required skills separated by commas: "
    )

    user_skills = get_skills(
        "Enter your current skills separated by commas: "
    )

    interest_level = get_interest_level()
    notes = input("Enter any notes: ").strip()

    new_application = Application(
        company,
        role,
        deadline,
        status,
        required_skills,
        user_skills,
        interest_level,
        notes
    )

    applications.append(new_application)

    print("\nApplication added successfully.")


def view_applications(applications):
    """Displays all saved applications."""

    if len(applications) == 0:
        print("\nNo applications saved yet.")
    else:
        print("\nAll Applications")

        for application in applications:
            application.display()


def filter_by_status(applications):
    """Displays applications that match a selected status."""

    if len(applications) == 0:
        print("\nNo applications saved yet.")
        return

    selected_status = get_status()
    found_application = False

    print(f"\nApplications with status: {selected_status}")

    for application in applications:
        if application.status == selected_status:
            application.display()
            found_application = True

    if found_application is False:
        print("No applications found with that status.")


def update_application_status(applications):
    """Updates the status of a selected application."""

    if len(applications) == 0:
        print("\nNo applications saved yet.")
        return

    print("\nSelect an application to update:")

    for index, application in enumerate(applications, start=1):
        print(
            f"{index}. {application.company} - "
            f"{application.role} ({application.status})"
        )

    while True:
        choice = input("Choose an application number: ").strip()

        if choice.isdigit():
            choice = int(choice)

            if 1 <= choice <= len(applications):
                selected_application = applications[choice - 1]

                print(
                    f"\nCurrent status for {selected_application.company} - "
                    f"{selected_application.role}: "
                    f"{selected_application.status}"
                )

                new_status = get_status()
                selected_application.status = new_status

                print("\nApplication status updated successfully.")
                return

        print("Invalid choice. Please choose a valid application number.")


def delete_application(applications):
    """Deletes a selected application."""

    if len(applications) == 0:
        print("\nNo applications saved yet.")
        return

    print("\nSelect an application to delete:")

    for index, application in enumerate(applications, start=1):
        print(
            f"{index}. {application.company} - "
            f"{application.role} ({application.status})"
        )

    while True:
        choice = input("Choose an application number: ").strip()

        if choice.isdigit():
            choice = int(choice)

            if 1 <= choice <= len(applications):
                selected_application = applications[choice - 1]

                print(
                    f"\nYou selected: {selected_application.company} - "
                    f"{selected_application.role}"
                )

                confirm = input(
                    "Are you sure you want to delete this application? (yes/no): "
                ).strip().lower()

                if confirm == "yes":
                    applications.pop(choice - 1)
                    print("\nApplication deleted successfully.")
                    return
                elif confirm == "no":
                    print("\nDelete canceled.")
                    return
                else:
                    print("Invalid response. Delete canceled.")
                    return

        print("Invalid choice. Please choose a valid application number.")


def main():
    """Runs the CareerPath Application Tracker program."""

    applications = load_applications()

    while True:
        display_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_application(applications)
            save_applications(applications)

        elif choice == "2":
            view_applications(applications)

        elif choice == "3":
            filter_by_status(applications)

        elif choice == "4":
            update_application_status(applications)
            save_applications(applications)

        elif choice == "5":
            delete_application(applications)
            save_applications(applications)

        elif choice == "6":
            save_applications(applications)
            print("\nGoodbye.")
            break

        else:
            print("Invalid choice. Please choose 1, 2, 3, 4, 5, or 6.")


if __name__ == "__main__":
    main()