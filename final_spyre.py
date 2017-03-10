import yaml
import os
import ssl
from psycopg2.extras import Json
import psycopg2
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from spyre import server
import seaborn as sns
import pandas as pd
from urllib2 import urlopen
import json




class StockExample(server.App):
    title = " Historical Surge"

    inputs = [{     "type":'dropdown',
                    "label": 'Location', 
                    "options" : [ {"label": "galvanize", "value":"galvanize"},
                                  {"label": "AT_T", "value":"AT_T"},
                                  {"label": "airport", "value":"airport"},
                                  {"label": "baker_beach", "value":"baker_beach"},
                                  {"label": "cal_acad_science", "value":"cal_acad_science"},
                                  {"label": "castro", "value":"castro"},
                                  {"label": "china_town", "value":"china_town"},
                                  {"label": "design_district", "value":"design_district"},
                                  {"label": "dogpatch", "value":"dogpatch"},
                                  {"label": "dolores_park", "value":"dolores_park"},
                                  {"label": "embarcadero", "value":"embarcadero"},
                                  {"label": "financial_district", "value":"financial_district"},
                                  {"label": "forest_hill", "value":"forest_hill"},
                                  {"label": "ggbridge", "value":"ggbridge"},
                                  {"label": "ggpark", "value":"ggpark"},
                                  {"label": "ghirardeli_sq", "value":"ghirardeli_sq"},
                                  {"label": "glen_park", "value":"glen_park"},
                                  {"label": "lombart", "value":"lombart"},
                                  {"label": "mission_bart", "value":"mission_bart"},
                                  {"label": "mt_davidson", "value":"mt_davidson"},
                                  {"label": "outer_sunset", "value":"outer_sunset"},
                                  {"label": "painted_ladies", "value":"painted_ladies"},
                                  {"label": "pier_39", "value":"pier_39"},
                                  {"label": "sf_zoo", "value":"sf_zoo"},
                                  {"label": "stonestown", "value":"stonestown"},
                                  {"label": "sutro_baths", "value":"sutro_baths"},
                                  {"label": "tenderloin", "value":"tenderloin"},
                                  {"label": "twin_peaks", "value":"twin_peaks"},
                                  {"label": "u_sq", "value":"u_sq"},
                                  {"label": "ucsf", "value":"ucsf"},
                                  {"label": "usf", "value":"usf"}],
                    "key": 'ticker', 
                    "action_id": "update_data"}]

    controls = [{   "type" : "hidden",
                    "id" : "update_data"}]

    tabs = ["Plot", "Table"]

    outputs = [{ "type" : "plot",
                    "id" : "plot",
                    "control_id" : "update_data",
                    "tab" : "Plot"},
                { "type" : "table",
                    "id" : "table_id",
                    "control_id" : "update_data",
                    "tab" : "Table",
                    "on_page_load" : True }]

    def getData(self, params):
      """Gets the data from PostgreSQL. 
      Ticker tells which locantion's data you need.
      Based on the laben and the value in the class defined above
      Returns a dataframe"""

        ticker = params['ticker']
        cur.execute("select {} from lyft".format(ticker))
        ly = cur.fetchall()
        cur.execute("select {} from uber".format(ticker))
        ub = cur.fetchall()
        df = pd.concat([pd.DataFrame(ub),pd.DataFrame(ly)], axis = 1)
        df.columns = ["uber","lyft"]
        return df

    def getPlot(self, params):
      """ This function guses the DataFrame created in getData.
      Plots it and assigns the created instance to an object,
      and, retuens that """
      
        df = self.getData(params)
        sns.set_style("darkgrid")
        plt_obj = df.plot()
        plt_obj.set_ylabel("surge")
        plt_obj.set_xlabel("Hour")
        plt_obj.set_title("UBER VS LYFT")
        fig = plt_obj.get_figure()
        return fig

if __name__ == "__main__":

  credentials = yaml.load(open(os.path.expanduser('taxi.yml')))
  conn = psycopg2.connect(database=credentials['postgres_uber'].get('database'), \
      user=credentials['postgres_uber'].get('user'),\
      host =credentials['postgres_uber'].get('host'),\
      port = credentials["postgres_uber"].get("port"),\
      password=credentials['postgres_uber'].get('password'))
  cur = conn.cursor()
  app = StockExample()
  app.launch(host="0.0.0.0",port=5000)

