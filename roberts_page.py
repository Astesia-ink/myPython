import streamlit as st
import cv2
import numpy as np

st.title('Roberts边界检测')

files = st.file_uploader('图像上传', type=["jpg", "jpeg", "png"])

# 将整个页面拆分为两部分，左侧为原始图像，右侧为处理后的结果
col1, col2 = st.columns(2)
if files is not None:
    values = files.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(values, np.uint8), cv2.IMREAD_COLOR)
    cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2GRAY)
    kernelx = np.array([[-1, 0], [0, 1]], dtype=int)
    kernely = np.array([[0, -1], [1, 0]], dtype=int)
    x = cv2.filter2D(cv2_img, cv2.CV_16S, kernelx)
    y = cv2.filter2D(cv2_img, cv2.CV_16S, kernely)
    absX = cv2.convertScaleAbs(x)
    absY = cv2.convertScaleAbs(y)
    Roberts = cv2.addWeighted(absX, 0.5, absY, 0.5, 0)
    cv2.imwrite('picture/roberts.bmp',Roberts)
    # 在左侧显示原始
    with col1:
        st.image(values, '原始结果')
    # 进行边界检测

    with col2:
        st.image(Roberts, '检测结果')