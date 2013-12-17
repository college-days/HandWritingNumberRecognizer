## 数据预处理以及各个模型计算结果的统计
* semeion.txt 是直接从官网上粘下来的数据，用.data一样的
* processdata.py 是处理semeion.txt中的数据成图像数据，保存在semeionsamples路径中
* statistic.py 是遍历semeionsamples路径，统计0-9数字训练样本的数量各是多少并将结果存在staticResult.txt中
* accuracy.py 是利用staticResult.txt以及下面算法中得到的分类结果来计算算法的正确率，并把结果写在accuracyresult路径中
* filetoimage.py 是将semeionsamples下的所有文本格式的文件转换为图片并保存在semeionimages路径下
