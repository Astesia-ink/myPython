import streamlit as st
import cv2
import numpy as np

st.title('sobel边界检测')

files = st.file_uploader('图像上传', type=["jpg", "jpeg", "png"])

# 将整个页面拆分为两部分，左侧为原始图像，右侧为处理后的结果
col1, col2 = st.columns(2)
if files is not None:
    values = files.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(values, np.uint8), cv2.IMREAD_COLOR)

    cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2GRAY)
    x = cv2.Sobel(cv2_img, cv2.CV_16S, 1, 0)
    y = cv2.Sobel(cv2_img, cv2.CV_16S, 0, 1)
    absX = cv2.convertScaleAbs(x)
    absY = cv2.convertScaleAbs(y)
    Sobel = cv2.addWeighted(absX, 0.5, absY, 0.5, 0)
    cv2.imwrite('picture/sobel.bmp',Sobel)
    with col1:
        st.image(values, '原始结果')
    with col2:
        st.image(Sobel, '检测结果')