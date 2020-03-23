import json
from xml.dom import minidom
from xml.etree import ElementTree as ET
import os
N_IMGS=21258
ann_dir='dtc_train_annotations'
img_dir='dtc_train_images'
dst_ann_dir='annotations'
width, height = 1936, 1216
def prettify(elem):
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")
def json2xml(json_dict, num):
    top = ET.Element('top')

    child = ET.SubElement(top, 'folder')
    child.text = img_dir
    child = ET.SubElement(top, 'filename')
    child.text = 'train_%05d.jpg' % num

    child = ET.SubElement(top, 'frameIndex')
    child.text = str(json_dict['frameIndex'])

    child = ET.SubElement(top, 'attributes')
    region = ET.SubElement(child, 'route')
    time = ET.SubElement(child, 'timeofday')
    region.text = json_dict['attributes']['route']
    time.text = json_dict['attributes']['timeofday']

    child = ET.SubElement(top, 'size')
    w = ET.SubElement(child, 'width')
    h = ET.SubElement(child, 'height')
    c = ET.SubElement(child, 'depth')
    w.text, h.text, c.text = str(width), str(height), '3'

    for obj in json_dict['labels']:
        child = ET.SubElement(top, 'object')
        name = ET.SubElement(child, 'name')
        name.text = obj['category']

        bndbox = ET.SubElement(child, 'bndbox')
        xmin = ET.SubElement(bndbox, 'xmin')
        ymin = ET.SubElement(bndbox, 'ymin')
        xmax = ET.SubElement(bndbox, 'xmax')
        ymax = ET.SubElement(bndbox, 'ymax')
        xmin.text, xmax.text = str(obj['box2d']['x1']), str(obj['box2d']['x2'])
        ymin.text, ymax.text = str(obj['box2d']['y1']), str(obj['box2d']['y2'])


    return prettify(top)

os.mkdir(dst_ann_dir)

for i in range(N_IMGS):
    if((i+1)%1000==0): print(i)
    with open(os.path.join(ann_dir,'train_%05d.json' % i), 'r') as f:
        json_dict = json.load(f)
    with open(os.path.join(dst_ann_dir,'train_%05d.xml' % i), 'w') as f:
        f.write(json2xml(json_dict,i))
