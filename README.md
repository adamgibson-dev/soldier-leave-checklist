# Soldier Leave Checklist Generator

A Python-based Army administrative tool that helps Soldiers generate leave and pass checklists while validating dates, calculating leave duration, and exporting completed checklists to both text and PDF formats.

---

## Overview

The Soldier Leave Checklist Generator was created to solve a realistic military administrative problem by helping Soldiers organize leave requirements in a structured way.

The application allows users to enter Soldier information, validate leave dates, calculate total leave duration, generate customized checklists for different leave types, and export completed leave summaries.

This project was built to strengthen Python programming, problem-solving, and software development skills while creating a practical tool with military relevance.

---

## Project Highlights

This project demonstrates:

- Python programming fundamentals
- Functions and modular programming
- File generation (.txt and .pdf)
- Input validation
- Error handling
- Date calculations
- Conditional logic
- Software workflow design
- Git and GitHub version control
- Problem-solving using a real Army administrative scenario

---

## Features

- Soldier name personalization
- Leave start and end date input
- Date format validation (`YYYY-MM-DD`)
- Prevention of invalid leave ranges
- Automatic leave day calculation
- Multiple leave types:
    - Ordinary Leave
    - Emergency Leave
    - Convalescent Leave
    - Pass
- Professional leave request summary
- Leave status summary
- Text file export
- PDF export
- Custom file names
- Multiple checklist workflow
- Improved terminal display formatting

---

## Technologies Used

- Python
- ReportLab (PDF generation)
- Git
- GitHub
- VS Code

---

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/adamgibson-dev/soldier-leave-checklist.git
```

### 2. Navigate to the project folder

```bash
cd soldier-leave-checklist
```

### 3. Install required package

```bash
pip install reportlab
```

### 4. Run the program

```bash
python main.py
```

---

## Example Output

```text
========================================
 LEAVE REQUEST SUMMARY
========================================

Soldier: Adam
Start Date: 2026-07-01
End Date: 2026-07-10
Total Leave Days: 9

Ordinary Leave Checklist
------------------------
1. Submit absence request in IPPS-A
2. Confirm leave address and contact information
3. Verify leave dates do not conflict with duty or training
4. Notify first-line leader of planned leave dates
5. Confirm approval authority and routing chain

========================================
 LEAVE STATUS
========================================
Leave Type: Ordinary Leave
Duration: 9 day(s)
Status: Ready for Submission
```

Generated files:

```text
Adam_leave_checklist.txt
Adam_leave_checklist.pdf
```

---

## Project Structure

```text
soldier-leave-checklist/
│
├── main.py
├── README.md
├── .gitignore
├── Adam_leave_checklist.txt
└── Adam_leave_checklist.pdf
```

---

## Future Improvements

Planned upgrades include:

- Leave approval simulation
- Digital signature support
- Unit-specific leave requirements
- Holiday/pass day calculation
- GUI (Graphical User Interface)
- IPPS-A integration concepts
- Export to Word document

---

## Lessons Learned

During development of this project, I practiced:

- Python fundamentals
- Functions
- Variables
- Loops
- Error handling
- Date validation
- File handling
- PDF generation
- Git version control
- Debugging and troubleshooting

---

## Why I Built This

I wanted to create a project that combined software development with a realistic Army administrative use case. Instead of building a generic beginner project, this tool was designed to solve a practical problem while strengthening technical skills in Python, automation, and software development.

This project also helped reinforce iterative software development practices through continuous improvements, debugging, and version control using Git and GitHub.