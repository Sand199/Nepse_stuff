from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time, math

browser = webdriver.Chrome()

# tms website
browser.get("https://tms57.nepsetms.com.np")
assert "NEPSE" in browser.title

userElem = browser.find_element(
    By.CSS_SELECTOR,
    "body > app-root > app-login > div > div > div.login__wrap > form > div:nth-child(1) > input",
)
# put username below
userElem.send_keys("")

passElem = browser.find_element(By.CSS_SELECTOR, "#password-field")
# put password below
passElem.send_keys("")


while browser.current_url != "https://tms57.nepsetms.com.np/tms/client/dashboard":
    time.sleep(0.5)

browser.get("https://tms57.nepsetms.com.np/tms/me/memberclientorderentry")

# stock info
scrip = "SHLB"
qty = 10
closing = 1941.6
maxprice = math.floor(closing * 11) / 10
price = 2020 
# price = 1285


def select():
    # buy order button
    browser.find_element(
        By.CSS_SELECTOR,
        "body > app-root > tms > main > div > div > app-member-client-order-entry > div > div > div.box.order__options.flex-wrap.d-flex.justify-content-between.align-items-center.order__indeterminate > div.order__options--buysell > app-three-state-toggle > div > div > label:nth-child(3)",
    ).click()


def buy():
    select()
    # symbol text field
    symbol = browser.find_element(
        By.CSS_SELECTOR,
        "body > app-root > tms > main > div > div > app-member-client-order-entry > div > div > div.box-order-entry.box-buy > form > div:nth-child(2) > div.order__form--name > input",
    )
    symbol.clear()
    symbol.send_keys(scrip)
    symbol.send_keys(Keys.RETURN)

    # qty text field
    quant = browser.find_element(By.CSS_SELECTOR,
        "body > app-root > tms > main > div > div > app-member-client-order-entry > div > div > div.box-order-entry.box-buy > form > div:nth-child(2) > div.order__form--qty > input"
    )

    # price(npr) text field
    pp = browser.find_element(By.CSS_SELECTOR,
        "body > app-root > tms > main > div > div > app-member-client-order-entry > div > div > div.box-order-entry.box-buy > form > div:nth-child(2) > div.order__form--price > input"
    )

    i = 1

    while True:
        quant.clear()
        quant.send_keys(qty)
        pp.clear()
        pp.send_keys(price)
        pp.send_keys(Keys.RETURN)
        print(i)
        i += 1


def pre(otype):
    select()
    # pre open button
    browser.find_element(By.CSS_SELECTOR,
        "body > app-root > tms > main > div > div > app-member-client-order-entry > div > div > div.box.order__options.flex-wrap.d-flex.justify-content-between.align-items-center.order__buy > div.order__options--choice > form > label:nth-child(2) > fieldset"
    ).click()

    browser.find_element(By.CSS_SELECTOR,
        "body > app-root > tms > main > div > div > app-member-client-order-entry > div > div > div.box-order-entry.box-buy > form > div:nth-child(2) > div.order__form--name > input"
    ).send_keys(scrip)

    quant = browser.find_element(By.CSS_SELECTOR,
        "body > app-root > tms > main > div > div > app-member-client-order-entry > div > div > div.box-order-entry.box-buy > form > div:nth-child(2) > div.order__form--qty > input"
    )
    quant.send_keys(qty)

    if otype == "mkt":
        browser.find_element(By.CSS_SELECTOR,
            "body > app-root > tms > main > div > div > app-member-client-order-entry > div > div > div.box-order-entry.box-buy > form > div.d-flex.flex-wrap.justify-content-between.align-items-center.mb-10 > div:nth-child(1) > div.order__form--ordertype > div:nth-child(3) > label.np__check > span"
        ).click()
        quant.send_keys(Keys.RETURN)
        quant.send_keys(Keys.RETURN)
        quant.send_keys(Keys.RETURN)

    if otype == "lmt":
        qq = browser.find_element(By.CSS_SELECTOR,
            "body > app-root > tms > main > div > div > app-member-client-order-entry > div > div > div.box-order-entry.box-buy > form > div:nth-child(2) > div.order__form--price > input"
        )
        qq.send_keys(price)

        while True:
            qq.send_keys(Keys.RETURN)
            quant.send_keys(qty)
            qq.send_keys(price)


buy()
# pre("mkt")
# pre("lmt")
