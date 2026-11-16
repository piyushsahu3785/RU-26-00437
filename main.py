"""
Student Attendance & Performance Tracker
PS No. 34 | Python 3

Run:
    python attendance_tracker.py
"""

from pathlib import Path
import sys
import pandas as pd
import matplotlib.pyplot as plt

REQUIRED_COLUMNS = ["Name", "Classes_Held", "Classes_Attended", "Marks"]
CSV_FILE = "students.csv"


def load_and_clean_data(file_path):
    """Load CSV data, validate rows, and return (valid_data, errors)."""
    path = Path(file_path)

    if not path.exists():
        print(f"Error: CSV file '{file_path}' was not found.")
        return pd.DataFrame(columns=REQUIRED_COLUMNS), []

    try:
        raw = pd.read_csv(path)
    except Exception as exc:
        print(f"Error reading CSV file: {exc}")
        return pd.DataFrame(columns=REQUIRED_COLUMNS), []

    missing = [column for column in REQUIRED_COLUMNS if column not in raw.columns]
    if missing:
        print("Error: Missing required CSV column(s): " + ", ".join(missing))
        return pd.DataFrame(columns=REQUIRED_COLUMNS), []

    valid_rows = []
    errors = []

    for index, row in raw.iterrows():
        csv_row_number = index + 2  # header is row 1
        name = str(row["Name"]).strip() if pd.notna(row["Name"]) else ""

        if not name or name.lower() == "nan":
            errors.append(f"Row {csv_row_number} skipped: missing student name.")
            continue

        numeric_values = {}
        row_invalid = False

        for column in ["Classes_Held", "Classes_Attended", "Marks"]:
            value = pd.to_numeric(row[column], errors="coerce")
            if pd.isna(value):
                errors.append(
                    f"Row {csv_row_number} skipped: invalid {column.replace('_', ' ')} "
                    f"'{row[column]}'."
                )
                row_invalid = True
                break
            numeric_values[column] = float(value)

        if row_invalid:
            continue

        held = numeric_values["Classes_Held"]
        attended = numeric_values["Classes_Attended"]
        marks = numeric_values["Marks"]

        if held <= 0:
            errors.append(f"Row {csv_row_number} skipped: Classes_Held must be greater than 0.")
            continue
        if held < 0 or attended < 0:
            errors.append(f"Row {csv_row_number} skipped: class counts cannot be negative.")
            continue
        if attended > held:
            errors.append(
                f"Row {csv_row_number} skipped: attended ({attended:g}) "
                f"cannot exceed held ({held:g})."
            )
            continue
        if not 0 <= marks <= 100:
            errors.append(f"Row {csv_row_number} skipped: Marks must be between 0 and 100.")
            continue

        attendance = (attended / held) * 100
        at_risk = attendance < 75 or marks < 40

        valid_rows.append({
            "Name": name,
            "Classes_Held": held,
            "Classes_Attended": attended,
            "Marks": marks,
            "Attendance_Percentage": attendance,
            "Status": "At Risk" if at_risk else "OK"
        })

    return pd.DataFrame(valid_rows), errors


def print_validation_errors(errors):
    for error in errors:
        print(error)


def show_student_report(data):
    """Display each student's attendance, marks, and risk status."""
    if data.empty:
        print("No valid data to analyse.")
        return

    print("\nSTUDENT PERFORMANCE REPORT")
    print("-" * 66)
    print(f"{'Name':<18}{'Attendance':<16}{'Marks':<12}{'Status'}")
    print("-" * 66)

    for _, student in data.iterrows():
        print(
            f"{student['Name']:<18}"
            f"{student['Attendance_Percentage']:>7.2f}%"
            f"{'':<9}"
            f"{student['Marks']:>5.0f}"
            f"{'':<7}"
            f"{student['Status']}"
        )
    print("-" * 66)


def show_summary(data):
    """Display class averages and at-risk students."""
    if data.empty:
        print("No valid data to analyse.")
        return

    average_attendance = data["Attendance_Percentage"].mean()
    average_marks = data["Marks"].mean()
    at_risk = data[data["Status"] == "At Risk"]

    print("\nCLASS SUMMARY")
    print("-" * 40)
    print(f"Total valid students : {len(data)}")
    print(f"Average attendance  : {average_attendance:.2f}%")
    print(f"Average marks       : {average_marks:.2f}")
    print(f"At Risk students    : {len(at_risk)}")

    if not at_risk.empty:
        print("At Risk names       : " + ", ".join(at_risk["Name"].tolist()))
    else:
        print("At Risk names       : None")
    print("-" * 40)


def create_charts(data, output_dir="."):
    """Create and save a bar chart and a scatter plot."""
    if data.empty:
        print("No valid data available. Charts were not created.")
        return

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Chart 1: Attendance percentage by student
    plt.figure(figsize=(9, 5))
    plt.bar(data["Name"], data["Attendance_Percentage"])
    plt.axhline(y=75, linestyle="--", label="75% attendance threshold")
    plt.title("Student Attendance Percentage")
    plt.xlabel("Student Name")
    plt.ylabel("Attendance (%)")
    plt.ylim(0, 105)
    plt.legend()
    plt.tight_layout()
    attendance_file = output_path / "attendance_chart.png"
    plt.savefig(attendance_file)
    plt.close()

    # Chart 2: Attendance versus marks
    plt.figure(figsize=(9, 5))
    plt.scatter(data["Attendance_Percentage"], data["Marks"])
    for _, student in data.iterrows():
        plt.annotate(
            student["Name"],
            (student["Attendance_Percentage"], student["Marks"]),
            xytext=(5, 5),
            textcoords="offset points"
        )
    plt.title("Attendance vs Marks")
    plt.xlabel("Attendance (%)")
    plt.ylabel("Marks (out of 100)")
    plt.xlim(0, 105)
    plt.ylim(0, 105)
    plt.tight_layout()
    scatter_file = output_path / "attendance_vs_marks.png"
    plt.savefig(scatter_file)
    plt.close()

    print("\nCharts saved successfully:")
    print(f"- {attendance_file}")
    print(f"- {scatter_file}")


def get_csv_path():
    entered = input(f"Enter CSV file path (press Enter for '{CSV_FILE}'): ").strip()
    return entered if entered else CSV_FILE


def main():
    print("=" * 55)
    print("       STUDENT ATTENDANCE & PERFORMANCE TRACKER")
    print("=" * 55)

    csv_path = get_csv_path()
    data, errors = load_and_clean_data(csv_path)

    if errors:
        print("\nDATA VALIDATION")
        print_validation_errors(errors)

    if data.empty:
        print("\nNo valid data to analyse.")
    else:
        print(f"\nSuccessfully loaded {len(data)} valid student record(s).")

    while True:
        print("\nMENU")
        print("1. Student Report")
        print("2. Summary and Charts")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            show_student_report(data)
        elif choice == "2":
            show_summary(data)
            create_charts(data)
        elif choice == "3":
            print("Thank you for using the Student Attendance & Performance Tracker.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
