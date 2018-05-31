# -*- coding: utf-8 -*-
from functions import *
import json
import io
import os
import codecs

def generatePostpaidJsonObject(data, date, parentnodedescList,
                               parentusagecount, parenthangupcount,
                               parentagentcount, parentdisconnectcount):
    ivrtreeobject = ivrtree('', '', '', '', '', '', '', '', '', '', [], '', '')
    ivrtreeobject.modulename = data.values()[2]
    ivrtreeobject.nodedesctag = data.values()[1]
    mynodedesclist = parentnodedescList
    mynodedesclist.append(ivrtreeobject.nodedesctag)

    ivrtreeobject.totalcall = querybuilder('', mynodedesclist, date)
    ivrtreeobject.totalagent = querybuilder('AGENT', mynodedesclist, date)
    ivrtreeobject.totalhangup = querybuilder('HANGUP', mynodedesclist, date)
    ivrtreeobject.totaldisconnect = querybuilder('DISCONNECT', mynodedesclist, date)

    try:
        ivrtreeobject.totalperc = float(ivrtreeobject.totalcall) / float(parentusagecount) * 100
    except ZeroDivisionError:
        print('Sıfıra Bölme Hatası TOTAL: ')
        ivrtreeobject.totalperc = 0

    try:
        ivrtreeobject.agentperc = float(ivrtreeobject.totalagent) / float(parentagentcount) * 100
    except ZeroDivisionError:
        print('Sıfıra Bölme Hatası AGENT : ')
        ivrtreeobject.agentperc = 0

    try:
        ivrtreeobject.hangupperc = float(ivrtreeobject.totalhangup) / float(parenthangupcount) * 100
    except ZeroDivisionError:
        print('Sıfıra Bölme Hatası HANGUP : ')
        ivrtreeobject.hangupperc = 0

    try:
        ivrtreeobject.disconnectperc = float(ivrtreeobject.totaldisconnect) / float(parentdisconnectcount) * 100
    except ZeroDivisionError:
        print('Sıfıra Bölme Hatası DISCONNECT : ')
        ivrtreeobject.disconnectperc = 0

    ivrtreeobject.dtmf = data.values()[3]
    ivrtreeobject.beginddate = date
    ivrtreeobject.enddate = ''

    for d in data.values()[0]:
        ivrtreeobject.details.append(generatePostpaidJsonObject(d, date, mynodedesclist, ivrtreeobject.totalcall,
                                                                ivrtreeobject.totalhangup, ivrtreeobject.totalagent,
                                                                ivrtreeobject.totaldisconnect))

    mynodedesclist.pop()
    """
    print(ivrtreeobject.totalperc)
    """
    return ivrtreeobject


def invokedfiletojson(gelendata, date,typeof):
    seriliazedencodeddata = MyEncoder().encode(gelendata)
    parsed = json.loads(seriliazedencodeddata)
    parsed = json.dumps(parsed, indent=4, ensure_ascii=False)
    print('Creating a new file')
   #degistir
    path = "/Users/oredata/Desktop/tree-"+typeof+"-outputs"
    #degistir
    name = '/' + date + '-'+typeof+'.json'  # Name of text file coerced with +.txt

    with io.open(path + name, 'w', encoding='utf-8')  as f:
        print('dosya yazdırılıyor : ' + path + name)
        f.write(parsed)


def startAnalytics(typeof,date):
    #degistir
    with io.open('/Users/oredata/Desktop/tree-'+typeof+'.json', encoding='utf-8') as f:
        data = json.load(f, encoding='utf-8')
    allcallcount = querybuilder("", [], date)
    callagentcount = querybuilder('AGENT', [], date)
    callhangupcount = querybuilder('HANGUP', [], date)
    calldisconnectcount = querybuilder('DISCONNECT', [], date)

    invokedfiletojson(
        generatePostpaidJsonObject(data, date, [], allcallcount, callhangupcount, callagentcount, calldisconnectcount),
        date,typeof)


def analyzereport(typeof,date):
    with io.open('/Users/oredata/Desktop/raporlama_input-'+typeof+'.json', encoding='utf-8') as f:
        data = json.load(f, encoding='utf-8')

    rootdirectory = data.get('category')

    colorlist = ["color:green","color:red","color:yellow","color:blue","color:lightgray","color:purple","color:pink","color:darkblue","color:orange"]
    mainpath = r'/Users/oredata/Desktop/'+typeof+'-raporlar-outputs/'

    if not os.path.exists(mainpath+date+'-'+typeof+'-raporlari/'):
        os.makedirs(mainpath+date+'-'+typeof+'-raporlari/')

    mainpath = mainpath+date+'-'+typeof+'-raporlari/'

    rootdirectorypathname = mainpath + rootdirectory + '/'
    if not os.path.exists(rootdirectorypathname):
        os.makedirs(rootdirectorypathname)

    # burada root directory dizini oluşturulacak.
    for sc in data.get('subcategories'):
        subdirectory = sc.get('subcategoryname')
        subdirectorypathname = rootdirectorypathname + subdirectory
        if not os.path.exists(subdirectorypathname + '/'):
            os.makedirs(subdirectorypathname)
        # burada subdirectory oluşturulacak.
        for reports in sc.get('reports'):
            myreporttree = reporttree('', '', '', {}, [])
            nodedesclist = []
            filename = reports.get('reportname')
            myreporttree.options['title'] = filename
            myreporttree.title = filename

            myreporttree.type = reports.get('type')
            #opsiyonel olacak.
            if reports.get('type') == 'column':
                myreporttree.data = [["DTMF", "Process", {"role": "style"}]]
            else:
                myreporttree.data = [["Report", "Process"]]
            filenamepath = subdirectorypathname +'/' + filename


            result = reports.get('result')
            nodedesc=reports.get('nodedesc')
            if(len(nodedesc)>0):
                nodedesclist.append(nodedesc)
            divider = querybuilder(result,nodedesclist,date)
            counter = 0
            for piece in reports.get('pieces'):
                datalist = []

                piecenodedesclist = []
                piecename = piece.get('piecename')
                pieceresult = piece.get('result')

                piecenodedesc = piece.get('nodedesc')
                if (len(piecenodedesc) > 0):
                    piecenodedesclist.append(piecenodedesc)
                divident = querybuilder(pieceresult,piecenodedesclist,date)
                ratio = float(divident)/ float(divider)* 100
                if reports.get('type') == 'column':
                    datalist.append(piecename)
                    datalist.append(ratio)
                    datalist.append(colorlist[counter])
                else:
                    datalist.append(piecename)
                    datalist.append(ratio)
                myreporttree.data.append(datalist)
                counter+=1

            seriliazedencodeddata = MyEncoder().encode(myreporttree)
            parsed = json.loads(seriliazedencodeddata)
            parsed = json.dumps(parsed, indent=4, ensure_ascii=False)
            with codecs.open(filenamepath+'.json', 'w', encoding='utf-8')  as f:
                f.write(parsed)


mydatelistpostpaid = ['2018-05-06','2018-05-07','2018-05-08','2018-05-09','2018-05-10','2018-05-11','2018-05-12']
mydatelistprepaid = ['2018-05-09','2018-05-10','2018-05-11','2018-05-12']

for date in mydatelistprepaid:
    analyzereport('prepaid',date)
    #startAnalytics('prepaid',date)
