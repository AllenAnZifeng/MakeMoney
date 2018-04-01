from window_capture import *
import pytesseract as tess


def recognize_text(img: Image):
    text = []
    q = cut_image_percentage(img, (0, 0.25, 1, 0.35))
    q = tess.image_to_string(q, 'eng').replace('\n', ' ')
    text.append(q)
    a1 = cut_image_percentage(img, (0.05, 0.42, 0.95, 0.5))
    a1 = tess.image_to_string(a1, 'eng')
    text.append(a1)
    a2 = cut_image_percentage(img, (0.05, 0.5, 0.95, 0.58))
    a2 = tess.image_to_string(a2, 'eng')
    text.append(a2)
    a3 = cut_image_percentage(img, (0.05, 0.58, 0.95, 0.66))
    a3 = tess.image_to_string(a3, 'eng')
    text.append(a3)
    return text

if __name__ == '__main__':
    img = capture_area(get_window_rect(find_window_by_title('UNKNOWN')[0][0]))
    print(recognize_text(img))
