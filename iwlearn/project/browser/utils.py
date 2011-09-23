# utils

def get_basin_color(base,n):
    r = min(255, max(5 +(10 * n), 32))
    if base.startswith('#'):
        base = base[1:]
    return ('#%x' % r) + base[2:]

def get_color(n):
        r = min(255, max(5 +(10 * n), 16))
        g = min(255, max(255 -r, 16))
        b = 64
        return '#%x%x%x' % (r,g,b)

def get_query(form):
    query = {}
    form_fields = ['Title', 'getProject_type', 'getAgencies',
            'getProject_status', 'getBasin', 'getSubRegions',
            'SearchableText']
    for field in form_fields:
        if form.get(field, None):
            query[field] = form[field]
    query['portal_type'] = 'Project'
    sortorder = form.get('sortorder',None)
    if sortorder=='desc':
        sort_order = 'reverse'
    else:
        sort_order = None
    sort_on = None
    sortname = form.get('sortname',None)
    if sortname=='Title':
        sort_on = 'sortable_title'
    elif sortname:
        sort_on = sortname
    if sort_on:
        query['sort_on'] = sort_on
        if sort_order:
            query['sort_order'] = sort_order
    return query
