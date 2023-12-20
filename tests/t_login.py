import os
import traceback

from core import JuejinDriver, Juejin

if __name__ == '__main__':

    # if not all([MAIL_TO, MAIL_PORT, MAIL_HOST, MAIL_ADDRESS, MAIL_PASSWORD, PUBLISH_SWITCH,
    #             MAIL_USER, JUEJIN_USERNAME, JUEJIN_PASSWORD, JUEJIN_NICKNAME, SWITCH]):
    #     raise Exception("Wrong configuration")

    # 掘金登录签到过程
    juejin_driver = JuejinDriver(headless=True)
    juejin_cookies, sign_return = None, None

    try:
        juejin_cookies = juejin_driver.run()
        sign_return = juejin_driver.do_sign()
    except Exception as e:
        traceback.print_exc()
        print("不好意登录签到遇到问题了， 结果为：" + str(e) + "\n")
    finally:
        juejin_driver.driver.close()
        juejin_driver.driver.quit()

    if juejin_cookies is None:
        print("登录失败, juejin_cookies is None")
        exit(1)

    juejin = Juejin(driver_cookies=juejin_cookies)
    user = juejin.get_user().get("data", {})
    print(user)
