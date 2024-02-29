import pandas as pd
from Split import splitVideo
from Calculate_emotions import calculate_emotions
from Calculate_empathy import calculate_empathy

pairs_path = '../Pairs'
splitVideo(pairs_path)

all_video_path = '../Severable_Video'
output_path = '../Emotions'
calculate_emotions(all_video_path, output_path)

# 读总文件
list_path = "../Others/Original_Videos_List_adjusted.xlsx"
list_df = pd.read_excel(list_path)
list_df.drop("Unnamed: 0", axis=1, inplace=True)
list_df.set_index("VideoID", inplace=True)


emotion_path = '../Emotions'
calculate_empathy(list_df, emotion_path)

