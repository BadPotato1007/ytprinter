import whisper
from pytube import YouTube
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.config import change_settings

# Specify the path to the ImageMagick binary
change_settings({"IMAGEMAGICK_BINARY": "C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})


def download_youtube_video(url, output_path='video.mp4'):
    yt = YouTube(url)
    yt_stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    yt_stream.download(filename=output_path)
    return output_path

def transcribe_video(video_path):
    model = whisper.load_model("base")
    result = model.transcribe(video_path)
    return result["segments"]

def add_subtitles(video_path, segments, output_path='output_with_subs.mp4'):
    video = VideoFileClip(video_path)
    subtitles = []

    for segment in segments:
        start = segment['start']
        end = segment['end']
        text = segment['text']
        subtitle = TextClip(text, fontsize=24, color='white', size=video.size, method='label', bg_color='black', stroke_color='black', stroke_width=1)
        subtitle = subtitle.set_position(('center', 'bottom')).set_start(start).set_duration(end - start)
        subtitles.append(subtitle)

    video_with_subs = CompositeVideoClip([video, *subtitles])
    video_with_subs.write_videofile(output_path, codec="libx264", audio_codec="aac")

def main(url):
    # Step 1: Download the video
    video_path = download_youtube_video(url)
    print("downloaded video")
    print(video_path)
    # Step 2: Transcribe the video to get subtitles with timestamps
    segments = transcribe_video("./video.mp4")
    print(segments)
    # Step 3: Add subtitles to the video
    add_subtitles("./video.mp4", segments)
    print("added subtitles")

if __name__ == "__main__":
    youtube_url = 'https://www.youtube.com/watch?v=Uo0KjdDJr1c'  # Replace with your YouTube URL
    main(youtube_url)
