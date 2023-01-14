loc_num = {
    'Berlin':138,
    'Brasilia':63,
    'NewDelhi':37,
    'NewYork':49,
    'Portsmouth':87,
    'Rio':12,
    'SanDiego':12,
    'SaoLuis':6,
    'Sydney':14,
    'Copenhagen':141,
    'Barcelona':18
}
for n in loc_num:
    loc_num[n]=loc_num[n]//2

import json
js_path = 'mergetrain.json'
def get_train_val_images():
    trainset = []
    valset = []
    js = json.load(open(js_path,'r'))
    images = js['images']
    for im in images:
        name = im['file_name']
        info = name.split('_')
        loc = info[1]
        if (loc in loc_num) and (loc_num[loc]): 
            valset.append(im)
            loc_num[loc]-=1
        else:
            trainset.append(im)
    return trainset, valset

def get_ann(imgset):
    def _check(info):
        imids = [im['id'] for im in imgset]
        if len(imids)!=len(set(imids)):
            print('error')

    imids = [im['id'] for im in imgset]
    dic = set(imids)
    js = json.load(open(js_path,'r'))
    anns = js['annotations']
    _check(anns)
    imganns = [ann for ann in anns if ann['image_id'] in dic]
    return imganns
    
def getjson(images, anns, key):
    im_dict = {im['id']:i for i, im in enumerate(images)}
    an_dict = {im['id']:i for i, im in enumerate(anns)}
    for im in images:
        im['id'] = im_dict[im['id']]
    
    for an in anns:
        an['id'] = an_dict[an['id']]
        an['image_id'] = im_dict[an['image_id']]
    js = json.load(open(js_path,'r'))
    js['images'] = images
    js['annotations'] = anns
    
    info = json.dumps(js)
    with open(key+'.json', 'w') as f:
        f.write(info)
    

def main():
    trainset, valset = get_train_val_images()
    trainanns = get_ann(trainset)
    valanns = get_ann(valset)
    getjson(trainset, trainanns, 'train')
    getjson(valset, valanns, 'val')
    
if __name__=='__main__':
    main()
