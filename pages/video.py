import streamlit as st
import cv2
import os
import tempfile
from moviepy.editor import ImageSequenceClip

# Cartoonify function using OpenCV
def cartoonify_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(gray, 255,
                                  cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, 9, 9)
    color = cv2.bilateralFilter(frame, 9, 250, 250)
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    return cartoon

# Streamlit app
st.title("🎬 Video to Cartoon Converter")
st.write("Upload a video and get a cartoon-style version!")

uploaded_file = st.file_uploader("Upload your .mp4 video", type=["mp4"])

if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(uploaded_file.read())

    st.video(uploaded_file)

    if st.button("Convert to Cartoon"):
        st.info("Processing video. Please wait...")

        vidcap = cv2.VideoCapture(tfile.name)
        fps = vidcap.get(cv2.CAP_PROP_FPS)
        frames = []
        success, image = vidcap.read()

        while success:
            cartoon_frame = cartoonify_frame(image)
            cartoon_frame = cv2.cvtColor(cartoon_frame, cv2.COLOR_BGR2RGB)
            frames.append(cartoon_frame)
            success, image = vidcap.read()

        # Save cartoon video using moviepy
        output_path = os.path.join(tempfile.gettempdir(), "cartoon_output.mp4")
        clip = ImageSequenceClip(frames, fps=fps)
        clip.write_videofile(output_path, codec='libx264')

        with open(output_path, "rb") as file:
            btn = st.download_button(
                label="Download Cartoon Video",
                data=file,
                file_name="cartoonized_video.mp4",
                mime="video/mp4"
            )
        st.success("Done! Click the button above to download your cartoon video.")
