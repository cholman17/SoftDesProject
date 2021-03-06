''' fetches course listings and places into txt file '''
import urllib2
from bs4 import BeautifulSoup
import re
import csv
from itertools import izip
from itertools import groupby

from audit import * #don't think this is needed
from creatingwebsite import * #not needed either
from courseobjects import *
from courseobjects import Course
from getstress import *
#from getstress import matching

#Should make all one object class (Information)?
#def __init__(self): pass
#def getCourseInfo(....):

base_url = "https://fusionmx.babson.edu/CourseListing/index.cfm?fuseaction=CourseListing.DisplayCourseListing&blnShowHeader=false&program=Undergraduate&semester=Spring+2017&sort_by=course_number&btnSubmit=Display+Courses"
page = urllib2.urlopen(base_url)
soup = BeautifulSoup(page, "lxml")

#leftovers = thefile.read().split() #['ACC1000', 'FME1000', 'CVA2034', 'ECN2000'] #change to open(file_reqs)

#print soup.prettify()
courseNum = []
courseSect = []
courseTitle = []
courseDay = []
courseStart = []
courseEnd = []
courseProf = []
courseCredits = []
courseStress = []
allCourses = []

matched = []
leftovers = []

def getCourseInfo():
    filename = "courseListing.txt"
    thefile = open("remaining.txt","r")
    f = open(filename,"w")

    tables = soup.findChildren('table')
    courseListing = tables[1]
    rows = courseListing.findChildren('tr', {"valign" : "top"})

    for row in rows: #should be all rows
        hits = []
        for hit in row.findChildren('td', {"width": "85"}):
            #print hit.contents[0].strip()
            Num = hit.contents[0].strip()
            Num = Num.split('-')
            Numb = Num[0]
            Sect = Num[1]
            courseNum.append(Numb)
            #print Numb
            courseSect.append(Sect)
            #print Sect
        for hit in row.findChildren('td', {"width": "250"}):
            #print hit.contents[0].text
            Title = hit.contents[0].text
            courseTitle.append(Title)
        hits = row.findChildren('td', {"width": "140"})
        #print hits[0].text
        sched = hits[0].text.strip() #contents[0].strip() #time, day, professor
        dates = re.split(r'\s{2,}', sched)
        day = dates[0]
        day = day.replace(" ","")
        #except (IndexError, TypeError, ValueError):
            #day = str("N?A")
        try:
            time = dates[1].replace(" ","")
            time = time.split('-')
            startTime = time[0]
            endTime = time[1]
        except (IndexError, TypeError, ValueError):
            time = str("")

        courseDay.append(day)
        courseStart.append(startTime)
        courseEnd.append(endTime)

        '''print '\n******************'
        print Num, Sect
        print day, time
        print '******************\n' '''

        #print hits[1].contents[0].strip()
        prof = hits[1].text.strip() #contents[0].strip()
        prof = prof.replace(r'\s{2,}',"")
        courseProf.append(prof)
        info = str(Numb)+"   "+str(Sect)+"   "+str(Title)+"  "+str(day)+"    "+str(startTime)+"   "+str(endTime)+"   "+str(prof)+"   "
        f.write(str(info)+'\n')

    f.close()
    for x in courseNum:
        a = getstress.matching(x)
        courseStress.append(a)
    print '+++++++ ADD STRESS ++++++++++'
    print len(courseStress)

    FILE = open("AllCourses.csv", "w")
    for i in xrange(len(courseNum)):
        FILE.write("{};{};{};{};{};{};{};{}'\n".format(courseNum[i],courseSect[i],courseTitle[i],courseDay[i],courseStart[i],courseEnd[i],courseProf[i], courseStress[i]))
    FILE.close

    for x in range(len(courseNum)):
        #print '+++++++++++ NEW ++++++++++++++++'
        allCourses.append( Course(courseNum[x],courseSect[x],courseTitle[x], courseDay[x], courseStart[x], courseEnd[x], courseProf[x], courseStress[i]) )
    print 'Made course objects'
    print len(allCourses)
    print allCourses[:3]

#filter.fnmatch(names, pattern) #comparinng codes to courseList
#iterate for the each/length of classes leftover
#matches = [] #list of section lists
def findMatch(reqs):

    charstoremove = ['[',']','.','"','?','!']
    for code in reqs: #iterate for each requirement
        ##new = code.translate(None,''.join(charstoremove)
        results = filter(lambda x:str(code) in x.num, allCourses)
        if results:
            print '\n Found %s section(s) for course: %s' % (len(results), code)
            matched.append(results)
            '''for item in results:
                print 'ITEMS +++++++++++++++++'
                print item.num+item.sect'''

    #for x in range(len(matched)):
            #print matched[x]

    return matched

def filtering(b,c): # the list, attribute, criteria
    #search through list of objects to group sections together
    '''b = raw_input('What do you want to filter by: num, title, day, time, prof? ')
    c = raw_input('What is the criteria?: ')'''
    #d = [] #list of section lists
    #for x in xrange(len(a)):
    b = str(b)
    try:
        results = filter(lambda x:str(c) in getattr(x,b), allCourses)
        print 'Found %s classes for %s: %s' % (len(results), b, c)
        res = [list(g) for k, g in groupby(results, key=lambda x: x.num[:7])]
        if not results:
            res = ""
    except NameError:
        print 'Wrong property! Try again.'
        #d.append(results)
    #return results
    return res

def refresh():
    courseNum[:] = []
    courseSect[:] = []
    courseTitle[:] = []
    courseDay[:] = []
    courseStart[:] = []
    courseEnd[:] = []
    courseProf[:] = []
    courseCredits[:] = []
    allCourses[:] = []

    matched[:] = []
    leftovers[:] = []

def fetchAll(b,c):
    refresh()
    thefile = open("remaining.txt","r")
    leftovers = thefile.read().split()
    print len(leftovers)

    match = [] #pulled down
    filters = []
    allThings= []
    elseThings = []

    getCourseInfo()

    findMatch(leftovers)
    match = findMatch(leftovers)
    allThings.append(match)

    print '__________ MATCHES FOUND _____________'
    #for code in match:
        #print code

    filtering(b,c)
    filters = filtering(b,c)
    elseThings.append(filters)
    print '_____________ FILTERS FOUND ____________'
    print len(filters)

    everything = []
    everything.append(allThings)
    everything.append(elseThings)

    print type(everything)
    return everything
