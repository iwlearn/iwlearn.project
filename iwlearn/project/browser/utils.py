# utils

def get_query(form):
    query = {}
    form_fields = ['Title', 'getProject_type', 'getAgencies',
            'getProject_status', 'getBasin', 'getSubRegions']
    for field in form_fields:
        query[field] = form.get(field, None)
    query['portal_type'] = 'Project'
    dkeys = []
    for k,v in query.iteritems():
        if not v:
            dkeys.append(k)
    for k in dkeys:
        del(query[k])
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
