import streamlit as st
st.title('首页')
pages = {
    #一级菜单
    'Hough变换':[   #存放二级菜单
        st.Page('pages/line_page.py',title='直线检测'),
        st.Page('pages/circle_page.py',title='圆形检测')
    ],
    "边界检测":[
        st.Page("pages/edgedet_page.py",title="canny边界检测"),
        st.Page("pages/roberts_page.py", title="roberts边界检测"),
        st.Page("pages/sobel_page.py", title="sobel边界检测")

    ],
    "视频处理":[
        st.Page("pages/video_page.py",title="视频增加水印")
    ],
    "图像增强": [
        st.Page("pages/printPicture_page.py", title="图像增强")
    ],
    "图像融合":[
        st.Page("pages/blendPicture_page.py", title="图片融合"),
    ],
    "人脸识别":[
        st.Page("pages/changeLip.py",title="更改嘴唇颜色"),
        st.Page("pages/compareFacePicture.py",title="单图像人脸比对"),
    ]
}
#创建导航栏
pg=st.navigation(pages)
pg.run()