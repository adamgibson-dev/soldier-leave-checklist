# Soldier Leave Accountability System

A Python-based Army administrative accountability system designed to streamline Soldier leave management, risk assessment, and leave tracking through automated checklists, reporting, database storage, and dashboard analytics.

The application allows leaders and Soldiers to create leave requests, validate administrative requirements, assess travel and recall risk, generate professional exports, and track leave history using a SQLite database.

---

## Overview

The **Soldier Leave Accountability System** was created to solve a realistic military administrative problem by helping Soldiers and leaders organize leave requirements in a structured and accountable way.

The application allows users to:

- Create leave requests
- Validate leave dates
- Track emergency contact information
- Assess travel and recall risk
- Generate customized leave checklists
- Export leave summaries
- Store leave records in a database
- Search leave history
- View Battalion-level dashboard analytics

This project was built to strengthen Python programming, problem-solving, software development, and automation skills while creating a practical tool with military relevance.

---

## Project Highlights

This project demonstrates:

- Python programming fundamentals
- Functions and modular programming
- SQLite database integration
- GUI development with Tkinter
- PDF generation
- Input validation
- Error handling
- Date calculations
- Conditional logic
- Software workflow design
- Git and GitHub version control
- Real-world Army administrative problem solving

---

## Features

### Leave Request Management

- Soldier information collection
- Rank validation
- Unit validation
- Company validation
- Emergency contact tracking
- Leave address collection
- Travel method tracking

### Leave Validation

- Leave date validation (`YYYY-MM-DD`)
- Prevention of invalid date ranges
- Automatic leave duration calculation
- Pass vs leave policy checks
- Weekend detection
- Holiday awareness

### Risk Assessment

- Recall risk categorization
- Travel risk analysis
- Commercial travel tracking
- Leadership review recommendation engine
- Policy warning system

### Leave Types

- Ordinary Leave
- Emergency Leave
- Convalescent Leave
- Pass

### Navigation & User Experience

- `BACK` navigation at every prompt
- `EXIT` support throughout workflow
- Multi-step leave editing system
- Improved terminal formatting
- Input hardening and validation

### File Exports

- Text export (`.txt`)
- PDF export (`.pdf`)
- Automatic file naming

### Database & Reporting

- SQLite database storage
- Leave request history search
- View all leave records
- Battalion leave dashboard
- GUI dashboard
- Leave analytics

### Dashboard Analytics

- Total leave requests
- Leadership review percentage
- High recall risk tracking
- Commercial travel tracking
- Average leave duration
- Most common unit
- Most common company
- Most common leave type
- Longest and shortest leave requests

---

## Technologies Used

- Python
- SQLite
- Tkinter
- ReportLab
- CSV
- Git
- GitHub
- VS Code

---

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/adamgibson-dev/soldier-leave-checklist.git