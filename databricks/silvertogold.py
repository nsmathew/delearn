# Databricks notebook source
dbutils.fs.ls('/mnt/silver/SalesLT/')

# COMMAND ----------

dbutils.fs.ls('/mnt/gold')

# COMMAND ----------

input_path = '/mnt/silver/SalesLT/Address/'
df = spark.read.format('delta').load(input_path)

# COMMAND ----------

display(df)

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, regexp_replace

columns = df.columns

for old_col in columns:
    new_col = "".join(["_" + char if char.isupper() and not old_col[i-1].isupper() else char for i, char in enumerate(old_col)]).lstrip("_")
    df = df.withColumnRenamed(old_col, new_col)

# COMMAND ----------

display(df)

# COMMAND ----------

table_name = []
for i in dbutils.fs.ls('/mnt/silver/SalesLT/'):
    table_name.append(i.name.split('/')[0])

# COMMAND ----------

table_name

# COMMAND ----------

for i in table_name:
    input_path = '/mnt/silver/SalesLT/'+i
    df = spark.read.format('delta').load(input_path)
    columns = df.columns

    for old_col in columns:
        new_col = "".join(["_" + char if char.isupper() and not old_col[i-1].isupper() else char for i, char in enumerate(old_col)]).lstrip("_")
        df = df.withColumnRenamed(old_col, new_col)
    
    output_path = '/mnt/gold/SalesLT/' + i + '/'
    df.write.format('delta').mode('overwrite').save(output_path)


# COMMAND ----------

display(df)
