# Databricks notebook source
#access Azure Data Lake gen2 directly using storage account key
accountName = "dlswta"
#copy your key1 account key between the double quotes
accountKey = ""
config = "fs.azure.account.key." + accountName + ".dfs.core.windows.net"

spark.conf.set(config, accountKey)

# COMMAND ----------

dbutils.fs.ls("abfss://landing@dlswta.dfs.core.windows.net/players")

# COMMAND ----------

#set the data lake file location
filePath = "abfss://landing@dlswta.dfs.core.windows.net/players/wta_players.csv"

#read the data into df dataframe
df = spark.read.csv(filePath)
display(df)

# COMMAND ----------

from pyspark.sql.types import *

#define a schema providing column names and data types
schema = StructType([
  StructField("player_id", IntegerType(), True),
  StructField("first_name",StringType(), True),
  StructField("last_name", StringType(), True),
  StructField("hand", StringType(), True),
  StructField("birth_date", IntegerType(), True),
  StructField("country_code", StringType(), True),
])

df = spark.read.csv(filePath, header=False, schema=schema)
display(df)

# COMMAND ----------

#set the data lake destination path
destPath = "abfss://cleansed@dlswta.dfs.core.windows.net/players"

#write the data to the new location forcing one partition
df.coalesce(1).write.csv(destPath, header="true", mode="overwrite")
