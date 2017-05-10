import couchdb
import json
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import json
import matplotlib.path as mplPath
import numpy as np
import requests
#sudo apt-get install python-tk
with open ('polygon.json') as data_file:
    polygon=json.load(data_file)
with open ('income.json') as income_file:
	income=json.load(income_file)
with open ('population.json') as population_file:
	polulation=json.load(population_file)




couch = couchdb.Server('http://127.0.0.1:5984')
db = couch['suburb_data']

for a in polygon['features']:
    sa2_id = 0
    total_population = 0
    average_income = 0
    postcode=str(a['properties']['postcode'].encode('ascii'))

    url = 'http://v0.postcodeapi.com.au/suburbs/%s.json' % (postcode)
    headers = {'Accept': 'application/json'}
    response = requests.get(url, headers=headers)
    data = [] 
    # set a default value, if you want
    try:
        if response.status_code == 200:    
            data = json.loads(response.text)
            suburb_name = data[0]['name']
            print "Get suburb name"
        else:    
            print "no data"
    except:
        pass

    for b in polulation['features']:
        sa2_name = str(b['properties']['sa2_name11'].encode('ascii')).replace("-","")
        if suburb_name.lower() in sa2_name.lower():
            total_population = b['properties']['erp_p_20']
            sa2_id = int(b['properties']['sa2_main11'])
            break
        
    print "Get population"

    for c in income['features']:
        d = c['properties']
        total_income = 0
        if sa2_id == int(d['SA2_MAIN11']):
            total_income = int(d['P_1000_1249_Tot'])*1125 + int(d['P_1250_1499_Tot'])*1375 + int(d['P_1500_1999_Tot'])*1750 + int(d['P_1_199_Tot'])*100 +int(d['P_2000_more_Tot'])*2250 + int(d['P_200_299_Tot'])*250 +int(d['P_300_399_Tot'])*350 + int(d['P_400_599_Tot'])*500+int(d['P_600_799_Tot'])*700 + int(d['P_800_999_Tot'])*900
            
            if int(d['P_Tot_Tot'])-int(d['P_PI_NS_ns_Tot']) != 0:
                average_income = total_income/(int(d['P_Tot_Tot'])-int(d['P_PI_NS_ns_Tot']))
            break
        
    print "Get income"

    data ={'sa2_id':sa2_id, 'postcode':postcode, 
       'suburb_name':suburb_name, 'average_income':average_income, 
       'population':total_population, 'result_brunch':0}
    db[postcode]=data
    print "Save data"