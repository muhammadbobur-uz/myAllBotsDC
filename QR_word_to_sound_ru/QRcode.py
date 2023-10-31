import pyqrcode
import png

def QRC(txt):
    u =pyqrcode.create(txt)
    return u.png('QR/qr.png', scale=6)

# s = "My QR code"
# url = pyqrcode.create(s)
# url.png('myqr.png', scale=6)