# honzuki.py
import requests
import re
import concurrent.futures
from selenium import webdriver
from bs4 import BeautifulSoup as bs

def search_process(book, session):
    # get ISBN
    book_page = session.get(book['href'])
    soup = bs(book_page.text, 'html.parser')

    info = soup.find("meta", attrs={"property":"books:isbn"})
    isbn = info['content']

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
    LOGIN_INFO = {
    'Email': '',
    'Password': '',
    'Action': '1',
    'ReturnUrl': '',
    'ReturnUrl_pop': '',
    'snsUserId': '0',
    'snsType': '0',
    'sysAppId': '1'
    }
    
    LOGIN_INFO['Email'] = input('email> ')
    LOGIN_INFO['Password'] = input('password> ')
    
#   webdriver.Chrome(executable_path="D:\Projects\chromedriver.exe")
    with requests.Session() as session:
#   with webdriver.Chrome() as session:

        login_req = session.post('https://www.aladin.co.kr/login/wlogin.aspx', data=LOGIN_INFO)

        status = login_req.status_code
        is_ok = login_req.ok

        if is_ok == False :
            raise Exception('LOGIN FAILED! STATUS_CODE =' + status)

        
        basket = session.get('http://www.aladin.co.kr/shop/wbasket.aspx')
        soup = bs(basket.text, 'html.parser')        

        book_list = soup.select('#ShopCode_Basket_0 a[style="color:#386DA1;"]')

        for i in book_list :
            print(i.text)

#        with concurrent.futures.ThreadPoolExecutor() as executor:
#            result = {executor.submit(search_process, book, session): book for book in book_list}

if __name__ == '__main__':
    main()
