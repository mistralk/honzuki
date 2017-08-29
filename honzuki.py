# honzuki.py
import time
import concurrent.futures
import requests
from seleniumrequests import Chrome
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs

def search_thread(book, webdriver):
    # get ISBN
    book_page = webdriver.request('GET', book.get_attribute('href'))
    soup = bs(book_page.text, 'html.parser')

    info = soup.find("meta", attrs={"property":"books:isbn"})
    isbn = info['content']

    # search in the used store
    used_store = webdriver.request('GET', 'http://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=UsedStore&SearchWord=' + isbn)
    soup = bs(used_store.text, 'html.parser')
            
    store_list = soup.select('a[class="usedshop_off_text3"]')

    if store_list : 
        result = book.text + ': '
        for i in store_list :
            result += ' ' + i.text
        print(result)

def main():    
    email = input('email> ')
    password = input('password> ')

    webdriver = Chrome()

    # log-in
    webdriver.get('https://www.aladin.co.kr/login/wlogin.aspx')
    
    input1 = webdriver.find_element_by_name('Email')
    input1.clear()
    input1.send_keys(email)
    
    input2 = webdriver.find_element_by_name('Password')
    input2.clear()
    input2.send_keys(password)

    input2.send_keys(Keys.RETURN)

    # open the mycart
    webdriver.get('http://www.aladin.co.kr/shop/wbasket.aspx')

    # click 'more' button
    more_button = webdriver.find_element_by_class_name('button_navy')
    
    while more_button.is_displayed() :  
        more = webdriver.find_element_by_class_name('button_middle_white_more')
        more.click()
        time.sleep(3) # wait for reload cart

    # parse books
    book_list = webdriver.find_elements_by_xpath('//*[starts-with(@id,"CartTr_")]/td[2]/a[1]')

#    for i in book_list :
#        print(i.text)

    with concurrent.futures.ThreadPoolExecutor() as executor:
       result = {executor.submit(search_thread, book, webdriver): book for book in book_list}
       
    webdriver.close()


if __name__ == '__main__':
    main()
