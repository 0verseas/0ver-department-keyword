#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import csv

import data_model
from ckiptagger import WS, POS, NER  # 斷詞、詞性標記、命名實體辨識
from ckiptagger import construct_dictionary


# 原始問題 https://github.com/ckiplab/ckiptagger/issues/52
# 暫時解法 https://github.com/ckiplab/ckiptagger/issues/50#issuecomment-2145367084
os.environ["TF_USE_LEGACY_KERAS"]='1'

def main():
	# 先檢查模型存在與否
	if not os.path.isdir("./data"):
		print("下載模型")
		data_model.download()

	# 開始

	origin_keywords = []
	total_keywords = []

	# 做點檢查是基本的
	if os.path.isfile('./quota_keyword_search_log.csv'):
		print('發現預設檔案，將讀取 quota_keyword_search_log.csv')
		keywords_filename = './quota_keyword_search_log.csv'
	else:
		keywords_filename = input("請輸入欲分析的 csv 檔案：")

	# 讀取關鍵字 csv
	with open(keywords_filename, newline='') as csvf:
		rows = csv.reader(csvf)
		for row in rows:
			origin_keywords.append(row[0])  # 將所有原始關鍵字都抽取出來

	print('開始斷詞')
	ws_keywords = ckip(origin_keywords)  # 次元切割刀
	print('斷詞完成')

	# 每列都是一個關鍵字切割後的結果的 csv
	print('產生第一個 csv')
	with open('origin_ws.csv', 'w', newline="") as ows:
		writer = csv.writer(ows)
		for keyword in ws_keywords:
			writer.writerow(keyword)

			# 順便再抽出最小單位的關鍵字
			for i in keyword:
				total_keywords.append(i)

	# 把全部切割出來的小關鍵字通通放在第一行
	print('產生第二個 csv')
	with open('all_ws.csv', 'w', newline='') as awsk:
		writer = csv.writer(awsk)
		for j in total_keywords:
			writer.writerow([j])

	# 開始計數

	unique_keywords = set(total_keywords)

	print("共切割出 {} 個關鍵字，去除重複後有 {} 個獨特關鍵字".format(len(total_keywords), len(unique_keywords)))

	# 準備計算出現次數
	print('開始計數')
	count_keyword = {}
	while len(unique_keywords) != 0:
		count_keyword[unique_keywords.pop()] = 0
	# 計數
	for words in total_keywords:
		count_keyword[words] += 1

	# 輸出 unique 關鍵字統計結果的 csv
	print('產生第三個 csv')
	with open('count_keyword.csv', 'w', newline="") as ckf:
		writer = csv.writer(ckf)
		writer.writerow(['keyword', 'times'])  # header
		for key, value in count_keyword.items():
			writer.writerow([key, value])


def ckip(keywords):
	""" CKIP Lab Chinese NLP """

	# 將三份工具的模型路徑指向我們剛才下載的模型
	# Load model
	ws = WS("./data")
	pos = POS("./data")
	ner = NER("./data")

	# 自訂字典
	if os.path.isfile('./school_data.csv'):  # 檢查下有沒有學校名稱列表
		print("發現官方學校名稱檔案，將作為強制詞加入字典")
		force_dictionary = construct_dictionary(school('school_data', True))
	else:
		force_dictionary = {}
	if os.path.isfile('./school_alias.csv'):  # 各種別名、簡稱等
		print("發現非官方學校名稱檔案，將作為推薦詞加入字典")
		encourage_dictionary = construct_dictionary(school('school_alias'))
	else:
		encourage_dictionary = {}

	# 分析文本
	ws_results = ws(keywords, recommend_dictionary = encourage_dictionary, coerce_dictionary = force_dictionary)
	# pos_results = pos(ws_results)
	# ner_results = ner(ws_results, pos_results)  # ner(文本, POS結果)

	# 結果
	# print(ws_results)  # 斷詞
	# print(pos_results)  # 詞性
	# for name in ner_results[0]:  # 實體辨識
	#     print(name)

	# release memory
	del ws
	del pos
	del ner

	return ws_results


def school(filename_of_data, official = False):
	""" 學校資料轉換成自訂字典 """

	name_set = set()
	word_to_weight = {}
	with open('./'+filename_of_data+'.csv', 'r', newline='') as sf:
		rows = csv.reader(sf)
		for row in rows:
			for name in row:
				name_set.add(name)
		# 設定權重
		if official:
			word_weight = 10
		else:
			word_weight = 3
		for i in name_set:
			word_to_weight[i] = word_weight

	return word_to_weight


if __name__ == '__main__':
	main()
