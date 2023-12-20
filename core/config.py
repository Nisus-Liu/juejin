import os

JUEJIN_USERNAME = os.getenv("JUEJIN_USERNAME")
JUEJIN_PASSWORD = os.getenv("JUEJIN_PASSWORD")
JUEJIN_NICKNAME = os.getenv("JUEJIN_NICKNAME")

MAIL_ADDRESS = os.getenv("MAIL_ADDRESS")
MAIL_HOST = os.getenv("MAIL_HOST")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_PORT = int(os.getenv("MAIL_PORT", 465))
MAIL_TO = os.getenv("MAIL_TO")
MAIL_USER = os.getenv("MAIL_USER")

SWITCH = os.getenv("SWITCH", "on")
PUBLISH_SWITCH = os.getenv("PUBLISH_SWITCH", "off")

SLIDER_IMG_TEMP = "temp/slider_img.png"
SLIDER_BACKGROUND_IMG_TEMP = "temp/slider_background_img.png"
SLIDER_IMG_BAK_TEMP = "temp/slider_img_bak.png"
SLIDER_BACKGROUND_IMG_BAK_TEMP = "temp/slider_background_img_bak.png"
