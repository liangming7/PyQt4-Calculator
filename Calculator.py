import sys
from PyQt4 import QtCore, QtGui, uic
Ui_MainWindow, QtBaseClass = uic.loadUiType("calculator_demo.ui")

class Stack():
	def __init__(self):
		self.items = []
		
	def push(self,val):
		self.items.append(val)
		
	def pop(self):
		return self.items.pop()
	
	def peek(self):
		return self.items[-1:][0]
		
	def is_empty(self):
		if self.items == []	:
			return True
		else :
			return False

class Queue:
	def __init__(self):
		self.items = []

	def is_empty(self):
		return self.items == []

	def enqueue(self,item):
		self.items.append(item)

	def dequeue(self):
		return self.items.pop(0)

	def front(self):
		return self.items[len(self.items)-1]

	def size(self):
		return len(self.items)

class Calculator():
	def __init__(self):
		self.prec = {}
		self.prec["x"] = 3
		self.prec["/"] = 3
		self.prec["+"] = 2
		self.prec["-"] = 2
		self.prec["("] = 1
		self.operators = ['+','-','x','/']
		
	def calculate(self,input_str=None):
		if input_str is None :
			return "Error"
		postfix_str = self.infix2postfix(input_str)
		#print postfix_str
		if len(postfix_str) > 0 :
			return self.eval_postfix(postfix_str)
		else :
			return "Error"	

	def infix2postfix(self,infix_str):
		out_Queue = Queue()
		operator_Stack = Stack()
		tokens = infix_str.split()
		postfix_str=""
		for token in tokens :
			try :
				d = float(token)
				out_Queue.enqueue(d)
			except :
				if token == '(':
					operator_Stack.push(token)
				elif token == ')':
					tmp = operator_Stack.pop()
					while  tmp != '(' :			
						out_Queue.enqueue(tmp)
						tmp = operator_Stack.pop()
				else : # token is an operator		
					while (not operator_Stack.is_empty()) and (self.prec[operator_Stack.peek()] >= self.prec[token]) :
						out_Queue.enqueue(operator_Stack.pop())
					operator_Stack.push(token)
			
		while not operator_Stack.is_empty() :
			out_Queue.enqueue(operator_Stack.pop())

		while not out_Queue.is_empty():
			postfix_str += str(out_Queue.dequeue())+" "

		return postfix_str

	def eval_postfix(self,postfix_str):
		operand_queue = Queue()
		operand_1=None
		operand_2=None
		tokens = postfix_str.split()
		for token in tokens :
			try :
				d = float(token)
				operand_queue.enqueue(d)
			except:
				if not operand_queue.is_empty() :
					operand_1 = operand_queue.dequeue()
				else :
					operand_1 = None	
				if not operand_queue.is_empty() :
					operand_2 = operand_queue.dequeue()	
				else :
					operand_2 = None
				if not (operand_1 is None or operand_2 is None) :					
					try:
						result = self.do_math(token,operand_1,operand_2)
					except ZeroDivisionError :
						return "Division Error"  
				else :
					result = 0	
				operand_queue.enqueue(result)
		return operand_queue.dequeue()

	def do_math(self,operator,operand1,operand2):					
		if operator == "x":
			return operand1 * operand2
		elif operator == "/":
				return operand1 / operand2
		elif operator == "+":
			return operand1 + operand2
		else:
			return operand1 - operand2
	
		
class MyApp(QtGui.QMainWindow, Ui_MainWindow):
	#on_click = pyqtSignal(str)
	
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		Ui_MainWindow.__init__(self)
		self.setupUi(self)
		self.init_ui()
		self.calculator = Calculator()

	def init_ui(self):
		self.num_btn_1.clicked.connect(self.append_text)
		self.num_btn_2.clicked.connect(self.append_text)
		self.num_btn_3.clicked.connect(self.append_text)
		self.num_btn_4.clicked.connect(self.append_text)
		self.num_btn_5.clicked.connect(self.append_text)
		self.num_btn_6.clicked.connect(self.append_text)
		self.num_btn_7.clicked.connect(self.append_text)
		self.num_btn_8.clicked.connect(self.append_text)
		self.num_btn_9.clicked.connect(self.append_text)
		self.num_btn_0.clicked.connect(self.append_text)
		self.left_paren_btn.clicked.connect(self.append_text)
		self.right_paren_btn.clicked.connect(self.append_text)
		self.plus_btn.clicked.connect(self.append_text)
		self.minus_btn.clicked.connect(self.append_text)
		self.mult_btn.clicked.connect(self.append_text)
		self.div_btn.clicked.connect(self.append_text)		
		self.dot_btn.clicked.connect(self.append_text)
		self.bsp_btn.clicked.connect(self.backspace)
		self.clear_btn.clicked.connect(self.clear_text)
		self.exe_btn.clicked.connect(self.calculate)
	
	def append_text(self):
		sender = self.sender()
		val = sender.text()
		if val in ['/','+','-','(',')','x'] :
			val = " "+val+" "
		disp = self.disp_text.text()
		disp += val
		self.disp_text.clear()
		self.disp_text.setText(disp)
		
	def backspace(self):
		self.disp_text.backspace()	
		
	def clear_text(self):
		self.disp_text.clear()		
		
	def calculate(self):
		# need to change to pythonic string
		txt = str(self.disp_text.text())		
		if len(txt) > 0 :
			result = self.calculator.calculate(txt)
			self.disp_text.clear()
			self.disp_text.setText(str(result))
			
			
		
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
