#import dependencies
from flask import Flask,render_template,jsonify
import pandas as pd
import numpy as np

# create instance of Flask app
app = Flask(__name__)

#create index route
@app.route("/")
def index():
    return render_template('index.html')

    #create names route
@app.route("/names")
def names():
    df_names= pd.read_csv("DataSets/belly_button_biodiversity_samples.csv")
    
    #create an empty list for sample IDs
    nameList= []
    for name in df_names.columns[1:]:
        nameList.append(name)
        nameList=nameList
        return jsonify(nameList)
    
    return render_template("index.html", nameList=jsonify(nameList))

    #create otu route
@app.route("/otu")
def otuFunc():
    df_otu=pd.read_csv("DataSets/belly_button_biodiversity_otu_id.csv")
    
    #create an empty list for otus
    otuList=[]
    for otuDesc in df_otu["lowest_taxonomic_unit_found"]:
        otuList.append(otuDesc)
        return jsonify(otuList)
    
    return render_template("index.html", otuDescription=jsonify(otuList))

#create metadata sample route
@app.route("/metadata/sample")
def metasample():
    df_metadata = pd.read_csv("DataSets/Belly_Button_Biodiversity_Metadata.csv")
    
    df_metadata["SAMPLEID"]= "BB_" + df_metadata["SAMPLEID"].astype(str)
    
    df_metadata = df_metadata[['AGE','BBTYPE','ETHNICITY','GENDER','LOCATION','SAMPLEID']]
    
    json_metadata= df_metadata.to_json(orient='records')
    
    return json_metadata

    return render_template("index.html", metaSampleData=jsonify(json_metadata))
#create wfreq sample route    
@app.route("/wfreq/sample")
def wfreqsample():
    df_metadata = pd.read_csv("DataSets/Belly_Button_Biodiversity_Metadata.csv")
    df_metadata["SAMPLEID"]= "BB_" + df_metadata["SAMPLEID"].astype(str) 
    df_metadata_wfreq = df_metadata[['SAMPLEID', 'WFREQ']]
    df_metadata_wfreq= df_metadata_wfreq.fillna(0)
    df_metadata_wfreq= df_metadata_wfreq.to_json(orient='records')
    return df_metadata_wfreq

    return render_template("index.html", metaSampleWFREQ=jsonify(df_metadata_wfreq))

## route for pie and bubble plot --------------------------------------------------------------------------------------------------
@app.route("/sample/plot/pie") 
def DictSortedSampleValues():

     df_Biodiversity = pd.read_csv('DataSets/belly_button_biodiversity_samples.csv')

     df_otu = pd.read_csv("DataSets/belly_button_biodiversity_otu_id.csv")
     df_Biodiversity_merge = df_Biodiversity.merge(df_otu, on=['otu_id'],how='outer')
     df_Biodiversity_merge["Total"] = df_Biodiversity_merge.iloc[::,1:].sum(axis=1)
     df_Biodiversity_sorted=df_Biodiversity_merge[['otu_id','lowest_taxonomic_unit_found', 'Total']]
     df_Biodiversity_sorted = df_Biodiversity_sorted.sort_values(by=['Total'],ascending=False).head(10)
     return df_Biodiversity_sorted.to_json(orient='records')
 
     samplePIECHART = DictSortedSampleValues()


     return render_template("index.html", samplePIE = jsonify(samplePIECHART))


if __name__ == "__main__":
 app.run(debug=True)


            