import cv2
import numpy as np
import streamlit as st
st.title('直线检测')

files=st.file_uploader('图像上传',type=["jpg","jpeg","png"])

#将整个页面拆分为两部分，左侧为原始图像，右侧为边界检测结果
col1,col2=st.columns(2)
if files is not None:
    values=files.getvalue()
    cv2_img=cv2.imdecode(np.frombuffer(values,np.uint8),cv2.IMREAD_COLOR)
    #彩色->灰色
    im_gray=cv2.cvtColor(cv2_img,cv2.COLOR_BGR2GRAY)
    #高斯平滑去噪声
    im_gray=cv2.GaussianBlur(im_gray,(3,3),1)
    #canny边界检测
    edges=cv2.Canny(im_gray,100,200)
    lines1=cv2.HoughLinesP(edges,1.0,np.pi/180,50,minLineLength=50,maxLineGap=10)
    img=cv2_img.copy()
    for line in lines1:
        xt,yt=line[0][0],line[0][1]
        xe,ye=line[0][2],line[0][3]
        cv2.line(img,(xt,yt),(xe,ye),(0,0,255),2)
    #在左侧显示原始
    with col1:
        st.image(values,'原始结果')
    with col2:
        st.image(img)