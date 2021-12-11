"""
# -*- coding: utf-8 -*-

Created on Nov 2021
@author: PRATEEK YADAV

"""
import uuid
import sqlite3
import pandas as pd


class ExportJson:

    def __init__(self, db_driver, main_table, para_question_table, question_answer_table):
        self.db_driver = db_driver
        self.table_info = {'main_table': main_table, 'para_question_table': para_question_table,
                           'question_answer_table': question_answer_table}

    def get_connection(self):
        try:
            connection = sqlite3.connect(self.db_driver)
            # cursor = connection.cursor()
            return connection
        except sqlite3.Error as error:
            print('Connection establish problem..')
            print(error)

    # def create_connection(self):
    #     try:
    #         engine = sqal.create_engine(self.db_driver)
    #         connection = engine.connect()
    #         return connection
    #     except Exception as e:
    #         print('Connection establish problem..')
    #         print(e.__str__())
    #         return None

    def get_Dataframes(self):
        with self.get_connection() as conn:
            tempTable = conn.execute("SELECT * from {}".format(self.table_info['main_table']))
            main_df = pd.DataFrame(tempTable.fetchall())
            main_df.columns = [description[0] for description in tempTable.description]

            tempTable1 = conn.execute("SELECT * from {}".format(self.table_info['para_question_table']))
            para_question_df = pd.DataFrame(tempTable1.fetchall())
            para_question_df.columns = [description[0] for description in tempTable1.description]

            tempTable2 = conn.execute("SELECT * from {}".format(self.table_info['question_answer_table']))
            question_answer_df = pd.DataFrame(tempTable2.fetchall())
            question_answer_df.columns = [description[0] for description in tempTable2.description]

        return main_df, para_question_df, question_answer_df

    def get_all_questions_from_paraId(self, para_id, para_qs_df):
        groupObj = para_qs_df.groupby(para_qs_df.paraid)
        for item in list(groupObj):
            if item[0] == para_id:
                return item[1][['ques_id', 'question']].reset_index().to_dict('list')

    def get_all_answers_from_questionId(self, qid, qa_ans_df):
        groupObj = qa_ans_df.groupby(qa_ans_df.question_id)
        for item in list(groupObj):
            if item[0] == qid:
                return item[1][['question_id', 'answer_content']].reset_index().to_dict('list')

    def sql_df_to_squad_json(self):
        list_of_df = self.get_Dataframes()
        final_list = []
        main_df, para_qs_df, qs_ans_df = list_of_df
        for idx, row in main_df.iterrows():
            temp_dict = {}
            paraId = row['paraid']

            # fetch qid from para_id
            questions_fetch = self.get_all_questions_from_paraId(paraId, para_qs_df)
            temp_dict['context'] = row['content']
            temp_dict['title'] = row['para_tit']

            # fetch aid from qid
            qas_dict = {}
            qas_list = []
            try:
                for qid, qContent in zip(questions_fetch['ques_id'], questions_fetch['question']):
                    all_answers = self.get_all_answers_from_questionId(qid, qs_ans_df)
                    if not all_answers == None:
                        qas_dict['answers'] = [{'answer_start': 'start_location', 'text': item} for item in all_answers['answer_content']]
                        qas_dict['id'] = uuid.uuid4().hex
                        qas_dict['question'] = qContent
                        qas_list.append(qas_dict)
                    temp_dict['qas'] = qas_list
                
                final_list.append(temp_dict)
            except:
                {'data': []}
        return {'data': final_list}


if __name__ == '__main__':
    # pass
    print("RUNNING ==============")
    classObj = ExportJson(r'db1.sqlite3', 'annoatations', 'questions', 'answers')
    print(classObj.sql_df_to_squad_json())
