# -*- coding: utf-8 -*-


from ckiptagger import data_utils


def download():
	# 到 Google drive 上下載模型
	data_utils.download_data_gdown("./")


if __name__ == '__main__':
	main()
