# -*- encoding: utf-8 -*-

import pandas as pd
from pandas import Series, DataFrame

# 城市信息：city1 city2 path_cost
_city_info = None

# 按照路径消耗进行排序的队列,低路径消耗在前面
# 存储每个被扩展扩展节点的当前路径代价g(n)
_frontier_priority = []

# 节点数据结构
class Node:
	def __init__(self, state, parent, action, path_cost):
		self.state = state
		self.parent = parent
		self.action = action
		self.path_cost = path_cost


def import_city_info():
	global _city_info
	data = [
			{'city1': '北京', 'city2': '天津', 'path_cost': 33},
			{'city1': '北京', 'city2': '石家庄', 'path_cost': 42},
			{'city1': '石家庄', 'city2': '郑州', 'path_cost': 51},
			{'city1': '天津', 'city2': '济南', 'path_cost': 63},
			{'city1': '济南', 'city2': '南京', 'path_cost': 88},
			{'city1': '郑州', 'city2': '南京', 'path_cost': 62},
			{'city1': '郑州', 'city2': '合肥', 'path_cost': 73},
			{'city1': '合肥', 'city2': '杭州', 'path_cost': 47},
			{'city1': '杭州', 'city2': '上海', 'path_cost': 31},
			{'city1': '南京', 'city2': '上海', 'path_cost': 41}]

	_city_info = DataFrame(data, columns=['city1', 'city2', 'path_cost'])
	# print(_city_info)


def breadth_first_search(src_state, dst_state):
	global _city_info

	node = Node(src_state, None, None, 0)
	# 目标测试
	if node.state == dst_state:
		return node
	frontier = [node]
	explored = []

	while True:
		if len(frontier) == 0:
			return False
		node = frontier.pop(0)
		explored.append(node.state)
		if node.parent is not None:
			print('处理城市节点:%s\t父节点:%s\t路径损失为:%d' % (node.state, node.parent.state, node.path_cost))
		else:
			print('处理城市节点:%s\t父节点:%s\t路径损失为:%d' % (node.state, None, node.path_cost))

		# 遍历子节点
		for i in range(len(_city_info)):
			dst_city = ''
			if _city_info['city1'][i] == node.state:
				dst_city = _city_info['city2'][i]
			elif _city_info['city2'][i] == node.state:
				dst_city = _city_info['city1'][i]
			if dst_city == '':
				continue
			child = Node(dst_city, node, 'go', node.path_cost + _city_info['path_cost'][i])
			print('\t孩子节点:%s 路径损失为%d' % (child.state, child.path_cost))
			if child.state not in explored and not is_node_in_frontier(frontier, child):
				# 目标测试
				if child.state == dst_state:
					print('\t\t 这个孩子节点就是目的城市')
					return child
				frontier.append(child)
				print('\t\t 添加孩子节点到这个孩子')


def uniform_cost_search(src_state, dst_state):
	global _city_info, _frontier_priority

	node = Node(src_state, None, None, 0)  # state, parent, action, path_cost
	frontier_priority_add(node)
	explored = []  # 已经探索过的节点，不在进行探索。

	while True:  # 循环进行扩展以及入队和出队。
		if len(_frontier_priority) == 0:
			return False
		node = _frontier_priority.pop(0)
		if node.parent is not None:
			print('处理城市节点:%s\t父节点:%s\t路径损失为:%d' % (node.state, node.parent.state, node.path_cost))
		else:
			print('处理城市节点:%s\t父节点:%s\t路径损失为:%d' % (node.state, None, node.path_cost))

		# 目标测试
		if node.state == dst_state:
			print('\t 目的地已经找到了')
			return node
		explored.append(node.state)

		# 对于pop出来的节点，遍历其子节点，进行扩展
		for i in range(len(_city_info)):
			dst_city = ''
			if _city_info['city1'][i] == node.state:
				dst_city = _city_info['city2'][i]
			# elif _city_info['city2'][i] == node.state:
			# 	dst_city = _city_info['city1'][i]
			if dst_city == '':
				continue
			# 构建被扩展的子节点
			child = Node(dst_city, node, 'go', node.path_cost + _city_info['path_cost'][i])
			print('\t孩子节点:%s 路径损失为:%d' % (child.state, child.path_cost))

			# 子节点不在explored列表，也不在优先级队列中时，添加到优先级队列
			if child.state not in explored and not is_node_in_frontier(_frontier_priority, child):
				frontier_priority_add(child)
				print('\t\t 添加孩子到优先队列')
			elif is_node_in_frontier(_frontier_priority, child):  # 如果在explored中，代表已经找到到达该node的最优的路径了。
				# 已经在优先级队列中的节点，替代为路径消耗少的节点
				# frontier_priority_replace_by_priority(child)
				frontier_priority_add(child)
				print('\t\t 添加孩子到优先队列')

		print("------------------------------------------------------------------------------")


def frontier_priority_add(node):
	"""
	将被扩展的节点插入优先级队列
	:param Node node:
	:return:
	"""
	global _frontier_priority
	size = len(_frontier_priority)
	# 在这里组织优先级队列的数据
	for i in range(size):
		if node.path_cost < _frontier_priority[i].path_cost:
			_frontier_priority.insert(i, node)
			return
	# 代价没有比它小的，则直接插入到最后
	_frontier_priority.append(node)


# 判断节点是否在优先级队列中
def is_node_in_frontier(frontier, node):
	for x in frontier:
		if node.state == x.state:
			return True
	return False


# 更新
# def frontier_priority_replace_by_priority(node):
# 	"""
# 	:param Node node:
# 	:return:
# 	"""
# 	global _frontier_priority
# 	size = len(_frontier_priority)
# 	for i in range(size):
# 		if _frontier_priority[i].state == node.state and _frontier_priority[i].path_cost > node.path_cost:
# 			print('\t\t 替换状态: %s 旧的损失:%d 新的损失:%d' % (node.state, _frontier_priority[i].path_cost, node.path_cost))
# 			_frontier_priority[i] = node
# 			return

def main():
	global _city_info
	import_city_info()

	while True:
		src_city = input('输入初始城市\n')
		dst_city = input('输入目的城市\n')
		# result = breadth_first_search(src_city, dst_city)
		result = uniform_cost_search(src_city, dst_city) # 进行UCS查找

		printRoute(result,src_city,dst_city)


def printRoute(result,src_city,dst_city):
	if not result:
		print('从城市: %s 到城市 %s 查找失败' % (src_city, dst_city))
	else: # 找到结果，进行输出
		print('从城市: %s 到城市 %s 查找成功' % (src_city, dst_city))
		path = []
		while True: # 将路径组织进path中
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