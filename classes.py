from json import JSONEncoder

class ivrtree:
    modulename = ''
    nodedesctag = ''
    totalcall = ''
    totalagent = ''
    totalhangup = ''
    totaldisconnect = ''
    totalperc = ''
    agentperc = ''
    hangupperc = ''
    disconnectperc = ''
    dtmf = ''
    details = []
    beginddate = ''
    enddate = ''

    def __init__(self, modulename, nodedesctag, totalcall, totalagent, totalhangup,totaldisconnect, totalperc, agentperc,
                 disconnectperc, dtmf, details, beginddate, enddate):
        self.modulename = modulename
        self.nodedesctag = nodedesctag
        self.totalcall = totalcall
        self.totalagent = totalagent
        self.totalhangup = totalhangup
        self.totaldisconnect = totaldisconnect
        self.totalperc = totalperc
        self.agentperc = agentperc
        self.disconnectperc = disconnectperc
        self.dtmf = dtmf
        self.details = details
        self.beginddate = beginddate
        self.enddate = enddate

class reporttree:
    title = ''
    image = ''
    type = ''
    options = {}
    data = []

    def __init__(self,title,image,type,options,data):
        self.title = title
        self.image = image
        self.type = type
        self.options = options
        self.data = data


class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
