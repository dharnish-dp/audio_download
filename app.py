import streamlit as st
import yt_dlp
import os
from pathlib import Path

os.environ["PATH"] += os.pathsep + "/usr/local/bin"  # Helps find ffmpeg

# === Page Config ===
st.set_page_config(
    page_title="YT to MP3 - By Dharnish",
    page_icon="🎵",
    layout="centered"
)

# === Title & Style ===
st.title("🎵 YT to MP3 Converter")
st.markdown("### Fast • 320kbps • Free • Created by **DharnishDP**")
st.markdown("---")

# Input
url = st.text_input("Paste YouTube Link Here:", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Download as MP3 (320kbps)", type="primary"):
    if not url:
        st.error("Please paste a YouTube link!")
    else:
        with st.spinner("Downloading & converting to MP3..."):
            try:
                # Temporary download folder
                output_dir = "downloads"
                os.makedirs(output_dir, exist_ok=True)

                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '320',
                    }],
                    'quiet': False,
                    'no_warnings': False,
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    title = info.get('title', 'audio')
                    filename = ydl.prepare_filename(info)
                    mp3_filename = Path(filename).with_suffix('.mp3')
                    mp3_path = os.path.join(output_dir, mp3_filename.name)

                # Success!
                st.success(f"Downloaded: **{title}**")
                
                # Provide download button
                with open(mp3_path, "rb") as file:
                    st.download_button(
                        label="Download MP3 File",
                        data=file,
                        file_name=f"{title}.mp3",
                        mime="audio/mpeg"
                    )

                # Optional: Auto-delete after download (keeps folder clean)
                # shutil.rmtree(output_dir)

            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Try another video or check your internet connection.")

# Footer
st.markdown("---")
st.caption("Made with ❤️ by **Dharnish** | Works on Mobile & Desktop")