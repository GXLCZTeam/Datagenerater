"""
转换LBH2XYZ ， 包含WebMercator2WGS84
Time:2022/2/26 21:07
Author:WRZ
"""
from osgeo import gdal
import numpy as np
import math

def INFO_image(path):
    """
    获取影像的信息
    Args:
        path: img_path as:c:/xx/xx.tif

    Returns: [列，行，波段]，坐标变换，投影，

    坐标变换：   0：图像左上角的X坐标；
                1：图像东西方向分辨率；
                2：旋转角度，如果图像北方朝上，该值为0；
                3：图像左上角的Y坐标；
                4：旋转角度，如果图像北方朝上，该值为0；
                5：图像南北方向分辨率；
    """
    dataset = gdal.Open(path)
    return [dataset.RasterXSize,dataset.RasterYSize,dataset.RasterCount],\
           [i for i in dataset.GetGeoTransform()],dataset.GetProjection()

def WebMercator2WGS84(ImageTrans):
    """
    Args:
        ImageTrans: 变换参数，参考INFO_image

    Returns: WebMercator2WGS84

    """
    def cast(x,y):
        return x / 20037508.3427892 * 180,\
               180 / math.pi * (2 * math.atan(math.exp(y / 20037508.3427892 * 180 * math.pi / 180)) - math.pi / 2)
    L_,B_ = cast(ImageTrans[0] + ImageTrans[1],ImageTrans[3]+ImageTrans[5])
    ImageTrans[0],ImageTrans[3] = cast(ImageTrans[0],ImageTrans[3])
    ImageTrans[1],ImageTrans[5] = L_  - ImageTrans[0]  , B_ - ImageTrans[3]
    return ImageTrans

def point2point(list,ImageShape,ImageTrans,Mercator=True):
    LineRow = []
    if Mercator:
        ImageTrans = WebMercator2WGS84(ImageTrans)

    for each_LBH in list:
        L,B = each_LBH[0],each_LBH[1]
        line = np.around((L - ImageTrans[0])/ImageTrans[1])
        row = np.around((B - ImageTrans[3])/ImageTrans[5])
        assert line<= ImageShape[0] and  row<= ImageShape[1] , 'The data range exceeds the limit'
        LineRow.append([line,row])
    return LineRow

def main(PointList,ImagePath,Mercator=True):
    """

    Args:
        PointList: [[L,B,H],……[L1,B1,H1]] or [[L,B],……[L1,B1]]
        ImagePath: 影像路径

    Returns:

    """
    ImageShape, ImageTrans, ImagePrj = INFO_image(ImagePath)
    LineRow = point2point(PointList,ImageShape,ImageTrans,Mercator=Mercator)
    return ImageShape, ImageTrans, ImagePrj,LineRow

if __name__ == '__main__':
    PointList = [[104.1946579448498, 30.71085336996432], [104.1963037905027, 30.71085336996432], [104.1963037905027, 30.7110782811443], [104.1946579448498, 30.7110782811443]]
    ImagePath = r'C:\Users\Asus\Desktop\川藏线目标识别\影像下载_2112072113.tif'
    ImageShape, ImageTrans, ImagePrj,LineRow = main(PointList,ImagePath,Mercator=True)
