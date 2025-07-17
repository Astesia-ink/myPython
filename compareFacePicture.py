import streamlit as st
import cv2
import numpy as np
from pathlib import Path
import face_recognition as fr
st.title('人脸比对')

files=st.file_uploader('多人脸图像上传',type=["jpg","jpeg","png"])
files1=st.file_uploader('查找图像上传',type=["jpg","jpeg","png"])

#将整个页面拆分为两部分，左侧为原始图像，右侧为处理后的结果
col1,col2=st.columns(2)

if files is not None and files1 is not None:
    values = files.getvalue()
    values1= files1.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(values, np.uint8), cv2.IMREAD_COLOR)
    im_tst = cv2_img
    cv2_img1=cv2.imdecode(np.frombuffer(values1, np.uint8), cv2.IMREAD_COLOR)
    compare_tst = cv2_img1
    print(im_tst.shape)
    # 提取图像人脸的编码

    fea_tst = fr.face_encodings(im_tst)
    com_tst = fr.face_encodings(compare_tst)

    compare_list = []
    name_list = []
    i = 0
    for pare in com_tst:
        compare_list.append(pare)
        name_list.append(i)
        i += 1

    res = fr.compare_faces(compare_list, fea_tst[0], 0.6)  # 列表，编码，容忍程度
    if len(res) > 0:
        flag = False
        for i, face_rec in enumerate(res):
            if face_rec:
                st.success(f"✅ 匹配成功！识别为: {name_list[i]}")
                print(f'匹配成功，名字是：{name_list[i]}')
                flag = True
                break
        if not flag:
            print(f'该人脸不在图片中')
            st.warning("⚠️ 未找到匹配的人脸")