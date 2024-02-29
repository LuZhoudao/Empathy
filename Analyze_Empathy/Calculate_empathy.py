import os
import pandas as pd
import math


def measure1(QA_list):
    question_score = {}
    answer_score = {}
    difference_score = {}
    for QA in QA_list:
        QA_path = os.path.join(file_path, QA)
        QA_df = pd.read_csv(QA_path)
        QA_df.drop("frame", axis=1, inplace=True)
        mean_dict = {col: QA_df[col].mean() for col in QA_df}

        Q_or_A = QA.split("_")[0]
        if Q_or_A == "Question":
            question_score[QA.split("_")[1]] = mean_dict
        else:
            answer_score[QA.split("_")[1]] = mean_dict

    for key in question_score.keys():
        if key in answer_score.keys():
            difference_score[key] = {}
            for emotion in question_score[key].keys():
                difference_score[key][emotion] = question_score[key][emotion]-answer_score[key][emotion]

    n = len(difference_score)
    print(difference_score)
    print(n)
    emotion_lst = ["anger", "disgust", "fear", "happiness", "sadness", "surprise", "neutral"]
    scores = {}
    for index in emotion_lst:
        scores[index] = 0
    for key in difference_score.keys():
        for emotion in difference_score[key].keys():
            if math.isnan(difference_score[key][emotion]):
                break
            scores[emotion] += difference_score[key][emotion]

    values_sum = 0
    for value in scores.values():
        values_sum += (value / n)**2

    return math.sqrt(values_sum) / math.sqrt(6)


def measure2(QA_list):
    question_score = {}
    answer_score = {}
    difference_score = {}
    for QA in QA_list:
        QA_path = os.path.join(file_path, QA)
        QA_df = pd.read_csv(QA_path)
        QA_df.drop("frame", axis=1, inplace=True)
        max_dict = {col: QA_df[col].max() for col in QA_df}

        Q_or_A = QA.split("_")[0]
        if Q_or_A == "Question":
            question_score[QA.split("_")[1]] = max_dict
        else:
            answer_score[QA.split("_")[1]] = max_dict

    for key in question_score.keys():
        if key in answer_score.keys():
            difference_score[key] = {}
            for emotion in question_score[key].keys():
                difference_score[key][emotion] = question_score[key][emotion] - answer_score[key][emotion]

    n = len(difference_score)
    emotion_lst = ["anger", "disgust", "fear", "happiness", "sadness", "surprise", "neutral"]
    scores = {}
    for index in emotion_lst:
        scores[index] = 0
    for key in difference_score.keys():
        for emotion in difference_score[key].keys():
            if math.isnan(difference_score[key][emotion]):
                break
            scores[emotion] += difference_score[key][emotion]

    values_sum = 0
    for value in scores.values():
        values_sum += (value / n) ** 2

    return math.sqrt(values_sum) / math.sqrt(6)


def measure3(QA_list):
    question_score = {}
    answer_score = {}
    difference_score = {}
    for QA in QA_list:
        QA_path = os.path.join(file_path, QA)
        QA_df = pd.read_csv(QA_path)
        QA_df.drop("frame", axis=1, inplace=True)
        mean_dict = {'happiness': QA_df['happiness'].mean()}

        Q_or_A = QA.split("_")[0]
        if Q_or_A == "Question":
            question_score[QA.split("_")[1]] = mean_dict
        else:
            answer_score[QA.split("_")[1]] = mean_dict

    for key in question_score.keys():
        if key in answer_score.keys():
            difference_score[key] = {}
            difference_score[key]['happiness'] = abs(question_score[key]['happiness'] - answer_score[key]['happiness'])

    n = len(difference_score)
    scores = {'happiness': 0}
    for key in difference_score.keys():
        if math.isnan(difference_score[key]['happiness']):
            break
        scores['happiness'] += difference_score[key]['happiness']

    values_sum = scores['happiness'] / n

    return values_sum


def measure4_10(QA_list):
    question_score = {}
    answer_score = {}
    difference_score = {}
    for QA in QA_list:
        QA_path = os.path.join(file_path, QA)
        QA_df = pd.read_csv(QA_path)
        QA_df.drop("frame", axis=1, inplace=True)

        threshold = QA_df['happiness'].quantile(0.9)
        selected_rows = QA_df[QA_df['happiness'] >= threshold]
        mean_dict = {'happiness': selected_rows['happiness'].mean()}

        Q_or_A = QA.split("_")[0]
        if Q_or_A == "Question":
            question_score[QA.split("_")[1]] = mean_dict
        else:
            answer_score[QA.split("_")[1]] = mean_dict

    for key in question_score.keys():
        if key in answer_score.keys():
            difference_score[key] = {}
            difference_score[key]['happiness'] = abs(question_score[key]['happiness'] - answer_score[key]['happiness'])

    n = len(difference_score)
    scores = {'happiness': 0}
    for key in difference_score.keys():
        if math.isnan(difference_score[key]['happiness']):
            break
        scores['happiness'] += difference_score[key]['happiness']

    values_sum = scores['happiness'] / n

    return values_sum


def measure4_20(QA_list):
    question_score = {}
    answer_score = {}
    difference_score = {}
    for QA in QA_list:
        QA_path = os.path.join(file_path, QA)
        QA_df = pd.read_csv(QA_path)
        QA_df.drop("frame", axis=1, inplace=True)

        threshold = QA_df['happiness'].quantile(0.8)
        selected_rows = QA_df[QA_df['happiness'] >= threshold]
        mean_dict = {'happiness': selected_rows['happiness'].mean()}

        Q_or_A = QA.split("_")[0]
        if Q_or_A == "Question":
            question_score[QA.split("_")[1]] = mean_dict
        else:
            answer_score[QA.split("_")[1]] = mean_dict

    for key in question_score.keys():
        if key in answer_score.keys():
            difference_score[key] = {}
            difference_score[key]['happiness'] = abs(question_score[key]['happiness'] - answer_score[key]['happiness'])

    n = len(difference_score)
    scores = {'happiness': 0}
    for key in difference_score.keys():
        if math.isnan(difference_score[key]['happiness']):
            break
        scores['happiness'] += difference_score[key]['happiness']

    values_sum = scores['happiness'] / n

    return values_sum


def measure5(QA_list):
    question_score = {}
    answer_score = {}
    difference_score = {}
    for QA in QA_list:
        QA_path = os.path.join(file_path, QA)
        QA_df = pd.read_csv(QA_path)
        QA_df.drop("frame", axis=1, inplace=True)
        max_dict = {'happiness': QA_df['happiness'].max()}

        Q_or_A = QA.split("_")[0]
        if Q_or_A == "Question":
            question_score[QA.split("_")[1]] = max_dict
        else:
            answer_score[QA.split("_")[1]] = max_dict

    for key in question_score.keys():
        if key in answer_score.keys():
            difference_score[key] = {}
            difference_score[key]['happiness'] = abs(question_score[key]['happiness'] - answer_score[key]['happiness'])

    n = len(difference_score)
    scores = {'happiness': 0}
    for key in difference_score.keys():
        if math.isnan(difference_score[key]['happiness']):
            break
        scores['happiness'] += difference_score[key]['happiness']

    values_sum = scores['happiness'] / n

    return values_sum


def measure6(QA_list):
    question_score = {}
    answer_score = {}
    difference_score = {}
    for QA in QA_list:
        QA_path = os.path.join(file_path, QA)
        QA_df = pd.read_csv(QA_path)
        QA_df.drop("frame", axis=1, inplace=True)
        max_dict = {col: QA_df[col].max() for col in QA_df}

        Q_or_A = QA.split("_")[0]
        if Q_or_A == "Question":
            question_score[QA.split("_")[1]] = max_dict
        else:
            answer_score[QA.split("_")[1]] = max_dict

    for key in question_score.keys():
        if key in answer_score.keys():
            difference_score[key] = {}
            difference_score[key]['happiness'] = abs(question_score[key]['happiness'] - answer_score[key]['happiness'])

    n = 0
    scores = {'happiness': 0}
    for key in difference_score.keys():
        if math.isnan(difference_score[key]['happiness']):
            break
        if question_score[key]['happiness'] == max(question_score[key].values()):
            n += 1
            scores['happiness'] += difference_score[key]['happiness']

    if n != 0:
        values_sum = scores['happiness'] / n
    else:
        values_sum = float('nan')

    return values_sum


def measure7(QA_list):
    question_score = {}
    answer_score = {}
    difference_score = {}
    for QA in QA_list:
        QA_path = os.path.join(file_path, QA)
        QA_df = pd.read_csv(QA_path)
        QA_df.drop("frame", axis=1, inplace=True)
        mean_dict = {'sadness': QA_df['sadness'].mean()}

        Q_or_A = QA.split("_")[0]
        if Q_or_A == "Question":
            question_score[QA.split("_")[1]] = mean_dict
        else:
            answer_score[QA.split("_")[1]] = mean_dict

    for key in question_score.keys():
        if key in answer_score.keys():
            difference_score[key] = {}
            difference_score[key]['sadness'] = abs(question_score[key]['sadness'] - answer_score[key]['sadness'])

    n = len(difference_score)
    scores = {'sadness': 0}
    for key in difference_score.keys():
        if math.isnan(difference_score[key]['sadness']):
            break
        scores['sadness'] += difference_score[key]['sadness']

    values_sum = scores['sadness'] / n

    return values_sum


def measure8_10(QA_list):
    question_score = {}
    answer_score = {}
    difference_score = {}
    for QA in QA_list:
        QA_path = os.path.join(file_path, QA)
        QA_df = pd.read_csv(QA_path)
        QA_df.drop("frame", axis=1, inplace=True)
        threshold = QA_df['sadness'].quantile(0.9)
        selected_rows = QA_df[QA_df['sadness'] >= threshold]
        mean_dict = {'sadness': selected_rows['sadness'].mean()}

        Q_or_A = QA.split("_")[0]
        if Q_or_A == "Question":
            question_score[QA.split("_")[1]] = mean_dict
        else:
            answer_score[QA.split("_")[1]] = mean_dict

    for key in question_score.keys():
        if key in answer_score.keys():
            difference_score[key] = {}
            difference_score[key]['sadness'] = abs(question_score[key]['sadness'] - answer_score[key]['sadness'])

    n = len(difference_score)
    scores = {'sadness': 0}
    for key in difference_score.keys():
        if math.isnan(difference_score[key]['sadness']):
            break
        scores['sadness'] += difference_score[key]['sadness']

    values_sum = scores['sadness'] / n

    return values_sum


def measure8_20(QA_list):
    question_score = {}
    answer_score = {}
    difference_score = {}
    for QA in QA_list:
        QA_path = os.path.join(file_path, QA)
        QA_df = pd.read_csv(QA_path)
        QA_df.drop("frame", axis=1, inplace=True)
        threshold = QA_df['sadness'].quantile(0.8)
        selected_rows = QA_df[QA_df['sadness'] >= threshold]
        mean_dict = {'sadness': selected_rows['sadness'].mean()}

        Q_or_A = QA.split("_")[0]
        if Q_or_A == "Question":
            question_score[QA.split("_")[1]] = mean_dict
        else:
            answer_score[QA.split("_")[1]] = mean_dict

    for key in question_score.keys():
        if key in answer_score.keys():
            difference_score[key] = {}
            difference_score[key]['sadness'] = abs(question_score[key]['sadness'] - answer_score[key]['sadness'])

    n = len(difference_score)
    scores = {'sadness': 0}
    for key in difference_score.keys():
        if math.isnan(difference_score[key]['sadness']):
            break
        scores['sadness'] += difference_score[key]['sadness']

    values_sum = scores['sadness'] / n

    return values_sum


def measure9(QA_list):
    question_score = {}
    answer_score = {}
    difference_score = {}
    for QA in QA_list:
        QA_path = os.path.join(file_path, QA)
        QA_df = pd.read_csv(QA_path)
        QA_df.drop("frame", axis=1, inplace=True)
        max_dict = {'sadness': QA_df['sadness'].max()}

        Q_or_A = QA.split("_")[0]
        if Q_or_A == "Question":
            question_score[QA.split("_")[1]] = max_dict
        else:
            answer_score[QA.split("_")[1]] = max_dict

    for key in question_score.keys():
        if key in answer_score.keys():
            difference_score[key] = {}
            difference_score[key]['sadness'] = abs(question_score[key]['sadness'] - answer_score[key]['sadness'])

    n = len(difference_score)
    scores = {'sadness': 0}
    for key in difference_score.keys():
        if math.isnan(difference_score[key]['sadness']):
            break
        scores['sadness'] += difference_score[key]['sadness']

    values_sum = scores['sadness'] / n

    return values_sum


def measure10(QA_list):
    question_score = {}
    answer_score = {}
    difference_score = {}
    for QA in QA_list:
        QA_path = os.path.join(file_path, QA)
        QA_df = pd.read_csv(QA_path)
        QA_df.drop("frame", axis=1, inplace=True)
        max_dict = {col: QA_df[col].max() for col in QA_df}

        Q_or_A = QA.split("_")[0]
        if Q_or_A == "Question":
            question_score[QA.split("_")[1]] = max_dict
        else:
            answer_score[QA.split("_")[1]] = max_dict

    for key in question_score.keys():
        if key in answer_score.keys():
            difference_score[key] = {}
            difference_score[key]['sadness'] = abs(question_score[key]['sadness'] - answer_score[key]['sadness'])

    n = 0
    scores = {'sadness': 0}
    for key in difference_score.keys():
        if math.isnan(difference_score[key]['sadness']):
            break
        if question_score[key]['sadness'] == max(question_score[key].values()):
            n += 1
            scores['sadness'] += difference_score[key]['sadness']

    if n != 0:
        values_sum = scores['sadness'] / n
    else:
        values_sum = float('nan')

    return values_sum


# 读总文件
list_path = "../Others/Original_Videos_List_adjusted.xlsx"
list_df = pd.read_excel(list_path)
list_df.drop("Unnamed: 0", axis=1, inplace=True)
list_df.set_index("VideoID", inplace=True)


def calculate_empathy(list_df, emotion_path):
    emotion_file_lst = os.listdir(emotion_path)
    score_df = pd.DataFrame()
    for file in emotion_file_lst:
        file_path = os.path.join(emotion_path, file)
        QA_lst = os.listdir(file_path)

        result = dict(list_df.loc[int(file), ['GVKEY', 'CEOName']])
        result['GVKEY'] = result['GVKEY'].astype(int)
        # measurement 1
        measurement1 = measure1(QA_lst)
        result["measurement1_score"] = measurement1

        # measurement 2
        measurement2 = measure2(QA_lst)
        result["measurement2_score"] = measurement2

        # measurement 3
        measurement3 = measure3(QA_lst)
        result["measurement3_score"] = measurement3

        # measurement 4 10%
        measurement4_10 = measure4_10(QA_lst)
        result["measurement4_10%_score"] = measurement4_10

        # measurement 4 20%
        measurement4_20 = measure4_20(QA_lst)
        result["measurement4_20%_score"] = measurement4_20

        # measurement 5
        measurement5 = measure5(QA_lst)
        result["measurement5_score"] = measurement5

        # measurement 6
        measurement6 = measure6(QA_lst)
        result["measurement6_score"] = measurement6

        # measurement 7
        measurement7 = measure7(QA_lst)
        result["measurement7_score"] = measurement7

        # measurement 8 10%
        measurement8_10 = measure8_10(QA_lst)
        result["measurement8_10%_score"] = measurement8_10

        # measurement 8 20%
        measurement8_20 = measure8_20(QA_lst)
        result["measurement8_20%_score"] = measurement8_20

        # measurement 9
        measurement9 = measure9(QA_lst)
        result["measurement9_score"] = measurement9

        # measurement 10
        measurement10 = measure10(QA_lst)
        result["measurement10_score"] = measurement10

        new_df = pd.DataFrame(result, index=[file])
        score_df = pd.concat([score_df, new_df])
        print(new_df)

    score_df.to_csv('../score.csv')



