import pyspark
import numpy as np
from pyspark.sql.types import FloatType
from pyspark.sql.functions import UserDefinedFunction
from pyspark.sql.types import IntegerType,StringType
import pandas as pd
import time
from pyspark import sparkcontext sparkconf
import yaml
import os
import ssl
from psycopg2.extras import Json
import psycopg2
from boto.s3.connection import S3Connection
from boto.s3.key import Key



credentials = yaml.load(open(os.path.expanduser('taxi.yml')))



rides = {"galvanize": "pier_39",
"ggpark": "ggbridge",
"ggbridge": "sutro_baths",
"sutro_baths": "ggbridge",
"pier_39": "galvanize",
"twin_peaks": "sf_zoo",
"airport": "sf_zoo",
"usf" : "sf_zoo",
"glen_park" : "airport",
"sf_zoo" : "airport",
"dolores_park" : "galvanize",
"AT_T": "tenderloin",
"castro": "galvanize",
"lombart": "ggpark",
"u_sq": "airport",
"china_town": "lombart",
"baker_beach": "sf_zoo",
"painted_ladies": "castro",
"embarcadero": "sutro_baths",
"tenderloin": "galvanize",
"financial_district" : "tenderloin",
"ghirardeli_sq" : "pier_39",
"outer_sunset" : "sf_zoo",
"ucsf" : "twin_peaks",
"stonestown" : "AT_T",
"design_district" : "lombart",
"forest_hill" : "dolores_park",
"mission_bart" : "china_town",
"dogpatch" : "ghirardeli_sq",
"mt_davidson" : "ucsf",
"cal_acad_science": "galvanize"

}

def get_final_uber_df(uber_df):
    """Converts json to Dataframe and puts the data in the most accessabe format"""

    roundit = UserDefinedFunction(lambda x: int(x)/2,IntegerType())
    joined = uber_df.select(roundit(uber_df["galvanize.time"]).alias("main_time"))
    for start,end in rides.items():

        df = uber_df.select(roundit(uber_df["{}.time".format(start)]).alias("time"),\
                            uber_df["{}.{}.surge_multiplier".format(start,end)][2].alias("uber_{}".format(start)))
        joined = joined.join(df,joined.main_time==df.time).drop("time")
    return joined.sort("main_time")


def get_final_lyft_df(lyft_df):
    """Converts json to a dataframe thats easily accessable """
    numerify = UserDefinedFunction(lambda x: 1+float(str(x).replace("%",""))/100,FloatType())
    roundit = UserDefinedFunction(lambda x: int(x)/2,IntegerType())
    joined = lyft_df.select(roundit(lyft_df["galvanize.time"]).alias("main_time"))
    for start,end in rides.items():

        df = lyft_df.select(roundit(lyft_df["{}.time".format(start)]).alias("time"),\
                            numerify(lyft_df["{}.{}.cost_estimates.primetime_percentage".format(start,end)][2]).alias("lyft_{}".format(start)))
        
        joined = joined.join(df,joined.main_time==df.time).drop("time")
    return joined.sort("main_time")

def main():
	""" Main function"""
	## Loads data from s3
	uber_df = spark_session.read.json("s3a://uber-rides/2017/03/*/*/*")lyft_df = spark_session.read.json("s3a://lyft-rides/2017/03/*/*/*")
	lyft_df = spark_session.read.json("s3a://lyft-rides/2017/03/*/*/*")


	#Spark DataFrame manipulatioins using some functioins defined above
	final_uber_df = get_final_uber_df(uber_df)
	final_lyft_df = get_final_lyft_df(lyft_df)

	## Cache for further use
	final_uber_df.cache()
	final_lyft_df.cache()

	#get hour column from the main_time ""time.time()"" column 
	gethour = UserDefinedFunction(lambda x: time.strftime('%H', time.localtime(x*120)) ,StringType())
	u = final_uber_df.withColumn("uber_hour", gethour("main_time"))
	l = final_lyft_df.withColumn("lyft_hour",gethour("main_time"))

	#Save the DataFrames as parquet for backup
	u.write.parquet("s3://parquet-uber-lyft/final_uber_df")
	l.write.parquet("s3://parquet-uber-lyft/final_lyft_df")


	# Convrt to pandas for some plotting and eda
	up = u.toPandas()

	lp = l.toPandas()

	avg_day_uber= up.groupby("uber_hour").mean().reset_index()
	avg_day_lyft = lp.groupby("lyft_hour").mean().reset_index()

	return avg_day_uber, avg_day_lyft


def postgresql(avg_day_uber, avg_day_lyft):
	""" Connects to 2 existimh empty tables : uber and lyft.
	Creates the columns. Each column is a location. there are 31 locations.
	Adds the values into the tables """

	conn = psycopg2.connect(database=credentials['postgres_uber'].get('database'), \
	user=credentials['postgres_uber'].get('user'),\
	host =credentials['postgres_uber'].get('host'),\
    port = credentials["postgres_uber"].get("port"),\
	password=credentials['postgres_uber'].get('password'))

	cur = conn.cursor()


	cur.execute("""ALTER TABLE lyft ADD hour BIGINT""")
	cur.execute("""ALTER TABLE uber ADD hour BIGINT""")

	conn.commit()

	cols = [i.replace("uber_","") for i in avg_day_uber if i not in ["main_time","uber_hour"]]

	for col in cols:
	    cur.execute("ALTER TABLE uber ADD {} DOUBLE PRECISION".format(col))
	    cur.execute("ALTER TABLE lyft ADD {} DOUBLE PRECISION".format(col))
	    conn.commit()

	avg_u = avg_day_uber.drop("main_time",axis=1)
	avg_u["uber_hour"] = avg_u["uber_hour"].apply(lambda x : int(x.encode("utf-8")))



	avg_l = avg_day_lyft.drop("main_time",axis=1)
	avg_l["lyft_hour"] = avg_l["lyft_hour"].apply(lambda x : int(x.encode("utf-8")))




	for i in range(len(avg_l)):
    l = list(avg_l.iloc[i])
    print len(l)

    cur.execute("INSERT INTO lyft (hour, AT_T,\
    airport,\
    baker_beach,\
    cal_acad_science,\
    castro,china_town,\
    design_district,\
    dogpatch,\
    dolores_park,\
    embarcadero,\
    financial_district,\
    forest_hill,\
    galvanize,\
    ggbridge,\
    ggpark,\
    ghirardeli_sq,\
    glen_park,\
    lombart,\
    mission_bart,\
    mt_davidson,\
    outer_sunset,\
    painted_ladies,\
    pier_39,\
    sf_zoo,\
    stonestown,\
    sutro_baths,\
    tenderloin,\
    twin_peaks,\
    u_sq,\
    ucsf,\
    usf) VALUES ({},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{})".format(*l))
    conn.commit()


for i in range(len(avg_u)):
    l = list(avg_u.iloc[i])
    print len(l)

    cur.execute("INSERT INTO uber (hour, AT_T,\
    airport,\
    baker_beach,\
    cal_acad_science,\
    castro,china_town,\
    design_district,\
    dogpatch,\
    dolores_park,\
    embarcadero,\
    financial_district,\
    forest_hill,\
    galvanize,\
    ggbridge,\
    ggpark,\
    ghirardeli_sq,\
    glen_park,\
    lombart,\
    mission_bart,\
    mt_davidson,\
    outer_sunset,\
    painted_ladies,\
    pier_39,\
    sf_zoo,\
    stonestown,\
    sutro_baths,\
    tenderloin,\
    twin_peaks,\
    u_sq,\
    ucsf,\
    usf) VALUES ({},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{})".format(*l))
    conn.commit()

if __name__ == "__main__":

    conf = SparkConf().setAppName(APP_NAME)
    conf = conf.setMaster("local[*]")
    sc = SparkContext(conf=conf)

	spark_session = SparkSession.builder \
	.master("local") \
	.appName("Word Count") \
	.config("spark.some.config.option", "some-value") \
	.getOrCreate()

	ub,ly = main()
	postgresql(ub,ly)
