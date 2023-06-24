# Audio File Preprocessing for Voice Command Recognition Models

This is a Python script that can be used to normalize .wav audio files in a directory (and its subdirectories) to a 
specific frame rate and frames count. This is particularly useful when preparing custom audio datasets for machine 
learning models, as it ensures uniformity of the input data for further processing or analysis.

By default, the script will process all .wav files in the current directory and its subdirectories. It will modify the 
frame rate and frame count of each file to match the provided (or default) frame rate and frames count.

### ⚠️ Important:
1. If the audio file is shorter than the desired length, the script will add silence at the end of the file to reach
the required frame count.
2. If the audio file is longer than the desired length, the script will split the file into multiple segments, each 
with the required frames count.

## Usage

To use the script, you can pass in the desired frame rate and frame count as command line arguments. If these arguments 
are not provided, the script defaults to a frame rate of 44100 and a frame count of 44032 which will output ~1sec long
audio files.

```bash
python main.py --frame-rate <desired_frame_rate> --frames-count <desired_frames_count>
```

## Requirements
* Python 3.x
* pydub

You can install the requirements via pip:
```bash
pip install -r requirements.txt
```