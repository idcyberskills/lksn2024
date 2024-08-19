class Node:
	def __init__(self, value):
		self.value = value
		self.next = None

class Stack:
	def __init__(self):
		self.head = Node("LKSN")
		self.size = 0

	def __str__(self):
		cur = self.head.next
		out = ""
		while cur:
			out += str(cur.value)
			cur = cur.next
		return out

	def push(self, value):
		node = Node(value)
		node.next = self.head.next
		self.head.next = node
		self.size += 1

if __name__ == "__main__":
	stack = Stack()
	flag = input("Flag = ")
	flag = flag.split("LKSN{")[1].split("}")[0]
	for i in flag:
		stack.push(i)
	if str(stack) != "can_you_read_this?":
		print("Flag is wrong!")
	else:
		print("Flag is correct!")
