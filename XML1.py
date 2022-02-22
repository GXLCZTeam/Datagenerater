from lxml.etree import Element,SubElement,tostring
import xml.etree.ElementTree as et
from xml.dom.minidom import parseString
import os


def make_xml(filename):
    doc = et.parse(filename)
    nmsp = '{http://www.opengis.net/kml/2.2}'
    b = {}
    a = {}
    root = doc.getroot()
    a['filename'] = (root[0][0].text)
    image_name = root[0][0].text
    for pm in doc.iterfind('.//{0}Placemark'.format(nmsp)):

        a = pm.find('{0}name'.format(nmsp)).text
        for ls in pm.iterfind(
                '{0}MultiGeometry/{0}Polygon/{0}outerBoundaryIs/{0}LinearRing/{0}coordinates'.format(nmsp)):

            b[a] = (ls.text.strip().replace(' ', ''))
    object_name = []
    xmin_tuple = []
    ymin_tuple = []
    xmax_tuple = []
    ymax_tuple = []
    for i, j in b.items():
        object_name.append(i)
        m = j.split(',')
        lis = [k.strip('0') for k in m]
        lis = [float(e) for e in lis if e != '']  # 删除空值
        xlis = sorted(lis[::2])
        ylis = sorted(lis[1::2])
        xmin_tuple.append(min(xlis))
        ymin_tuple.append(min(ylis))
        xmax_tuple.append(max(xlis))
        ymax_tuple.append(max(ylis))
    node_root=Element('annotation')

    node_folder=SubElement(node_root,'folder')
    node_folder.text='images'
    node_filename=SubElement(node_root,'filename')
    node_filename.text=image_name+'.jpg'  #图像名称

    node_source=SubElement(node_root,'source')
    node_database=SubElement(node_source,'database')
    node_database.text='Unknown'
    node_annotation=SubElement(node_source,'annotation')
    node_annotation.text='Unknown'
    node_image=SubElement(node_source,'image')
    node_image.text='Unknown'

    node_size=SubElement(node_root,'size')
    node_width=SubElement(node_size,'width')
    node_width.text='100'
    node_height=SubElement(node_size,'height')
    node_height.text='100'
    node_depth=SubElement(node_size,'depth')
    node_depth.text='3'

    node_segmented=SubElement(node_root,'segmented')
    node_segmented.text='0'

    for i in range(len(xmin_tuple)):
        node_object=SubElement(node_root,'object')
        node_name=SubElement(node_object,'name')
        node_name.text=str(object_name[i])   #物体名称
        node_pose=SubElement(node_object,'pose')
        node_pose.text='Unspecified'
        node_truncated=SubElement(node_object,'truncated')
        node_truncated.text='0'
        node_difficult=SubElement(node_object,'difficult')
        node_difficult.text='0'

        node_bndbox=SubElement(node_object,'bndbox')
        node_xmin=SubElement(node_bndbox,'xmin')
        node_xmin.text=str(xmin_tuple[i])
        node_ymin=SubElement(node_bndbox,'ymin')
        node_ymin.text=str(ymin_tuple[i])
        node_xmax=SubElement(node_bndbox,'xmax')
        node_xmax.text=str(xmax_tuple[i])
        node_ymax=SubElement(node_bndbox,'ymax')
        node_ymax.text=str(ymax_tuple[i])

    xml=tostring(node_root,pretty_print=True)
    dom=parseString(xml)

    return dom


def get_all_files(dir):
    files_=[]
    list=os.listdir(dir)
    for i in range(0,len(list)):
        path = os.path.join(dir,list[i])
        if os.path.isdir(path):
            files_.extend(get_all_files(path))
        if os.path.isfile(path):
            files_.append(path)
    return files_

if __name__ == '__main__':
    image_name_list=get_all_files('C:/Users/Asus/Desktop/2') #KML路径
    print(image_name_list)
    for row in image_name_list:
        image_name=row.split('\\')[1].split('.')[0]
        dom=make_xml(row)

        xml_name=os.path.join('C:/Users/Asus/Desktop/3',image_name + '.xml') #XML存储路径
        with open(xml_name, 'wb')as f:
            f.write(dom.toprettyxml(newl='', encoding='utf-8'))
