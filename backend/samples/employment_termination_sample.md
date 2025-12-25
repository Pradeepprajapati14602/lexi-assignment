---
template_id: tpl_employment_termination
title: Employment Termination Letter
file_description: Formal letter for termination of employment with notice period
jurisdiction: IN
doc_type: employment_letter
variables:
  - key: employee_full_name
    label: Employee's full name
    description: Full legal name of the employee being terminated
    example: "Priya Deshmukh"
    required: true
    dtype: string
  - key: employee_id
    label: Employee ID
    description: Company-assigned employee identification number
    example: "EMP-2023-0456"
    required: true
    dtype: string
  - key: employee_designation
    label: Designation
    description: Current job title or designation
    example: "Senior Software Engineer"
    required: true
    dtype: string
  - key: termination_date
    label: Termination effective date
    description: Date from which employment will be terminated (ISO format)
    example: "2025-02-28"
    required: true
    dtype: date
  - key: notice_period_days
    label: Notice period (days)
    description: Number of days of notice period as per employment contract
    example: "30"
    required: true
    dtype: number
  - key: termination_reason
    label: Reason for termination
    description: Brief, professional reason for termination
    example: "redundancy due to organizational restructuring"
    required: true
    dtype: string
  - key: company_name
    label: Company name
    description: Full legal name of the employer company
    example: "Tech Innovations Private Limited"
    required: true
    dtype: string
  - key: company_address
    label: Company address
    description: Registered office address of the company
    example: "Tower A, Cyber City, Bangalore - 560103"
    required: true
    dtype: string
  - key: last_working_day
    label: Last working day
    description: Last day the employee should attend work
    example: "2025-02-28"
    required: true
    dtype: date
  - key: hr_manager_name
    label: HR Manager name
    description: Name of the HR Manager or authorized signatory
    example: "Amit Verma"
    required: true
    dtype: string
similarity_tags: ["employment", "termination", "notice", "india", "hr", "resignation"]
---

**EMPLOYMENT TERMINATION LETTER**

{{company_name}}
{{company_address}}

Date: {{issue_date}}

**PRIVATE & CONFIDENTIAL**

{{employee_full_name}}
Employee ID: {{employee_id}}
Designation: {{employee_designation}}

**Subject: Termination of Employment**

Dear {{employee_full_name}},

This letter is to formally notify you that your employment with {{company_name}} will be terminated effective {{termination_date}}.

**Reason for Termination:**

This decision has been made due to {{termination_reason}}. We regret having to take this step.

**Notice Period:**

As per your employment agreement, you are required to serve a notice period of {{notice_period_days}} days. Your last working day with the company will be {{last_working_day}}.

**Final Settlement:**

Your final settlement will include:
- Salary for the month worked
- Encashment of unutilized leave (if applicable)
- Statutory dues (PF, Gratuity as applicable)
- Any other benefits as per company policy

The final settlement amount will be processed and credited to your bank account within 30 days from your last working day.

**Handover of Responsibilities:**

You are required to complete the handover of all your responsibilities, company assets, documents, and any other property belonging to the company before your last working day. This includes:
- Company laptop, mobile phone, access cards
- All confidential information and documents
- Client data and project files
- Completion of exit formalities

**Relieving Letter and Experience Certificate:**

Upon successful completion of your exit formalities, the company will issue:
1. Relieving Letter
2. Experience Certificate
3. Full and Final Settlement statement

**Non-Disclosure and Non-Compete:**

You are reminded that the Non-Disclosure Agreement and Non-Compete clauses in your employment contract remain valid and enforceable even after termination of employment.

**Exit Interview:**

The HR department will schedule an exit interview with you before your last working day. This is a valuable opportunity for us to understand your feedback and improve our processes.

We appreciate your contributions to {{company_name}} and wish you the very best in your future endeavors.

Should you have any questions regarding this termination or the exit process, please contact the HR department.

Yours sincerely,

{{hr_manager_name}}
HR Manager
{{company_name}}

---

**Employee Acknowledgment:**

I, {{employee_full_name}}, acknowledge receipt of this termination letter and confirm that I have read and understood its contents.

Employee Signature: _______________
Date: _______________

<!-- Template created by UOIONHHC -->
