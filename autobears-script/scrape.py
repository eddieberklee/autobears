def slugify(s):
    import unicodedata
    import re
    s = unicodedata.normalize('NFKD', s)
    s = s.encode('ascii', 'ignore')
    s = re.sub(r'[^a-zA-Z0-9\-\/,\']+', '+', s)
    s = re.sub(r'\/', '%2f', s)
    s = re.sub(r',', '%2c', s)
    s = re.sub(r'\'', '%27', s)
    s = re.sub(r'[-]+', '-', s)
    # print s
    return s

def enrollment_page(dept):
    import urllib2
    from bs4 import BeautifulSoup
    import re

    year = 13
    term = 'FL'
    deptname = slugify(unicode(dept))

    base_url = 'http://osoc.berkeley.edu/OSOC/osoc?p_term='+term+'&x=75&p_classif=--+Choose+a+Course+Classification+--&p_deptname='+deptname+'&p_presuf=--+Choose+a+Course+Prefix%2fSuffix+--&y=' + str(year)
    # print 'BASE_URL',base_url

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    response = opener.open(base_url)
    html = response.read()
    soup = BeautifulSoup(html)
    return soup

def enrollment_info(dept):
    dept = 'Computer Science'
    soup = enrollment_page(dept)

    tables = soup.find_all('table')
    tables = tables[1:]
    data = {}

    from scrape2 import get_categories
    import datetime
    today = datetime.datetime.today()
    today = today.strftime("master-%m-%d-%Y-%H-%M")
    today_filename = today + '.txt'

    for table in tables:
        course = False
        course_title = False
        location = False
        instructor = False
        last_changed = False
        ccn = False
        units = False
        final_exam = False
        restrictions = False
        note = False
        enrollment = False
        trs = table.find_all('tr')
        if trs:
            for tr in trs:
                tds = tr.find_all('td')
                if str(tds):
                    for td in tds:
                        if td:
                            # TODO: find the "see next results" form post request
                            if course == True:
                                course = td.get_text().strip()
                                data[course] = {}
                            elif course_title == True:
                                course_title = td.get_text().strip()
                                data[course]['course_title'] = course_title
                            elif location == True:
                                location = td.get_text().strip()
                                data[course]['location'] = location
                            elif instructor == True:
                                instructor = td.get_text().strip()
                                data[course]['instructor'] = instructor
                            elif last_changed == True:
                                last_changed = td.get_text().strip()
                                data[course]['last_changed'] = last_changed
                            elif ccn == True:
                                ccn = td.get_text().strip()
                                data[course]['ccn'] = ccn
                            elif units == True:
                                units = td.get_text().strip()
                                data[course]['units'] = units
                            elif final_exam == True:
                                final_exam = td.get_text().strip()
                                data[course]['final_exam'] = final_exam
                            elif restrictions == True:
                                restrictions = td.get_text().strip()
                                data[course]['restrictions'] = restrictions
                            elif note == True:
                                note = td.get_text().strip()
                                data[course]['note'] = note
                            elif enrollment == True:
                                enrollment = td.get_text().strip()
                                data[course]['enrollment'] = enrollment

                            try:
                                td = td.find('font').find('b').get_text()
                                if td.startswith('Course:'):
                                    course = True
                                elif td.startswith('Course Title:'):
                                    course_title = True
                                elif td.startswith('Location:'):
                                    location = True
                                elif td.startswith('Instructor:'):
                                    instructor = True
                                elif td.startswith('Status/Last Changed:'):
                                    last_changed = True
                                elif td.startswith('Course Control Number:'):
                                    ccn = True
                                elif td.startswith('Units/Credit:'):
                                    units = True
                                elif td.startswith('Final Exam Group:'):
                                    final_exam = True
                                elif td.startswith('Restrictions:'):
                                    restrictions = True
                                elif td.startswith('Note:'):
                                    note = True
                                elif td.startswith('Enrollment on '):
                                    enrollment = True
                            except:
                                pass


def total_count(dept):
    soup = enrollment_page(dept)

    first_table = soup.find_all('table')[0]
    second_tr = first_table.find_all('tr')[1]
    num_matches = second_tr.get_text()
    num_matches = num_matches.split("\n")
    for i in num_matches:
        if i.startswith('Displaying'):
            num_matches = i
            break
        elif i.startswith('No classes match your request'):
            num_matches = None
            break
        elif i.startswith('Information about courses'):
            return -1 # Information about courses are on an external site
            # TODO: actually scrape the other page that is linked
    if not num_matches:
        return 0
    # print 'num_matches', num_matches
    m = re.search('Displaying ([\d]+)-([\d]+) of ([\d]+)', num_matches)
    if m:
        # print m.group(0),m.group(1),m.group(2),m.group(3)
        num_matches = m.group(3)
        num_matches = int(num_matches)
    if not m:
        # if m doesn't match that means it only has 1 class: "Displaying 1 match to your request..."
        m = re.search('Displaying 1', num_matches)
        if m:
            return 1

    return num_matches

def save_all_classifications():
    from scrape2 import get_categories
    import datetime
    today = datetime.datetime.today()
    today = today.strftime("classif-%m-%d-%Y-%H-%M")
    today_filename = today + '.txt'
    f = open(today_filename, 'w')

    categories = get_categories()

    # TODO: Finish this method

def save_all_dept():
    from scrape2 import get_type
    import datetime
    today = datetime.datetime.today()
    today = today.strftime("dept-%m-%d-%Y-%H-%M")
    today_filename = today + '.txt'
    f = open(today_filename, 'w')

    dept_names = get_type('Department Name')
    sum = 0
    for dept in dept_names:
        # print type(dept)
        # print '-',dept,'-'
        # print dept, ':', total_count(unicode(dept))
        print "%s : %d" % (dept, total_count(unicode(dept)))
        f.write("%s : %d\n" % (dept, total_count(unicode(dept))))
        sum += int(total_count(unicode(dept)))

    f.close()



def total_from_dept(filename):
    f = open(filename, 'r')
    sum = 0
    for line in f:
        import re
        m = re.search(': ([\d]+)', line)
        if m:
            count = int(m.group(1))
            sum += count
    # print 'TOTAL:',sum
    f.close()
    return sum

def scrape_all():
    from scrape2 import get_type
    import datetime
    today = datetime.datetime.today()
    today = today.strftime("all-%m-%d-%Y-%H-%M")
    today_filename = today + '.txt'
    f = open(today_filename, 'w')

    dept_names = get_type('Department Name')
    sum = 0
    for dept in dept_names:
        print enrollment_info(unicode(dept))

if __name__ == '__main__':
    # print total_from_dept('dept-08-28-2013-12-55.txt')

    # import urllib
    # params = urllib.urlencode({
    #     'bookstore_id-1':'554',
    #     'term_id-1':'2013D',
    #     'div-1':'',
    #     'crn-1':'26103',
    #     '_InField1':'RESTRIC',
    #     '_InField2':'26103',
    #     '_InField3':'13D2',
    # })
    # import requests
    # url = 'https://telebears.berkeley.edu/enrollment-osoc/osc'
    # resp = requests.post(url, params=params, allow_redirects=True)
    # print resp.__dict__
    # print resp.text

    scrape_all()

# TODO: Brainstorm ideas for how to make this code more extendable.
#       More generalized and more modularized.


# tr = first_table.find_all('tbody')[0].find_all('tr')[1]
# print tr
# depttotal = soup.find_all('font')
# print depttotal
















