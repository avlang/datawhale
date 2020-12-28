# Databricks notebook source
#access Azure Data Lake gen2 directly using storage account key
accountName = "dlswta"
#copy your key1 account key between the double quotes
accountKey = ""
config = "fs.azure.account.key." + accountName + ".dfs.core.windows.net"

spark.conf.set(config, accountKey)

# COMMAND ----------

dbutils.fs.ls("abfss://landing@dlswta.dfs.core.windows.net/matches")

# COMMAND ----------

#set the data lake file location
#filePath = "abfss://landing@dlswta.dfs.core.windows.net/matches/*.csv"
filePath = "abfss://landing@dlswta.dfs.core.windows.net/matches/wta_matches_*.csv"

#read the data into df dataframe
df = spark.read.csv(filePath, header=True, inferSchema=True)
display(df)

# COMMAND ----------

df.printSchema()

# COMMAND ----------

#get total number of rows
df.count()

# COMMAND ----------

df.printSchema()

# COMMAND ----------

#creating a temporary view that we can query using SQL
df.createOrReplaceTempView("vw_matches")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*)
# MAGIC FROM vw_matches

# COMMAND ----------

#use the %sql magic command and begin writing SQL statements

# COMMAND ----------

# MAGIC %sql 
# MAGIC SELECT COUNT(*)
# MAGIC FROM vw_matches

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT tourney_name
# MAGIC   ,tourney_date
# MAGIC   ,match_num
# MAGIC   ,winner_name
# MAGIC   ,winner_ioc
# MAGIC   ,loser_name
# MAGIC   ,loser_ioc
# MAGIC   ,score
# MAGIC FROM vw_matches
# MAGIC WHERE winner_name='Bianca Andreescu'
# MAGIC ORDER BY tourney_date DESC, match_num DESC

# COMMAND ----------

#set the data lake destination path
destPath = "abfss://cleansed@dlswta.dfs.core.windows.net/matches"

#write the data to the new location forcing one partition
df.coalesce(1).write.csv(destPath, header="true", mode="overwrite")
