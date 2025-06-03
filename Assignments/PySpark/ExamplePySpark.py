from pyspark.sql import SparkSession
from pyspark.sql.functions import col, mean, monotonically_increasing_id, udf
from pyspark.sql.types import StringType, IntegerType

file_path = "/tmp/US_UK_2025/jinu/input/samplefile.csv"
df = spark.read.option("header", True).option("inferSchema", True).csv(file_path)


#Get the data types of each column
print("Schema:")
df.printSchema()

#Check for missing values in each column
df.select([col(c).isNull().alias("{}_is_null".format(c)) for c in df.columns]).show()
df.show()

#Rename a column (e.g., Salary to Annual_Salary)
df = df.withColumnRenamed("Salary", "Annual_Salary")
df.show()

#Filter where Age > 30
df_filtered = df.filter(col("Age") > 30)
df_filtered.show()

#Select specific columns (e.g., Name and Age)
df_selected = df.select("Name", "Age")
df_selected.show()

#Drop a column (e.g., Department)
df_dropped = df.drop("Department")
df_dropped.show()

#Multiply a column by 2 (e.g., Annual_Salary)
df_transformed = df.withColumn("Double_Salary", col("Annual_Salary") * 2)
df_transformed.show()

#Add a new column based on existing (e.g., Age + 5)
df_new_column = df_transformed.withColumn("Age_In_5_Years", col("Age") + 5)
df_new_column.show()

#Group by Department and get mean salary
df.groupBy("Department").agg(mean("Annual_Salary").alias("Avg_Salary")).show()

#Sort by Annual_Salary descending
df.orderBy(col("Annual_Salary").desc()).show()

#Merge with another DataFrame on Department
location_data = [("HR", "Building A"), ("IT", "Building B"), ("Finance", "Building C")]
df_location = spark.createDataFrame(location_data, ["Department", "Location"])
df_merged = df.join(df_location, on="Department", how="left")
df_merged.show()

#Join two DataFrames using index
df1 = df.withColumn("id", monotonically_increasing_id())
df2 = df.withColumn("id", monotonically_increasing_id())
df_index_join = df1.join(df2, "id").select(df1.Name.alias("Name1"), df2.Name.alias("Name2"))
df_index_join.show()

#Apply a function using UDF (.apply() equivalent)
def format_name(name):
    return "Employee_" + name

format_name_udf = udf(format_name, StringType())
df_udf = df.withColumn("Formatted_Name", format_name_udf(col("Name")))
df_udf.show()

#Filter rows with multiple conditions (e.g., Age > 30 and Salary > 60000)
df_multi_filter = df.filter((col("Age") > 30) & (col("Annual_Salary") > 60000))
df_multi_filter.show()

#Convert column to numeric type (just for example if Age was string)
df_casted = df.withColumn("Age", col("Age").cast(IntegerType()))
df_casted.printSchema()

#Save to CSV
df_casted.write.csv("/tmp/US_UK_2025/jinu/output/modified_employee.csv", header=True, mode="overwrite")
df_casted.show()





