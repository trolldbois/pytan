def formtodict(form):
    formdict = {}
    for k in form.keys():
        if type(form[k]) in [list, tuple]:
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
    if type(l) in [list, tuple]:
        l = j.join(l)
    return l


def getitem(item, string):
    return item.get(string, '')


def remove_count(rd):
    for r in rd:
        try:
            r.pop('Count')
        except:
            pass
    return rd


def remove_noresults(rd):
    return [r for r in rd if '[no results]' not in r.values()]


def rd_dict(rs):
    if rs:
        rs = remove_count(dictify_resultset(rs))
    return rs
