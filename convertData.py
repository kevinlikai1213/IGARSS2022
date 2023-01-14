import json
template = r"/data/track2/buildings_only_train.json"
process_json = r"/data/track1/roof_fine_train.json"


def main():
    temp = json.load(open(template))
    proc = json.load(open(process_json))

    temp_dict = {im['file_name']: im['id']for im in temp['images']}
    proc_dict = {im['file_name']: im['id']for im in proc['images']}
    new_images_set, new_ids_set = get_newImgDict(temp_dict, proc_dict)
    # print(new_images_set, new_ids_set)
    new_images_list, new_anns_list = get_newAnnDict(new_images_set, new_ids_set, temp_dict, proc, temp)
    delta_im = len(temp['images'])*2
    delta_ann = len(temp['annotations'])*2
    
    for im in new_images_list:
        im['id']+=delta_im
    for ann in new_anns_list:
        ann['id']+=delta_ann
        ann['image_id']+=delta_im
        
    temp['images'].extend(new_images_list)
    temp['annotations'].extend(new_anns_list)
    info = json.dumps(temp)
    with open('mergetrain.json', 'w') as f:
        f.write(info)

def get_newImgDict(temp_dict, proc_dict):
    new_images_set, new_ids_set = set(), set()
    for name in proc_dict:
        if name not in temp_dict.keys():
            new_images_set.add(name)
            new_ids_set.add(proc_dict[name])
    return new_images_set, new_ids_set

def get_newAnnDict(new_images_set, new_ids_set, temp_dict, proc, temp):
    imid = new_ids_set
    new_images_dict = new_images_set
    new_anns_list =[]
    ids=len(temp_dict)
    for i,ann in enumerate(proc['annotations']):
        if ann['image_id'] in imid:
            ann['category_id']=1
            ann['id'] = ids
            ids+=1
            new_anns_list.append(ann)

    new_images_list = []
    img_ids = len(temp['images'])
    for im in proc['images']:
        if im['file_name'] in new_images_dict:
            new_images_list.append(im)
    return new_images_list, new_anns_list

if __name__=="__main__":
    main()