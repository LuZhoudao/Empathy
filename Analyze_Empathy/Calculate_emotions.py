import os
from feat import Detector
from Split import makedir


def calculate_emotions(all_video_path, output_path):
    detector = Detector(
            face_model="retinaface",
            landmark_model="mobilefacenet",
            au_model='xgb',
            emotion_model="resmasknet",
            facepose_model="img2pose",
        )

    video_file_lst = os.listdir(all_video_path)
    makedir(output_path)

    for video_file in video_file_lst:
        video_file_path = f'{all_video_path}/{video_file}'
        makedir(f"{output_path}/{video_file}")
        video_lst = os.listdir(video_file_path)
        if len(video_lst) % 2 != 0:
            question_lst = [file.split("_")[1] for file in video_lst if file.startswith('Question')]
            answer_lst = [file.split("_")[1] for file in video_lst if file.startswith('Answer')]
            unique_elements = [x for x in question_lst + answer_lst if x not in question_lst or x not in answer_lst]
            for file in video_lst:
                if file.split("_")[1] in unique_elements:
                    video_lst.remove(file)
        for video in video_lst:
            small_video_file = os.path.join(video_file_path, video)
            if f"{os.path.splitext(video)[0]}.csv" not in os.listdir(f"{output_path}/{video_file}"):
                try:
                    video_prediction = detector.detect_video(small_video_file, 24)
                    video_prediction.emotions.to_csv(f"{output_path}/{video_file}/{os.path.splitext(video)[0]}.csv")
                except:
                    pass



#video_file = "E:/year3_sem2/SA/CEO/empathy/Original_Video/3000138136.mp4"
#video_prediction = detector.detect_video(video_file, 24)

