import os
import pandas as pd


def makedir(new_path):
    if not os.path.exists(new_path):
        os.makedirs(new_path)

def call_command(cmd_content, call_path=None):
    """
    调用命令行
    call_path: 执行命令的目录
    """
    print(f"执行：{cmd_content}")
    import subprocess
    if call_path == None:
        this_file_dir_path = os.getcwd()
    # result = subprocess.run(f'ffmpeg -i video.m4s -i audio.m4s -codec copy {file_path}', shell=True, stdout=subprocess.PIPE, cwd=this_file_dir_path)
    return subprocess.run(cmd_content, shell=True, stdout=subprocess.PIPE, cwd=this_file_dir_path)


def splitVideo(df_path):
    severable_video_path = '../Severable_Video'
    all_video_path = '../Original_Video'
    makedir(severable_video_path)

    df_lst = os.listdir(df_path)
    for df in df_lst:
        single_df_path = os.path.join(df_path,df)
        pairs_df = pd.read_csv(single_df_path)
        pairs_df = pairs_df.drop("Unnamed: 0", axis=1)

        video_name = os.path.splitext(df)[0]
        video_path = f'{all_video_path}/{video_name}.mp4'

        # make directory
        output_path = f'{severable_video_path}/{video_name}'
        makedir(output_path)

        for index, row in pairs_df.iterrows():
            question_start_time = row["Question_Start_Time"]
            question_end_time = row["Question_End_Time"]
          #  if question_start_time == question_end_time:
                # question_end_time
            answer_start_time = row["Answer_Start_Time"]
            answer_end_time = row["Answer_End_Time"]

            call_command(
                f'ffmpeg -i {video_path} -vcodec copy -ss {question_start_time} -to {question_end_time} {output_path}/Question_{index+1}_{video_name}_{question_start_time.replace(":", "")}-{question_end_time.replace(":", "")}.mp4 -y')
            call_command(
                f'ffmpeg -i {video_path} -vcodec copy -ss {answer_start_time} -to {answer_end_time} {output_path}/Answer_{index + 1}_{video_name}_{answer_start_time.replace(":", "")}-{answer_end_time.replace(":", "")}.mp4 -y')


#splitVideo('E:/year3_sem2/SA/CEO/empathy/Pairs')