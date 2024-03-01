import os
# import Diarization
from interviewee_judgement import judge_interviewee
from sample_generation import assign_QA
from preprocessing import get_QA


def makedir(new_path):
    if not os.path.exists(new_path):
        os.makedirs(new_path)


def main():
    input_path = "../Original_video"
    output_path = "../Handle"
    makedir(output_path)

    video_list = os.listdir(input_path)
    #glob.glob(os.path.join(input_path, '*.wav'))
    for video in video_list:
        original_video_path = f"{input_path}/{video}"

        # if os.path.splitext(video)[0] not in os.listdir(output_path):
        #     Diarization.speakerDiarization(original_video_path, output_path, video)


    # find interviewee/ers
    # users should change the key of openai by themselves
    key = 'sk-UeBVqz16qDzsoRwJF451E39d616d4eC1B11f07BaA18039C0'
    #judge_interviewee(key)
    assign_QA(key)
    get_QA()

if __name__ == '__main__':
    main()