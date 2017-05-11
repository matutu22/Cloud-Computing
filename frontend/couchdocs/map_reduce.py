import couchdb
import re
MONTH = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
MONTH_NUM = ['01','02','03','04','05','06','07','08','09','10','11','12']
couch = couchdb.Server('http://admin:123@localhost:15984/')
db1 = couch['suburb_data']
db2 = couch['geotwitter']
post_income = {}
post_senti = {}
# for each in db1:
#     postcode = db1[each].get('postcode')
#     income = db1[each].get('average_income')
#     post_income[postcode] = income

for each in db2.view("for_frontend/post_senti_count",group = True):
    # print each.key+':'+str(each.value)
    post_senti[str(each.key)] = each.value

for each in db2.view("for_frontend/post_senti", group = True):
    # print each.key+':'+str(each.value)
    post_senti[str(each.key)] = float(each.value) / post_senti[each.key]
print post_senti
