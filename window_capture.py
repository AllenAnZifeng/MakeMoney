import ctypes
import win32gui
from PIL import ImageGrab, Image


def callback(hwnd: int, window_names: dict):
    if win32gui.IsWindowVisible(hwnd):
        window_names[int(hwnd)] = [win32gui.GetWindowText(hwnd),
                                   win32gui.GetClassName(hwnd)]


def get_visible_windows() -> dict:
    windows = {}
    win32gui.EnumWindows(callback, windows)
    return windows


def find_window_by_title(title: str) -> list:
    windows = get_visible_windows()
    matched = []
    for wid in windows:
        if windows[wid][0].find(title) != -1:
            matched.append((wid, windows[wid][0], windows[wid][1]))
    return matched


def capture_area(coord: tuple) -> Image:
    img = ImageGrab.grab(coord)
    return img


def get_window_rect(hwnd: int, border_width: int = 7):
    # C Type structure to store the coordinates
    class RECT(ctypes.Structure):
        _fields_ = [('left', ctypes.c_int),
                    ('top', ctypes.c_int),
                    ('right', ctypes.c_int),
                    ('bottom', ctypes.c_int)]

        def get_coord(self, border_width: int):
            return (
                self.left + border_width, self.top + border_width,
                self.right - border_width, self.bottom - border_width)

    rect = RECT()
    ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))
    return rect.get_coord(border_width)


def get_focused_window() -> int:
    return win32gui.GetForegroundWindow()


def cut_image(img: Image, box: tuple) -> Image:
    return img.crop(box)


def cut_image_percentage(img: Image, box: tuple) -> Image:
    w, h = img.size
    box = (box[0] * w, box[1] * h, box[2] * w, box[3] * h)
    return cut_image(img, box)


if __name__ == '__main__':
    print(find_window_by_title('UNKNOWN'))
