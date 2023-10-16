import win32api
import win32file
 
#
# esto esta bien
#
DRIVE_TYPES = """
0 	Unknown
1 	No Root Directory
2 	Removable Disk
3 	Local Disk
4 	Network Drive
5 	Compact Disc
6 	RAM Disk
"""
drive_types = dict((int (i), j) for (i, j) in (l.split ("\t") for l in DRIVE_TYPES.splitlines () if l))
 
drives = (drive for drive in win32api.GetLogicalDriveStrings ().split ("\000") if drive)
for drive in drives:
  print (drive, "=>", drive_types[win32file.GetDriveType (drive)])