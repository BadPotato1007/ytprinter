import whisper
from pytube import YouTube
import json
from colorama import Fore, Back, Style
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from moviepy.config import change_settings

# Specify the path to the ImageMagick binary
change_settings(
    {"IMAGEMAGICK_BINARY": "C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"})


def download_youtube_video(url, output_path='video.mp4'):
    yt = YouTube(url)
    yt_stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by(
        'resolution').desc().first()
    yt_stream.download(filename=output_path)
    return output_path


def transcribe_video(video_path):
    model = whisper.load_model("base")
    result = model.transcribe(video_path, word_timestamps=True)

    return result['segments']


def add_subtitles(video_path, segment, output_path='output_with_subs.mp4'):
    video = VideoFileClip(video_path)
    subtitles = []
    data = segment
    y = json.dumps(data)
    use = json.loads(y)
    for i in range(len(use)):
        print(len(use))
        print('=' * 10)
        print(len(use[i]['words']))
        for j in range(len(use[i]['words'])):
            print(use[i]['words'][j]['word'], end=' ')  # word
            # start time of the word
            print(use[i]['words'][j]['start'], end=' ')
            print(use[i]['words'][j]['end'], end='\n')  # end time of that word
            start = use[i]['words'][j]['start']
            end = use[i]['words'][j]['end']
            text = use[i]['words'][j]['word']
            subtitle = TextClip(
                text,
                font="../fonts/agencyr.ttf",
                fontsize=35,
                color="white",
                stroke_color="black",
                stroke_width=1,
            )
            print("added word")

            subtitle = subtitle.set_position(('center', 'center')).set_start(
                start).set_duration(end - start)
            subtitles.append(subtitle)

    video_with_subs = CompositeVideoClip([video, *subtitles])
    video_with_subs.write_videofile(
        output_path, codec="libx264", audio_codec="aac")


def main(url):
    # Step 1: Download the video
    video_path = download_youtube_video(url)
    print("Downloaded video to:", video_path)
    # Step 2: Transcribe the video to get subtitles with timestamps
    segments = transcribe_video(video_path)
    print("Transcription segments:", segments)

    # Step 3: Add subtitles to the video
    add_subtitles(video_path, segments)
    print("Added subtitles and saved the output video")


if __name__ == "__main__":
    # Replace with your YouTube URL
    youtube_url = 'https://www.youtube.com/shorts/yBfqEcxZXdI'
    main(youtube_url)
