# honzuki.py
import time
import concurrent.futures
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs

def search_thread(book, session):
    # get ISBN        
    book_page = session.get(book.get_attribute('href'))
    soup = bs(book_page.text, 'html.parser')

    # is a book in 'online used store'?
    if book.text.startswith('[온') == True :
        address = soup.select('td[class="p_goodstd02"] a')
        book_page = session.get(address[0]['href'])
        soup = bs(book_page.text, 'html.parser')
        
    info = soup.find("meta", attrs={"property":"books:isbn"})

    if info :
        isbn = info['content']
    else :
        return
        
    # search in the used store
    used_store = session.get('http://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=UsedStore&SearchWord=' + isbn)
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

    driver = webdriver.Chrome()

    # log-in
    driver.get('https://www.aladin.co.kr/login/wlogin.aspx')
    
    email_input = driver.find_element_by_name('Email')
    email_input.clear()
    email_input.send_keys(email)
    
    pw_input = driver.find_element_by_name('Password')
    pw_input.clear()
    pw_input.send_keys(password)

    pw_input.send_keys(Keys.RETURN)

    # open the mycart
    driver.get('http://www.aladin.co.kr/shop/wbasket.aspx')

    # click 'more' button
    more_button = driver.find_element_by_class_name('button_navy')
    
    while more_button.is_displayed() :  
        more = driver.find_element_by_class_name('button_middle_white_more')
        more.click()
        time.sleep(4) # wait for reload cart

    # parse books
    book_list = driver.find_elements_by_xpath('//*[starts-with(@id,"CartTr_")]/td[2]/a[1]')

    session = requests.Session()
    
    for book in book_list :
        search_thread(book, session)

#    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
#       result = {executor.submit(search_thread, book, session): book for book in book_list}
       
    driver.close()
       
if __name__ == '__main__':
    main()
