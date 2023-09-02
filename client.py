from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtGui
from PyQt5.QtGui import *
from threading import Thread
import socket
import sys
import ctypes


# 页面实例
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
class MainWin(QMainWindow):
    def __init__(self, parent=None):
        super(MainWin, self).__init__(parent)

        self.pc = None  # 预设这个变量

        self.MainSet()
        self.createWidget()
        self.componentWidgets()

    # 设定Main窗口属性的函数
    def MainSet(self):
        self.setWindowTitle("HOPE CHAT")
        self.setWindowIcon(QtGui.QIcon("hope-chat.ico"))

    # self.setFixedSize(600,400)

    # 加载控件
    def createWidget(self):
        self.centerWidget = QWidget()  # 中心窗口控件

        self.mainLayout = QGridLayout()
        self.rightTopLayout = QGridLayout()
        self.rightBottomLayout = QVBoxLayout()

        self.ConfigBox = QGroupBox("连接信息")
        self.ContralBox = QGroupBox("控制面板")

        self.chatEdit = QTextEdit()  # 聊天对话框
        self.inputLine = QLineEdit()  # 输入框
        self.sendBtn = QPushButton("发送")  # 发送按钮
        self.sendBtn.clicked.connect(self.sendInfo)  # 向服务器发送信息(如果是服务器本身则广播)
        self.clearBtn = QPushButton("清空")  # 清空按钮
        self.clearBtn.clicked.connect(lambda: self.inputLine.clear())

        self.ipEdit = QLineEdit()  # IP输入栏
        self.ipEdit.setInputMask('000.000.000.000; ')  # 设定为IP输入格式
        self.hostIPbtn = QPushButton("获得本机IP")  # 点击直接获得本机IP
        self.hostIPbtn.clicked.connect(self.getHostIP)
        self.portEdit = QLineEdit()  # 端口输入栏
        self.portEdit.setPlaceholderText("9999")  # 默认端口为9999
        self.hostEdit = QLineEdit()  # 主机名输入栏
        self.hostEdit.setPlaceholderText(socket.gethostname())  # 默认为本地主机
        self.hostEdit.setVisible(False)
        self.serverRbtn = QRadioButton("建立聊天")  # 选择为服务器
        self.serverRbtn.setChecked(True)
        self.serverRbtn.toggled.connect(self.radiobtnChange)
        self.clientRbtn = QRadioButton("加入聊天")  # 选择为客户端

        self.connectBtn = QPushButton("连接服务器")  # 连接服务器按钮
        self.connectBtn.clicked.connect(self.setClient)
        self.connectBtn.setEnabled(False)
        self.buildServerBtn = QPushButton("建立服务器")  # 建立服务器按钮
        self.buildServerBtn.clicked.connect(self.setServer)
        self.quitBtn = QPushButton("退出")  # 退出按钮
        self.quitBtn.clicked.connect(self.quit)
        # ---------------------------------------------------------
        self.statusBar = QStatusBar()  # 状态栏

    # 组装控件
    def componentWidgets(self):
        self.setCentralWidget(self.centerWidget)
        self.setStatusBar(self.statusBar)
        # --------------------------------------------------------
        self.centerWidget.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.chatEdit, 0, 0, 6, 2)
        self.mainLayout.addWidget(self.inputLine, 6, 0, 1, 2)
        self.mainLayout.addWidget(self.sendBtn, 7, 0, 1, 1)
        self.mainLayout.addWidget(self.clearBtn, 7, 1, 1, 1)
        self.mainLayout.addWidget(self.ConfigBox, 0, 2, 5, 1)
        self.mainLayout.addWidget(self.ContralBox, 5, 2, 3, 1)

        self.ConfigBox.setLayout(self.rightTopLayout)
        self.rightTopLayout.addWidget(QLabel("服务器IP"), 0, 0, 1, 4)
        self.rightTopLayout.addWidget(self.ipEdit, 1, 0, 1, 3)
        self.rightTopLayout.addWidget(self.hostIPbtn, 1, 3, 1, 1)
        self.rightTopLayout.addWidget(QLabel("服务器端口"), 2, 0, 1, 1)
        self.rightTopLayout.addWidget(self.portEdit, 2, 1, 1, 3)
        self.rightTopLayout.addWidget(QLabel(f"你的昵称是：{sys.argv[1]}"), 3, 0, 1, 1)
        self.rightTopLayout.addWidget(self.hostEdit, 3, 1, 1, 3)
        self.rightTopLayout.addWidget(self.serverRbtn, 4, 0, 1, 2)
        self.rightTopLayout.addWidget(self.clientRbtn, 4, 2, 1, 2)

        self.ContralBox.setLayout(self.rightBottomLayout)
        self.rightBottomLayout.addWidget(self.connectBtn)
        self.rightBottomLayout.addWidget(self.buildServerBtn)
        self.rightBottomLayout.addWidget(self.quitBtn)

    # 静置函数 - 用于写事件函数-------------------------
    # 单选按钮切换函数
    def radiobtnChange(self, status):
        if status:
            self.connectBtn.setEnabled(False)
            self.buildServerBtn.setEnabled(True)
        else:
            self.connectBtn.setEnabled(True)
            self.buildServerBtn.setEnabled(False)

    def getHostIP(self):
        hostip = socket.gethostbyname_ex(socket.gethostname())
        self.ipEdit.setText(hostip[-1][-1])

    # 状态栏情况发送函数
    def sendInfo(self):
        if self.pc == None:
            self.statusBar.showMessage("请先连接至服务器!!")
        else:
            info = self.inputLine.text()
            if info != "":
                info = self.pc.hostName + ":\n" + info
                self.pc.btnsend(info)
            else:
                self.statusBar.showMessage("不能为空!")

    # 设定本主机为服务器
    def setServer(self):
        host = self.hostEdit.text()
        port = self.portEdit.text()
        ip = self.ipEdit.text()
        print(ip)
        if host == "": host = str(sys.argv[1])   # 服务主机
        if port == "": port = 9999  # 默认端口
        if ip == "...": ip = "127.0.0.1"  # 默认IP
        self.pc = Server(self, ip, host, int(port))

    # 设定本主机为客户端
    def setClient(self):
        host = self.hostEdit.text()
        port = self.portEdit.text()
        ip = self.ipEdit.text()
        if host == "": host = str(sys.argv[1])   # 匿名用户
        if port == "": port = 9999  # 默认端口
        if ip == "...": ip = "127.0.0.1"  # 默认IP
        self.pc = Client(self, ip, host, int(port))

    def quit(self):
        if self.pc != None:
            self.pc.closeThread()
        self.close()


# 服务端
class Server():
    def __init__(self, widget, ip, host, port):
        # 设定本主机的一些基本信息 ---------------------------------------
        self.widget = widget
        self.ip = ip  # 获得该主机ip
        self.hostName = host  # 获得该主机名
        self.port = port  # 设定默认端口号(服务器端口号和客户端接入端口号都是这个默认端口)
        self.serverDict = {}  # 服务线程字典
        self.serverID = 0  # 初始的服务线程id

        self.buildSocket()

    # 创建网络连接实例
    def buildSocket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # socket.AF_INET(!!INET - IPv4  INET6 - IPv6)
        # socket.SOCK_STREAM - 传输控制协议(TCP)
        self.initialServer()

    # 初始化服务(仅限服务器)
    def initialServer(self):
        # 首先绑定服务端口号
        self.socket.bind((self.ip, self.port))  # 绑定端口与主机名
        self.socket.listen(5)  # 设定最大连接数

        self.buildServer()  # 初始化一个服务线程

    # 创建服务线程
    def buildServer(self):
        server = ServerThread(str(self.serverID), self.socket)
        self.serverDict[str(self.serverID)] = server
        self.serverID += 1
        server._flag.connect(self.getFlag)
        server._signal.connect(self.getMessage)
        server._text.connect(self.getText)
        server.start()

    # 广播所有消息
    def bordCastInfo(self, info):
        print(len(self.serverDict))
        for client in self.serverDict:
            try:
                if self.serverDict[client].clientsocket != None:
                    print("尝试将信息广播出去")
                    self.serverDict[client].sendToClient(info)  # 将消息传入指定的客户端
                    print("广播成功")
            except Exception as reason:
                self.getFlag("@@@".join([client, "disconnect"]))  # 运行函数,停止某个客户端的监听(相当于关闭)
                print("服务端", reason)

    def btnsend(self, text):
        self.widget.chatEdit.append(text)
        self.bordCastInfo(text)

    # 关闭所有的服务
    def closeThread(self):
        for server in self.serverDict:
            self.serverDict[server].runflag = False

    def getFlag(self, flag):
        flag = flag.split("@@@")
        if flag[1] == "connect":  # 如果传来连接成功,则新开一个线程监听
            self.buildServer()
        elif flag[1] == "disconnect":  # 如果连接出现问题
            self.serverDict[flag[0]].runflag = False

    def getMessage(self, signal):
        signal = signal.split("@@@")
        self.widget.statusBar.showMessage("客户端数量:" + signal[0] + " 状态:" + signal[1])

    def getText(self, text):
        self.widget.chatEdit.append(text)
        self.bordCastInfo(text)  # 广播出去


# 客户端
class Client():  # 主机默认为本地主机,
    def __init__(self, widget, ip, hostName, port):
        self.widget = widget
        self.ip = ip
        self.hostName = hostName  # 获得该主机名
        self.port = port  # 设定默认端口号(服务器端口号和客户端接入端口号都是这个默认端口)
        self.buildSocket()

    def buildSocket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.buildClient()

    def buildClient(self):
        self.client = ClientThread(self.socket)  # 获取连接
        self.client._flag.connect(self.getFlag)
        self.client._signal.connect(self.getMessage)
        self.client._text.connect(self.getText)
        if self.client.connectServer(self.ip, self.port):
            self.client.start()

    def sendToServer(self, text):  # 向服务器发送消息
        try:
            self.socket.send(text.encode('utf-8'))
        except Exception as reason:
            self.getMessage(reason)
            self.getFlag("disconnect")  # 发送连接失败标志

    def btnsend(self, text):
        self.sendToServer(text)

    def closeThread(self):
        self.runflag = False

    def getFlag(self, flag):
        if flag == "connect":
            self.widget.statusBar.showMessage("成功连接到了服务器!!")
        elif flag == "disconnect":
            self.client.runflag = False

    def getMessage(self, signal):
        self.widget.statusBar.showMessage(signal)

    def getText(self, text):
        self.widget.chatEdit.append(text)


# 监听连接线程,负责构成会话(服务端线程)
class ServerThread(QThread):
    _signal = pyqtSignal(str)  # 设定信号,主要向主线程发送信号
    _text = pyqtSignal(str)  # 设定信号,向主线程发送接收到的信息
    _flag = pyqtSignal(str)  # 设定信号,向主线程发送连接状态标志

    def __init__(self, serverID, serverSocket):
        super(ServerThread, self).__init__()
        self.serverID = serverID  # 获得主机实例
        self.serverSocket = serverSocket
        self.clientsocket = None
        self.addr = None
        self.runflag = True

        self.connectList = ["connect", "disconnect"]  # 连接成功与连接失败

    # 自动进行该函数
    def run(self):
        self.sendMessage("等待连接......")
        self.clientsocket, self.addr = self.serverSocket.accept()  # 收到客户端的连接后返回 连接控件,地址(持续监听,直到接收到执行下一个操作)
        print(self.clientsocket)
        self.sendText("%s" % str(self.addr) + " 正在连接服务器！")
        self.sendFlag(0)  # 发送连接成功标志
        self.getMessage()

    # 持续接受消息
    def getMessage(self):
        while self.runflag:
            try:
                data = self.clientsocket.recv(1024).decode('utf-8')  # 接受到字符串并按照utf-8编译
                self.sendText(data)
            except Exception as reason:
                self.sendMessage(str(reason))
                self.sendText(str(self.addr) + "退出了服务器。")
                self.sendFlag(1)  # 发送断开连接标志
                break
        self.clientsocket.close()
        print("线程关闭成功")

    def sendToClient(self, info):
        print(self.clientsocket)
        try:
            self.clientsocket.send(info.encode("utf-8"))
            print("广播成功")
        except Exception as reason:
            print("广播失败原因", reason)
            self.sendMessage(self.addr + " 啊呀，连接断啦...")
            self.sendFlag(1)

    # 发送状态信号函数
    def sendMessage(self, message):
        self._signal.emit("@@@".join([self.serverID, message]))

    # 发送接收到的消息信号
    def sendText(self, text):
        self._text.emit(text)

    # 发送连接状态标志
    def sendFlag(self, flagIndex):
        self._flag.emit("@@@".join([self.serverID, self.connectList[flagIndex]]))


class ClientThread(QThread):
    _signal = pyqtSignal(str)
    _text = pyqtSignal(str)
    _flag = pyqtSignal(str)

    def __init__(self, serverSocket):
        super(ClientThread, self).__init__()
        self.serverSocket = serverSocket
        self.runflag = True
        self.connectList = ["connect", "disconnect"]  # 连接成功与连接失败

    def connectServer(self, ip, port):
        try:
            self.serverSocket.connect((ip, port))
            self.sendFlag(0)  # 发送连接成功标志
            return True
        except Exception as reason:
            self.sendMessage(reason)
            self.sendFlag(1)  # 发送链接失败标志
            return reason

    def run(self):
        while self.runflag:
            try:
                msg = self.serverSocket.recv(1024).decode("utf-8")  # 接受服务端消息
                self.sendText(msg)
            except Exception as reason:
                self.sendMessage(reason)
                self.sendFlag(1)  # 发送连接失败标志
                break

    def sendMessage(self, message):
        self._signal.emit(str(message))

    def sendText(self, text):
        self._text.emit(str(text))

    def sendFlag(self, flagIndex):
        self._flag.emit(str(self.connectList[flagIndex]))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWin()
    win.show()
    sys.exit(app.exec_())
