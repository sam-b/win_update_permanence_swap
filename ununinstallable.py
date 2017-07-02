#technique taken from http://borncity.com/win/2016/10/21/windows-updates-fehlende-deinstallation-erzwingen/
import glob
import sys
import ctypes

if ctypes.windll.shell32.IsUserAnAdmin() != 1:
	print "you'll need to be an admin..."
	sys.exit(1)

if len(sys.argv) < 3:
	print 'python ununinstallable.py (perm|remov) $KBNAME, example: python ununinstallable.py remov KB3200970'
	sys.exit(1)

update = sys.argv[2]
packages = "C:\\Windows\\servicing\\Packages\\"

if sys.argv[1] == 'perm':
	find = 'removable'
	replace = 'permanent'
elif sys.argv[1] == 'remov':
	find = 'permanent'
	replace = 'removable'
else:
	print 'python ununinstallable.py (perm|remov) $KBNAME, example: python ununinstallable.py remov KB3200970'
	sys.exit(1)

for package in glob.glob(packages + '*' + update + "*.mum"):
	out = ''
	with open(package, 'r') as f:
		package_data = f.read()
	if 'permanence' in package_data:
		out = package_data.replace(find, replace)
	else:
		start = package_data.find('restart')
		out += package_data[:start]
		out += "permanence=\"" + replace + "\" "
		out += package_data[start:]
	
	with open(package, 'w') as f:
		f.write(out)
		f.flush()