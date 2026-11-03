# Hospital Flow AI — UI/UX Refresh

This update focuses on the Streamlit presentation layer in `app.py`.

## What changed
- Introduced a consistent healthcare dashboard theme with navy, teal, and light neutral colours.
- Added a compact application brand area and a professional top banner.
- Improved sidebar navigation styling, active-page emphasis, spacing, and typography.
- Styled metric cards, forms, buttons, tables, expanders, and alerts consistently.
- Improved the dashboard's section hierarchy and KPI help text.
- Added a compact footer and moved the educational safety notice into a collapsible section.
- Added responsive CSS adjustments for narrower screens.

## What was intentionally preserved
- AI agent implementations and execution.
- LangGraph workflow logic.
- Database schema and database operations.
- Patient registration, queue, routing, resource, bed allocation, discharge, transfer, and notification logic.
- Existing integrations and application dependencies.

## Run locally
Use your existing project virtual environment and dependencies:

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

The application is an educational prototype. Use synthetic demonstration data only. The visual refresh does not validate AI outputs for clinical use.


## Follow-up layout fixes
- Corrected the top brand title/subtitle contrast so the title is visible on the light workspace background.
- Changed the resource chart to horizontal bars to prevent long resource labels from rotating vertically in a narrow column.
- Set a controlled chart height and improved the patient/resource table column sizing and heights.
- Limited the resource table to Resource, Total, and Available columns so it fits the dashboard cleanly.
