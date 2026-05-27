import csv
import sqlite3
import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def print_header():
    print("\n" + "=" * 40)
    print(" SOLDIER LEAVE CHECKLIST GENERATOR")
    print("=" * 40)

def display_main_menu():
    print("\n" + "=" * 40)
    print(" SOLDIER LEAVE ACCOUNTABILITY SYSTEM")
    print("=" * 40)
    print("1. Create Leave Request")
    print("2. Search Soldier Leave History")
    print("3. View All Leave Records")
    print("4. Battalion Dashboard")
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
    )

    if contact_name == "BACK":
        return "BACK"

    relationship = get_valid_relationship(
        "Enter relationship to Soldier: "
    )

    if relationship == "BACK":
        return "BACK"

    phone_number = get_valid_phone_number(
        "Enter emergency contact phone number: "
    )

    if phone_number == "BACK":
        return "BACK"

    leave_address = get_valid_address(
        "Enter Soldier leave address: "
    )

    if leave_address == "BACK":
        return "BACK"

    travel_method = get_valid_travel_method(
        "Enter travel method "
        "(POV, FLIGHT, BUS, TRAIN): "
    )

    if travel_method == "BACK":
        return "BACK"

    emergency_contact = {
        "contact_name": contact_name,
        "relationship": relationship,
        "phone_number": phone_number,
        "leave_address": leave_address,
        "travel_method": travel_method
    }

    return emergency_contact

def get_dates_between(start_date, end_date):
    start = datetime.strptime(
        start_date,
        "%Y-%m-%d"
    )

    end = datetime.strptime(
        end_date,
        "%Y-%m-%d"
    )

    dates = []

    current_date = start

    while current_date <= end:
        dates.append(current_date)
        current_date = current_date.replace(
            day=current_date.day
        ) + timedelta(days=1)

    return dates


def get_weekend_warnings(start_date, end_date):
    weekend_warnings = []

    leave_dates = get_dates_between(
        start_date,
        end_date
    )

    weekend_days = []

    for date in leave_dates:
        if date.weekday() in [5, 6]:
            weekend_days.append(
                date.strftime("%Y-%m-%d")
            )

    if weekend_days:
        weekend_warnings.append(
            "Leave includes weekend days: "
            + ", ".join(weekend_days)
        )

    return weekend_warnings


def get_holiday_warnings(start_date, end_date):
    holiday_warnings = []

    federal_holidays = {
        "2026-01-01": "New Year's Day",
        "2026-01-19": "Martin Luther King Jr. Day",
        "2026-02-16": "Presidents Day",
        "2026-05-25": "Memorial Day",
        "2026-06-19": "Juneteenth",
        "2026-07-03": "Independence Day Observed",
        "2026-09-07": "Labor Day",
        "2026-10-12": "Columbus Day",
        "2026-11-11": "Veterans Day",
        "2026-11-26": "Thanksgiving Day",
        "2026-12-25": "Christmas Day"
    }

    leave_dates = get_dates_between(
        start_date,
        end_date
    )

    for date in leave_dates:
        date_string = date.strftime("%Y-%m-%d")

        if date_string in federal_holidays:
            holiday_warnings.append(
                "Leave overlaps "
                + federal_holidays[date_string]
                + " on "
                + date_string
            )

    return holiday_warnings

def get_recall_risk_warning(
    travel_method,
    leave_address
):
    recall_warnings = []

    leave_address = (
        leave_address.upper()
    )

    high_risk_locations = [
        "FLORIDA",
        "TEXAS",
        "CALIFORNIA",
        "HAWAII",
        "NEW YORK",
        "OVERSEAS",
        "GERMANY",
        "JAPAN",
        "KOREA"
    ]

    alaska_locations = [
        "ANCHORAGE",
        "JBER",
        "WASILLA",
        "PALMER",
        "EAGLE RIVER",
        "FAIRBANKS"
    ]

    if (
        travel_method == "POV"
        and any(
            location in leave_address
            for location
            in alaska_locations
        )
    ):
        return recall_warnings

    if any(
        location in leave_address
        for location
        in high_risk_locations
    ):
        recall_warnings.append(
            "Travel location may impact "
            "recall readiness."
        )

    if (
        travel_method
        in ["FLIGHT", "TRAIN"]
    ):
        recall_warnings.append(
            "Commercial travel may "
            "delay emergency recall."
        )

    return recall_warnings

def get_travel_category(
    travel_method,
    leave_address
):
    leave_address = (
        leave_address.upper()
    )

    alaska_locations = [
        "ANCHORAGE",
        "JBER",
        "EAGLE RIVER",
        "PALMER",
        "WASILLA",
        "FAIRBANKS"
    ]

    continental_us = [
        "TEXAS",
        "FLORIDA",
        "CALIFORNIA",
        "NEW YORK",
        "WASHINGTON",
        "OREGON",
        "NEVADA",
        "ARIZONA",
        "COLORADO"
    ]

    overseas_locations = [
        "GERMANY",
        "JAPAN",
        "KOREA",
        "ITALY",
        "POLAND",
        "OVERSEAS"
    ]

    if any(
        location in leave_address
        for location
        in alaska_locations
    ):
        return (
            "LOCAL AREA",
            "LOW"
        )

    if any(
        location in leave_address
        for location
        in continental_us
    ):
        return (
            "EXTENDED DISTANCE",
            "HIGH"
        )

    if any(
        location in leave_address
        for location
        in overseas_locations
    ):
        return (
            "OVERSEAS",
            "HIGH"
        )

    if travel_method == "POV":
        return (
            "REGIONAL",
            "MEDIUM"
        )

    return (
        "UNKNOWN",
        "MEDIUM"
    )

def get_leader_recommendation(
    risk_flags,
    policy_warnings,
    recall_risk
):
    recommendation_reasons = []

    if risk_flags:
        recommendation_reasons.extend(
            risk_flags
        )

    if policy_warnings:
        recommendation_reasons.extend(
            policy_warnings
        )

    if recall_risk == "HIGH":
        recommendation_reasons.append(
            "High recall risk"
        )

    if recommendation_reasons:
        return (
            "LEADERSHIP REVIEW REQUIRED",
            recommendation_reasons
        )

    return (
        "APPROVE",
        []
    )

def save_leave_record_to_csv(
    soldier_name,
    unit,
    company,
    checklist,
    start_date,
    end_date,
    leave_days,
    emergency_contact,
    status,
    recommendation
):
    filename = "leave_records.csv"

    travel_category, recall_risk = (
        get_travel_category(
            emergency_contact[
                "travel_method"
            ],
            emergency_contact[
                "leave_address"
            ]
        )
    )

    try:
        with open(
            filename,
            "x",
            newline=""
        ) as file:
            writer = csv.writer(
                file
            )

            writer.writerow([
                "Date Created",
                "Soldier",
                "Unit",
                "Company",
                "Leave Type",
                "Start Date",
                "End Date",
                "Leave Days",
                "Travel Method",
                "Travel Category",
                "Recall Risk",
                "Status",
                "Recommendation"
            ])

    except FileExistsError:
        pass

    with open(
        filename,
        "a",
        newline=""
    ) as file:
        writer = csv.writer(
            file
        )

        writer.writerow([
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            soldier_name,
            unit,
            company,
            checklist["title"],
            start_date,
            end_date,
            leave_days,
            emergency_contact[
                "travel_method"
            ],
            travel_category,
            recall_risk,
            status,
            recommendation
        ])

    print(
        "\nLeave record saved "
        "to leave_records.csv"
    )

def initialize_database():
    connection = sqlite3.connect("leave_records.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leave_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_created TEXT,
            soldier TEXT,
            unit TEXT,
            company TEXT,
            leave_type TEXT,
            start_date TEXT,
            end_date TEXT,
            leave_days INTEGER,
            travel_method TEXT,
            travel_category TEXT,
            recall_risk TEXT,
            status TEXT,
            recommendation TEXT
        )
    """)

    connection.commit()
    connection.close()


def save_leave_record_to_database(
    soldier_name,
    unit,
    company,
    checklist,
    start_date,
    end_date,
    leave_days,
    emergency_contact,
    status,
    recommendation
):
    initialize_database()

    travel_category, recall_risk = get_travel_category(
        emergency_contact["travel_method"],
        emergency_contact["leave_address"]
    )

    connection = sqlite3.connect("leave_records.db")
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO leave_records (
            date_created,
            soldier,
            unit,
            company,
            leave_type,
            start_date,
            end_date,
            leave_days,
            travel_method,
            travel_category,
            recall_risk,
            status,
            recommendation
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        soldier_name,
        unit,
        company,
        checklist["title"],
        start_date,
        end_date,
        leave_days,
        emergency_contact["travel_method"],
        travel_category,
        recall_risk,
        status,
        recommendation
    ))

    connection.commit()
    connection.close()

    print("\nLeave record saved to leave_records.db")

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

    policy_warnings = []

    if (
        checklist["title"] != "Pass Checklist"
        and leave_days <= 4
    ):
        policy_warnings.append(
            "Leave duration is 4 days or less. "
            "This may qualify as a pass instead of leave."
        )

    if (
        checklist["title"] == "Pass Checklist"
        and leave_days > 4
    ):
        policy_warnings.append(
            "Pass duration exceeds 4 days. "
            "This may require ordinary leave instead."
        )

    weekend_warnings = get_weekend_warnings(
        start_date,
        end_date
    )

    holiday_warnings = get_holiday_warnings(
        start_date,
        end_date
    )

    recall_warnings = get_recall_risk_warning(
        emergency_contact["travel_method"],
        emergency_contact["leave_address"]
    )

    travel_category, recall_risk = get_travel_category(
        emergency_contact["travel_method"],
        emergency_contact["leave_address"]
    )

    policy_warnings.extend(
        weekend_warnings
    )

    policy_warnings.extend(
        holiday_warnings
    )

    policy_warnings.extend(
        recall_warnings
    )

    recommendation, recommendation_reasons = (
        get_leader_recommendation(
            risk_flags,
            policy_warnings,
            recall_risk
        )
    )

    if (
        risk_flags
        or policy_warnings
        or recommendation == "LEADERSHIP REVIEW REQUIRED"
    ):
        status = "Requires Leadership Review"
    else:
        status = "Ready for Submission"

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

    print(
        f"Travel Category: "
        f"{travel_category}"
    )

    print(
        f"Recall Risk: "
        f"{recall_risk}"
    )

    print("\n" + "=" * 40)
    print(" POLICY WARNINGS")
    print("=" * 40)

    if policy_warnings:
        for warning in policy_warnings:
            print(f"WARNING: {warning}")
    else:
        print("No policy warnings identified")

    print("\n" + "=" * 40)
    print(" RISK ASSESSMENT")
    print("=" * 40)

    if risk_flags:
        for flag in risk_flags:
            print(f"WARNING: {flag}")
    else:
        print("No risk flags identified")

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

    print("\n" + "=" * 40)
    print(" LEADER RECOMMENDATION")
    print("=" * 40)

    print(
        f"Recommended Action: "
        f"{recommendation}"
    )

    if recommendation_reasons:
        print("\nReasons:")

        for reason in recommendation_reasons:
            print(f"- {reason}")

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
        emergency_contact,
        policy_warnings
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
        emergency_contact,
        policy_warnings
    )

    save_leave_record_to_database(
        soldier_name,
        unit,
        company,
        checklist,
        start_date,
        end_date,
        leave_days,
        emergency_contact,
        status,
        recommendation
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
    emergency_contact,
    policy_warnings
):
    travel_category, recall_risk = get_travel_category(
        emergency_contact["travel_method"],
        emergency_contact["leave_address"]
    )

    recommendation, recommendation_reasons = (
        get_leader_recommendation(
            risk_flags,
            policy_warnings,
            recall_risk
        )
    )

    filename = (
        f"{soldier_name}"
        "_leave_checklist.txt"
    )

    with open(filename, "w") as file:
        file.write(f"Soldier: {soldier_name}\n")
        file.write(f"Unit: {unit}\n")
        file.write(f"Company: {company}\n")
        file.write(f"Start Date: {start_date}\n")
        file.write(f"End Date: {end_date}\n")
        file.write(f"Total Leave Days: {leave_days}\n\n")

        file.write(f"{checklist['title']}\n")
        file.write("-" * len(checklist["title"]) + "\n")

        for number, item in enumerate(
            checklist["items"],
            start=1
        ):
            file.write(f"{number}. {item}\n")

        file.write("\n")
        file.write("=" * 40 + "\n")
        file.write("EMERGENCY CONTACT\n")
        file.write("=" * 40 + "\n")
        file.write(f"Contact Name: {emergency_contact['contact_name']}\n")
        file.write(f"Relationship: {emergency_contact['relationship']}\n")
        file.write(f"Phone Number: {emergency_contact['phone_number']}\n")
        file.write(f"Leave Address: {emergency_contact['leave_address']}\n")
        file.write(f"Travel Method: {emergency_contact['travel_method']}\n")
        file.write(f"Travel Category: {travel_category}\n")
        file.write(f"Recall Risk: {recall_risk}\n")

        file.write("\n")
        file.write("=" * 40 + "\n")
        file.write("POLICY WARNINGS\n")
        file.write("=" * 40 + "\n")

        if policy_warnings:
            for warning in policy_warnings:
                file.write(f"WARNING: {warning}\n")
        else:
            file.write("No policy warnings identified\n")

        file.write("\n")
        file.write("=" * 40 + "\n")
        file.write("RISK ASSESSMENT\n")
        file.write("=" * 40 + "\n")

        if risk_flags:
            for flag in risk_flags:
                file.write(f"WARNING: {flag}\n")
        else:
            file.write("No risk flags identified\n")

        file.write("\n")
        file.write("=" * 40 + "\n")
        file.write("LEAVE STATUS\n")
        file.write("=" * 40 + "\n")
        file.write(f"Leave Type: {checklist['title']}\n")
        file.write(f"Duration: {leave_days} day(s)\n")
        file.write(f"Status: {status}\n")

        file.write("\n")
        file.write("=" * 40 + "\n")
        file.write("LEADER RECOMMENDATION\n")
        file.write("=" * 40 + "\n")
        file.write(f"Recommended Action: {recommendation}\n")

        if recommendation_reasons:
            file.write("\nReasons:\n")

            for reason in recommendation_reasons:
                file.write(f"- {reason}\n")

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
        show_navigation_options()

        phone_number = input(prompt).strip()
        phone_number = handle_navigation(phone_number)

        if phone_number == "BACK":
            return "BACK"

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

        print("\nInvalid phone number.")
        print("Please enter a 10-digit phone number.")
        print("Example: 907-555-1234\n")


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
        show_navigation_options()

        address = input(prompt).strip()

        address = handle_navigation(
            address
        )

        if address == "BACK":
            return "BACK"

        if (
            len(address) >= 8
            and any(
                character.isdigit()
                for character in address
            )
            and any(
                character.isalpha()
                for character in address
            )
        ):
            return address.title()

        print("\nInvalid address.")
        print(
            "Please enter a valid "
            "leave address.\n"
        )

        print(
            "Example:"
        )

        print(
            "123 Main St, "
            "Orlando, Florida\n"
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
        show_navigation_options()

        relationship = input(prompt).strip().upper()
        relationship = handle_navigation(relationship)

        if relationship == "BACK":
            return "BACK"

        if relationship in valid_relationships:
            return relationship.title()

        print("\nInvalid relationship.")
        print("Valid options include:")
        print(", ".join(valid_relationships) + "\n")

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
                "\nEnd date cannot "
                "be earlier than "
                "start date."
            )

            print(
                "Please enter the "
                "dates again.\n"
            )

        elif leave_days > 30:
            print(
                "\nWARNING:"
            )

            print(
                "Leave exceeds "
                "30 days."
            )

            print(
                "Please adjust "
                "leave dates.\n"
            )

        else:
            return (
                start_date,
                end_date
            )

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
    emergency_contact,
    policy_warnings
):
    travel_category, recall_risk = get_travel_category(
        emergency_contact["travel_method"],
        emergency_contact["leave_address"]
    )

    recommendation, recommendation_reasons = (
        get_leader_recommendation(
            risk_flags,
            policy_warnings,
            recall_risk
        )
    )

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

    y_position -= 20

    pdf.drawString(
        72,
        y_position,
        f"Travel Category: {travel_category}"
    )

    y_position -= 20

    pdf.drawString(
        72,
        y_position,
        f"Recall Risk: {recall_risk}"
    )

    y_position -= 30

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(72, y_position, "Policy Warnings")

    y_position -= 20

    pdf.setFont("Helvetica", 11)

    if policy_warnings:
        for warning in policy_warnings:
            pdf.drawString(
                72,
                y_position,
                f"WARNING: {warning}"
            )

            y_position -= 20
    else:
        pdf.drawString(
            72,
            y_position,
            "No policy warnings identified"
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

    y_position -= 30

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(72, y_position, "Leader Recommendation")

    y_position -= 20

    pdf.setFont("Helvetica", 11)

    pdf.drawString(
        72,
        y_position,
        f"Recommended Action: {recommendation}"
    )

    y_position -= 20

    if recommendation_reasons:
        pdf.drawString(
            72,
            y_position,
            "Reasons:"
        )

        y_position -= 20

        for reason in recommendation_reasons:
            pdf.drawString(
                72,
                y_position,
                f"- {reason}"
            )

            y_position -= 20

    pdf.save()

    print(f"PDF saved as {filename}")

def confirm_leave_request(
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
    print(" CONFIRM LEAVE REQUEST")
    print("=" * 40)

    print(f"Soldier: {soldier_name}")
    print(f"Unit: {unit}")
    print(f"Company: {company}")
    print(f"Leave Type: {checklist['title']}")
    print(f"Start Date: {start_date}")
    print(f"End Date: {end_date}")
    print(f"Total Leave Days: {leave_days}")

    print("\nEmergency Contact")
    print("-" * 17)
    print(
        f"Name: "
        f"{emergency_contact['contact_name']}"
    )
    print(
        f"Relationship: "
        f"{emergency_contact['relationship']}"
    )
    print(
        f"Phone: "
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

    print("\nRisk Assessment")
    print("-" * 15)

    if risk_flags:
        for flag in risk_flags:
            print(f"WARNING: {flag}")
    else:
        print("No risk flags identified")

    confirmation = get_confirmation_choice(
        "\nProceed with submission? "
        "(YES/EDIT/CANCEL): "
    )

    return confirmation

def get_confirmation_choice(prompt):
    valid_choices = [
        "YES",
        "EDIT",
        "CANCEL",
        "BACK"
    ]

    while True:
        show_navigation_options()

        choice = input(prompt).strip().upper()

        choice = handle_navigation(
            choice
        )

        if choice in valid_choices:
            return choice

        print("\nInvalid response.")
        print("Please enter YES, EDIT, or CANCEL.\n")

def display_main_menu():
    print("\n" + "=" * 40)
    print(" SOLDIER LEAVE ACCOUNTABILITY SYSTEM")
    print("=" * 40)
    print("1. Create Leave Request")
    print("2. Search Soldier Leave History")
    print("3. View All Leave Records")
    print("4. Battalion Dashboard")
    print("5. Launch GUI Dashboard")
    print("6. Exit")

def get_main_menu_choice():
    valid_choices = ["1", "2", "3", "4", "5", "6"]

    while True:
        show_navigation_options()

        choice = input("Select an option: ").strip()
        choice = handle_navigation(choice)

        if choice == "BACK":
            return "BACK"

        if choice in valid_choices:
            return choice

        print("\nInvalid option.")
        print("Please select 1 through 6.\n")

def search_leave_history():
    initialize_database()

    search_name = get_required_input(
        "Enter Soldier name to search: "
    )

    if search_name == "BACK":
        return

    connection = sqlite3.connect("leave_records.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            soldier,
            unit,
            company,
            leave_type,
            start_date,
            end_date,
            leave_days,
            status,
            recommendation
        FROM leave_records
        WHERE UPPER(soldier) LIKE ?
    """, (
        f"%{search_name.upper()}%",
    ))

    results = cursor.fetchall()
    connection.close()

    print("\n" + "=" * 40)
    print(" LEAVE HISTORY RESULTS")
    print("=" * 40)

    if not results:
        print("\nNo leave records found for that Soldier.")
        return

    for row in results:
        print(f"\nSoldier: {row[0]}")
        print(f"Unit: {row[1]}")
        print(f"Company: {row[2]}")
        print(f"Leave Type: {row[3]}")
        print(f"Start Date: {row[4]}")
        print(f"End Date: {row[5]}")
        print(f"Leave Days: {row[6]}")
        print(f"Status: {row[7]}")
        print(f"Recommendation: {row[8]}")
        print("-" * 40)

def view_all_leave_records():
    initialize_database()

    connection = sqlite3.connect("leave_records.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            soldier,
            leave_type,
            start_date,
            end_date,
            status,
            recommendation
        FROM leave_records
        ORDER BY date_created DESC
    """)

    results = cursor.fetchall()
    connection.close()

    print("\n" + "=" * 40)
    print(" ALL LEAVE RECORDS")
    print("=" * 40)

    if not results:
        print("\nNo leave records found.")
        return

    for row in results:
        print(f"\nSoldier: {row[0]}")
        print(f"Leave Type: {row[1]}")
        print(f"Dates: {row[2]} to {row[3]}")
        print(f"Status: {row[4]}")
        print(f"Recommendation: {row[5]}")
        print("-" * 40)

def display_battalion_dashboard():
    initialize_database()

    connection = sqlite3.connect("leave_records.db")
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM leave_records")
    total_requests = cursor.fetchone()[0]

    if total_requests == 0:
        connection.close()
        print("\nNo leave records found.")
        return

    cursor.execute("""
        SELECT COUNT(*)
        FROM leave_records
        WHERE status = 'Requires Leadership Review'
    """)
    leadership_review = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM leave_records
        WHERE status = 'Ready for Submission'
    """)
    ready_submission = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM leave_records
        WHERE recall_risk = 'HIGH'
    """)
    high_recall = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM leave_records
        WHERE travel_method IN ('FLIGHT', 'TRAIN', 'BUS')
    """)
    commercial_travel = cursor.fetchone()[0]

    cursor.execute("""
        SELECT ROUND(AVG(leave_days), 0)
        FROM leave_records
    """)
    average_leave = cursor.fetchone()[0]

    cursor.execute("""
        SELECT unit, COUNT(*)
        FROM leave_records
        GROUP BY unit
        ORDER BY COUNT(*) DESC
        LIMIT 1
    """)
    most_common_unit = cursor.fetchone()

    cursor.execute("""
        SELECT company, COUNT(*)
        FROM leave_records
        GROUP BY company
        ORDER BY COUNT(*) DESC
        LIMIT 1
    """)
    most_common_company = cursor.fetchone()

    cursor.execute("""
        SELECT travel_method, COUNT(*)
        FROM leave_records
        GROUP BY travel_method
        ORDER BY COUNT(*) DESC
        LIMIT 1
    """)
    most_common_travel = cursor.fetchone()

    cursor.execute("""
        SELECT leave_type, COUNT(*)
        FROM leave_records
        GROUP BY leave_type
        ORDER BY COUNT(*) DESC
        LIMIT 1
    """)
    most_common_leave = cursor.fetchone()

    cursor.execute("""
        SELECT soldier, leave_days
        FROM leave_records
        ORDER BY leave_days DESC
        LIMIT 1
    """)
    longest_leave = cursor.fetchone()

    cursor.execute("""
        SELECT soldier, leave_days
        FROM leave_records
        ORDER BY leave_days ASC
        LIMIT 1
    """)
    shortest_leave = cursor.fetchone()

    connection.close()

    leadership_review_percent = round(
        (leadership_review / total_requests) * 100
    )

    print("\n" + "=" * 40)
    print(" BATTALION LEAVE DASHBOARD")
    print("=" * 40)

    print(f"Total Leave Requests: {total_requests}")
    print(f"Pending Leadership Review: {leadership_review}")
    print(f"Ready For Submission: {ready_submission}")
    print(f"Leadership Review Rate: {leadership_review_percent}%")
    print(f"High Recall Risk: {high_recall}")
    print(f"Commercial Travel Requests: {commercial_travel}")
    print(f"Average Leave Length: {int(average_leave)} day(s)")

    print("\nMost Common Unit:")
    print(most_common_unit[0])

    print("\nMost Common Company:")
    print(most_common_company[0])

    print("\nMost Common Travel Method:")
    print(most_common_travel[0])

    print("\nMost Common Leave Type:")
    print(most_common_leave[0])

    print("\nLongest Leave Request:")
    print(f"{longest_leave[0]} - {longest_leave[1]} day(s)")

    print("\nShortest Leave Request:")
    print(f"{shortest_leave[0]} - {shortest_leave[1]} day(s)")

def display_menu():
    print("\nSelect Leave Type")
    print("-" * 17)
    print("1. Ordinary Leave")
    print("2. Emergency Leave")
    print("3. Convalescent Leave")
    print("4. Pass")
    print("5. Back")

def launch_gui_dashboard():
    initialize_database()

    connection = sqlite3.connect("leave_records.db")
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM leave_records")
    total_requests = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM leave_records
        WHERE status = 'Requires Leadership Review'
    """)
    leadership_review = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM leave_records
        WHERE status = 'Ready for Submission'
    """)
    ready_submission = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM leave_records
        WHERE recall_risk = 'HIGH'
    """)
    high_recall = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM leave_records
        WHERE travel_method IN ('FLIGHT', 'TRAIN', 'BUS')
    """)
    commercial_travel = cursor.fetchone()[0]

    cursor.execute("""
        SELECT ROUND(AVG(leave_days), 0)
        FROM leave_records
    """)
    average_leave = cursor.fetchone()[0]

    connection.close()

    if average_leave is None:
        average_leave = 0

    window = tk.Tk()
    window.title("Soldier Leave Accountability Dashboard")
    window.geometry("500x400")

    title_label = tk.Label(
        window,
        text="Battalion Leave Dashboard",
        font=("Arial", 18, "bold")
    )
    title_label.pack(pady=15)

    stats = [
        f"Total Leave Requests: {total_requests}",
        f"Pending Leadership Review: {leadership_review}",
        f"Ready For Submission: {ready_submission}",
        f"High Recall Risk: {high_recall}",
        f"Commercial Travel Requests: {commercial_travel}",
        f"Average Leave Length: {int(average_leave)} day(s)"
    ]

    for stat in stats:
        label = tk.Label(
            window,
            text=stat,
            font=("Arial", 12)
        )
        label.pack(pady=5)

    close_button = tk.Button(
        window,
        text="Close Dashboard",
        command=window.destroy
    )
    close_button.pack(pady=20)

    window.mainloop()

def main():
    while True:
        display_main_menu()

        main_choice = get_main_menu_choice()

        if main_choice == "BACK":
            continue

        if main_choice == "6":
            print("\nGoodbye.")
            break

        if main_choice == "2":
            search_leave_history()
            continue

        if main_choice == "3":
            view_all_leave_records()
            continue

        if main_choice == "4":
            display_battalion_dashboard()
            continue

        if main_choice == "5":
            launch_gui_dashboard()
            continue

        if main_choice == "1":
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
                        break

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

                    choice = get_valid_menu_choice(
                        "\nSelect an option: "
                    )

                    if choice == "BACK":
                        step = "dates"

                    elif choice == "5":
                        break

                    else:
                        checklist = get_checklist(
                            choice
                        )

                        step = "risk"

                elif step == "risk":
                    risk_flags = get_risk_assessment()

                    if risk_flags == "BACK":
                        step = "leave_type"
                    else:
                        step = "emergency_contact"

                elif step == "emergency_contact":
                    emergency_contact = (
                        get_emergency_contact_info()
                    )

                    if emergency_contact == "BACK":
                        step = "risk"
                    else:
                        step = "confirm"

                elif step == "confirm":
                    confirmation = (
                        confirm_leave_request(
                            checklist,
                            soldier_name,
                            unit,
                            company,
                            start_date,
                            end_date,
                            risk_flags,
                            emergency_contact
                        )
                    )

                    if confirmation == "YES":
                        step = "print"

                    elif confirmation == "EDIT":
                        step = "edit_menu"

                    elif confirmation == "CANCEL":
                        print(
                            "\nLeave request cancelled."
                        )
                        break

                    elif confirmation == "BACK":
                        step = "emergency_contact"

                elif step == "edit_menu":
                    print("\n" + "=" * 40)
                    print(" EDIT LEAVE REQUEST")
                    print("=" * 40)
                    print("1. Soldier Info")
                    print("2. Unit / Company")
                    print("3. Leave Dates")
                    print("4. Leave Type")
                    print("5. Risk Assessment")
                    print("6. Emergency Contact")
                    print("7. Return to Confirmation")

                    edit_choice = input(
                        "\nSelect section to edit: "
                    ).strip()

                    edit_choice = handle_navigation(
                        edit_choice
                    )

                    if edit_choice == "BACK":
                        step = "confirm"

                    elif edit_choice == "1":
                        step = "rank"

                    elif edit_choice == "2":
                        step = "unit"

                    elif edit_choice == "3":
                        step = "dates"

                    elif edit_choice == "4":
                        step = "leave_type"

                    elif edit_choice == "5":
                        step = "risk"

                    elif edit_choice == "6":
                        step = "emergency_contact"

                    elif edit_choice == "7":
                        step = "confirm"

                    else:
                        print(
                            "\nInvalid option. "
                            "Please select 1 through 7."
                        )

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

                    break

if __name__ == "__main__":
    main()