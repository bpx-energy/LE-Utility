import sys
sys.path.append('../')

class Window(QtGui.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 500, 300)
        self.SetWindowTitle()
        

def TestMethod():
    print('Test')
