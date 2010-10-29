# test vocabularies

from iwlearn.project import vocabulary

print vocabulary.get_regions()
srl = ['Polynesia']
print vocabulary.get_regions(subregions=srl)
srl = ['Polynesia','East Asia']
print vocabulary.get_regions(subregions=srl)
