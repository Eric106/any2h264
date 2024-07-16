from os import listdir, system, mkdir
from os.path import exists, abspath
from argparse import ArgumentParser, BooleanOptionalAction
from dataclasses import dataclass, field
from platform import platform
import sys

@dataclass(frozen=False)
class Transcoder:
    platform
    input_folder : str = field(init=True)
    output_folder : str = field(init=True)
    ffmpeg_path : str = field(init=True, default=None)
    ten_bit_encode : bool = field(init=True, default=False)
    os_type : str = field(init=False)
    input_files : list[str] = field(init=False)
    output_files : list[str] = field(init=False)

    def __post_init__(self) -> list[str]:
        self.os_type = platform()
        self.input_folder = abspath(self.input_folder)
        self.output_folder = abspath(self.output_folder)
        if self.ffmpeg_path == None:
            self.ffmpeg_path = '/usr/bin/ffmpeg' if "Linux" in self.os_type else "ffmpeg"
        video_extensions = ['avi','mp4','mkv','m4v']
        file_names : list[str] = list(filter(
            lambda filename: filename[-3:] in video_extensions,
            listdir(self.input_folder)
        ))
        self.input_files = list(map(lambda filename: f'{self.input_folder}/{filename}',file_names))
        self.output_files = list(map(lambda filename: f'{self.output_folder}/{filename[:-4]}.mkv',file_names))
    
    def transcode_to_h264(self):
        if not exists(self.output_folder): mkdir(self.output_folder)
        for i, input_file in enumerate(self.input_files):
            input_file_extension = input_file.split('.')[-1]
            output_file = self.output_files[i]
            if 'Linux' in self.os_type:
                ffmpeg_command = f'{self.ffmpeg_path} -y -i "{input_file}" -c:v h264 -preset superfast -crf 17 -c:s copy "{output_file}"'
            elif 'Windows' in self.os_type:
                if self.ten_bit_encode:
                    ffmpeg_command = f'{self.ffmpeg_path} -y -hwaccel cuda -i "{input_file}" -vf format=yuv420p -c:v h264_nvenc -preset fast -crf 17 -c:s copy "{output_file}"'
                else:
                    ffmpeg_command = f'{self.ffmpeg_path} -y -hwaccel cuda -i "{input_file}" -c:v h264_nvenc -preset fast -crf 17 -c:s copy "{output_file}"'
            print(ffmpeg_command)
            system(ffmpeg_command)

def main():
    try:
        parser = ArgumentParser(description="any2h264 args parser")
        parser.add_argument('-i', dest='input_folder', type=str)
        parser.add_argument('-o', dest='output_folder', type=str)
        parser.add_argument('-ffmpeg', dest='ffmpeg_path', type=str)
        parser.add_argument('-10b', dest='ten_bit_encode', action=BooleanOptionalAction)
        args = parser.parse_args()
        transcoder = Transcoder(args.input_folder, args.output_folder, args.ffmpeg_path, args.ten_bit_encode)
        transcoder.transcode_to_h264()
    except KeyboardInterrupt:
        sys.exit()

if __name__ == '__main__':
    main()
