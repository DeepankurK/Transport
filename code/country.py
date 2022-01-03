import pandas as pd
from geopy.geocoders import Nominatim
from geopy.geocoders import Photon
import sys
from csv import DictWriter

df=pd.read_csv("./Data_departure.csv")
d=0 if len(sys.argv)!=2 else sys.argv[1]
with open('Data_departure2.csv','a+') as file:
    writer_object = DictWriter(file,fieldnames=["POI"])
    for j in range(int(d),len(df['POI'])):
        geo=Photon(user_agent=str(j)+df.loc[j,'POI']+str(j))
        location=geo.geocode(df.loc[j,'POI'])
        if 'United States' in location.address.split(',')[-1]:
            writer_object.writerow({"POI":0})
        else:
            writer_object.writerow({"POI":1})
        print(j,len(df))
