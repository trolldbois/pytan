def formtodict(form):
    formdict = {}
    for k in form.keys():
        if type(form[k]) == list:
            formdict[k] = form.getlist(k)
        else:
            formdict[k] = form[k].value
    return formdict


def print_html(html):
    print "Content-Type: text/html; charset=UTF-8\n"
    print html


def dictify_resultset(rs):
    return [dictify_resultset_row(x) for x in rs.rows]


def dictify_resultset_row(rs_row):
    d = dict(zip(
        [x.display_name for x in rs_row.columns],
        [join_list(x, ', ') for x in rs_row.vals]
    ))
    return d


def join_list(l, j='\n'):
    if None in l:
        l = ""
    if type(l) == list:
        l = j.join(l)
    return l


def getitem(item, string):
    return item.get(string, '')
