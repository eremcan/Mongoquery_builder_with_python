# -*- coding: utf-8 -*-
import ast
import dateutil.parser
# noinspection PyUnresolvedReferences
from classes import *
from pymongo import MongoClient

client = MongoClient('localhost', 27017)  # 27017 is the default port number for mongodb
db = client.BilgeDb
#degistir
bilge = db.PostpaidIVR


def querynodedescbuilder(nodedesclist):

    length = len(nodedesclist)
    if (length > 1):
        result = " , '$and':["
        orresult = " {'$or':["
        andresult = " {'$and':["
        idx = 0
        for item in nodedesclist:
            idx = idx + 1
            if '||' in item:
                splittednodes = item.split('||')
                splittednodeslen = len(splittednodes)
                orcount = 0
                for nodes in splittednodes:
                    orcount+=1
                    item2 = nodes.strip()
                    isNot = False
                    if item2.startswith('!!'):
                        isNot = True
                    if isNot == False:
                        orresult += "{'node_desc_list' : "
                        orresult = orresult + "'"
                        orresult += item2
                        orresult += "'}"
                    else:
                        orresult += "{'node_desc_list' : "
                        orresult = orresult + "{'$nin' : ['"
                        orresult = orresult + item2.replace('!!', '')
                        orresult = orresult + "']}"
                        orresult += "}"

                    if (orcount < splittednodeslen):
                        orresult += ','
                    else:
                        orresult += ']}'
                result = result + orresult


            elif '&&' in item:
                splittednodes = item.split('&&')
                splittednodeslen = len(splittednodes)
                andcount = 0
                for nodes in splittednodes:
                    andcount+=1
                    item2 = nodes.strip()
                    isNot = False
                    if item2.startswith('!!'):
                        isNot = True
                    if isNot == False:
                        andresult += "{\"node_desc_list\" : "
                        andresult = andresult + "\""
                        andresult += item2
                        andresult += "\"}"
                    else:
                        andresult += "{\"node_desc_list\" : "
                        andresult = andresult + "{\"$nin\" : [\""
                        andresult = andresult + item2.replace('!!', '')
                        andresult = andresult + "\"]}"
                        andresult += "}"
                    if (andcount < splittednodeslen):
                        andresult += ','
                    else:
                        andresult += ']}'
                result = result + andresult

            elif(', MT Transfer' in item):
                result += "{'node_desc' : { '$regex' : '"
                result += item
                result += "' }}"

            else:
                isNot = False
                if item.startswith('!!'):
                    isNot = True

                if isNot == False:
                    result = result + "{'node_desc_list' : "
                    result = result + "'"
                    result = result + item
                    result = result + "'}"
                else:
                    result = result + "{'node_desc_list' : "
                    result = result + "{'$nin' : ['"
                    result = result + item.replace('!!', '')
                    result = result + "']}"
                    result = result + "}"


            if (idx < length):
                result = result + ','
        result +=  ']'
        return  result

    elif len(nodedesclist) == 1:
        if (', MT Transfer' in nodedesclist[0]):
            result = " , 'node_desc' : { '$regex' : '"
            result += nodedesclist[0]
            result += "' }"

        elif ('&&' in nodedesclist[0]):
            andresult = " , '$and':["

            splittednodes = nodedesclist[0].split('&&')
            splittednodeslen = len(splittednodes)
            andcount = 0
            for nodes in splittednodes:
                andcount += 1
                item2 = nodes.strip()
                isNot = False
                if item2.startswith('!!'):
                    isNot = True
                if isNot == False:
                    andresult += "{\"node_desc_list\" : "
                    andresult = andresult + "\""
                    andresult += item2
                    andresult += "\"}"
                else:
                    andresult += "{\"node_desc_list\" : "
                    andresult = andresult + "{\"$nin\" : [\""
                    andresult = andresult + item2.replace('!!', '')
                    andresult = andresult + "\"]}"
                    andresult += "}"
                if (andcount < splittednodeslen):
                    andresult += ','
                else:
                    andresult += ']'
            return andresult

        else:
            result = " , 'node_desc_list' : '" + nodedesclist[0] + "'"
        return result

    elif len(nodedesclist) == 0:
        return ''

    else:
        return "hata"


def querybuilder(resultType, nodedesclist, date):
    querystring = '{'
    querystring = querystring + "'date': '" + date + "'"

    if (resultType != ""):
        querystring = querystring + " , 'result': '" + resultType + "'"

    querystring = querystring + querynodedescbuilder(nodedesclist)
    querystring+="}"
    print(querystring + '\n')
    dateformat = dateutil.parser.parse(date)
    querydict = ast.literal_eval(querystring)
    querydict['date'] = dateformat

    return bilge.find(querydict).count()




def bilgeMongoDbQuery(properties, **kwargs):
    if (properties == 'findbymultiplenode_desc_and_date'):
        print('dyr')
   # querystring = config.get('DatabaseSection', properties)
    querystring = 'a'

    if 'node_desc' in kwargs:
        querystring = querystring.replace('%%node_desc%%', kwargs['node_desc'])

    elif 'node_desc_arg6' in kwargs:
        querystring = querystring.replace('%%node_desc_arg1%%', kwargs['node_desc_arg1']).replace('%%node_desc_arg2%%',
            kwargs['node_desc_arg2']).replace('%%node_desc_arg3%%', kwargs['node_desc_arg3']).replace('%%node_desc_arg4%%',
            kwargs['node_desc_arg4']).replace('%%node_desc_arg5%%', kwargs['node_desc_arg5']).replace('%%node_desc_arg6%%',kwargs['node_desc_arg6'])

    elif 'node_desc_arg5' in kwargs:
        querystring = querystring.replace('%%node_desc_arg1%%', kwargs['node_desc_arg1']).replace('%%node_desc_arg2%%',
            kwargs['node_desc_arg2']).replace('%%node_desc_arg3%%', kwargs['node_desc_arg3']).replace('%%node_desc_arg4%%',
            kwargs['node_desc_arg4']).replace('%%node_desc_arg5%%', kwargs['node_desc_arg5'])

    elif 'node_desc_arg4' in kwargs:
        querystring = querystring.replace('%%node_desc_arg1%%', kwargs['node_desc_arg1']).replace('%%node_desc_arg2%%',
            kwargs['node_desc_arg2']).replace('%%node_desc_arg3%%', kwargs['node_desc_arg3']).replace('%%node_desc_arg4%%',
            kwargs['node_desc_arg4'])

    elif 'node_desc_arg3' in kwargs:
        querystring = querystring.replace('%%node_desc_arg1%%', kwargs['node_desc_arg1']).replace('%%node_desc_arg2%%',
            kwargs['node_desc_arg2']).replace('%%node_desc_arg3%%', kwargs['node_desc_arg3'])



    elif 'node_desc_arg2' in kwargs:
        querystring = querystring.replace('%%node_desc_arg1%%', kwargs['node_desc_arg1']).replace('%%node_desc_arg2%%',
            kwargs['node_desc_arg2'])

    else:
        print('else e düştük')

    if 'node_desc_nin' in kwargs:
        querystring = querystring.replace('%%node_desc_nin%%', kwargs['node_desc_nin'])

    if 'result' in kwargs:
        querystring = querystring.replace('%%result%%', kwargs['result'])

    if 'date' in kwargs:
        dateformat = dateutil.parser.parse(kwargs['date'])
        querystring = querystring.replace('%%date%%', kwargs['date'])
        querydict = ast.literal_eval(querystring)
        querydict['date'] = dateformat
        return bilge.find(querydict).count()



    elif 'date_gte' in kwargs:
        gtedateformat = dateutil.parser.parse(kwargs['date_gte'])
        ltdateformat = dateutil.parser.parse(kwargs['date_lt'])
        querystring = querystring.replace('%%date_gte%%', kwargs['date_gte']).replace('%%date_lt%%', kwargs['date_lt'])
        querydict = ast.literal_eval(querystring)
        querydict['date']['$gte'] = gtedateformat
        querydict['date']['$lt'] = ltdateformat
        return bilge.find(querydict).count()


    else:
        querydict = ast.literal_eval(querystring)
        return bilge.find(querydict).count()




