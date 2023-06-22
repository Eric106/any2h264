from os import listdir, system, mkdir
from os.path import exists
from argparse import ArgumentParser
from dataclasses import dataclass, field

@dataclass(frozen=False)
class Transcoder:
    input_folder : str = field(init=True)
    output_folder : str = field(init=True)
    ffmpeg_path : str = field(init=True, default='/usr/bin/ffmpeg')
    input_files : list[str] = field(init=False)
    output_files : list[str] = field(init=False)

    def __post_init__(self) -> list[str]:
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
            system(f'{self.ffmpeg_path} -i "{input_file}" -c:v libx264 -preset ultrafast -crf 17 "{output_file}"')

def main():
    parser = ArgumentParser(description="any2h264 args parser")
    parser.add_argument('-i', dest='input_folder', type=str)
    parser.add_argument('-o', dest='output_folder', type=str)
    parser.add_argument('-ffmpeg', dest='ffmpeg_path', type=str)
    args = parser.parse_args()
    if args.ffmpeg_path == None:
        transcoder = Transcoder(args.input_folder, args.output_folder)
    else:
        transcoder = Transcoder(args.input_folder, args.output_folder, args.ffmpeg_path)
    transcoder.transcode_to_h264()

if __name__ == '__main__':
    main()