一、总览：

本项目基于Anaconda来使用python语言进行开发，使用到了opencv-python，Numpy和Streamlit进行结果的显示.

对视频和图像均可进行查看和修改

二、环境配置：

因为使用虚拟环境可以解决依赖隔离和版本冲突，且使得项目具有良好的可再现性和灵活性，所以在python开发中强烈建议使用虚拟环境。
接下来采用命令行配置环境的方法。以下安装的包皆为该项目所使用版本。

打开anaconda Prompt或直接打开cmd或是terminal
然后执行如下语句(在windows和macos上均可使用)：

1. 此处为非人脸识别的环境配置：

conda create -n image python=3.13.2

conda activate image

pip install numpy

pip install opencv-python

conda install streamlit
2. 此处为人脸识别的环境配置：

本项目的人脸识别采用dlib

conda create -n dlib python=3.8

conda activate dlib

pip install numpy

pip install opencv-python

conda install streamlit

pip install dlib(执行后按照弹出信息安装必需包)

三、运行：

程序入口为index.py，若是使用pycharm则在打开项目后在左下角点开终端，并输入“streamlit run index.py”来进行程序的运行。
若是使用vscode打开项目，则点击右下角Prettier后选择终端，然后使用“streamlit run index.py”来运行项目

四、功能：

1.可对图像进行边缘检测：分为sobel，roberts和canny算子检测三种

每一种边缘检测都会在"picture"目录下生成对应的bmp图像文件，但只会保存最后一次运行的结果。

2.可对图像进行Hough变换，其中分为直线检测和圆形检测，直线检测会以蓝色显示出直线，圆形检测则会在图像上用绿色画出圆

3.可对视频进行增加水印处理，可选择水印内容，颜色，大小，在视频中的位置（距离左上角百分比），可选择导出的文件格式，若不想下载也可重新生成

4.人脸识别：支持单人脸图像在多人脸图像中匹配；可对上传的人物图像进行嘴唇上的修改

5.图像融合：可将上传的两张图片进行融合，可自由调节融合程度，在浏览器中会显示第一张，第二张，和融合后的图像

6.图像增强：可自由调节图像的对比度，亮度；可对图像进行去噪，锐化，直方图均衡化和边缘增强，并可将增强之后的图像下载到本地，
