import ctypes,json,sys
from ctypes import wintypes as W
from pathlib import Path
assert sys.version_info[:3]==(3,11,15) and sys.flags.safe_path and sys.dont_write_bytecode
class US(ctypes.Structure):
    _fields_=[('Length',W.USHORT),('MaximumLength',W.USHORT),('Buffer',W.LPWSTR)]
class OA(ctypes.Structure):
    _fields_=[('Length',W.ULONG),('RootDirectory',W.HANDLE),('ObjectName',ctypes.POINTER(US)),('Attributes',W.ULONG),('SecurityDescriptor',W.LPVOID),('SecurityQualityOfService',W.LPVOID)]
class IOS(ctypes.Structure):
    _fields_=[('StatusOrPointer',ctypes.c_void_p),('Information',ctypes.c_size_t)]
nt=ctypes.WinDLL('ntdll'); create=nt.NtCreateFile
create.restype=W.LONG
create.argtypes=[ctypes.POINTER(W.HANDLE),W.DWORD,ctypes.POINTER(OA),ctypes.POINTER(IOS),W.LPVOID,W.ULONG,W.ULONG,W.ULONG,W.ULONG,W.LPVOID,W.ULONG]
k=ctypes.WinDLL('kernel32',use_last_error=True);k.CloseHandle.argtypes=[W.HANDLE];k.CloseHandle.restype=W.BOOL
p='\\??\\'+str(Path.cwd())
rows=[]
for flag in (0x40,0x1040):
    buf=ctypes.create_unicode_buffer(p);s=US(len(p.encode('utf-16-le')),len(p.encode('utf-16-le')),ctypes.cast(buf,W.LPWSTR));a=OA(ctypes.sizeof(OA),None,ctypes.pointer(s),flag,None,None)
    h=W.HANDLE();io=IOS()
    status=create(ctypes.byref(h),0x100080,ctypes.byref(a),ctypes.byref(io),None,0,7,1,0x21,None,0)
    rows.append(dict(flags=hex(flag),status=hex(status&0xffffffff),handle_opened=bool(h.value)))
    if h.value:assert k.CloseHandle(h)
print(json.dumps(dict(executable=sys.executable,version=sys.version,cwd=str(Path.cwd()),read_only_directory_opens=rows),indent=2))
