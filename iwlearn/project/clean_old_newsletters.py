#
from htmllaundry import sanitize
from BeautifulSoup import BeautifulSoup



def cleanup_newsletters(self):
    for brain in self.portal_catalog(portal_type = 'News Item',
            path='iwlearn/websitetoolkit/e-bulletin/e-bulletin'):
        obj = brain.getObject()
        text = obj.getText()
        soup = BeautifulSoup(text)
        anchors = soup.findAll('a')
        changed = False
        for a in anchors:
            if a.has_key('href'):
                if a['href'].endswith('/view'):
                    a['href'] = a['href'][:-4]
                    changed = True
        if changed:
            ntext = soup.prettify()
            obj.setText(ntext)
