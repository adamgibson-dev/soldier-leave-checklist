from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

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

def get_risk_assessment():
    risk_flags = []

    print("\n" + "=" * 40)
    print(" LEAVE RISK ASSESSMENT")
    print("=" * 40)

    overseas_travel = input(
        "Will the Soldier travel outside the United States? (yes/no): "
    ).lower()

    if overseas_travel == "yes":
        risk_flags.append("Overseas travel requires additional review")

    emergency_contact = input(
        "Does the Soldier have a verified emergency contact? (yes/no): "
    ).lower()

    if emergency_contact != "yes":
        risk_flags.append("Emergency contact is missing or not verified")

    recall_number = input(
        "Does the Soldier have a valid recall phone number? (yes/no): "
    ).lower()

    if recall_number != "yes":
        risk_flags.append("Recall phone number is missing or invalid")

    training_conflict = input(
        "Does this leave conflict with duty, training, or appointments? (yes/no): "
    ).lower()

    if training_conflict == "yes":
        risk_flags.append("Leave conflicts with duty, training, or appointments")

    mileage_restriction = input(
        "Does travel exceed local mileage or pass distance limits? (yes/no): "
    ).lower()

    if mileage_restriction == "yes":
        risk_flags.append("Travel may exceed mileage or pass distance limits")

    return risk_flags

def print_checklist(
    checklist,
    soldier_name,
    unit,
    start_date,
    end_date,
    risk_flags
):
    leave_days = calculate_leave_days(
        start_date,
        end_date
    )

    print("\n" + "=" * 40)
    print(" LEAVE REQUEST SUMMARY")
    print("=" * 40)

    print(f"Soldier: {soldier_name}")
    print(f"Unit: {unit}")
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
    print(" RISK ASSESSMENT")
    print("=" * 40)

    if risk_flags:
        for flag in risk_flags:
            print(f"WARNING: {flag}")

        status = "Requires Leadership Review"
    else:
        print("No risk flags identified")
        status = "Ready for Submission"

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
        f"Status: {status}"
    )

    save_checklist_to_file(
        checklist,
        soldier_name,
        unit,
        start_date,
        end_date,
        leave_days,
        risk_flags,
        status
    )

    save_checklist_to_pdf(
        checklist,
        soldier_name,
        unit,
        start_date,
        end_date,
        leave_days,
        risk_flags,
        status
    )

def calculate_leave_days(start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    leave_days = (end - start).days

    return leave_days

def save_checklist_to_file(
    checklist,
    soldier_name,
    unit,
    start_date,
    end_date,
    leave_days,
    risk_flags,
    status
):
    filename = (
        f"{soldier_name}"
        "_leave_checklist.txt"
    )

    with open(filename, "w") as file:
        file.write(f"Soldier: {soldier_name}\n")
        file.write(f"Unit: {unit}\n")
        file.write(f"Start Date: {start_date}\n")
        file.write(f"End Date: {end_date}\n")
        file.write(
            f"Total Leave Days: "
            f"{leave_days}\n\n"
        )

        file.write(
            f"{checklist['title']}\n"
        )

        file.write(
            "-" *
            len(checklist["title"])
            + "\n"
        )

        for number, item in enumerate(
            checklist["items"],
            start=1
        ):
            file.write(
                f"{number}. {item}\n"
            )

        file.write("\n")
        file.write("=" * 40 + "\n")
        file.write(
            "RISK ASSESSMENT\n"
        )
        file.write("=" * 40 + "\n")

        if risk_flags:
            for flag in risk_flags:
                file.write(
                    f"WARNING: {flag}\n"
                )
        else:
            file.write(
                "No risk flags identified\n"
            )

        file.write("\n")
        file.write("=" * 40 + "\n")
        file.write(
            "LEAVE STATUS\n"
        )
        file.write("=" * 40 + "\n")

        file.write(
            f"Leave Type: "
            f"{checklist['title']}\n"
        )

        file.write(
            f"Duration: "
            f"{leave_days} day(s)\n"
        )

        file.write(
            f"Status: {status}\n"
        )

    print(
        f"\nText file saved as "
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

def save_checklist_to_pdf(
    checklist,
    soldier_name,
    unit,
    start_date,
    end_date,
    leave_days,
    risk_flags,
    status
):
    filename = (
        f"{soldier_name}"
        "_leave_checklist.pdf"
    )

    pdf = canvas.Canvas(filename, pagesize=letter)

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(72, 750, "Soldier Leave Checklist")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(72, 720, f"Soldier: {soldier_name}")
    pdf.drawString(72, 700, f"Unit: {unit}")
    pdf.drawString(72, 680, f"Start Date: {start_date}")
    pdf.drawString(72, 660, f"End Date: {end_date}")
    pdf.drawString(72, 640, f"Total Leave Days: {leave_days}")

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(72, 605, checklist["title"])

    y_position = 580

    pdf.setFont("Helvetica", 11)

    for number, item in enumerate(
        checklist["items"],
        start=1
    ):
        pdf.drawString(
            72,
            y_position,
            f"{number}. {item}"
        )

        y_position -= 20

    y_position -= 20

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(72, y_position, "Risk Assessment")

    y_position -= 20

    pdf.setFont("Helvetica", 11)

    if risk_flags:
        for flag in risk_flags:
            pdf.drawString(
                72,
                y_position,
                f"WARNING: {flag}"
            )

            y_position -= 20
    else:
        pdf.drawString(
            72,
            y_position,
            "No risk flags identified"
        )

        y_position -= 20

    y_position -= 20

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(72, y_position, "Leave Status")

    y_position -= 20

    pdf.setFont("Helvetica", 11)

    pdf.drawString(
        72,
        y_position,
        f"Leave Type: {checklist['title']}"
    )

    y_position -= 20

    pdf.drawString(
        72,
        y_position,
        f"Duration: {leave_days} day(s)"
    )

    y_position -= 20

    pdf.drawString(
        72,
        y_position,
        f"Status: {status}"
    )

    pdf.save()

    print(f"PDF saved as {filename}")

def main():
    while True:
        print_header()

        rank = input(
            "\nEnter Soldier rank: "
        ).upper()

        last_name = input(
            "Enter Soldier last name: "
        ).title()

        soldier_name = (
            f"{rank} {last_name}"
        )

        unit = input(
            "Enter unit: "
        ).upper()

        start_date, end_date = (
            get_leave_dates()
        )

        display_menu()

        choice = input(
            "\nSelect an option: "
        )

        if choice == "5":
            print(
                f"Goodbye, "
                f"{soldier_name}."
            )
            break

        checklist = get_checklist(
            choice
        )

        if checklist:
            risk_flags = get_risk_assessment()

        if checklist:
            print_checklist(
                checklist,
                soldier_name,
                unit,
                start_date,
                end_date,
                risk_flags
            )
        else:
            print(
                "Invalid option. "
                "Please select a "
                "number from 1 to 5."
            )

        run_again = input(
            "\nWould you like "
            "to create another "
            "checklist? "
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