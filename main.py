from os import getcwd, mkdir
from random import randint
from re import sub
from time import sleep

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


def login():
    try:
        driver.get(f"https://ridibooks.com/account/login?return_url={url}")
        driver.find_element_by_id("login_id").send_keys(userId)
        driver.find_element_by_id("login_pw").send_keys(password)
        driver.find_element_by_css_selector("button.full-button").click()
    except Exception as e:
        print(f"로그인을 하던 중 오류가 발생했습니다. 오류: {e}")


def make_dir():
    novelDir = f"""{getcwd()}\\{sub('[/:*?"<>|]', '', title)}"""
    mkdir(novelDir)

    return novelDir


def get_novel_content():
    try:
        WebDriverWait(driver, 5).until(
            ec.presence_of_element_located((By.ID, "ridi_c1")))

        contents = ""
        for i in BeautifulSoup(driver.find_element_by_id("ridi_c1").get_attribute("innerHTML"), "html.parser").children:
            contents += f"{BeautifulSoup(str(i), 'html.parser').text}\n"

        novelFile = f"{novelDir}//{indexPlus}.txt"

        file = open(novelFile, "w", encoding="utf-8")
        file.write(contents)
        file.close()

        if indexPlus == novelCount:
            return

        waitTime = randint(5, 10)
        print(f"내용을 구했지만 밴 방지를 위해 {waitTime}초 동안 기다리고 있습니다.")
        sleep(waitTime)

        driver.find_element_by_css_selector("button.control_button:nth-child(2)").click()
    except Exception as e:
        print(f"오류로 인해 소설 내용을 구하지 못했습니다. 오류: {e}")


print("리디북스 다운로더\n제작자: green1052\n")
print("비 로그인으로 진행하려면\n아이디와 비밀번호 입력시 엔터로 넘기세요\n")
userId = input("아이디를 입력해주세요: ")
password = input("비밀번호를 입력해주세요: ")
book = input("URL 주소 또는 책 번호를 입력해주세요: ")

if not book:
    print("올바르지 못한 입력")
    exit()

url = ""

if "ridibooks.com" in book:
    url = book
else:
    url = f"https://ridibooks.com/books/{book}"

options = Options()
options.headless = True

profile = webdriver.FirefoxProfile()
profile.set_preference("security.enterprise_roots.enabled", True)

driver = webdriver.Firefox(options=options, firefox_profile=profile)

try:
    if userId and password:
        login()
    else:
        driver.get(url)

    title = str(driver.find_element_by_css_selector("h3.info_title_wrap").text)
    novelCount = int(driver.find_element_by_class_name("book_count").text[2:-1])

    novelDir = make_dir()

    driver.find_element_by_class_name("rui_button_blue_50").click()

    for i in range(novelCount):
        indexPlus = i + 1

        print(f"{indexPlus}화의 내용을 구하고 있습니다.")
        get_novel_content()
        print("완료")
except Exception as e:
    print(f"메인 코드에서 오류가 발생했습니다. 오류: {e}")
finally:
    driver.quit()
