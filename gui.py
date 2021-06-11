import sys
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.ticker as ticker
import queue
import numpy as np
import sounddevice as sd
import argparse

from PyQt5 import QtCore, QtWidgets,QtGui
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtMultimedia import QAudioDeviceInfo,QAudio,QCameraInfo

parser = argparse.ArgumentParser(description='Start the Alias gui.')
parser.add_argument('deviceNumber', metavar='N', type=int,
                    help='Specify the sounddevice to use.')
args = parser.parse_args()

input_audio_deviceInfos = sd.query_devices()#QAudioDeviceInfo.availableDevices(QAudio.AudioInput)

class MplCanvas(FigureCanvas):
	def __init__(self, parent=None, width=5, height=4, dpi=100):
		fig = Figure(figsize=(width, height), dpi=dpi)
		self.axes = fig.add_subplot(111)
		super(MplCanvas, self).__init__(fig)
		fig.tight_layout()

class Alias_Effect_APP(QtWidgets.QMainWindow):
	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		self.ui = uic.loadUi('main.ui',self)
		self.resize(888, 600)
		icon = QtGui.QIcon()
		self.setWindowIcon(icon)
		self.UiComponents()
		self.threadpool = QtCore.QThreadPool()	
		self.devices_list= []
		for device in range(0,len(input_audio_deviceInfos)):
			self.devices_list.append(input_audio_deviceInfos[device]['name'])
		
		self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
		self.ui.gridLayout_4.addWidget(self.canvas, 2, 1, 1, 1)
		self.reference_plot = None
		self.q = queue.Queue(maxsize=20)

		self.device = args.deviceNumber
		self.window_length = 1000
		self.downsample = 1
		self.channels = [1]
		self.interval = 30
		self.aa = False
		self.killThread = False
		
		self.device_info =  sd.query_devices(self.device, 'input')
		self.samplerate = self.device_info['default_samplerate']
		print(self.samplerate)
		self.aaSamplerate = 1000
		self.length  = int(self.window_length*self.samplerate/(1000*self.downsample))
		sd.default.samplerate = self.samplerate
		
		self.plotdata =  np.zeros((self.length,len(self.channels)))
		
		self.update_plot()
		self.timer = QtCore.QTimer()
		self.timer.setInterval(self.interval) #msec
		self.timer.timeout.connect(self.update_plot)
		self.timer.start()
		self.pushButton_3.clicked.connect(self.aaOn)

		self.start_worker()

	def UiComponents(self):
		self.showFullScreen()
		
	def resetPlotData(self):
		if self.aa:
			self.length  = int(self.window_length*self.aaSamplerate/(1000*self.downsample))
			self.plotdata= np.resize(self.plotdata, (self.length,len(self.channels)))
		else:
			self.length  = int(self.window_length*self.samplerate/(1000*self.downsample))
			self.plotdata = np.resize(self.plotdata, (self.length,len(self.channels)))
	
	def getAudio(self):
		try:
			def audio_callback(indata,outdata,frames,time,status):
				if self.aa:
					divider = 32
					for i in range(indata.size):
						if i%divider == 0:
							current = indata[i]
						else:
							indata[i] = current
				outdata[:] = indata
				self.q.put(outdata[::self.downsample,[0]])
			self.stream  = sd.Stream( device = (self.device, self.device), blocksize=256, channels = max(self.channels), dtype = 'float32', latency = 'low' , samplerate =self.samplerate, callback  = audio_callback)
			with self.stream:
				input()
		except Exception as e:
			print("ERROR: ",e)

	def start_worker(self):
		self.worker = Worker(self.start_stream, )
		self.threadpool.start(self.worker)

	def start_stream(self):
		self.pushButton_3.setEnabled(True)
		self.pushButton_3.setText("Alias-Effect An")
		self.getAudio()

	def aaOn(self):
		if not self.aa:
			#self.pushButton_4.setEnabled(True)
			self.pushButton_3.setText("Alias-Effect Aus")
			self.checkBox.setChecked(True)
			self.killThread = True
			self.aa = True
			self.update_plot()
		else:
			self.pushButton_3.setText("Alias-Effect An")
			#self.pushButton_4.setEnabled(False)
			self.checkBox.setChecked(False)
			self.killThread = True
			self.aa = False
			self.update_plot()
		
	def update_now(self,value):
		self.device = self.devices_list.index(value)
		print('Device:',self.devices_list.index(value))

	def update_window_length(self,value):
		self.window_length = int(value)
		length  = int(self.window_length*self.samplerate/(1000*self.downsample))
		self.plotdata =  np.zeros((length,len(self.channels)))
		self.update_plot()

	def update_sample_rate(self,value):
		self.samplerate = int(value)
		sd.default.samplerate = self.samplerate
		length  = int(self.window_length*self.samplerate/(1000*self.downsample))
		self.plotdata =  np.zeros((length,len(self.channels)))
		self.update_plot()
	
	def update_down_sample(self,value):
		self.downsample = int(value)
		length  = int(self.window_length*self.samplerate/(1000*self.downsample))
		self.plotdata =  np.zeros((length,len(self.channels)))
		self.update_plot()

	def update_interval(self,value):
		self.interval = int(value)
		self.timer.setInterval(self.interval) #msec
		self.timer.timeout.connect(self.update_plot)
		self.timer.start()

	def update_plot(self):
		try:
			data=[0]
			
			while True:
				try: 
					data = self.q.get_nowait()
				except queue.Empty:
					break
				if self.reference_plot is None:
					self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
					self.ui.gridLayout_4.addWidget(self.canvas, 2, 1, 1, 1)
				shift = len(data)
				self.plotdata = np.roll(self.plotdata, -shift,axis = 0)
				self.plotdata[-shift:,:] = data
				self.ydata = self.plotdata[:]
				self.canvas.axes.set_facecolor((0,0,0))
				
      
				if self.reference_plot is None:
					plot_refs = self.canvas.axes.plot( self.ydata, color=(0,1,0.29))
					self.reference_plot = plot_refs[0]				
				else:
					self.reference_plot.set_ydata(self.ydata)

			
			self.canvas.axes.yaxis.grid(True,linestyle='--')
			start, end = self.canvas.axes.get_ylim()
			self.canvas.axes.yaxis.set_ticks(np.arange(start, end, 0.1))
			self.canvas.axes.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.1f'))
			self.canvas.axes.set_ylim( ymin=-0.5, ymax=0.5)		
			self.canvas.draw()
		except:
			pass


class Worker(QtCore.QRunnable):

	def __init__(self, function, *args, **kwargs):
		super(Worker, self).__init__()
		self.function = function
		self.args = args
		self.kwargs = kwargs

	@pyqtSlot()
	def run(self):

		self.function(*self.args, **self.kwargs)		
		



app = QtWidgets.QApplication(sys.argv)
mainWindow = Alias_Effect_APP()
mainWindow.show()
sys.exit(app.exec_())
