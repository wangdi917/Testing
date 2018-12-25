import yaml
import os


def yaml_read():
	print ("\nThe yaml is:\n")

	# 获取当前脚本所在文件夹路径
	curr_path = os.path.dirname(os.path.realpath(__file__))
	# 获取yaml文件路径
	yaml_path = os.path.join(curr_path, "cluster_subclasses.md")

	# 用open方法直接打开
	f = open(yaml_path, 'r', encoding='utf-8')
	cfg = f.read()
	# print (type(cfg)) # 读出来是字符串
	# print (cfg)

	yaml_dict = yaml.load(cfg) # 用load方法转字典
	print (yaml_dict)
	print (type(yaml_dict))


if __name__ == "__main__":
	yaml_read()
	print ("\nOK!\n")
	