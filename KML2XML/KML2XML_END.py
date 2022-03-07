import LBH2XYZ
import os
import KML_EXT

def KML2XML_END(kmlpath, ImagePath ,outputName):
    ImageShape, ImageTrans, ImagePrj = LBH2XYZ.INFO_image(ImagePath)
    coordinate_Geo, Rectangular_box_name = KML_EXT.make_coordinate(kmlpath)
    LineRow = LBH2XYZ.point2point(coordinate_Geo, ImageShape,
                                  ImageTrans, Mercator=True)
    file_name = ImagePath.split('\\')[-1].split('.')[0]
    Pix_coordinate = []
    for i in range(0, len(LineRow), 4):
        LineRow_1 = LineRow[i:i+4]
        Pix_coordinate.append(LineRow_1)
    Geo_coordinate = []
    for j in range(0, len(coordinate_Geo), 4):
        coordinate_Geo1 = coordinate_Geo[j:j+4]
        Geo_coordinate.append(coordinate_Geo1)

    dom = KML_EXT.make_xml(file_name, source=ImagePrj, size=ImageShape,
                           Rectangular_box_name=Rectangular_box_name,
                           Geo_coor=Geo_coordinate, Pix_coor=Pix_coordinate)

    with open(outputName, 'wb')as f:
        f.write(dom)



if __name__ == '__main__':
    kmlpath = r'C:\Users\SAR\Desktop\作业或工作论文汇报与ppt\工作\做项目\国家重点研发计划\川藏线目标识别\矢量化示例\影像下载_2112072113\19\test1.kml'
    ImagePath = r'C:\Users\SAR\Desktop\作业或工作论文汇报与ppt\工作\做项目\国家重点研发计划\川藏线目标识别\矢量化示例\影像下载_2112072113\19\tif\影像下载_2112072113.tif'
    xml_name = os.path.join(r'C:\Users\SAR\Desktop\git_push\SWJTU-GXL Team\Datagenerater\KML2XML',   'test.xml')  # XML存储名称

    KML2XML_END(kmlpath, ImagePath, xml_name)
