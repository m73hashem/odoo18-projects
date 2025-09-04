
# Project Expenses Management

## Overview
**Project Expenses Management** is a custom Odoo 18 Community module designed to help organizations manage and track expenses on a per-project basis. 
It provides functionality for defining expense types, submitting and approving expense requests, handling product-related expenses with stock integration, and generating reports. 
The module also includes a simple portal interface for expense submission by project managers.

## Features
- **Expense Types Management**: Define various expense categories with spending limits per company.
- **Expense Requests**: Create, confirm, approve, and complete expense requests linked to specific projects.
- **Multi-line Requests**: Support for multiple expense lines and product lines in a single request.
- **Stock Integration**: Automatically create outgoing pickings for product lines with linked customers.
- **Project Overview**: Track total expense amounts directly on the project record.
- **Reporting**: Generate expense reports for selected projects via a wizard.
- **Portal Submission**: Allow project managers to submit expense requests through the website portal.

## Module Structure
```
project_expenses/
│
├── models/
│   ├── expense_type.py           # Defines expense type model
│   ├── project_inherit.py        # Extends project model with total expenses
│   ├── expense_request.py        # Main expense request logic
│   └── wizard_report.py          # Wizard for generating reports
│
├── views/
│   ├── expense_type_views.xml    # Views for expense types
│   ├── project_expense_views.xml # Views for project with expenses
│   ├── expense_request_views.xml # Views for expense requests
│   ├── stock_templates.xml       # Stock picking integration
│   ├── menu.xml                  # Main menu configuration
│
├── wizards/
│   └── project_expense_report_views.xml  # Wizard form view
│
├── reports/
│   └── report_template.xml       # QWeb template for expense reports
│
├── controllers/
│   └── portal.py                 # Portal expense submission controller
│
├── data/
│   ├── sequence_data.xml         # Sequence configuration
│   └── security XMLs & CSVs      # Access rights and security groups
│
└── __manifest__.py               # Module manifest file
```

## Installation
1. Copy the `project_expenses` folder to your Odoo `addons` directory.
2. Restart your Odoo server.
3. Activate Developer Mode in Odoo.
4. Go to **Apps** and click on **Update Apps List**.
5. Search for **Project Expenses Management** and install it.

## Usage
### Configure Expense Types
1. Navigate to **Project Expenses → Expense Types**.
2. Create and configure different expense types with spending limits.

### Create Expense Requests
1. Navigate to **Project Expenses → Expense Requests**.
2. Create a new request, select the project, and add expense lines and/or product lines.
3. Confirm, approve, and mark the request as done.

### Generate Reports
1. Navigate to **Project Expenses → Project Expenses Report**.
2. Select one or more projects and click **Print** to generate the report.

### Submit via Portal
1. Log in to the Odoo website as a project manager.
2. Access the portal form at `/project_expenses/portal/new`.
3. Fill in the details and submit.

## Security
- Access rights are defined for expense managers and standard users.
- Validation ensures that expense amounts are positive and do not exceed predefined limits.

## Dependencies
- **base**
- **project**
- **stock**
- **portal**
- **contacts**

## Author
**Mahmoud Hashem**

## License
This module is licensed under the Odoo Proprietary License.
