from datetime import datetime

def print_header():
    print("\n" + "=" * 40)
    print(" SOLDIER LEAVE CHECKLIST GENERATOR")
    print("=" * 40)

def display_menu():
    print("\nSelect Leave Type")
    print("-" * 17)
    print("1. Ordinary Leave")
    print("2. Emergency Leave")
    print("3. Convalescent Leave")
    print("4. Pass")
    print("5. Exit")


def get_checklist(leave_type):
    checklists = {
        "1": {
            "title": "Ordinary Leave Checklist",
            "items": [
                "Submit absence request in IPPS-A",
                "Confirm leave address and contact information",
                "Verify leave dates do not conflict with duty, training, or appointments",
                "Notify first-line leader of planned leave dates",
                "Confirm approval authority and routing chain",
                "Review unit leave policy for any additional requirements"
            ]
        },
        "2": {
            "title": "Emergency Leave Checklist",
            "items": [
                "Notify chain of command immediately",
                "Submit emergency absence request in IPPS-A",
                "Provide emergency contact information",
                "Provide supporting documentation if required",
                "Coordinate travel plan with leadership",
                "Confirm approval before departure unless otherwise directed"
            ]
        },
        "3": {
            "title": "Convalescent Leave Checklist",
            "items": [
                "Obtain medical provider recommendation",
                "Ensure medical documentation supports convalescent leave",
                "Submit absence request in IPPS-A",
                "Coordinate with chain of command",
                "Confirm profile or medical limitations if applicable",
                "Follow all medical instructions during recovery period"
            ]
        },
        "4": {
            "title": "Pass Checklist",
            "items": [
                "Confirm pass dates with first-line leader",
                "Verify pass does not conflict with duty or training",
                "Provide location and contact information if required",
                "Review local mileage or travel restrictions",
                "Ensure accountability requirements are understood",
                "Return by the required time"
            ]
        }
    }

    return checklists.get(leave_type)


def print_checklist(
    checklist,
    soldier_name,
    start_date,
    end_date
):
    leave_days = calculate_leave_days(
        start_date,
        end_date
    )

    print("\n" + "=" * 40)
    print(" LEAVE REQUEST SUMMARY")
    print("=" * 40)

    print(f"Soldier: {soldier_name}")
    print(f"Start Date: {start_date}")
    print(f"End Date: {end_date}")
    print(f"Total Leave Days: {leave_days}")

    print("\n" + checklist["title"])
    print("-" * len(checklist["title"]))

    for number, item in enumerate(
        checklist["items"],
        start=1
    ):
        print(f"{number}. {item}")

    print("\n" + "=" * 40)
    print(" LEAVE STATUS")
    print("=" * 40)

    print(
        f"Leave Type: "
        f"{checklist['title']}"
    )

    print(
        f"Duration: "
        f"{leave_days} day(s)"
    )

    print(
        "Status: Ready for Submission"
    )

    save_checklist_to_file(
        checklist,
        soldier_name,
        start_date,
        end_date,
        leave_days
    )

def calculate_leave_days(start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    leave_days = (end - start).days

    return leave_days

def save_checklist_to_file(
    checklist,
    soldier_name,
    start_date,
    end_date,
    leave_days
):
    filename = (
    f"{soldier_name}"
    "_leave_checklist.txt"
    )

    with open(filename, "w") as file:
        file.write(
            f"Soldier: {soldier_name}\n"
        )

        file.write(
            f"Start Date: {start_date}\n"
        )

        file.write(
            f"End Date: {end_date}\n"
        )

        file.write(
            f"Total Leave Days: {leave_days}\n\n"
        )

        file.write(
            f"{checklist['title']}\n"
        )

        file.write(
            "-" * len(checklist["title"])
            + "\n"
        )

        for number, item in enumerate(
            checklist["items"],
            start=1
        ):
            file.write(
                f"{number}. {item}\n"
            )

    print(
        f"\nChecklist saved as "
        f"{filename}"
    )

def get_valid_date(prompt):
    while True:
        user_input = input(prompt)

        try:
            datetime.strptime(
                user_input,
                "%Y-%m-%d"
            )

            return user_input

        except ValueError:
            print(
                "\nInvalid date format."
            )

            print(
                "Please use YYYY-MM-DD.\n"
            )

def get_leave_dates():
    while True:
        start_date = get_valid_date(
            "Enter leave start date (YYYY-MM-DD): "
        )

        end_date = get_valid_date(
            "Enter leave end date (YYYY-MM-DD): "
        )

        leave_days = calculate_leave_days(
            start_date,
            end_date
        )

        if leave_days < 0:
            print(
                "\nEnd date cannot be earlier than start date."
            )

            print(
                "Please enter the dates again.\n"
            )
        else:
            return start_date, end_date

def main():
    while True:
        print_header()

        soldier_name = input(
            "\nEnter Soldier name: "
        )

        start_date, end_date = get_leave_dates()

        display_menu()

        choice = input(
            "\nSelect an option: "
        )

        if choice == "5":
            print(
                f"Goodbye, {soldier_name}."
            )
            break

        checklist = get_checklist(choice)

        if checklist:
            print_checklist(
                checklist,
                soldier_name,
                start_date,
                end_date
            )
        else:
            print(
                "Invalid option. "
                "Please select a number from 1 to 5."
            )

        run_again = input(
            "\nWould you like to create "
            "another checklist? "
            "(yes/no): "
        ).lower()

        if run_again != "yes":
            print(
                f"\nGoodbye, "
                f"{soldier_name}."
            )
            break

if __name__ == "__main__":
    main()