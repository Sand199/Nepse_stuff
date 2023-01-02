# show holdings of broker for a script
import logging, time, json, copy
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from datetime import date, timedelta

ticker = "JALPA"

# year month day format
# end_date is not included
start_date = date(2022, 3, 14)
end_date = date(2022, 6, 28)

d = {}
data = {}


# skips end_date
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def calc(date, flag):
    for key in d.keys():
        try:
            d[key]["rate"] = d[key]["amt"] / d[key]["qty"]
        except ZeroDivisionError:
            d[key]["rate"] = "-"

    floating = 0

    for value in d.values():
        if value["qty"] > 0:
            floating += value["qty"]

    logging.info("Total floating shares is ", str(floating))

    for key, value in d.items():
        d[key]["holding"] = d[key]["qty"] / floating * 100

    if flag:
        data[date.strftime("%Y-%m")] = [copy.deepcopy(d), floating]
    else:
        data["current"] = [d, floating]


logging.basicConfig(
    filename="logfile.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s  - %(message)s",
)
# logging.disable(logging.CRITICAL)


driver = webdriver.Chrome()

# https://merolagani.com/Floorsheet.aspx

driver.get("https://merolagani.com/Floorsheet.aspx")

scrip = driver.find_element(
    By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_ASCompanyFilter_txtAutoSuggest"
)
scrip.send_keys(ticker)

# ddate = driver.find_element(
#    By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_txtFloorsheetDateFilter"
# )


for single_date in daterange(start_date, end_date):
    print(single_date.strftime("%m/%d/%Y"))
    ddate = driver.find_element(
        By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_txtFloorsheetDateFilter"
    )

    ddate.clear()
    ddate.send_keys(single_date.strftime("%m/%d/%Y"))
    ddate.send_keys(Keys.RETURN)

    search = driver.find_element(
        By.CSS_SELECTOR, "#ctl00_ContentPlaceHolder1_lbtnSearchFloorsheet"
    )
    search.send_keys(Keys.RETURN)

    time.sleep(0.5)

    logging.info(single_date.strftime("%m/%d/%Y"))

    if int(single_date.strftime("%d")) == 1:
        calc(single_date, 1)

    i = 1
    try:

        while True:
            buyer = driver.find_element(
                By.CSS_SELECTOR,
                f"#ctl00_ContentPlaceHolder1_divData > div.table-responsive > table > tbody > tr:nth-child({i- (i-1)//500*500}) > td:nth-child(4) > a",
            ).text

            seller = driver.find_element(
                By.CSS_SELECTOR,
                f"#ctl00_ContentPlaceHolder1_divData > div.table-responsive > table > tbody > tr:nth-child({i- (i-1)//500*500}) > td:nth-child(5) > a",
            ).text

            quantity = int(
                driver.find_element(
                    By.CSS_SELECTOR,
                    f"#ctl00_ContentPlaceHolder1_divData > div.table-responsive > table > tbody > tr:nth-child({i- (i-1)//500*500}) > td:nth-child(6)",
                ).text.replace(",", "")
            )

            amount = float(
                driver.find_element(
                    By.CSS_SELECTOR,
                    f"#ctl00_ContentPlaceHolder1_divData > div.table-responsive > table > tbody > tr:nth-child({i- (i-1)//500*500}) > td:nth-child(8)",
                ).text.replace(",", "")
            )

            d.setdefault(buyer, {"qty": 0, "amt": 0.0, "rate": 0.0})
            d.setdefault(seller, {"qty": 0, "amt": 0.0, "rate": 0.0})

            d[buyer]["qty"] += quantity
            d[buyer]["amt"] -= amount

            d[seller]["qty"] -= quantity
            d[seller]["amt"] += amount

            logging.debug(
                f"Values after {i} entry -> quantity= {quantity} , buyer {buyer} = {d[buyer]['qty']} , seller {seller} = {d[seller]['qty']}"
            )

            if (i % 500) == 0:
                """
                if i == 500:
                    nextb = driver.find_element(
                        By.CSS_SELECTOR,
                        "#ctl00_ContentPlaceHolder1_divData > div:nth-child(5) > div:nth-child(2) > a:nth-child(5)",
                    )
                else:
                    nextb = driver.find_element(
                        By.CSS_SELECTOR,
                        "#ctl00_ContentPlaceHolder1_divData > div:nth-child(5) > div:nth-child(2) > a:nth-child(7)",
                    )
                """
                nextb = driver.find_element(By.LINK_TEXT, "Next")
                nextb.send_keys("Keys.RETURN")
                nextb.click()
                logging.debug("Clicked Next button Successfully")
                time.sleep(0.5)
            i += 1

    except selenium.common.exceptions.NoSuchElementException:
        logging.warning(f"Cant find element {i}")
        logging.info(f"Recorded {i-1} entries ")
        logging.info(d)


calc(end_date, 0)

file = open(
    ticker
    + "_from_"
    + start_date.strftime("%Y-%m-%d")
    + "_to_"
    + end_date.strftime("%Y-%m-%d")
    + ".json",
    "w+",
)

json.dump(data, file)

print(data)

logging.info("End of Program")
