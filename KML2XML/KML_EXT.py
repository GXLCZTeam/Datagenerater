from lxml.etree import Element, SubElement, tostring
import xml.etree.ElementTree as et

def make_coordinate(filename):
    doc = et.parse(filename)   #解析树
    nmsp = '{http://www.opengis.net/kml/2.2}' #xpath
    b = {}
    for pm in doc.iterfind('.//{0}Placemark'.format(nmsp)):
        a = pm.find('{0}name'.format(nmsp)).text   #读取placemark名称
        for ls in pm.iterfind(
                '{0}MultiGeometry/{0}Polygon/{0}outerBoundaryIs/{0}LinearRing/{0}coordinates'.format(nmsp)):  #读取标记坐标
            b[a] = (ls.text.strip().replace(' ', '')) #将标记名称和坐标写入字典
    PointList=[]
    Rectangular_box_name=[]
    for i, j in b.items():
        m = j.split(',')
        Rectangular_box_name.append(i)
        lis = [k.strip('0') for k in m]  # 删除KML坐标中开头出现的0
        lis = [float(e) for e in lis if e != '']  # 删除空值
        del lis[-2:]

        for n in range(0,len(lis),2):
            coord_1=lis[n:n+2]
            PointList.append(coord_1)

    return PointList,Rectangular_box_name

def make_xml(file_name,
             source='',
             size='',
             Rectangular_box_name=None,
             Geo_coor=None,
             Pix_coor=None):

    node_root=Element('annotation') #构建XML文件格式
    node_folder=SubElement(node_root,'folder')
    node_folder.text='images'  #此处按照样例直接写死，后期可以修改
    node_filename=SubElement(node_root,'filename')
    node_filename.text=file_name+'.jpg'  #图像名称

    node_source=SubElement(node_root,'source')
    #node_database=SubElement(node_source,'database')
    #node_database.text=source['database']
    #node_annotation=SubElement(node_source,'annotation')
    #node_annotation.text=source['annotation']
    #node_image=SubElement(node_source,'image')
    #node_image.text=source['image']
    node_coordinate = SubElement(node_source, 'coordinate')
    node_coordinate.text=source
    #node_resolution = SubElement(node_source, 'resolution')
    #node_resolution.text=source['resolution']

    node_size=SubElement(node_root,'size')
    node_width=SubElement(node_size,'width')
    node_width.text=str(size[0])
    node_height=SubElement(node_size,'height')
    node_height.text=str(size[1])
    node_depth=SubElement(node_size,'depth')
    node_depth.text=str(size[2])

    node_segmented=SubElement(node_root,'segmented')
    node_segmented.text='0'
    for i,j in enumerate(Rectangular_box_name):
        node_object=SubElement(node_root,'object')
        node_name=SubElement(node_object,'name')
        node_name.text=str(j)   #物体名称
        node_pose=SubElement(node_object,'pose')
        node_pose.text='Unspecified'
        node_truncated=SubElement(node_object,'truncated')
        node_truncated.text='0'
        node_difficult=SubElement(node_object,'difficult')
        node_difficult.text='0'
        node_bndbox=SubElement(node_object,'bndbox')
        node_xc1=SubElement(node_bndbox,'xc1')
        node_xc1.text=str(Geo_coor[i][0][0])
        node_x1=SubElement(node_bndbox,'x1')
        node_x1.text=str(Pix_coor[i][0][0])
        node_yc1=SubElement(node_bndbox,'yc1')
        node_yc1.text=str(Geo_coor[i][0][1])
        node_y1=SubElement(node_bndbox,'y1')
        node_y1.text=str(Pix_coor[i][0][1])
        node_xc2=SubElement(node_bndbox,'xc2')
        node_xc2.text=str(Geo_coor[i][1][0])
        node_x2 = SubElement(node_bndbox, 'x2')
        node_x2.text = str(Pix_coor[i][1][0])
        node_yc2=SubElement(node_bndbox,'yc2')
        node_yc2.text=str(Geo_coor[i][1][1])
        node_y2=SubElement(node_bndbox,'y2')
        node_y2.text=str(Pix_coor[i][1][1])
        node_xc3=SubElement(node_bndbox,'xc3')
        node_xc3.text=str(Geo_coor[i][2][0])
        node_x3 = SubElement(node_bndbox, 'x3')
        node_x3.text = str(Pix_coor[i][2][0])
        node_yc3=SubElement(node_bndbox,'yc3')
        node_yc3.text=str(Geo_coor[i][2][1])
        node_y3=SubElement(node_bndbox,'y3')
        node_y3.text=str(Pix_coor[i][2][1])
        node_xc4=SubElement(node_bndbox,'xc4')
        node_xc4.text=str(Geo_coor[i][3][0])
        node_x4 = SubElement(node_bndbox, 'x4')
        node_x4.text = str(Pix_coor[i][3][0])
        node_yc4=SubElement(node_bndbox,'yc4')
        node_yc4.text=str(Geo_coor[i][3][1])
        node_y4=SubElement(node_bndbox,'y4')
        node_y4.text=str(Pix_coor[i][3][1])
    dom=tostring(node_root,pretty_print=True)
    return dom
