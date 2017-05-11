# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render_to_response
from couchdb import Server
from django.views.decorators.csrf import csrf_exempt
import re
import geojson
from geojson import Feature, Point, FeatureCollection
import math
# Create your views here.

MONTH = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
MONTH_NUM = ['01','02','03','04','05','06','07','08','09','10','11','12']

def check_month(month):
    return MONTH_NUM[MONTH.index(month)]

@csrf_exempt
def index(request):
    print "in index"
    return render_to_response('couchdocs/index.html')

@csrf_exempt
def senarios(request):
    print request
    print "in senarios"
    url = str(request.get_full_path())
    senarios_num = re.findall(r'.+se+(\d).+',url)
    senarios_num = str(senarios_num[0])
    if senarios_num == '1':
        print "start desc"
        left, right = descartes()
        print "loading success"
        return render_to_response('couchdocs/se1.html',{'left':left,'right':right})
    elif senarios_num == '2':
        print "start loading"
        dates, data, volumns = kline()
        print "loading success"
        return render_to_response('couchdocs/se2.html',{'dates':dates,'data':data,'volumns':volumns})
    elif senarios_num == '3':
        print "start loading pic chart"
        day_of_week, avg_senti = pic_bar()
        print "loading success"
        return render_to_response('couchdocs/se3.html',{"day_of_week":day_of_week,"avg_senti":avg_senti})
    elif senarios_num == '4':
        print "start loading income data"
        total_income, total_senti = dynamic_chart()
        print "loading success"
        return render_to_response('couchdocs/se4.html',{'income':total_income,'senti':total_senti})
    elif senarios_num == '5':
        # print "start loading sport data"
        # income,fitness,sport,outdoor = line_chart_sport()
        return render_to_response('couchdocs/heatmap.html')
    elif senarios_num == '6':
        print 'layer map'
        return render_to_response('couchdocs/layer_map.html')

@csrf_exempt
def senarios_show(request):
    print "in senarios_show !!!!!"
    url = str(request.get_full_path())
    print url
    senarios_num = re.findall(r'.+se+(\d)_.+',url)
    senarios_num = str(senarios_num[0])
    if senarios_num == '1':
        return render_to_response('couchdocs/se1_show/heatmap.html')
    elif senarios_num == '2':
        return render_to_response('couchdocs/se2_show.html')
    elif senarios_num == '3':
        return render_to_response('couchdocs/se3_show.html')
    elif senarios_num == '4':
        return render_to_response('couchdocs/se4_show.html')
    elif senarios_num == '5':
        return render_to_response('couchdocs/se5_show.html')
    else:
        return render_to_response('couchdocs/se6_show.html')

def kline():
    couch = Server('http://admin:123@localhost:15984/')
    db1 = couch['fintwitter']
    db2 = couch['asx_200_show']
    dates = []
    data = []
    senti_sum = []
    senti_quan = []
    senti_date = []
    senti_date_avg = {}
    volumns = []
    # load Index data
    for each in db2:
        date = db2[each].get('date')
        datum = [int(db2[each].get('open')), int(db2[each].get('close')), int(db2[each].get('low')),
                 int(db2[each].get('high'))]
        split_date = str(date).split(' ')
        month_num = check_month(split_date[0])
        dates.append(('2017-' + month_num + '-' + split_date[1]).encode('utf-8'))
        data.append(datum)

    # load sentiment sum by each day
    for each in db1.view('for_frontend/date_senti_value_sum', group=True):
        date = each.key
        split_date = re.split('; |, | |\n', date)
        month_num = check_month(str(split_date[0]))
        senti_date.append(('2017-' + month_num + '-' + split_date[1]).encode('utf-8'))
        senti_sum.append(each.value)
    # load sentiment quantity by each day
    for each in db1.view('for_frontend/date_senti_quan', group=True):
        senti_quan.append(each.value)
    # calculate average sentiment value
    for i in range(len(senti_date)):
        senti_date_avg[senti_date[i]] = int((senti_sum[i] / senti_quan[i])*10000000)
    # assign average sentiment
    for i in range(len(dates)):
        if dates[i] in senti_date_avg:
            data[i].append(senti_date_avg[dates[i]])
            volumns.append(senti_date_avg[dates[i]])
    return dates, data, volumns

def descartes():
    couch = Server('http://admin:123@localhost:15984/')
    db1 = couch['weather_show']
    db2 = couch['geotwitter']
    desc_data_left = []
    desc_data_right = []
    for each in db1:
        desc_single_data = []
        date = db1[each].get('date')
        body_temp = db1[each].get('body_temp')
        date_list = date.split(' ')
        month = int(date_list[0])
        day = int(date_list[1])
        desc_single_data.append(month-1,)
        desc_single_data.append(day-1)
        desc_single_data.append(round(body_temp))
        desc_data_left.append(desc_single_data)

    for each in db2.view("for_frontend/date_sentiment",group = True):
        desc_single_data = []
        month_date = each.key
        senti = each.value
        split_date = month_date.split(' ')
        month = split_date[0]
        month_num = check_month(month)
        if month_num[0] == '0':
            month_num = int(month_num[1])
        else:
            month_num = int(month_num)
        date = split_date[1]
        desc_single_data.append(month_num -1)
        desc_single_data.append(int(date)-1)
        desc_single_data.append(senti)
        desc_data_right.append(desc_single_data)
    count = 0
    for each in db2.view("for_frontend/date_sentiment_count",group = True):
        senti_count = each.value
        senti_avg = desc_data_right[count][2] / float(senti_count)
        desc_data_right[count][2] = round(senti_avg*10)
        count+=1
    return desc_data_left,desc_data_right

def pic_bar():
    couch = Server('http://admin:123@localhost:15984/')
    db1 = couch['geotwitter']
    day_of_week = []
    avg_senti = []
    for each in db1.view("for_frontend/weekday_senti_count",group = True):
        day_of_week.append(str(each.key))
        avg_senti.append(each.value)
    count = 0
    for each in db1.view("for_frontend/weekday_senti_sum",group = True):
        avg_senti[count] = (float(each.value) / avg_senti[count])*1000
        count += 1
    print day_of_week
    print avg_senti
    return day_of_week, avg_senti

def dynamic_chart():
    couch = Server('http://admin:123@localhost:15984/')
    db1 = couch['suburb_data']
    db2 = couch['geotwitter']
    post_income = {}
    post_senti = {}
    postcode = []
    income = []
    senti = []
    total_income = {}
    total_senti = {}
    for each in db1:
        postcode_ = db1[each].get('postcode')
        income_ = db1[each].get('average_income')
        post_income[postcode_] = income_

    for each in db2.view("for_frontend/post_senti_count",group = True):
        post_senti[str(each.key)] = each.value

    for each in db2.view("for_frontend/post_senti", group = True):
        post_senti[str(each.key)] = float(each.value) / post_senti[str(each.key)] *150
    count = 0
    overall_count = 0
    for key in post_income.keys():
        if str(key) in post_senti and post_income[key] != 0 and count <16:
            income.append(post_income[str(key)])
            senti.append(post_senti[str(key)])
            print '********'
            count += 1
        elif count >= 16:
            overall_count += 1
            total_income[overall_count] = income
            total_senti[overall_count] = senti
            income = []
            senti = []
            count = 0
    print total_income
    print total_senti
    return total_income, total_senti

def line_chart_sport():
    couch = Server('http://admin:123@localhost:15984/')
    db1 = couch['suburb_data']
    db2 = couch['geotwitter']
    surburb_name = []
    outdoor = []
    fitness = []
    sports = []
    incomes = []
    for each in db1:
        name = db1[each].get('suburb_name')
        income = db1[each].get('average_income')
        postcode_outdoor = db1[each].get('outdoor')
        postcode_fitness = db1[each].get('fitness')
        postcode_sports = db1[each].get('sports')
        population = db1[each].get('population')
        incomes.append(income)
        if population != 0:
            outdoor.append(postcode_outdoor/float(population)*5000)
            fitness.append(postcode_fitness/float(population)*5000)
            sports.append(postcode_sports/float(population)*5000)
            # surburb_name.append(str(name))
        else:
            outdoor.append(0.0)
            fitness.append(0.0)
            sports.append(0.0)
            # surburb_name.append(str(name))
    print incomes[345:360]
    print fitness[345:360]
    print sports[345:360]
    print outdoor[345:360]
    return incomes[345:360],fitness[345:360],sports[345:360],outdoor[345:360]


def heatmap():
    file = open('static/json/coordinate.geojson','w')
    print 'json file has created'
    couch = Server('http://admin:123@localhost:15984/')
    db1 = couch['twitter_data']
    myfeature_collection = []
    for row in db1.view('test_design/test_view'):
        point_coordinate = row.key
        long = point_coordinate[0]
        lait = point_coordinate[1]
        myfeature_collection.append(Feature(geometry=Point((long, lait))))
    geojson.dump(FeatureCollection(myfeature_collection), file)
    print 'dump success'




