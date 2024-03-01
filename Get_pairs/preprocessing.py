import os
import pandas as pd
import datetime


def makedir(new_path):
    if not os.path.exists(new_path):
        os.makedirs(new_path)


def QA_handle(interview):
    length = len(interview)
    pair_or_not = True
    answer_or_not = False
    a_nothing_lst = []

    for index, row in interview.iterrows():
        if index + 1 < length:
            if interview.loc[index, "status"] == "Not sure" and interview.loc[index + 1, "status"] != "Not sure":
                remove_index = index
                # 若not sure同时有QA，统一
                not_sure_QA = interview.loc[remove_index, "QA"]

                while remove_index >= 0 and interview.loc[remove_index, "status"] == "Not sure" and interview.loc[
                    remove_index, "QA"] != "Nothing":
                    if answer_or_not:
                        interview.loc[remove_index, "QA"] = not_sure_QA
                    remove_index -= 1

    for index, row in interview.iterrows():
        QA = interview.loc[index, "QA"]

        if QA == "Question":
            answer_or_not = False
            if pair_or_not:
                pair_or_not = False
            a_nothing_lst = []
        elif QA == "Answer":
            if index > 0:
                # Nothing后Answer,Nothing变answer
                last_QA = interview.loc[index - 1, "QA"]
                status = interview.loc[index, "status"]
                if last_QA == "Nothing" and status != interview.loc[index - 1, "status"]:
                    answer_or_not = True
                    remove_index = index - 1
                    print(remove_index)
                    while remove_index >= 0 and interview.loc[remove_index, "QA"] == "Nothing" and status != \
                            interview.loc[remove_index, "status"]:
                        interview.loc[remove_index, "QA"] = "Question"
                        remove_index -= 1

            if not pair_or_not:
                pair_or_not = True
                answer_or_not = True
            else:
                # 最开始answer,则全变为nothing
                if not answer_or_not:
                    interview.loc[index, "QA"] = "Nothing"
            if len(a_nothing_lst) > 0:
                # Answer中夹着Nothing变Answer
                for i in a_nothing_lst:
                    interview.loc[i, "QA"] = "Answer"
        else:
            if not pair_or_not:
                # question中nothing时，nothing变question
                if interview.loc[index, "status"] == "interviewer" or interview.loc[index, "status"] == "Not sure":
                    interview.loc[index, "QA"] = "Question"
                # question后nothing,变nothing
                else:
                    interview.loc[index, "QA"] = "Answer"
            else:
                if answer_or_not:
                    a_nothing_lst.append(index)

        # 结尾是question,全变为nothing
        if index + 1 == length and interview.loc[index, "QA"] == "Question":
            remove_index = index
            while remove_index >= 0 and interview.loc[remove_index, "QA"] == "Question":
                interview.loc[remove_index, "QA"] = "Nothing"
                remove_index -= 1


def conversion_time(time_str):
    time_parts = time_str.split(':')
    hours = time_parts[0]
    minutes = time_parts[1]
    seconds = str(int(float(time_parts[2])))
    if len(hours) < 2:
        hours = f"0{hours}"
    if len(minutes) < 2:
        minutes = f"0{minutes}"
    if len(seconds) < 2:
        seconds = f"0{seconds}"
    time_str = f"{hours}:{minutes}:{seconds}"

    time_obj = datetime.datetime.strptime(time_str, "%H:%M:%S")
    return time_obj


def get_QA():
    csv_path = '../Result'
    csv_lst = os.listdir(csv_path)
    makedir('../Pairs')
    for csv_file in csv_lst:
        result_path = os.path.join(csv_path, csv_file)
        interview = pd.read_csv(result_path)
        interview = interview.drop("Unnamed: 0", axis=1)

        QA_handle(interview)

        mask = interview["QA"] != "Nothing"
        interview = interview[mask]

        interview = interview.reset_index(drop=True)

        # 以防全为0
        if len(interview) == 0:
            continue

        turn = pd.DataFrame(
            columns=["Question_Start_Time", "Question_End_Time", "Answer_Start_Time", "Answer_End_Time", "Question",
                     "Answer", "Pause_Between_QA", "Pauses_Between_Qs", "Pauses_Between_As"])

        Q_num = 0
        A_num = 0
        text = ""
        question = ""
        answer = ""
        end = False
        QA_dict = {}
        Q_end_dict = {}
        Q_start_dict = {}
        A_end_dict = {}
        A_start_dict = {}
        for index, row in interview.iterrows():
            QA = interview.loc[index, "QA"]
            if QA == "Question":
                Q_num += 1
                question += str(interview.loc[index, "text"])
                Q_end_dict[" ".join(str(interview.loc[index, "text"]).split(" ")[-5:])] = conversion_time(
                    interview.loc[index, "end_time"])
                Q_start_dict[" ".join(str(interview.loc[index, "text"]).split(" ")[:5])] = conversion_time(
                    interview.loc[index, "start_time"])

                if Q_num == 1:
                    QA_dict["Question_Start_Time"] = conversion_time(interview.loc[index, "start_time"])

            elif QA == "Answer":
                A_num += 1
                answer += str(interview.loc[index, "text"])
                A_end_dict[" ".join(str(interview.loc[index, "text"]).split(" ")[-5:])] = conversion_time(
                    interview.loc[index, "end_time"])
                A_start_dict[" ".join(str(interview.loc[index, "text"]).split(" ")[:5])] = conversion_time(
                    interview.loc[index, "start_time"])

                if A_num == 1 and index > 0:
                    QA_dict["Question_End_Time"] = conversion_time(interview.loc[index - 1, "end_time"])
                    QA_dict["Question"] = question
                    QA_dict["Answer_Start_Time"] = conversion_time(interview.loc[index, "start_time"])

            if index + 1 == len(interview):
                QA_dict["Answer_End_Time"] = conversion_time(interview.loc[index, "end_time"])
                QA_dict["Answer"] = answer
                end = True
            else:
                if QA == "Answer":
                    judgement = interview.loc[index + 1, "QA"]
                    if judgement == "Question":
                        QA_dict["Answer_End_Time"] = conversion_time(interview.loc[index, "end_time"])
                        QA_dict["Answer"] = answer
                        end = True

            if end:
                QA_dict["Pause_Between_QA"] = {"{} -> {}".format(" ".join(QA_dict["Question"].split(" ")[-5:]),
                                                                 " ".join(QA_dict["Answer"].split(" ")[:5])): QA_dict["Answer_Start_Time"] -QA_dict["Question_End_Time"]}

                Q_start_key_lst = list(Q_start_dict.keys())
                Q_start_value_lst = list(Q_start_dict.values())
                Q_end_key_lst = list(Q_end_dict.keys())
                Q_end_value_lst = list(Q_end_dict.values())
                QA_dict["Pauses_Between_Qs"] = {}
                for times in range(len(Q_start_key_lst) - 1):
                    QA_dict["Pauses_Between_Qs"]["{} -> {}".format(Q_end_key_lst[times], Q_start_key_lst[times + 1])] = \
                    Q_start_value_lst[times + 1] - Q_end_value_lst[times]

                A_start_key_lst = list(A_start_dict.keys())
                A_start_value_lst = list(A_start_dict.values())
                A_end_key_lst = list(A_end_dict.keys())
                A_end_value_lst = list(A_end_dict.values())
                QA_dict["Pauses_Between_As"] = {}
                for times in range(len(A_start_key_lst) - 1):
                    QA_dict["Pauses_Between_As"]["{} -> {}".format(A_end_key_lst[times], A_start_key_lst[times + 1])] = \
                    A_start_value_lst[times + 1] - A_end_value_lst[times]

                turn = pd.concat([turn, pd.DataFrame([QA_dict])], ignore_index=True)

                Q_num = 0
                A_num = 0
                text = ""
                question = ""
                answer = ""
                end = False
                QA_dict = {}
                Q__end_dict = {}
                Q_start_dict = {}
                A_end_dict = {}
                A_start_dict = {}

        turn["Question_Start_Time"] = turn["Question_Start_Time"].dt.strftime("%H:%M:%S")
        turn["Question_End_Time"] = turn["Question_End_Time"].dt.strftime("%H:%M:%S")
        turn["Answer_Start_Time"] = turn["Answer_Start_Time"].dt.strftime("%H:%M:%S")
        turn["Answer_End_Time"] = turn["Answer_End_Time"].dt.strftime("%H:%M:%S")

        turn.to_csv(f'../Pairs/{os.path.splitext(csv_file)[0]}.csv')
        print(turn)
