import os
import glob
import pathlib
import argparse

from pydub import AudioSegment
from pydub.utils import make_chunks


def process(audio_file, desired_duration_ms, desired_frame_rate):
    result = []

    duration_ms = (audio_file.frame_count() / desired_frame_rate) * 1000

    if duration_ms < desired_duration_ms:
        silent = AudioSegment.silent(
            duration=desired_duration_ms - duration_ms,
            frame_rate=desired_frame_rate
        )

        result.append(audio_file + silent)
    elif duration_ms > desired_duration_ms:
        for chunk in make_chunks(audio_file, desired_duration_ms):
            result.extend(process(chunk, desired_duration_ms, desired_frame_rate))

    return result


def normalize(desired_duration_ms, desired_frames_count, desired_frame_rate):
    try:
        for path in glob.glob(os.path.join(os.getcwd(), '**', '*.wav')):
            if not os.path.isfile(path):
                continue

            directory_path = os.path.sep.join(path.split(os.path.sep)[:-1])
            original_file_name = pathlib.Path(path).stem

            audio_file = AudioSegment.from_file(path, "wav")

            if audio_file.frame_count() == desired_frames_count and audio_file.frame_rate == desired_frame_rate:
                continue

            if audio_file.frame_rate != desired_frame_rate:
                audio_file = audio_file.set_frame_rate(desired_frame_rate)

            newFiles = process(audio_file, desired_duration_ms, desired_frame_rate)

            for index, audio_segment in enumerate(newFiles, start=1):
                if len(newFiles) == 1:
                    new_filename = f"{original_file_name}.wav"
                else:
                    new_filename = f"{original_file_name}_{index}.wav"

                audio_segment.export(os.path.join(directory_path, new_filename), format="wav")

                print(
                    f"{original_file_name} - ",
                    f"duration: {len(audio_segment)}ms, ",
                    f"frame rate: {audio_file.frame_rate}, ",
                    f"frames count: {audio_file.frame_count()}")
    except Exception as err:
        print("Error: {0}".format(err))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Normalize .wav audio files in a directory to a "
                                                 "specific frame rate and frames count, ensuring "
                                                 "uniformity for further processing or analysis.")

    parser.add_argument(
        '--frame_rate',
        type=int,
        default=44100,
        help="Desired frame rate for the audio files. Default is 44100."
    )

    parser.add_argument(
        '--frames_count',
        type=int,
        default=44032,
        help="Desired frames count for the audio files. Default is 44032."
    )

    args = parser.parse_args()

    desired_frame_rate = args.frame_rate
    desired_frames_count = args.frames_count
    desired_duration_ms = (desired_frames_count / desired_frame_rate) * 1000

    normalize(desired_duration_ms, desired_frames_count, desired_frame_rate)
