# Power BI setup

Import `data/manufacturing_defects.csv` using the Text/CSV source. Each row represents one defect observation.

Use the Pareto+ visual with these fields:

| Chart | Categories | Values | Visual-level model filter |
|---|---|---|---|
| All models | Production Model | Count of Defect Type | All models |
| Model 595130-195 | Defect Type | Count of Defect Type | Model 595130-195 |
| Model 595214-125 | Defect Type | Count of Defect Type | Model 595214-125 |
| Model 595242-854 | Defect Type | Count of Defect Type | Model 595242-854 |

Use **Count**, not distinct count. Keep all observation areas and inspection weeks included. Sort categories by descending defect count. Display the cumulative percentage line and fit all categories without horizontal scrolling before exporting.

The expected model totals are 888, 663, and 630. The overall chart contains 3,150 records. Retain unknown and ambiguous categories and explain their limitations rather than silently removing or merging them.

If adding the original Power BI file later, save it as `reports/Manufacturing_Defect_Analysis.pbix` and add a link in the README.
