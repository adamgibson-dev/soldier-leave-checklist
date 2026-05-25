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

    overseas_travel = get_yes_or_no(
        "Will the Soldier travel outside the United States? (YES/NO): "
    )

    if overseas_travel == "BACK":
        return "BACK"

    if overseas_travel == "YES":
        risk_flags.append(
            "Overseas travel requires additional review"
        )

    emergency_contact = get_yes_or_no(
        "Does the Soldier have a verified emergency contact? (YES/NO): "
    )

    if emergency_contact == "BACK":
        return "BACK"

    if emergency_contact == "NO":
        risk_flags.append(
            "Emergency contact is missing or not verified"
        )

    recall_number = get_yes_or_no(
        "Does the Soldier have a valid recall phone number? (YES/NO): "
    )

    if recall_number == "BACK":
        return "BACK"

    if recall_number == "NO":
        risk_flags.append(
            "Recall phone number is missing or invalid"
        )

    training_conflict = get_yes_or_no(
        "Does this leave conflict with duty, training, or appointments? (YES/NO): "
    )

    if training_conflict == "BACK":
        return "BACK"

    if training_conflict == "YES":
        risk_flags.append(
            "Leave conflicts with duty, training, or appointments"
        )

    mileage_restriction = get_yes_or_no(
        "Does travel exceed local mileage or pass distance limits? (YES/NO): "
    )

    if mileage_restriction == "BACK":
        return "BACK"

    if mileage_restriction == "YES":
        risk_flags.append(
            "Travel may exceed mileage or pass distance limits"
        )

    return risk_flags

def get_emergency_contact_info():
    print("\n" + "=" * 40)
    print(" EMERGENCY CONTACT INFORMATION")
    print("=" * 40)

    contact_name = get_valid_name(
        "Enter emergency contact full name: "
    ).title()

    relationship = get_valid_relationship(
        "Enter relationship to Soldier: "
    ).title()

    phone_number = get_valid_phone_number(
        "Enter emergency contact phone number: "
    )

    leave_address = get_valid_address(
        "Enter Soldier leave address: "
    ).title()

    travel_method = get_valid_travel_method(
        "Enter travel method (POV, FLIGHT, BUS, TRAIN, OTHER): "
    )

    emergency_contact = {
        "contact_name": contact_name,
        "relationship": relationship,
        "phone_number": phone_number,
        "leave_address": leave_address,
        "travel_method": travel_method
    }

    return emergency_contact


def print_checklist(
    checklist,
    soldier_name,
    unit,
    company,
    start_date,
    end_date,
    risk_flags,
    emergency_contact
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
    print(f"Company: {company}")
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
    print(" EMERGENCY CONTACT")
    print("=" * 40)

    print(
        f"Contact Name: "
        f"{emergency_contact['contact_name']}"
    )

    print(
        f"Relationship: "
        f"{emergency_contact['relationship']}"
    )

    print(
        f"Phone Number: "
        f"{emergency_contact['phone_number']}"
    )

    print(
        f"Leave Address: "
        f"{emergency_contact['leave_address']}"
    )

    print(
        f"Travel Method: "
        f"{emergency_contact['travel_method']}"
    )

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
        company,
        start_date,
        end_date,
        leave_days,
        risk_flags,
        status,
        emergency_contact
    )

    save_checklist_to_pdf(
        checklist,
        soldier_name,
        unit,
        company,
        start_date,
        end_date,
        leave_days,
        risk_flags,
        status,
        emergency_contact
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
    company,
    start_date,
    end_date,
    leave_days,
    risk_flags,
    status,
    emergency_contact
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
            f"Unit: {unit}\n"
        )

        file.write(
            f"Company: {company}\n"
        )

        file.write(
            f"Start Date: {start_date}\n"
        )

        file.write(
            f"End Date: {end_date}\n"
        )

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
            "EMERGENCY CONTACT\n"
        )
        file.write("=" * 40 + "\n")

        file.write(
            f"Contact Name: "
            f"{emergency_contact['contact_name']}\n"
        )

        file.write(
            f"Relationship: "
            f"{emergency_contact['relationship']}\n"
        )

        file.write(
            f"Phone Number: "
            f"{emergency_contact['phone_number']}\n"
        )

        file.write(
            f"Leave Address: "
            f"{emergency_contact['leave_address']}\n"
        )

        file.write(
            f"Travel Method: "
            f"{emergency_contact['travel_method']}\n"
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
        show_navigation_options()

        user_input = input(prompt).strip()

        user_input = handle_navigation(
            user_input
        )

        if user_input == "BACK":
            return "BACK"

        try:
            datetime.strptime(
                user_input,
                "%Y-%m-%d"
            )

            return user_input

        except ValueError:
            print("\nInvalid date format.")
            print("Please use YYYY-MM-DD.\n")

def get_valid_name(prompt):
    while True:
        show_navigation_options()

        name = input(prompt).strip()

        name = handle_navigation(
            name
        )

        if name == "BACK":
            return "BACK"

        split_name = name.split()

        if (
            len(split_name) >= 2
            and all(
                part.replace(
                    "-", ""
                ).replace(
                    "'", ""
                ).isalpha()
                for part in split_name
            )
        ):
            return name.title()

        print("\nInvalid name.")
        print(
            "Please enter a first "
            "and last name.\n"
        )

def get_required_input(prompt):
    while True:
        user_input = input(prompt).strip()

        if user_input:
            return user_input

        print(
            "\nThis field cannot be blank."
        )

        print(
            "Please enter a valid response.\n"
        )


def get_valid_phone_number(prompt):
    while True:
        phone_number = input(prompt).strip()

        cleaned_phone_number = (
            phone_number
            .replace("-", "")
            .replace("(", "")
            .replace(")", "")
            .replace(" ", "")
        )

        if (
            cleaned_phone_number.isdigit()
            and len(cleaned_phone_number) == 10
        ):
            return phone_number

        print(
            "\nInvalid phone number."
        )

        print(
            "Please enter a 10-digit phone number."
        )

        print(
            "Example: 907-555-1234\n"
        )


def get_valid_travel_method(prompt):
    valid_methods = [
        "POV",
        "FLIGHT",
        "BUS",
        "TRAIN"
    ]

    while True:
        travel_method = (
            input(prompt)
            .strip()
            .upper()
        )

        travel_method = (
            handle_navigation(
                travel_method
            )
        )

        if travel_method == "BACK":
            return "BACK"

        if (
            travel_method
            in valid_methods
        ):
            return travel_method

        print(
            "\nInvalid travel method."
        )

        print(
            "Valid travel methods:"
        )

        print(
            "POV, FLIGHT, "
            "BUS, TRAIN\n"
        )

def get_valid_rank(prompt):
    valid_ranks = [
        "PVT", "PV2", "PFC", "SPC", "CPL",
        "SGT", "SSG", "SFC", "MSG", "1SG",
        "SGM", "CSM", "2LT", "1LT", "CPT",
        "MAJ", "LTC", "COL", "CW2", "CW3",
        "CW4", "CW5"
    ]

    while True:
        show_navigation_options()

        rank = input(prompt).strip().upper()

        rank = handle_navigation(
            rank
        )

        if rank == "BACK":
            return "BACK"

        if rank in valid_ranks:
            return rank

        print("\nInvalid rank.")
        print("Please enter a valid Army rank.")
        print("Example: SPC, SGT, SSG, 2LT, CPT\n")

def get_valid_name_part(prompt):
    while True:
        show_navigation_options()

        name = input(prompt).strip()

        name = handle_navigation(
            name
        )

        if name == "BACK":
            return "BACK"

        if (
            name.isalpha()
            and len(name) >= 2
        ):
            return name.title()

        print("\nInvalid name.")
        print(
            "Please enter letters only, "
            "at least 2 characters.\n"
        )

def get_valid_unit(prompt):
    while True:
        show_navigation_options()

        unit = input(prompt).strip()

        unit = handle_navigation(
            unit
        )

        if unit == "BACK":
            return "BACK"

        if len(unit) >= 2:
            return unit.upper()

        print("\nInvalid unit.")
        print("Unit cannot be blank.\n")

def get_valid_company(prompt):
    valid_companies = [
        "HHC",
        "A CO",
        "B CO",
        "C CO",
        "D CO",
        "E CO",
        "F CO",
        "S6",
        "BN STAFF"
    ]

    while True:
        show_navigation_options()

        company = input(prompt).strip().upper()

        company = handle_navigation(
            company
        )

        if company == "BACK":
            return "BACK"

        if company in valid_companies:
            return company

        print("\nInvalid company.")
        print("Valid examples:")
        print(", ".join(valid_companies) + "\n")

def get_valid_address(prompt):
    while True:
        address = input(prompt).strip()

        if (
            len(address) >= 8
            and any(character.isdigit() for character in address)
            and any(character.isalpha() for character in address)
        ):
            return address.title()

        print(
            "\nInvalid address."
        )

        print(
            "Please enter a valid leave address "
            "with a street number and street name.\n"
        )

def get_yes_or_no(prompt):
    while True:
        show_navigation_options()

        answer = input(prompt).strip().upper()

        answer = handle_navigation(
            answer
        )

        if answer == "BACK":
            return "BACK"

        if answer in ["YES", "NO"]:
            return answer

        print("\nInvalid response.")
        print("Please enter YES or NO.\n")

def handle_navigation(user_input):
    user_input = user_input.strip()

    if user_input.upper() == "EXIT":
        print("\nExiting program...")
        exit()

    if user_input.upper() == "BACK":
        return "BACK"

    return user_input


def show_navigation_options():
    print("\nType BACK to return to the previous step.")
    print("Type EXIT to quit.\n")


def get_required_input(prompt):
    while True:
        show_navigation_options()

        user_input = input(prompt).strip()

        user_input = handle_navigation(
            user_input
        )

        if user_input == "BACK":
            return "BACK"

        if user_input:
            return user_input

        print("\nThis field cannot be blank.")
        print("Please enter a valid response.\n")

def get_valid_unit(prompt):
    valid_units = [
        "1ST BATTALION, 501ST INFANTRY REGIMENT (1-501 INF)",
        "3RD BATTALION, 509TH INFANTRY REGIMENT (3-509 INF)",
        "1ST SQUADRON, 40TH CAVALRY REGIMENT (1-40 CAV)",
        "2ND BATTALION, 377TH FIELD ARTILLERY REGIMENT (2-377 PFAR)",
        "6TH BRIGADE ENGINEER BATTALION (6TH BEB)",
        "725TH BRIGADE SUPPORT BATTALION (725TH BSB)"
    ]

    while True:
        show_navigation_options()

        unit = input(prompt).strip()

        unit = handle_navigation(
            unit
        )

        if unit == "BACK":
            return "BACK"

        unit_upper = unit.upper()

        if unit_upper in valid_units:
            return unit_upper

        print("\nInvalid unit.")
        print("Valid examples:")

        for valid_unit in valid_units:
            print(f"- {valid_unit}")

        print()

    while True:
        show_navigation_options()

        unit = input(prompt).strip().upper()

        unit = handle_navigation(
            unit
        )

        if unit == "BACK":
            return "BACK"

        if unit in valid_units:
            return unit

        print("\nInvalid unit.")
        print("Valid examples:")
        print(", ".join(valid_units) + "\n")

def get_valid_menu_choice(prompt):
    valid_choices = [
        "1",
        "2",
        "3",
        "4",
        "5"
    ]

    while True:
        show_navigation_options()

        choice = input(prompt).strip()

        choice = handle_navigation(
            choice
        )

        if choice == "BACK":
            return "BACK"

        if choice in valid_choices:
            return choice

        print("\nInvalid menu option.")
        print("Please select a number from 1 to 5.\n")

def get_valid_relationship(prompt):
    valid_relationships = [
        "MOTHER",
        "FATHER",
        "SPOUSE",
        "HUSBAND",
        "WIFE",
        "BROTHER",
        "SISTER",
        "GRANDMOTHER",
        "GRANDFATHER",
        "AUNT",
        "UNCLE",
        "FRIEND",
        "GUARDIAN",
        "OTHER"
    ]

    while True:
        relationship = (
            input(prompt)
            .strip()
            .upper()
        )

        if relationship in valid_relationships:
            return relationship.title()

        print(
            "\nInvalid relationship."
        )

        print(
            "Valid options include:"
        )

        print(
            ", ".join(valid_relationships)
            + "\n"
        )

    while True:
        travel_method = input(prompt).strip().upper()

        if travel_method in valid_methods:
            return travel_method

        print(
            "\nInvalid travel method."
        )

        print(
            "Valid options: POV, FLIGHT, BUS, TRAIN, OTHER\n"
        )

def get_valid_name_part(prompt):
    while True:
        go_back_prompt()

        name = input(prompt).strip()

        name = handle_navigation(
            name
        )

        if name.upper() == "BACK":
            return "BACK"

        if (
            name.isalpha()
            and len(name) >= 2
        ):
            return name.title()

        print(
            "\nInvalid name."
        )

        print(
            "Please enter letters only, "
            "at least 2 characters.\n"
        )

def handle_navigation(user_input):
    user_input = user_input.strip().upper()

    if user_input == "EXIT":
        print(
            "\nExiting program..."
        )
        exit()

    return user_input

def go_back_prompt():
    print(
        "\nType BACK to return "
        "to the previous step."
    )

    print(
        "Type EXIT to quit.\n"
    )

def get_leave_dates():
    while True:
        start_date = get_valid_date(
            "Enter leave start date (YYYY-MM-DD): "
        )

        if start_date == "BACK":
            return "BACK", "BACK"

        end_date = get_valid_date(
            "Enter leave end date (YYYY-MM-DD): "
        )

        if end_date == "BACK":
            continue

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
    company,
    start_date,
    end_date,
    leave_days,
    risk_flags,
    status,
    emergency_contact
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
    pdf.drawString(72, 680, f"Company: {company}")
    pdf.drawString(72, 660, f"Start Date: {start_date}")
    pdf.drawString(72, 640, f"End Date: {end_date}")
    pdf.drawString(72, 620, f"Total Leave Days: {leave_days}")

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(72, 585, checklist["title"])

    y_position = 560

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
    pdf.drawString(72, y_position, "Emergency Contact")

    y_position -= 20

    pdf.setFont("Helvetica", 11)

    pdf.drawString(
        72,
        y_position,
        f"Contact Name: {emergency_contact['contact_name']}"
    )

    y_position -= 20

    pdf.drawString(
        72,
        y_position,
        f"Relationship: {emergency_contact['relationship']}"
    )

    y_position -= 20

    pdf.drawString(
        72,
        y_position,
        f"Phone Number: {emergency_contact['phone_number']}"
    )

    y_position -= 20

    pdf.drawString(
        72,
        y_position,
        f"Leave Address: {emergency_contact['leave_address']}"
    )

    y_position -= 20

    pdf.drawString(
        72,
        y_position,
        f"Travel Method: {emergency_contact['travel_method']}"
    )

    y_position -= 30

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

        step = "rank"

        rank = ""
        first_name = ""
        last_name = ""
        soldier_name = ""
        unit = ""
        company = ""
        start_date = ""
        end_date = ""
        choice = ""
        checklist = None
        risk_flags = []
        emergency_contact = {}

        while True:
            if step == "rank":
                rank = get_valid_rank(
                    "\nEnter Soldier rank: "
                )

                if rank == "BACK":
                    continue

                step = "first_name"

            elif step == "first_name":
                first_name = get_valid_name_part(
                    "Enter Soldier first name: "
                )

                if first_name == "BACK":
                    step = "rank"
                else:
                    step = "last_name"

            elif step == "last_name":
                last_name = get_valid_name_part(
                    "Enter Soldier last name: "
                )

                if last_name == "BACK":
                    step = "first_name"
                else:
                    soldier_name = (
                        f"{rank} "
                        f"{first_name} "
                        f"{last_name}"
                    )

                    step = "unit"

            elif step == "unit":
                unit = get_valid_unit(
                    "Enter unit: "
                )

                if unit == "BACK":
                    step = "last_name"
                else:
                    step = "company"

            elif step == "company":
                company = get_valid_company(
                    "Enter company: "
                )

                if company == "BACK":
                    step = "unit"
                else:
                    step = "dates"

            elif step == "dates":
                start_date, end_date = (
                    get_leave_dates()
                )

                if (
                    start_date == "BACK"
                    or end_date == "BACK"
                ):
                    step = "company"
                else:
                    step = "leave_type"

            elif step == "leave_type":
                display_menu()

                choice = (
                    get_valid_menu_choice(
                        "\nSelect an option: "
                    )
                )

                if choice == "BACK":
                    step = "dates"

                elif choice == "5":
                    print(
                        f"Goodbye, "
                        f"{soldier_name}."
                    )
                    return

                else:
                    checklist = (
                        get_checklist(
                            choice
                        )
                    )

                    step = "risk"

            elif step == "risk":
                risk_flags = (
                    get_risk_assessment()
                )

                if risk_flags == "BACK":
                    step = "leave_type"
                else:
                    step = (
                        "emergency_contact"
                    )

            elif step == "emergency_contact":
                emergency_contact = (
                    get_emergency_contact_info()
                )

                if (
                    emergency_contact
                    == "BACK"
                ):
                    step = "risk"
                else:
                    step = "print"

            elif step == "print":
                print_checklist(
                    checklist,
                    soldier_name,
                    unit,
                    company,
                    start_date,
                    end_date,
                    risk_flags,
                    emergency_contact
                )

                step = "run_again"

            elif step == "run_again":
                run_again = (
                    get_yes_or_no(
                        "\nWould you like "
                        "to create another "
                        "checklist? "
                        "(YES/NO): "
                    )
                )

                if run_again == "BACK":
                    step = (
                        "emergency_contact"
                    )

                elif run_again == "YES":
                    break

                elif run_again == "NO":
                    print(
                        f"\nGoodbye, "
                        f"{soldier_name}."
                    )
                    return

if __name__ == "__main__":
    main()