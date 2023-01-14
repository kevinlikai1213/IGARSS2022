import json
import os
import platform
import shutil
from tqdm import tqdm

sys = platform.system()

mergetrainjson = 'mergetrain.json'
track1 = r'/data/track1'
track2 = r'/data/track2/train'

outpath = './data'
if os.path.exists(outpath):
    shutil.rmtree(outpath)
os.mkdir(outpath)
    
def copyTrack2():
    # if sys == 'Windows':
    shutil.copytree(os.path.join(track2,'rgb'), os.path.join(outpath,'rgb'))
    shutil.copytree(os.path.join(track2,'sar'),os.path.join(outpath,'sar'))
    # shutil.copytree(os.path.join(track1,'rgb'), os.path.join(outpath,'rgb'))
    # shutil.copytree(os.path.join(track1,'sar'),os.path.join(outpath,'sar'))    
    exist_im = set(os.listdir(os.path.join(outpath,'rgb')))
    images = json.load(open(mergetrainjson))['images']
    for im in tqdm(images):
        if im['file_name'] not in exist_im:
            # try:
            shutil.copy(os.path.join(track1,'rgb',im['file_name']), os.path.join(outpath,'rgb'))
            shutil.copy(os.path.join(track1,'sar',im['file_name']), os.path.join(outpath,'sar'))
            # except:
            #     print(os.path.join(track1,'sar',im['file_name']))
    
def main():
    copyTrack2()

main()