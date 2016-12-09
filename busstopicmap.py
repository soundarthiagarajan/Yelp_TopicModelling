import json
import cPickle as pickle
import csv
import os
from pylab import *

FILE_REVIEW_BID = 'reviews_restaurants.pkl'

data = pickle.load( open( FILE_REVIEW_BID, "rb" ));
f = open( FILE_REVIEW_BID, "rb" );
data = pickle.load(f)
data2 = pickle.load(f)
f.close()

year =['0','2008','2009','2010','2011','2012','2013','2014','2015','2016'];


bussmap ={}

#loop for each topic
for csvfilename in os.listdir("csv/"):
    with open("csv/"+csvfilename, 'rb') as csvfile:
        topicname = csvfilename.split('.')[0];
        windowtopic = csv.reader(csvfile, delimiter=',', quotechar='|')
        globals()[str(topicname)] = {}


        #loop for each year
        for row in windowtopic:
            window = year[int(row[0].split('-')[0])];

            globals()[str(topicname)+str(window)] = {}

            #loop for each word in year
            for j in range(1,len(row)):
                word = row[j];

                for filename in os.listdir("data/2015/"):
                    if word in open("data/2015/"+filename).read():
                        bid = data.get(filename.split('.')[0]);
                        if globals()[str(topicname)+str(window)].get(bid) != None:
                            globals()[str(topicname)+str(window)][bid] += 1;
                        else:
                            globals()[str(topicname)+str(window)][bid] = 1;

            #end word

            globals()[str(topicname)][window+"-"+row[0].split('-')[1]] = globals()[str(topicname)+str(window)]

        #end year

    bussmap[topicname] = globals()[str(topicname)]
#end topic

print bussmap


#loop for each topic
for csvfname in os.listdir("csv/"):

     with open("csv/"+csvfname, 'rb') as csvf:
        tname = csvfname.split('.')[0];
        wintopic = csv.reader(csvf, delimiter=',', quotechar='|')


        #loop for each year
        for r in wintopic:

            win = year[int(r[0].split('-')[0])];

            piechart = bussmap.get(tname).get(win+"-"+r[0].split('-')[1])


            pie([(piechart[k]) for k in piechart], labels=[data2.get(k) for k in piechart],
                autopct='%1.1f%%', shadow=True, startangle=90, colors=('b', 'g', 'r', 'c', 'm', 'y', 'k', 'w','#eeefff','0.75'))

            title('Topic %s for year %s-%s with business percentage'%(tname,win,r[0].split('-')[1]), bbox={'facecolor':'0.8', 'pad':5})
            show()

