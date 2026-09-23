## Problem Statement

People in this day and age face issues tracking their expenses and assessing their monthly spending and net cash inflow and outflow. Due to different methods of payment and spending existing it creates a confusion about where the money is leaking out of and where we can cut our spendings. Normal spreadsheets don't have enough functionality as much as a python program can have and normal human memory falls short as compared to a digitalised record.

## Scope

This app helps its user to add their expenses, edit them, and delete their expenses. This app also helps its users in creating their budgets giving them alerts, reports and csv exports for effective expense tracking. The app needs no login or bank details, and runs entirely in the command line.

**Out of scope:** The app does not connect to bank accounts, has no graphical interface, and does not support multiple user accounts.

## Target Users

This app's target users are people of all ages and backgrounds be it technical or non-technical and primarily targets our working section of society who needs to maintain their budget tightly and also for those who just want to get a track record of their expenses.

## High-Level Features

Module 1: Expense Management

- Adding an expense with amount, category, description and date
- Editing and deleting existing expenses
- Searching or filtering expenses (by category, date or amount)

Module 2: Budgets and Alerts

- Setting a monthly limit for each category
- Budget Management and alert generation for over spending or nearing the limit

Module 3: Reports and Analytics

- Monthly summary showing total spending for a chosen month
- Category-wise report showing how much was spent in each category
- Top spending report listing the highest expenses or categories

Cross-cutting features

- All data is stored in a local SQLite database, so nothing is lost between runs
- Every input is checked before it is saved, so invalid entries show an error message instead of crashing the app
- Actions and errors are recorded in a log file for easy troubleshooting