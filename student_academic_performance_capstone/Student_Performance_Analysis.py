import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report

df = pd.read_csv("student_academic_performance_raw_dataset.csv")
print(df.head(), df.tail(), df.shape, df.columns, df.info(), df.describe(include="all"))
print("Missing values before cleaning:\n", df.isna().sum())
print("Duplicate IDs:", df.Student_ID.duplicated().sum())

df["Department"] = df["Department"].astype(str).str.strip().str.upper()
df["Gender"] = df["Gender"].astype(str).str.strip().str.title()
df = df.drop_duplicates(subset="Student_ID", keep="first").copy()
numeric = ["Semester","Attendance_Percentage","Study_Hours_Per_Day","Assignment_Score","Internal_Marks","Previous_Semester_Marks","Final_Exam_Marks"]
for col in numeric:
    df[col] = pd.to_numeric(df[col], errors="coerce")
for col in ["Attendance_Percentage","Assignment_Score","Internal_Marks","Previous_Semester_Marks","Final_Exam_Marks"]:
    df.loc[~df[col].between(0,100) & df[col].notna(), col] = np.nan
df.loc[~df["Semester"].between(1,6), "Semester"] = np.nan
df.loc[df["Study_Hours_Per_Day"] < 0, "Study_Hours_Per_Day"] = np.nan
df["Result_Recalculated"] = np.where(df["Final_Exam_Marks"] >= 40, "Pass", "Fail")
df["Result_Mismatch"] = df["Result"].astype(str).str.strip().str.title() != df["Result_Recalculated"]
def category(x):
    if pd.isna(x): return "Unclassified"
    if x >= 85: return "Excellent"
    if x >= 70: return "Good"
    if x >= 50: return "Average"
    if x >= 40: return "Needs Improvement"
    return "Poor"
df["Performance_Category"] = df["Final_Exam_Marks"].apply(category)
print("Missing values after cleaning:\n", df.isna().sum())
print("Descriptive statistics:\n", df[numeric].agg(["mean","median","std","min","max"]))
print("Department summary:\n", df.groupby("Department").Final_Exam_Marks.agg(["count","mean","median"]))
print("Semester summary:\n", df.groupby("Semester").Final_Exam_Marks.mean())
print("Category proportions:\n", df.Performance_Category.value_counts(normalize=True)*100)
df["Attendance_Band"] = pd.cut(df.Attendance_Percentage,[-0.001,59.999,74.999,89.999,100],labels=["Below 60","60–74.9","75–89.9","90–100"])
df["Study_Hours_Band"] = pd.cut(df.Study_Hours_Per_Day,[-0.001,1.999,3.999,7],labels=["Below 2","2–3.9","4–7"])
print(df.groupby("Attendance_Band",observed=False).agg(Students=("Student_ID","count"),Average_Marks=("Final_Exam_Marks","mean"),Pass_Rate=("Result_Recalculated",lambda x:(x=="Pass").mean()*100)))
print(df.groupby("Study_Hours_Band",observed=False).Final_Exam_Marks.mean())
print("Correlation:\n",df.select_dtypes(include=np.number).corr())
for col in ["Attendance_Percentage","Study_Hours_Per_Day","Assignment_Score","Internal_Marks","Final_Exam_Marks"]:
    q1,q3=df[col].quantile([.25,.75]); iqr=q3-q1
    print(col,"IQR outliers:",((df[col]<q1-1.5*iqr)|(df[col]>q3+1.5*iqr)).sum())
sns.set_theme()
figures = [
    ("bar","Department","Final_Exam_Marks","Average final marks by department"),
]
df.groupby("Department").Final_Exam_Marks.mean().plot(kind="bar",title="Average Final Marks by Department",ylabel="Average marks")
plt.tight_layout(); plt.show()
df.Result_Recalculated.value_counts().plot(kind="bar",title="Pass versus Fail",xlabel="Result",ylabel="Students"); plt.tight_layout(); plt.show()
df.Final_Exam_Marks.hist(bins=20); plt.title("Final Examination Marks Distribution"); plt.xlabel("Final marks"); plt.ylabel("Students"); plt.tight_layout(); plt.show()
sns.boxplot(data=df,x="Department",y="Final_Exam_Marks"); plt.title("Final Marks by Department"); plt.tight_layout(); plt.show()
sns.regplot(data=df,x="Attendance_Percentage",y="Final_Exam_Marks",scatter_kws={"alpha":.4}); plt.title("Attendance versus Final Marks"); plt.tight_layout(); plt.show()
sns.scatterplot(data=df,x="Study_Hours_Per_Day",y="Final_Exam_Marks",alpha=.5); plt.title("Study Hours versus Final Marks"); plt.tight_layout(); plt.show()
sns.heatmap(df.select_dtypes(include=np.number).corr(),annot=True,cmap="coolwarm",fmt=".2f"); plt.title("Correlation Matrix"); plt.tight_layout(); plt.show()
df.Performance_Category.value_counts().reindex(["Excellent","Good","Average","Needs Improvement","Poor"]).plot(kind="bar",title="Students by Performance Category"); plt.tight_layout(); plt.show()

features=["Attendance_Percentage","Study_Hours_Per_Day","Assignment_Score","Internal_Marks","Previous_Semester_Marks","Gender","Department","Semester","Extracurricular","Internet_Access"]
model_data=df[features+["Result_Recalculated"]].dropna(subset=["Result_Recalculated"])
X=model_data[features]; y=model_data.Result_Recalculated.map({"Fail":0,"Pass":1})
numeric_features=["Attendance_Percentage","Study_Hours_Per_Day","Assignment_Score","Internal_Marks","Previous_Semester_Marks","Semester"]
categorical_features=[c for c in features if c not in numeric_features]
preprocessor=ColumnTransformer([("num",Pipeline([("imputer",SimpleImputer(strategy="median")),("scale",StandardScaler())]),numeric_features),("cat",Pipeline([("imputer",SimpleImputer(strategy="most_frequent")),("encode",OneHotEncoder(handle_unknown="ignore"))]),categorical_features)])
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=.25,random_state=42,stratify=y)
for name,estimator in [("Logistic Regression",LogisticRegression(max_iter=2000,random_state=42)),("Decision Tree",DecisionTreeClassifier(max_depth=5,min_samples_leaf=8,random_state=42))]:
    model=Pipeline([("preprocessor",preprocessor),("model",estimator)])
    model.fit(X_train,y_train); pred=model.predict(X_test)
    print(name)
    print("Accuracy:",accuracy_score(y_test,pred),"Precision:",precision_score(y_test,pred,zero_division=0),"Recall:",recall_score(y_test,pred,zero_division=0),"F1:",f1_score(y_test,pred,zero_division=0))
    print("Confusion matrix:\n",confusion_matrix(y_test,pred))
    print(classification_report(y_test,pred,zero_division=0))
