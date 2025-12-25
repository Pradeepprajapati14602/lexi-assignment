---
template_id: tpl_insurance_notice_sample
title: Incident Notice to Insurance Company
file_description: Notice to insurance company regarding a claimable incident under an active policy
jurisdiction: IN
doc_type: legal_notice
variables:
  - key: claimant_full_name
    label: Claimant's full name
    description: Full legal name of the person or entity raising the claim
    example: "Rajesh Kumar Sharma"
    required: true
    dtype: string
  - key: claimant_address
    label: Claimant's address
    description: Complete registered address of the claimant
    example: "45, Nehru Nagar, Mumbai - 400001, Maharashtra"
    required: true
    dtype: string
  - key: incident_date
    label: Date of incident
    description: The date on which the insured event occurred (ISO 8601 format)
    example: "2025-07-12"
    required: true
    dtype: date
    regex: "^\\d{4}-\\d{2}-\\d{2}$"
  - key: policy_number
    label: Policy number
    description: Insurance policy reference number exactly as printed on the policy schedule
    example: "POL-302786965"
    required: true
    dtype: string
  - key: insurer_name
    label: Insurance company name
    description: Full legal name of the insurance company
    example: "National Insurance Company Limited"
    required: true
    dtype: string
  - key: insurer_address
    label: Insurer's address
    description: Registered office address of the insurance company
    example: "3, Middleton Street, Kolkata - 700071"
    required: true
    dtype: string
  - key: incident_description
    label: Incident description
    description: Detailed description of what happened
    example: "On the said date, while the insured vehicle was parked at the residence, it was damaged by a falling tree branch during heavy rainfall."
    required: true
    dtype: string
  - key: demand_amount_inr
    label: Claim amount (INR)
    description: Total principal claim amount in Indian Rupees excluding interest and legal fees
    example: "450000"
    required: true
    dtype: number
  - key: vehicle_registration
    label: Vehicle registration number
    description: Registration number of the insured vehicle (if applicable)
    example: "MH-01-AB-1234"
    required: false
    dtype: string
similarity_tags: ["insurance", "notice", "india", "motor", "claim", "intimation"]
---

**NOTICE OF CLAIM UNDER INSURANCE POLICY**

To,
{{insurer_name}}
{{insurer_address}}

Date: {{current_date}}

**Subject: Notice of Claim under Policy No. {{policy_number}}**

Dear Sir/Madam,

I, {{claimant_full_name}}, residing at {{claimant_address}}, hereby give you notice of a claim under the above-referenced insurance policy.

**Details of the Incident:**

On {{incident_date}}, the following incident occurred:

{{incident_description}}

The insured vehicle bearing registration number {{vehicle_registration}} was covered under Policy No. {{policy_number}} at the time of the incident.

**Claim Amount:**

I hereby claim an amount of INR {{demand_amount_inr}} (Indian Rupees {{demand_amount_words}}) as compensation for the loss/damage sustained.

**Documents Enclosed:**

1. Copy of insurance policy
2. FIR/Police complaint (if applicable)
3. Photographs of the damage
4. Repair estimates from authorized service centers
5. Other supporting documents

**Request:**

I request you to kindly process this claim at the earliest and arrange for inspection of the damaged vehicle. Please intimate me of the surveyor's visit and the progress of the claim.

Please acknowledge receipt of this notice and provide a claim reference number within 7 days from the date of this notice.

I reserve my right to initiate legal proceedings if the claim is not settled within a reasonable time period as per the policy terms and the Insurance Act, 1938.

Thanking you,

Yours faithfully,

{{claimant_full_name}}
Contact: {{claimant_phone}}
Email: {{claimant_email}}

---

**For Office Use:**
Claim Reference No: _______________
Received on: _______________
Acknowledged by: _______________

<!-- Sample template created by UOIONHHC -->
