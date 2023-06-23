from os import listdir, system, mkdir
from os.path import exists, abspath
from argparse import ArgumentParser
from dataclasses import dataclass, field
from platform import platform
import sys

@dataclass(frozen=False)
class Transcoder:
    platform
    input_folder : str = field(init=True)
    output_folder : str = field(init=True)
    ffmpeg_path : str = field(init=True, default=None)
    os_type : str = field(init=False)
    input_files : list[str] = field(init=False)
    output_files : list[str] = field(init=False)

    def __post_init__(self) -> list[str]:
        self.os_type = platform()
        self.input_folder = abspath(self.input_folder)
        self.output_folder = abspath(self.output_folder)
        if self.ffmpeg_path == None:
            self.ffmpeg_path = '/usr/bin/ffmpeg' if "Linux" in self.os_type else "ffmpeg"
        video_extensions = ['avi','mp4','mkv']
        file_names : list[str] = list(filter(
            lambda filename: filename[-3:] in video_extensions,
            listdir(self.input_folder)
        ))
        self.input_files = list(map(lambda filename: f'{self.input_folder}/{filename}',file_names))
        self.output_files = list(map(lambda filename: f'{self.output_folder}/{filename[:-4]}.mkv',file_names))
    
    def transcode_to_h264(self):
        if not exists(self.output_folder): mkdir(self.output_folder)
        for i, input_file in enumerate(self.input_files):
            output_file = self.output_files[i]
            if 'Linux' in self.os_type:
                ffmpeg_command = f'{self.ffmpeg_path} -i "{input_file}" -c:v h264 -preset superfast -crf 17 "{output_file}"'
            else:
                ffmpeg_command = f'{self.ffmpeg_path} -hwaccel cuda -i "{input_file}" -c:v h264_nvenc -preset fast -crf 17 "{output_file}"'
            system(ffmpeg_command)

def main():
    try:
        parser = ArgumentParser(description="any2h264 args parser")
        parser.add_argument('-i', dest='input_folder', type=str)
        parser.add_argument('-o', dest='output_folder', type=str)
        parser.add_argument('-ffmpeg', dest='ffmpeg_path', type=str)
        args = parser.parse_args()
        transcoder = Transcoder(args.input_folder, args.output_folder, args.ffmpeg_path)
        transcoder.transcode_to_h264()
    except KeyboardInterrupt:
        sys.exit()

if __name__ == '__main__':
    main()