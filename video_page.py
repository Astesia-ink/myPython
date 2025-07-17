import streamlit as st
import cv2
import numpy as np
import tempfile
from datetime import datetime

st.title("高级视频水印工具")

watermark_text = st.text_input("输入水印文字", "Test Watermark")
font_scale = st.slider("水印大小", 0.5, 3.0, 1.0)
opacity = st.slider("水印透明度", 0.1, 1.0, 0.7)
font_color = st.color_picker("选择水印颜色", "#FFFFFF")
st.subheader("水印位置设置")
col1, col2 = st.columns(2)
with col1:
    x_position = st.slider("水平位置 (X)", 0, 100, 10, help="距离左边的百分比")
with col2:
    y_position = st.slider("垂直位置 (Y)", 0, 100, 90, help="距离顶部的百分比")
st.subheader("输出设置")
output_format = st.selectbox("输出视频格式", ["MP4", "AVI", "MOV"])
output_quality = st.slider("输出质量", 1, 100, 90, help="质量百分比")
uploaded_file = st.file_uploader("上传视频文件", type=["mp4", "avi", "mov"])
if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
        temp_file.write(uploaded_file.read())
        temp_path = temp_file.name
    st.video(temp_path)
    if st.button("添加水印并导出"):
        with st.spinner("正在处理视频..."):
            cap = cv2.VideoCapture(temp_path)
            frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            format_map = {
                "MP4": ("mp4v", ".mp4"),
                "AVI": ("AVID", ".avi"),
                "MOV": ("mp4v", ".mov")
            }
            fourcc_code, ext = format_map[output_format]
            fourcc = cv2.VideoWriter_fourcc(*fourcc_code)
            output_path = f"watermarked_{datetime.now().strftime('%Y%m%d%H%M%S')}{ext}"
            out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
            progress_bar = st.progress(0)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            processed_frames = 0
            rgb_color = tuple(int(font_color.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
            bgr_color = (rgb_color[2], rgb_color[1], rgb_color[0])
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # 计算水印位置
                x = int(frame_width * x_position / 100)
                y = int(frame_height * y_position / 100)

                # 创建水印层
                watermark = np.zeros_like(frame_rgb, dtype=np.uint8)
                cv2.putText(
                    watermark, watermark_text,
                    (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    font_scale,
                    bgr_color,
                    2,
                    cv2.LINE_AA
                )
                blended = cv2.addWeighted(frame_rgb, 1, watermark, opacity, 0)
                out.write(cv2.cvtColor(blended, cv2.COLOR_RGB2BGR))
                processed_frames += 1
                progress_bar.progress(processed_frames / frame_count)
            cap.release()
            out.release()
            st.success("视频处理完成！")
            st.video(output_path)
            with open(output_path, "rb") as file:
                st.download_button(
                    label="下载处理后的视频",
                    data=file,
                    file_name=output_path,
                    mime=f"video/{output_format.lower()}"
                )
