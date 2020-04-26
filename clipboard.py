# -*- coding: utf-8 -*-

import sys

if sys.platform == 'win32':

    import ctypes
    import ctypes.wintypes

    user32 = ctypes.WinDLL('user32')
    kernel32 = ctypes.WinDLL('kernel32')
    msvcrt = ctypes.CDLL('msvcrt')

    OpenClipboard = user32.OpenClipboard
    OpenClipboard.argtypes = ctypes.wintypes.HWND,
    OpenClipboard.restype = ctypes.wintypes.BOOL
    GetClipboardData = user32.GetClipboardData
    GetClipboardData.argtypes = ctypes.wintypes.UINT,
    GetClipboardData.restype = ctypes.wintypes.HANDLE
    EmptyClipboard = user32.EmptyClipboard
    EmptyClipboard.argtypes = None
    EmptyClipboard.restype = ctypes.wintypes.BOOL
    SetClipboardData = user32.SetClipboardData
    SetClipboardData.argtypes = (ctypes.wintypes.UINT, ctypes.wintypes.HANDLE)
    SetClipboardData.restype = ctypes.wintypes.HANDLE
    CloseClipboard = user32.CloseClipboard
    CloseClipboard.argtypes = None
    CloseClipboard.restype = ctypes.wintypes.BOOL
    GlobalLock = kernel32.GlobalLock
    GlobalLock.argtypes = ctypes.wintypes.HGLOBAL,
    GlobalLock.restype = ctypes.wintypes.LPVOID
    GlobalUnlock = kernel32.GlobalUnlock
    GlobalUnlock.argtypes = ctypes.wintypes.HGLOBAL,
    GlobalUnlock.restype = ctypes.wintypes.BOOL
    GlobalAlloc = kernel32.GlobalAlloc
    GlobalAlloc.argtypes = (ctypes.wintypes.HWND, ctypes.wintypes.UINT)
    GlobalAlloc.restype = ctypes.wintypes.HWND
    GlobalFree = kernel32.GlobalFree
    GlobalFree.argtypes = ctypes.wintypes.HGLOBAL,
    GlobalFree.restype = ctypes.wintypes.HGLOBAL
    wcscpy = msvcrt.wcscpy
    wcscpy.argtypes = (ctypes.c_wchar_p, ctypes.c_wchar_p)
    wcscpy.restype = ctypes.c_wchar_p

    GHND = 66
    CF_UNICODETEXT = 13

def get():
    if OpenClipboard(None):
        hMem = GetClipboardData(CF_UNICODETEXT)
        text = ctypes.c_wchar_p(GlobalLock(hMem)).value
        GlobalUnlock(hMem)
        CloseClipboard()
        return text

def put(text):
    hGlobalMem = GlobalAlloc(GHND, len(text.encode('UTF-16-BE')) + 2)
    lpGlobalMem = GlobalLock(hGlobalMem)
    wcscpy(ctypes.c_wchar_p(lpGlobalMem), text)
    GlobalUnlock(hGlobalMem)
    if OpenClipboard(None):
        EmptyClipboard()
        SetClipboardData(CF_UNICODETEXT, hGlobalMem)
        CloseClipboard()
