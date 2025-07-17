import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

# 设置页面标题
st.title('图像增强工具')

# 创建三列布局
col1, col2, col3 = st.columns(3)

# 文件上传器
uploaded_file = st.file_uploader('上传图像', type=["jpg", "jpeg", "png"])

# 在侧边栏添加增强选项
with st.sidebar:
    st.header("增强选项")

    # 对比度调整
    contrast = st.slider("对比度", 0.5, 2.0, 1.0, 0.1)

    # 亮度调整
    brightness = st.slider("亮度", -50, 50, 0, 5)

    # 锐化选项
    sharpen = st.checkbox("锐化处理")

    # 去噪选项
    denoise = st.checkbox("去噪处理")

    # 直方图均衡化
    equalize = st.checkbox("直方图均衡化")

    # 边缘增强
    edge_enhance = st.checkbox("边缘增强")

if uploaded_file is not None:
    # 读取图像
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    original_img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    original_img_rgb = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)  # 转换为RGB格式

    # 转换为灰度图
    gray_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)

    # 初始化增强后的灰度图像
    enhanced_gray = gray_img.copy()

    # 应用对比度和亮度调整
    enhanced_gray = np.clip(enhanced_gray.astype(np.float32) * contrast + brightness, 0, 255).astype(np.uint8)

    # 锐化处理
    if sharpen:
        kernel = np.array([[-1, -1, -1],[-1, 9, -1],[-1, -1, -1]])
        enhanced_gray = cv2.filter2D(enhanced_gray, -1, kernel)
    # 去噪处理
    if denoise:
        enhanced_gray = cv2.fastNlMeansDenoising(enhanced_gray, None, h=10,templateWindowSize=7,searchWindowSize=21)
    # 直方图均衡化
    if equalize:
        # 使用CLAHE（对比度受限的自适应直方图均衡化）
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced_gray = clahe.apply(enhanced_gray)

    # 边缘增强
    if edge_enhance:
        # 使用拉普拉斯算子增强边缘
        laplacian = cv2.Laplacian(enhanced_gray, cv2.CV_64F)
        enhanced_gray = np.clip(enhanced_gray + 0.5 * laplacian, 0, 255).astype(np.uint8)

    # 将增强后的灰度图像恢复为彩色
    # 方法：将原始图像的色彩空间转换到LAB，用增强后的灰度图替换L通道，再转回RGB
    lab_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2LAB)
    l_channel, a_channel, b_channel = cv2.split(lab_img)
    enhanced_lab = cv2.merge([enhanced_gray, a_channel, b_channel])
    enhanced_color = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2RGB)

    # 显示图像
    with col1:
        st.image(original_img_rgb, caption='原始彩色图像', use_container_width=True)

    with col2:
        st.image(enhanced_gray, caption='增强灰度图像', use_container_width=True, clamp=True)

    with col3:
        st.image(enhanced_color, caption='增强彩色图像', use_container_width=True)

    # 添加下载按钮
    if st.button('下载增强后的图像'):
        # 将图像转换为PIL格式
        enhanced_pil = Image.fromarray(enhanced_color)

        # 创建字节流
        img_byte_arr = io.BytesIO()
        enhanced_pil.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        # 提供下载
        st.download_button(
            label="点击下载彩色增强图像",
            data=img_byte_arr,
            file_name="enhanced_color_image.png",
            mime="image/png"
        )
else:
    st.info("请上传图像文件")

