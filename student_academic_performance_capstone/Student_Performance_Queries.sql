CREATE DATABASE IF NOT EXISTS Student_Performance_DB;
USE Student_Performance_DB;

DROP TABLE IF EXISTS Student_Performance;
CREATE TABLE Student_Performance (
 Student_ID VARCHAR(20) PRIMARY KEY, Student_Name VARCHAR(50), Gender VARCHAR(20),
 Department VARCHAR(20), Semester INT, Attendance_Percentage DECIMAL(6,2),
 Study_Hours_Per_Day DECIMAL(5,2), Assignment_Score DECIMAL(6,2),
 Internal_Marks DECIMAL(6,2), Previous_Semester_Marks DECIMAL(6,2),
 Final_Exam_Marks DECIMAL(6,2), Extracurricular VARCHAR(5),
 Internet_Access VARCHAR(5), Result VARCHAR(10), Performance_Category VARCHAR(30)
);

-- Import the cleaned CSV exported as Student_Performance_Cleaned.csv into this table using your SQL client's import wizard.

-- 1. Display all student records.
SELECT * FROM Student_Performance;

-- 2. Display the first 10 student records.
SELECT * FROM Student_Performance LIMIT 10;

-- 3. Show students in the MCA department.
SELECT * FROM Student_Performance WHERE Department='MCA';

-- 4. Find students with final marks greater than 80.
SELECT * FROM Student_Performance WHERE Final_Exam_Marks > 80;

-- 5. Find students with attendance below 75 percent.
SELECT * FROM Student_Performance WHERE Attendance_Percentage < 75;

-- 6. Count total students.
SELECT COUNT(*) AS Total_Students FROM Student_Performance;

-- 7. Calculate average, minimum and maximum final marks.
SELECT AVG(Final_Exam_Marks) AS Average_Marks, MIN(Final_Exam_Marks) AS Minimum_Marks, MAX(Final_Exam_Marks) AS Maximum_Marks FROM Student_Performance;

-- 8. Count students department-wise.
SELECT Department, COUNT(*) AS Student_Count FROM Student_Performance GROUP BY Department;

-- 9. Calculate department-wise average final marks.
SELECT Department, AVG(Final_Exam_Marks) AS Average_Final_Marks FROM Student_Performance GROUP BY Department;

-- 10. Count Pass and Fail students.
SELECT CASE WHEN Final_Exam_Marks >= 40 THEN 'Pass' ELSE 'Fail' END AS Result_Status, COUNT(*) AS Student_Count FROM Student_Performance GROUP BY Result_Status;

-- 11. Calculate pass percentage for each department.
SELECT Department, 100.0*SUM(CASE WHEN Final_Exam_Marks >= 40 THEN 1 ELSE 0 END)/COUNT(*) AS Pass_Percentage FROM Student_Performance GROUP BY Department;

-- 12. Find departments whose average final marks are above 70.
SELECT Department, AVG(Final_Exam_Marks) AS Average_Final_Marks FROM Student_Performance GROUP BY Department HAVING AVG(Final_Exam_Marks) > 70;

-- 13. Display the top 10 students by final marks.
SELECT Student_ID, Student_Name, Department, Final_Exam_Marks FROM Student_Performance ORDER BY Final_Exam_Marks DESC LIMIT 10;

-- 14. Find students whose current final marks are lower than previous semester marks.
SELECT Student_ID, Department, Previous_Semester_Marks, Final_Exam_Marks FROM Student_Performance WHERE Final_Exam_Marks < Previous_Semester_Marks;

-- 15. Find students with attendance above 85 percent but final marks below 40.
SELECT Student_ID, Department, Attendance_Percentage, Final_Exam_Marks FROM Student_Performance WHERE Attendance_Percentage > 85 AND Final_Exam_Marks < 40;

-- 16. Calculate average final marks by semester.
SELECT Semester, AVG(Final_Exam_Marks) AS Average_Final_Marks FROM Student_Performance GROUP BY Semester ORDER BY Semester;

-- 17. Classify students into five performance categories using CASE.
SELECT Student_ID, Final_Exam_Marks,
 CASE WHEN Final_Exam_Marks >= 85 THEN 'Excellent'
      WHEN Final_Exam_Marks >= 70 THEN 'Good'
      WHEN Final_Exam_Marks >= 50 THEN 'Average'
      WHEN Final_Exam_Marks >= 40 THEN 'Needs Improvement'
      ELSE 'Poor' END AS Performance_Category
FROM Student_Performance;

-- 18. Rank students by final examination marks using a window function.
SELECT Student_ID, Department, Final_Exam_Marks,
 RANK() OVER (ORDER BY Final_Exam_Marks DESC) AS Marks_Rank
FROM Student_Performance;
