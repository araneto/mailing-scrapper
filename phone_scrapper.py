"""
Extract name and phone number from Google Maps
TODO List:
- Add argparse support
- Add Flask/Django support
"""
from selenium.webdriver import Firefox
from time import sleep
import os

"""Log file"""
city = 'santos'
csv_name = city + ".csv"
logFile = None
if logFile is None:
    logFile = open(csv_name, mode="a")
    # set the file pointer to end of the file
    pos = logFile.seek(0, os.SEEK_END)
    if pos == 0:
        logFile.write("Name;Category;Phone;Address;\n")


browser = Firefox()
url = "https://www.google.com/maps/search/'publicidade+outdoor'+" + city
browser.get(url)


def register(names, categs, phones, locations):
    """Log Recorder"""
    info = "{};{};{};{}\n".format(names, categs, phones, locations)
    logFile.write(info)
    logFile.flush()


def close_register():
    logFile.close()
    browser.quit()


while True:
    # log sleep to avoid unloaded page
    sleep(10.0)
    parsed_page = browser.find_elements_by_class_name("section-result")
    for i in parsed_page:
        try:
            name = i.find_element_by_class_name('section-result-title').text
            print(name)
            cat = i.find_element_by_class_name('section-result-details').text
            phone = i.find_element_by_class_name('section-result-phone-number').text
            location = i.find_element_by_class_name('section-result-location').text
            register(name, cat, phone, location)
        except Exception as e:
            _ = e
            continue

    # go for the next page
    try:
        browser.find_element_by_id('n7lv7yjyC35__section-pagination-button-next').click()
    except Exception as e:
        _ = e
        close_register()
        break
