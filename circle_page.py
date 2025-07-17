import streamlit as st
import cv2
import numpy as np
st.title('圆形检测')

files=st.file_uploader('图像上传',type=["jpg","jpeg","png"])

#将整个页面拆分为两部分，左侧为原始图像，右侧为处理后的结果
col1,col2=st.columns(2)
if files is not None:
    values=files.getvalue()
    cv2_img=cv2.imdecode(np.frombuffer(values,np.uint8),cv2.IMREAD_COLOR)
    #转换为灰度
    gray_image=cv2.cvtColor(cv2_img,cv2.COLOR_BGR2GRAY)

    #在左侧显示原始

    with col1:
        st.image(values,'原始结果')

    #进行圆形监测
    
    circles=cv2.HoughCircles(gray_image,cv2.HOUGH_GRADIENT,20,param1=200,param2=100,minDist=100,maxRadius=500)
    
    #在图像上画圆
    
    im_shw=cv2_img.copy()

    for x,y,r in circles[0]: 
        cv2.circle(im_shw,(int(x),int(y)),int(r),(0,255,0),2)
        cv2.circle(im_shw,(int(x),int(y)),2,(0,255,255),2)#圆心
        #cv2.circle(im_shw,(int(x),int(y)),10,(255,255,255),2)
    with col2:
        st.image(im_shw,'检测结果')