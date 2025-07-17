import streamlit as st
import cv2
import numpy as np
import face_recognition

st.title('更改人物嘴唇颜色')

files = st.file_uploader('图像上传', type=["jpg", "jpeg", "png"])

# 将整个页面拆分为两部分，左侧为原始图像，右侧为处理后的结果
col1, col2 = st.columns(2)
if files is not None:
    values = files.getvalue()
    im = cv2.imdecode(np.frombuffer(values, np.uint8), cv2.IMREAD_COLOR)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(im, number_of_times_to_upsample=1, model='hog')
    #print(f'人脸检测结果：{face_locations}')
    # 人脸特征值
    face_feature = face_recognition.face_encodings(im, face_locations)
    #print(f'人脸特征值：{face_feature}, 特征维度：{face_feature[0].shape}')

    # 人脸标注点
    face_landmarks = face_recognition.face_landmarks(im, face_locations)
    #f1 = face_landmarks[0]
    #print(f1['left_eye'])

    def apply_lip_color(im, r, g, b):
        face_lip = face_landmarks[0]['top_lip']
        face_lip1 = face_landmarks[0]['bottom_lip']
        # 使用 RGB 顺序
        cv2.fillPoly(im, [np.array(face_lip)], (r, g, b))
        cv2.fillPoly(im, [np.array(face_lip1)], (r, g, b))


    r = st.slider("R", 0, 255, 0)
    g = st.slider("G", 0, 255, 0)
    b = st.slider("B", 0, 255, 0)

    apply_lip_color(im, r, g, b)
    with col1:
        st.image(values, '原始结果')
    with col2:
        st.image(im, '检测结果')

    cv2.imwrite('pictureFace/Lip.bmp',im)