# Student Attendance & Performance Tracker

**PS No.:** 34  
**University:** Rungta International Skills University  
**School:** School of Computer Science and Engineering  
**Program:** Bachelor of Technology – Computer Science and Engineering

A Python 3 console application that reads student records from a CSV file, calculates attendance percentages, identifies students at risk, displays class summaries, and generates charts.

## Features

- Reads student records using **Pandas**.
- Calculates attendance percentage for every valid student.
- Flags a student as **At Risk** if:
  - Attendance is below 75%, **or**
  - Marks are below 40.
- Validates input and skips invalid records (for example, attended classes greater than classes held, non-numeric marks, or marks outside 0–100).
- Displays an individual student report.
- Calculates average attendance and average marks.
- Generates:
  - `attendance_chart.png` — bar chart of attendance by student.
  - `attendance_vs_marks.png` — scatter plot of attendance versus marks.

## Project structure

```text
Student_Attendance_Performance_Tracker/
├── attendance_tracker.py
├── students.csv
├── README.md
└── requirements.txt
```

The two chart PNG files are generated in the current working directory when you select menu option 2.

## Requirements

- Python 3.8 or later
- pandas
- matplotlib

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## CSV format

The CSV file must contain these exact column headers:

```csv
Name,Classes_Held,Classes_Attended,Marks
Aman,40,36,80
Riya,40,28,65
Karan,40,30,35
```

`Classes_Held` must be greater than zero, `Classes_Attended` must be between zero and `Classes_Held`, and `Marks` must be between 0 and 100.

## How to run

Open a terminal in the project folder and run:

```bash
python attendance_tracker.py
```

When prompted for the CSV path, press **Enter** to use `students.csv`, or enter another CSV file path.

### Menu

1. **Student Report** — displays each student's attendance percentage, marks, and status.
2. **Summary and Charts** — displays class averages and at-risk students, then saves both charts.
3. **Exit** — closes the program.

## Test cases

### Test Case 1 — Normal input

Input:

```csv
Name,Classes_Held,Classes_Attended,Marks
Aman,40,36,80
Riya,40,28,65
Karan,40,30,35
```

Expected report:

| Student | Attendance | Marks | Status |
|---|---:|---:|---|
| Aman | 90.00% | 80 | OK |
| Riya | 70.00% | 65 | At Risk |
| Karan | 75.00% | 35 | At Risk |

Expected summary:

- Average attendance: **78.33%**
- Average marks: **60.00**
- At-risk students: **2 (Riya, Karan)**

### Test Case 2 — One valid row

Input:

```csv
Name,Classes_Held,Classes_Attended,Marks
Neha,40,30,40
```

Expected:

- Attendance: **75.00%**
- Marks: **40**
- Status: **OK**

### Test Case 3 — Invalid input

Input:

```csv
Name,Classes_Held,Classes_Attended,Marks
Aman,40,45,80
Riya,40,30,abc
```

Expected:

- First data row is skipped because attended classes (45) exceed classes held (40).
- Second data row is skipped because marks (`abc`) are not numeric.
- The program reports: **No valid data to analyse.**

### Test Case 4 — Summary and charts

Use the same CSV as Test Case 1 and select menu option 2.

Expected:

- Average attendance: **78.33%**
- Average marks: **60.00**
- At-risk students: **2 (Riya, Karan)**
- Both chart files are generated.

## Calculation logic

Attendance percentage:

```text
Attendance Percentage = (Classes_Attended / Classes_Held) * 100
```

At-risk condition:

```text
At Risk = (Attendance Percentage < 75) OR (Marks < 40)
```

The thresholds are strict: exactly 75% attendance and exactly 40 marks are considered **OK**, unless the other condition makes the student at risk.

## Notes

- Invalid rows are skipped rather than stopping the entire program.
- The program prints validation messages with CSV row numbers.
- If there are no valid records, reports and charts are not generated.
- Chart files are overwritten when option 2 is run again.
