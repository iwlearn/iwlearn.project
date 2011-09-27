# utils
import colorsys

def hexcolor_to_rgba(hexcolor, opacity = '3c'):
    if hexcolor.startswith('#'):
        hexcolor = hexcolor[1:]
    a = int(opacity, 16)/255.0
    if len(hexcolor) == 3:
        r = int(hexcolor[0],16)/16.0
        g = int(hexcolor[1],16)/16.0
        b = int(hexcolor[2],16)/16.0
    elif len(hexcolor) == 4:
        r = int(hexcolor[0],16)/16.0
        g = int(hexcolor[1],16)/16.0
        b = int(hexcolor[2],16)/16.0
        a = int(hexcolor[3],16)/16.0
    elif len(hexcolor) == 6:
        r = int(hexcolor[0:2],16)/255.0
        g = int(hexcolor[2:4],16)/255.0
        b = int(hexcolor[4:6],16)/255.0
    elif len(hexcolor) == 8:
        r = int(hexcolor[0:2],16)/255.0
        g = int(hexcolor[2:4],16)/255.0
        b = int(hexcolor[4:6],16)/255.0
        a = int(hexcolor[6:8],16)/255.0
    return r,g,b,a

def rgba_to_hexcolor(r,g,b,a=0.7):
    r = min(255, max(int(r*255),16))
    g = min(255, max(int(g*255),16))
    b = min(255, max(int(b*255),16))
    a = min(255, max(int(a*255),16))
    return "#%x%x%x%x" %(r,g,b,a)


def get_basin_color(base,n):
    #return ('#%x%x' % (r,g)) + base[4:]

    #r,g,b,a = hexcolor_to_rgba(base)
    #h,s,v = colorsys.rgb_to_hsv(r, g, b)
    #ns = ((1-s)/20)*n + s
    #nv = ((1-v)/20)*n + v
    #nh = ((1-h)/20)*n + h
    #r,g,b = colorsys.hsv_to_rgb(nh, s, v)
    r,g,b,a = hexcolor_to_rgba(base)
    h,l,s = colorsys.rgb_to_hls(r, g, b)
    nh = ((1-h)/20)*n + h
    nl = ((1-l)/20)*n + l
    ns = ((1-s)/20)*n + s
    if n==0:
        #l = l/2
        s = s/2
    r,g,b = colorsys.hls_to_rgb(nh, l, s)
    return rgba_to_hexcolor(r,g,b,a)



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
