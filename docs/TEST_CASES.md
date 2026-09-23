# Test Cases

## Test strategy
Testing focuses on the main user workflow, governance rules, CSV profiling, exports, and error handling.

| ID | Test | Expected result |
|---|---|---|
| TC01 | Open application | Dashboard loads without an exception |
| TC02 | Click Load demo dataset | Demo data appears with profile metrics |
| TC03 | Upload valid CSV | Rows, columns, missing cells and duplicates are shown |
| TC04 | Upload invalid CSV | A readable error is displayed |
| TC05 | Generate with complete metadata | Checks are Complete and package is generated |
| TC06 | Remove Privacy Review text | Privacy is reported as a Gap |
| TC07 | Remove several governance fields | Completeness decreases and risk may increase |
| TC08 | Use a high-impact purpose term | High-impact domain review appears |
| TC09 | Download JSON | Valid JSON package is produced |
| TC10 | Download Markdown | Governance report is produced |
| TC11 | Download PDF | PDF report is produced |
| TC12 | Dataset with missing/duplicate values | Profile reports them correctly |

## Acceptance criteria
- The application can generate a governance package from the default example.
- A CSV can be uploaded and profiled.
- Missing governance evidence is visible.
- Risk level changes according to configured rules.
- Export buttons produce the documented artifacts.
- The app explains that results are a governance aid and not certification.

## Manual test record
Before final submission, run the application locally and mark each test as Pass/Fail with the date and tester name. Add screenshots for the main successful workflow.