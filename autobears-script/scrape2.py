def get_categories():
    category = 'Department Name'
    categories = get_type(category)
    return categories

def get_type(category):
    # Saves everything to a hash but only returns the type you requested,
    # by supplying the input type as a key to the hash.
    import urllib2
    from bs4 import BeautifulSoup

    base_url = 'http://schedule.berkeley.edu/srchfall.html' 
    # print 'BASE_URL',base_url

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    response = opener.open(base_url)
    html = response.read()
    soup = BeautifulSoup(html)

    table = soup.find('table')
    trs = table.find_all('tr')
    types = {}
    for tr in trs:
        tds = tr.find_all('td')
        counter = 0
        for td in tds:
            if td:
                if counter == 0:
                    category_title = td.get_text().strip()
                    # print 'CATEGORY_TITLE',category_title
                elif counter == 1:
                    if category_title == 'Department Name':
                        dept_names = td.find_all('option')
                        dept_names = map(lambda d:d.get_text(), dept_names)
                        dept_names = dept_names[1:]
                        types[category_title] = dept_names
                    else:
                        category_options = td.get_text().strip()
                        # print 'CATEGORY_OPTIONS',category_options
                        types[category_title] = category_options
            counter += 1
    return types[category]

# categories = get_categories()
# print categories['Department Name']









