keywords = context.portal_catalog.Indexes['Subject'].uniqueValues(withLengths=True)
print context.portal_catalog.Indexes['Subject'].getIndexSourceNames()
for kw in keywords:
    if kw[1] > 7:
       print kw
    else:
        for brain in context.portal_catalog(Subject = kw):
            ob = brain.getObject()
            keywords = list(ob.Subject())
            if kw[0] in keywords:
                keywords.remove(kw[0])
                ob.setSubject(keywords)
                print 'nuke:', kw
            else:
                print kw, 'not in', keywords

return printed
