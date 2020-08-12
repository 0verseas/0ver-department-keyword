#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os

import data_model
from ckiptagger import WS, POS, NER  # 斷詞、詞性標記、命名實體識別


def main():
	# 先檢查模型存在與否
	if not os.path.isdir("./data"):
		print("下載模型")
		data_model.download()

	# 範例用
	ths = ['和我簽下契約，成為魔法少女吧', '魔法和奇蹟都是真實存在的', '那樣的話，大家不就只能去死了嗎', '已經沒什麼好害怕的了', '星光迴路遮斷器', '那是什麼，能吃嗎？', '你為什麼這麼熟練阿', '這麼可愛一定是男孩子', '不要瞎掰好嗎', '並沒有', '希望有一天，你能與珍愛的人重逢']
	ckip(ths)


def ckip(keywords):
	""" CKIP Lab Chinese NLP """

	# 將三份工具的模型路徑指向我們剛才下載的模型
	# Load model
	ws = WS("./data")
	pos = POS("./data")
	ner = NER("./data")

	# 分析文本
	ws_results = ws(keywords)
	pos_results = pos(ws_results)
	ner_results = ner(ws_results, pos_results)  # ner(文本, POS結果)

	# 結果
	print(ws_results)  # 斷詞
	print(pos_results)  # 詞性
	for name in ner_results[0]:  # 實體辨識
	    print(name)

	# release memory
	del ws
	del pos
	del ner


if __name__ == '__main__':
	main()
