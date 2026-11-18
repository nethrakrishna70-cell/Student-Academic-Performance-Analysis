STUDENT ACADEMIC PERFORMANCE CAPSTONE - DELIVERABLES

Files:
- Student_Performance_Analysis.xlsx: raw data, cleaned data, quality summary, pivot-style analyses and Excel charts.
- Student_Performance_Queries.sql: database/table setup and all 18 SQL questions.
- Student_Performance_Analysis.ipynb: runnable notebook covering inspection, cleaning, EDA, 8 charts, IQR and ML.
- Student_Performance_Analysis.py: standalone Python script (expects the supplied raw CSV in the same folder).
- Student_Performance_Cleaned.csv: cleaned import file for SQL and Power BI.
- powerbi/: DAX measures, theme, build guide and static dashboard preview.
- Student_Academic_Performance_Report.docx and .pdf: report draft with actual metrics and selected graphs.
- Student_Academic_Performance_Presentation.pptx: 6-slide presentation.
- graphs/: all eight required graphs.

IMPORTANT POWER BI:
A genuine .pbix must be created and saved in Power BI Desktop. Included are the cleaned CSV, DAX measures, theme JSON, instructions and dashboard preview. The PNG is a static visual preview, not an interactive PBIX.

CLEANING POLICY:
- 758 raw rows, 8 duplicate Student_ID rows removed, leaving 750 unique IDs.
- Original raw data preserved.
- Department labels trimmed and uppercased.
- Invalid attendance/marks outside 0-100 and invalid semester values are set to missing for analysis.
- Missing values are retained and excluded per metric; no fabricated imputation in the core EDA.
- Machine learning uses median/mode imputation inside a train/test pipeline.
- Pass threshold is 40/100.
- Student_ID, Student_Name and Final_Exam_Marks excluded from ML predictors.

Before submission:
1. Add your name, register number, department and date to the report and presentation.
2. Open the notebook in Jupyter and run all cells from top to bottom.
3. Import the cleaned CSV into MySQL and execute the SQL queries; export at least five query result screenshots as the brief requests.
4. Open Power BI Desktop, follow powerbi/PowerBI_Instructions.txt, and save the .pbix file.
5. Validate all outputs and be prepared to explain cleaning choices, correlation, false positives/negatives and limitations.
