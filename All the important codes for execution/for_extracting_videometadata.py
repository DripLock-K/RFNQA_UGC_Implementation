import pandas as pd
import json
import os
import subprocess
import glob
FFPROBE_METADATA_EXTRACTION_COMMAND = ('ffprobe -hide_banner -loglevel fatal -show_error -show_format -show_streams '+
                                      '-show_programs -show_chapters -show_private_data -print_format json "{}"')
def get_video_metadata(video_path):

    command = FFPROBE_METADATA_EXTRACTION_COMMAND.format(video_path)
    video_metadata = json.loads(subprocess.check_output(command, shell=True).decode())

    number_of_video_streams = 0

    video_stream_index = None

    for idx, stream in enumerate(video_metadata['streams']):
        if stream["codec_type"] == 'video':
            number_of_video_streams += 1
            video_stream_index = idx

    # CHECK THAT ONLY ONE AUDIO AND VIDEO STREAM ARE PRESENT IN VIDEO
    if number_of_video_streams != 1:
        raise ValueError("Number of video streams found: " + str(number_of_video_streams))

    video_metadata['streams'] = {
        'video_stream': video_metadata['streams'][video_stream_index],
    }

    return video_metadata


def json_metadata_to_csv(json_path, csv_path):
    with open(json_path, 'r') as f:
        video_metadata_dict = json.load(f)

    csv_rows = []

    for video_path, video_metadata in video_metadata_dict.items():
        avg_bitrate, width, height = video_metadata["streams"]["video_stream"]["bit_rate"], \
                                     video_metadata["streams"]["video_stream"]["width"], \
                                     video_metadata["streams"]["video_stream"]["height"]
        resolution = f"{width}x{height}"

        csv_rows.append({
            "video_path": video_path,
            "bitrate": avg_bitrate,
            "resolution": resolution
        })

    metadata_df = pd.DataFrame(csv_rows)
    metadata_df.to_csv(csv_path, index=False)

def process_video_folder(video_folder_path):
    video_path_list = sorted(glob.glob(os.path.join(video_folder_path, "*.mp4")))

    video_metadata_dict = {}

    for video_path in video_path_list:
        video_path = video_path.replace('\\', '\\\\')
        video_metadata = get_video_metadata(video_path)
        video_metadata_dict[video_path] = video_metadata

    with open('./video_metadata.json', 'w') as f:
        json.dump(video_metadata_dict, f)

process_video_folder("C:\\Users\\Krishna Baghel\\Desktop\\paper code and repos\\Extract-Frame-from-Videos-main\\videos")
json_metadata_to_csv("C:\\Users\\Krishna Baghel\\Desktop\\video_metadata.json", "C:\\Users\\Krishna Baghel\\Desktop\\video_metadata.csv")