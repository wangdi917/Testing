import numpy as np
import pandas as pd
from scipy import stats, integrate
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import seaborn as sns

# matplotlib、pylab、pyplot这些模块其实功能都相同，程序运行的时候都在运行相同的code，不同的是导入模块的方式不同。matplotlib有两个使用接口：一种是状态机层的接口，通过pyplot模块
# 来进行管理；另一种是面向对象的接口。为了方便快速绘图，matplotlib通过pyplot模块提供了一套和Matlab类似的绘图API，将众多绘图对象所构成的复杂结构隐藏在这套API内部。
# pylab是matplotlib面向对象绘图库的一个接口。它的语法和Matlab十分相似。pylab将所有的功能函数（pyplot状态机函数和numpy的大部函数）结合，既可以画图又可以进行简单的计算。
# 这样可以很好地与ipython或者类似的IDE比如pycharm实现很好的交互模式。
# 应该分开导入pyplot和pylab，即import matplotlib.pyplot as plt、import numpy as np等同于from pylab import *。

# 数据可视化 https://www.cnblogs.com/kylinlin/p/5232602.html, https://www.cnblogs.com/kylinlin/p/5234223.html, https://www.cnblogs.com/kylinlin/p/5236601.html
# 介绍Seaborn库 https://blog.csdn.net/ruoyunliufeng/article/details/78976083, https://blog.csdn.net/baibaibai66/article/details/51297230, https://www.kesci.com/home/project/59f687e1c5f3f511952baca0


def seaborn_plot1():
	# 单变量分布图
	sns.set_style("dark") # Seaborn有五个预设好的主题：darkgrid, whitegrid, dark, white, ticks。
	sns.set(style="whitegrid", palette="deep", color_codes=True) # Seaborn有五个预设好的主题：deep, muted, pastel, bright, dark, colorblind。
	# plt.plot(np.arange(10))

	# 多变量分布图
	mean, cov = [0,1], [(1,0.5), (0.5,1)]
	data = np.random.multivariate_normal(mean, cov, 200)
	df = pd.DataFrame(data, columns=['x','y'])
	print ("\nNow the frame is:\n", df.head())
	# x, y = np.random.multivariate_normal(mean, cov, 1000).T 这样就不必写data=df了。
	sns.jointplot(x='x', y='y', data=df)

	# 多变量分布图的六边形图
	sns.jointplot(x='x', y='y', kind='hex', data=df)

	# 多变量分布图的核密度函数
	sns.jointplot(x='x', y='y', kind='kde', data=df)

	# 多变量分布图的多维核密度函数
	fig, axes = plt.subplots(figsize=(6, 6))
	sns.kdeplot(df.x, df.y, axes=axes)
	sns.rugplot(df.x, color='g', axes=axes)
	sns.rugplot(df.y, color='r', vertical=True, axes=axes) # vertical控制y列数据是否垂直放置。
	# 多变量分布图的多维核密度函数（增加轮廓线）
	cmap = sns.cubehelix_palette(as_cmap=True, dark=0, light=1, reverse=True)
	sns.kdeplot(df.x, df.y, cmap=cmap, n_levels=60, shade=True)
	# 多变量分布图的多维核密度函数（增加图层）
	joint = sns.jointplot(x='x', y='y', data=df, kind='kde', color='m')
	joint.plot_joint(plt.scatter, c='w', s=30, linewidth=1, marker='+')
	joint.ax_joint.collections[0].set_alpha(0)
	joint.set_axis_labels("$X$", "$Y$") # 可以使用markdown语法。

	# 直方图和核密度函数（抹掉直方的直方图）
	randgen = np.random.RandomState(10) # 对于某一个伪随机数发生器，只要种子RandomState(seed)相同，产生的随机数序列就是相同的。
	x = randgen.normal(size=100)
	fig, axes = plt.subplots(2, 2, figsize=(7, 7), sharex=True)
	sns.distplot(x, color='m', ax=axes[0, 0])
	sns.distplot(x, kde=False, color='b', ax=axes[0, 1])
	# sns.distplot(x, hist=False, rug=True, color='r', ax=axes[0, 1])
	sns.kdeplot(x, bw=0.2, label='bandwidth=0.2', color='r', shade=True, ax=axes[1, 0])
	sns.distplot(x, label='bandwidth=2', hist=False, color='g', kde_kws={'shade': True}, ax=axes[1, 1])

	plt.show()


def seaborn_plot2():
	titanic = pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/master/titanic.csv")
	# 条形图
	sns.barplot(x='sex', y='survived', hue='pclass', data=titanic)
	plt.show()
	# 观察值图
	sns.countplot(x='deck', data=titanic, palette='Greens_d')
	plt.show()
	sns.countplot(x='deck', hue='pclass', data=titanic, palette='Reds_d')
	plt.show()
	# 线形图
	sns.pointplot(x='sex', y='survived', hue='class', data=titanic, palette={'First':'g', 'Second':'m', 'Third':'b'}, markers=['^','o','+'], linestyles=['-','--',''])
	plt.show()

	iris = pd.read_csv("D:\Programming\Testing\iris.csv") # read_csv("", delimiter='\t')
	# 多个成对的双变量分布图
	sns.pairplot(iris, hue='variety')
	# 多个成对的双变量分布图（增加图层）
	pair = sns.PairGrid(iris)
	pair.map_diag(sns.kdeplot)
	pair.map_offdiag(sns.kdeplot, cmap='Blues_d', n_levels=6)
	plt.show()
	# 热点图
	# iris_cov = iris.corr()
	# sns.heatmap(iris_cov)
	# plt.show()

	tips = pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv")
	# 分类散点图
	sns.stripplot(x='day', y='total_bill', data=tips)
	plt.show()
	# 分类散点图，添加一些随机的“抖动”来避免分类轴上的数据重叠
	sns.stripplot(x='day', y='total_bill', data=tips, jitter=True)
	plt.show()
	# 蜂窝散点图，使用算法来避免分类轴上的数据重叠
	sns.swarmplot(x='day', y='total_bill', data=tips, hue='sex') # 当两个变量都是categorical时更加明显。
	plt.show()
	# 箱型图，显示了3个四分位数值和极值，“晶须”延伸到位于下四分位数和上四分位数的1.5IQR内的点
	sns.boxplot(x='day', y='total_bill', hue='time', data=tips)
	plt.show()
	# 琴型图，结合箱型图和核密度估计过程
	sns.violinplot(x='total_bill', y='day', hue='time', data=tips)
	plt.show()
	sns.violinplot(x='total_bill', y='day', hue='time', split=True, data=tips)
	plt.show()

	# # 多子图面板图
	# sns.factorplot(x='time', y='total_bill', hue='smoker', col='day', data=tips, kind='box', size=4, aspect=0.5) # 按time即day分成若干个子图
	# plt.show()
	# sns.factorplot(x='day', y='total_bill', hue='smoker', col='time', data=tips, kind='swarm') # 按day即time分成若干个子图
	# plt.show()


def seaborn_plot3():
	N = 500
	current_palette = sns.color_palette('muted', n_colors=4)
	cmap = ListedColormap(sns.color_palette(current_palette).as_hex())
	data1 = np.random.randn(N)
	data2 = np.random.randn(N)
	colors = np.random.randint(0, 10, N)
	plt.scatter(data1, data2, c=colors, cmap=cmap)
	plt.colorbar()

	# regplot()和lmplot()都可以绘制线性回归曲线。区别是，regplot()接受各种格式的x和y，比如numpy arrays、pandas series、pandas Dataframe，而lmplot()只接受字符串对象，
	# 即long-form或tidy。除了输入数据的便利性外，regplot()可以看做拥有lmplot()特征的一个子集。https://blog.csdn.net/wuwan5296/article/details/78698125
	x = 10 ** np.arange(1, 10)
	y = x ** 2
	data = pd.DataFrame(data = {'x': x, 'y': y})
	grid = sns.lmplot('x', 'y', data, size=8, truncate=False, scatter_kws = {'s':100})
	grid.set_xticklabels(rotation = 45)

	plt.show()



if __name__ == "__main__":
	print ("\nOK!\n")
	# seaborn_plot1()
	seaborn_plot2()
	# seaborn_plot3()
	print ("\nDone!\n")
	