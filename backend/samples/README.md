# Sample Documents - UOIONHHC

This directory contains sample legal document templates in Markdown format with YAML front-matter.

## Available Samples:

1. **insurance_notice_sample.md**
   - Type: Insurance claim notice
   - Jurisdiction: India
   - Variables: 10 fields including claimant info, policy details, incident description
   - Use case: Notifying insurance company of a claimable incident

2. **employment_termination_sample.md**
   - Type: Employment termination letter
   - Jurisdiction: India
   - Variables: 10 fields including employee details, termination reasons, notice period
   - Use case: Formal termination of employment with proper notice

## How to Use These Samples:

### Option 1: Import via API
Upload these files through the Lexi UI to automatically extract variables and create templates.

### Option 2: Manual Testing
Use these as reference documents to test the system's variable extraction capabilities.

### Option 3: Pre-populate Database
Parse these markdown files and insert them directly into the templates table.

## Template Format

Each sample follows the standard format:

```markdown
---
template_id: unique_identifier
title: Human Readable Title
file_description: Brief description
jurisdiction: Country code (IN, US, UK, etc.)
doc_type: Category (legal_notice, employment_letter, etc.)
variables:
  - key: variable_key_snake_case
    label: Human Readable Label
    description: Detailed description
    example: "Sample value"
    required: true/false
    dtype: string/number/date/enum
    regex: "validation pattern" (optional)
similarity_tags: ["tag1", "tag2", ...]
---

Template body with {{variable_keys}} for substitution...
```

## Creating Your Own Samples

1. Follow the YAML front-matter structure
2. Use snake_case for variable keys
3. Include clear labels and descriptions
4. Provide realistic examples
5. Mark required vs optional fields
6. Add similarity tags for better matching
7. Use {{variable_key}} in the body for placeholders

## Testing the System

1. **Upload Test**: Upload the .md files as if they were DOCX/PDF
2. **Extraction Test**: Verify all variables are correctly identified
3. **Matching Test**: Test queries like "draft insurance notice" or "termination letter"
4. **Drafting Test**: Complete the Q&A flow and verify variable substitution

## Notes

- These samples are for demonstration purposes only
- Actual legal documents should be reviewed by qualified lawyers
- Customize jurisdiction and variables based on your requirements
- Add more samples to improve template matching accuracy

---

For more information, see the main README.md
