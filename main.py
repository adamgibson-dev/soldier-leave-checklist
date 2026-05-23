def display_menu():
    print("\nSoldier Leave Checklist Generator")
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


def print_checklist(checklist, soldier_name):
    print(f"\nSoldier: {soldier_name}")
    print(f"{checklist['title']}")
    print("-" * len(checklist["title"]))

    for number, item in enumerate(checklist["items"], start=1):
        print(f"{number}. {item}")


def main():
    soldier_name = input("Enter Soldier name: ")

    while True:
        display_menu()
        choice = input("\nSelect an option: ")

        if choice == "5":
            print(f"Goodbye, {soldier_name}.")
            break

        checklist = get_checklist(choice)

        if checklist:
            print_checklist(checklist, soldier_name)
        else:
            print("Invalid option. Please select a number from 1 to 5.")

        if choice == "5":
            print("Goodbye.")
            break

        checklist = get_checklist(choice)

        if checklist:
            print_checklist(checklist,soldier_name)
        else:
            print("Invalid option. Please select a number from 1 to 5.")


if __name__ == "__main__":
    main()