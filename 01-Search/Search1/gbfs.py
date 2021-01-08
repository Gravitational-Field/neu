# -*- encoding: utf-8 -*-


import pandas as pd
from pandas import Series, DataFrame

# 城市信息：city1 city2 path_cost
_city_info = None

# 按照路径消耗进行排序的FIFO,低路径消耗在前面
_frontier_priority = []


# 节点数据结构
class Node:
	def __init__(self, state, parent, action, path_cost, line_cost):

		self.state = state
		self.parent = parent
		self.action = action
		self.path_cost = path_cost
		# line_cost:代表距离上海的直线距离(单位为：10km)
		self.line_cost = line_cost
		self.evaluate_cost = path_cost+line_cost



def import_city_info():
	global _city_info
	data = [
			{'city1': '北京', 'city2': '天津', 'path_cost': 33, 'line_cost': 105},
			{'city1': '北京', 'city2': '石家庄', 'path_cost': 42, 'line_cost': 105},
			{'city1': '石家庄', 'city2': '郑州', 'path_cost': 51, 'line_cost': 98},
			{'city1': '天津', 'city2': '济南', 'path_cost': 63, 'line_cost': 93},
			{'city1': '济南', 'city2': '南京', 'path_cost': 88, 'line_cost': 71},
			{'city1': '郑州', 'city2': '南京', 'path_cost': 62, 'line_cost': 83},
			{'city1': '郑州', 'city2': '合肥', 'path_cost': 73, 'line_cost': 83},
			{'city1': '合肥', 'city2': '杭州', 'path_cost': 47, 'line_cost': 40},
			{'city1': '杭州', 'city2': '上海', 'path_cost': 31, 'line_cost': 16},
			{'city1': '南京', 'city2': '上海', 'path_cost': 41, 'line_cost': 26},
			{'city1': '北京', 'city2': '沈阳', 'path_cost': 87, 'line_cost': 105},
			{'city1': '沈阳', 'city2': '长春', 'path_cost': 48, 'line_cost': 117},
			{'city1': '长春', 'city2': '哈尔滨', 'path_cost': 46, 'line_cost': 145},
			{'city1': '沈阳', 'city2': '大连', 'path_cost': 56, 'line_cost': 117},
			{'city1': '大连', 'city2': '上海', 'path_cost': 124, 'line_cost': 84},
			{'city1': '合肥', 'city2': '武汉', 'path_cost': 51, 'line_cost': 40},
			{'city1': '合肥', 'city2': '南昌', 'path_cost': 58, 'line_cost': 40},
			{'city1': '武汉', 'city2': '长沙', 'path_cost': 43, 'line_cost': 69},
			{'city1': '南昌', 'city2': '长沙', 'path_cost': 38, 'line_cost': 60},
			{'city1': '长沙', 'city2': '广州', 'path_cost': 57, 'line_cost': 88},
			{'city1': '广州', 'city2': '香港', 'path_cost': 13, 'line_cost': 121},
			{'city1': '广州', 'city2': '澳门', 'path_cost': 10, 'line_cost': 121},
			{'city1': '杭州', 'city2': '福州', 'path_cost': 47, 'line_cost': 16},
			{'city1': '福州', 'city2': '台北', 'path_cost': 25, 'line_cost': 61},
			{'city1': '上海', 'city2': '杭州', 'path_cost': 31, 'line_cost': 0},
			{'city1': '香港', 'city2': '广州', 'path_cost': 13, 'line_cost': 122},
			{'city1': '澳门', 'city2': '广州', 'path_cost': 10, 'line_cost': 129},
			{'city1': '哈尔滨', 'city2': '长春', 'path_cost': 46, 'line_cost': 165},
			{'city1': '台北', 'city2': '福州', 'path_cost': 25, 'line_cost': 69}
	]

	_city_info = DataFrame(data, columns=['city1', 'city2', 'path_cost', 'line_cost'])
	print(_city_info)


# 判断节点是否在优先级队列中
def is_node_in_frontier(frontier, node):
	for x in frontier:
		if node.state == x.state:
			return True
	return False


# 贪婪最佳优先搜索
def greedy_best_first_search(src_state, dst_state):
	global _city_info, _frontier_priority
	line_cost = 9999
	# 从_city_info中查找src_state,并获得line_cost
	for i in range(len(_city_info)):
		if _city_info['city1'][i] == src_state:
			line_cost = _city_info['line_cost'][i]
			break

	# print(line_cost)

	node = Node(src_state, None, None, 0, line_cost)
	frontier_priority_add(node)
	explored = []

	while True:
		if len(_frontier_priority) == 0:  # 未找到
			return False
		node = _frontier_priority.pop(0)
		if node.parent is not None:
			print('处理城市节点:%s\t父节点:%s\t直线路径损失估计为:%d' % (node.state, node.parent.state, node.line_cost))
		else:
			print('处理城市节点:%s\t父节点:%s\t直线路径损失估计为:%d' % (node.state, None, node.line_cost))

		# 目标测试
		if node.state == dst_state:
			print('\t 目的地已经找到了')
			return node
		explored.append(node.state)

		# 遍历子节点
		for i in range(len(_city_info)):  # 找到待扩展的城市node
			dst_city = ''
			if _city_info['city1'][i] == node.state:
				dst_city = _city_info['city2'][i]
			# elif _city_info['city2'][i] == node.state:
			# 	dst_city = _city_info['city1'][i]
			if dst_city == '':
				continue

			# 此时找到了相邻的节点，需要找到其city1
			# 由于特殊的存储结构，只有城市为city1，才能找到该城市距离最终目的地的直线距离
			for j in range(len(_city_info)):
				if _city_info['city1'][j] == dst_city:
					line_cost = _city_info['line_cost'][j]
					break
					# print(line_cost)

			# 如果子节点的名字与爷爷节点名字一致，则跳过
			# if dst_city == node.parent:
			# 	continue
			if dst_city in explored:
				continue

			child = Node(dst_city, node, 'go', node.path_cost + _city_info['path_cost'][i], line_cost)
			print('\t孩子节点:%s 直线路径损失估计为:%d' % (child.state, child.line_cost))

			# 子节点不在explored列表，也不再优先级队列中时
			if child.state not in explored and not is_node_in_frontier(_frontier_priority, child):
				frontier_priority_add(child)
				print('\t\t 添加孩子到优先队列')
			elif is_node_in_frontier(_frontier_priority, child):
				frontier_priority_add(child)
				print('\t\t 添加孩子到优先队列')
				# 已经在优先级队列中的节点，替代为路径消耗少的节点
				# frontier_priority_replace_by_priority(child)
		print("-------------------------------------------------------")


def frontier_priority_add(node):
	"""
	:param Node node:
	:return:
	"""
	global _frontier_priority
	size = len(_frontier_priority)
	# 在这里组织优先级队列的数据
	for i in range(size):
		if node.line_cost < _frontier_priority[i].line_cost:
			_frontier_priority.insert(i, node)
			return
	_frontier_priority.append(node)


# def frontier_priority_replace_by_priority(node):
# 	"""
# 	:param Node node:
# 	:return:
# 	"""
# 	global _frontier_priority
# 	size = len(_frontier_priority)
# 	for i in range(size):
# 		if _frontier_priority[i].state == node.state and _frontier_priority[i].line_cost > node.line_cost:
# 			print('\t\t 替换状态: %s 旧的损失:%d 新的损失:%d' % (node.state, _frontier_priority[i].line_cost,node.line_cost))
# 			_frontier_priority[i] = node
# 			return

def main():
	global _city_info
	import_city_info()

	while True:
		src_city = input('输入初始城市\n')
		dst_city = input('输入目的城市\n')
		result = greedy_best_first_search(src_city, dst_city) # 进行GBFS查找

		printRoute(result,src_city,dst_city)


def printRoute(result,src_city,dst_city):
	if not result:
		print('从城市: %s 到城市 %s 查找失败' % (src_city, dst_city))
	else:  # 找到结果，进行输出
		print('从城市: %s 到城市 %s 查找成功' % (src_city, dst_city))
		path = []
		while True:  # 将路径组织进path中
			path.append(result.state)
			if result.parent is None:
				break
			result = result.parent
		size = len(path)
		for i in range(size):
			if i < size - 1:
				print('%s->' % path.pop(), end='')
			else:
				print(path.pop())



if __name__ == '__main__':
	main()