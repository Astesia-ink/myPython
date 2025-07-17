import streamlit as st
import cv2
import numpy as np
st.title("图像融合")
image1= st.file_uploader("第一张图像", type=["jpg", "jpeg", "png"])
image2 = st.file_uploader("第二张图像", type=["jpg", "jpeg", "png"])
if image1 is not None and image2 is not None:
    img1 = cv2.imdecode(np.asarray(bytearray(image1.read()), dtype=np.uint8), cv2.IMREAD_COLOR)
    img1_rgb = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    img1 = cv2.resize(img1, (900,600))
    img2 = cv2.imdecode(np.asarray(bytearray(image2.read()), dtype=np.uint8), cv2.IMREAD_COLOR)
    img2_rgb = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
    img2 = cv2.resize(img2, (900,600))
    alpha = st.slider("调整融合程度，初始为不融合,日常使用时0-1即可", 0.0, 1.0, 0.0)
    blended = cv2.addWeighted(img1, alpha, img2, 1 - alpha, 0)
    blended_rgb = cv2.cvtColor(blended, cv2.COLOR_BGR2RGB)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image(img1_rgb, caption='第一张', use_column_width=True)
    with col2:
        st.image(img2_rgb, caption='第二张', use_column_width=True)
    with col3:
        st.image(blended_rgb, caption='融合后', use_column_width=True)