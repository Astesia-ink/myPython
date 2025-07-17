import streamlit as st
import cv2
import numpy as np
st.title('canny边界检测')

files=st.file_uploader('图像上传',type=["jpg","jpeg","png"])

#将整个页面拆分为两部分，左侧为原始图像，右侧为处理后的结果
col1,col2=st.columns(2)
if files is not None:
    values=files.getvalue()
    cv2_img=cv2.imdecode(np.frombuffer(values,np.uint8),cv2.IMREAD_COLOR)

    #在左侧显示原始
    with col1:
        st.image(values,'原始结果')
    #进行边界检测
    img_gray=cv2.cvtColor(cv2_img,cv2.COLOR_BGR2GRAY)
    edge=cv2.Canny(img_gray,100,200)
    cv2.imwrite('picture/canny.bmp',edge)

    with col2:
        st.image(edge,'检测结果')