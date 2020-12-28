# Databricks notebook source
#access Azure Data Lake gen2 directly using storage account key
accountName = "dlswta"
#copy your key1 account key between the double quotes
accountKey = ""
config = "fs.azure.account.key." + accountName + ".dfs.core.windows.net"

spark.conf.set(config, accountKey)

# COMMAND ----------

dbutils.fs.ls("abfss://landing@dlswta.dfs.core.windows.net/rankings")

# COMMAND ----------

k

# COMMAND ----------

#set the data lake file location
filePath = "abfss://landing@dlswta.dfs.core.windows.net/rankings/*.csv"

#read the data into df dataframe
df = spark.read.csv(filePath)
display(df)

# COMMAND ----------

df.count()

# COMMAND ----------

from pyspark.sql.types import *

#define a schema providing column names and data types
schema = StructType([
  StructField("ranking_date", IntegerType(), True),
  StructField("ranking",IntegerType(), True),
  StructField("player_id", IntegerType(), True),
  StructField("ranking_points", IntegerType(), True),
  StructField("tours", IntegerType(), True)
])

df = spark.read.csv(filePath, header=False, schema=schema)
display(df)

# COMMAND ----------

#set the data lake destination path
destPath = "abfss://cleansed@dlswta.dfs.core.windows.net/rankings"

#write the data to the new location forcing one partition
df.coalesce(1).write.csv(destPath, header="true", mode="overwrite")
