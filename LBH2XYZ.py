"""
Time:2022/2/26 21:07
Author:WRZ
"""
from osgeo import gdal
import numpy as np
import math

def INFO_image(path):
    """
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

def point2point(list,ImageShape,ImageTrans,ImagePrj):
    LineRow = []
    for each_LBH in list:
        L,B = each_LBH[0],each_LBH[1]
        if 'Mercator' in ImagePrj:
            ImageTrans = WebMercator2WGS84(ImageTrans)
            line = np.around((L - ImageTrans[0])/ImageTrans[1])
            row = np.around((B - ImageTrans[3])/ImageTrans[5])
            assert line<= ImageShape[0] and  row<= ImageShape[1] , print('The data range exceeds the limit')
            LineRow.append([line,row])
    return LineRow

def main(PointList,ImagePath):
    """

    Args:
        PointList: [[L,B,H],……[L1,B1,H1]] or [[L,B],……[L1,B1]]
        ImagePath: 影像路径

    Returns:

    """
    ImageShape, ImageTrans, ImagePrj = INFO_image(ImagePath)
    LineRow = point2point(PointList,ImageShape,ImageTrans,ImagePrj)
    return ImageShape, ImageTrans, ImagePrj,LineRow

if __name__ == '__main__':
    PointList = [[104.663,30.125],[104.3333,30.15789]]
    ImagePath = r'C:\Users\SAR\Desktop\矢量化示例\影像下载_2112072113\19\影像下载_2112072113.tif'
    ImageShape, ImageTrans, ImagePrj,LineRow = main(PointList,ImagePath)