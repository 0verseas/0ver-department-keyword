#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import csv

import data_model
from ckiptagger import WS, POS, NER  # 斷詞、詞性標記、命名實體辨識


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
		keywords_filename = './quota_keyword_search_log.csv'
	else:
		keywords_filename = input("請輸入欲分析的 csv 檔案：")

	# 讀取關鍵字 csv
	with open(keywords_filename, newline='') as csvf:
		rows = csv.reader(csvf)
		for row in rows:
			origin_keywords.append(row[0])  # 將所有原始關鍵字都抽取出來

	ws_keywords = ckip(origin_keywords)  # 次元切割刀

	# 每列都是一個關鍵字切割後的結果的 csv
	with open('origin_ws.csv', 'w', newline="") as ows:
		writer = csv.writer(ows)
		for keyword in ws_keywords:
			writer.writerow(keyword)

			# 順便再抽出最小單位的關鍵字
			for i in keyword:
				total_keywords.append(i)

	# 把全部切割出來的小關鍵字通通放在第一行
	with open('all_ws.csv', 'w', newline='') as awsk:
		writer = csv.writer(awsk)
		for j in total_keywords:
			writer.writerow([j])


def ckip(keywords):
	""" CKIP Lab Chinese NLP """

	# 將三份工具的模型路徑指向我們剛才下載的模型
	# Load model
	ws = WS("./data")
	pos = POS("./data")
	ner = NER("./data")

	# 分析文本
	ws_results = ws(keywords)
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


if __name__ == '__main__':
	main()
