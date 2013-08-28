from scrape2 import get_categories

def slugify(s):
    import unicodedata
    import re
    s = unicodedata.normalize('NFKD', s)
    s = s.encode('ascii', 'ignore')
    s = re.sub(r'[^a-zA-Z0-9\-\/]+', '+', s)
    s = re.sub(r'\/', '%2f', s)
    s = re.sub(r'[-]+', '-', s)
    print s
    return s

def total_count(dept):
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
    if not num_matches:
        return 0
    print num_matches
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


if __name__ == '__main__':
    categories = get_categories()
    dept_names = categories['Department Name']
    dept_names = dept_names[20:]
    # print dept_names
    for dept in dept_names:
        print type(dept)
        print '-',dept,'-'
        print dept, ':', total_count(unicode(dept))

# TODO: Brainstorm ideas for how to make this code more extendable.
#       More generalized and more modularized.


# tr = first_table.find_all('tbody')[0].find_all('tr')[1]
# print tr
# depttotal = soup.find_all('font')
# print depttotal
















