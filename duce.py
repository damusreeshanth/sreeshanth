import json
import os
import random
import re
import sys
import threading
import time
import traceback
from decimal import Decimal
from urllib.parse import parse_qs, unquote, urlsplit
from webbrowser import open as web
from pack import browser_cookie3
import cloudscraper
import PySimpleGUI as sg
import requests
from bs4 import BeautifulSoup as bs
from http.client import RemoteDisconnected
from pack.base64 import *

# DUCE

sg.set_global_icon(icon)
sg.change_look_and_feel("dark")
sg.theme_background_color
sg.set_options(
    button_color=(sg.theme_background_color(), sg.theme_background_color()),
    border_width=0,
    font=10,
)
#rakesh
############## Scraper


# head = {
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84",
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
# }

def LocalFile():
    global local_links
    local_links = []
    # f = open('D:\\Udemy Free Cources\\test.txt', encoding='UTF-8')
    # data = json.load(f)
    # f.close()
    
    with open("D:\\Udemy-Course-Enroller-1.7\\GUI\\UdemyRecords.txt") as file_in:
        for line in file_in:
            local_links.append(line)
    main_window["pLocalFile"].update(0, visible=False)
    main_window["iLocalFile"].update(visible=True)
    
def discudemy():
    global du_links
    du_links = []
    big_all = []
    head = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    }
    backoff_time = 3  # start with a delay of 3 seconds
    for page in range(1, 4):
        for _ in range(5):  # try up to 5 times
            try:
                r = requests.get("https://www.discudemy.com/all/" + str(page), headers=head)
                break  # if the request is successful, break the loop
            except Exception as e:
                time.sleep(backoff_time)  # wait for 3 second before trying again
                backoff_time *= 2  # double the delay for the next retry

        #r = requests.get("https://www.discudemy.com/all/" + str(page), headers=head)
        soup = bs(r.content, "html5lib")
        small_all = soup.find_all("a", {"class": "card-header"})
        big_all.extend(small_all)
        main_window["pDiscudemy"].update(page)
    main_window["pDiscudemy"].update(0, max=len(big_all))

    for index, item in enumerate(big_all):
        main_window["pDiscudemy"].update(index + 1)

        title = item.string
        url = item["href"].split("/")[4]
        #r = requests.get("https://www.discudemy.com/go/" + url, headers=head)
        backoff_time = 3  # start with a delay of 3 seconds
        for _ in range(5):  # try up to 5 times
            try:
                r = requests.get("https://www.discudemy.com/go/" + url, headers=head)
                break  # if the request is successful, break the loop
            except Exception as e:
                time.sleep(backoff_time)  # wait for 3 second before trying again
                backoff_time *= 2  # double the delay for the next retry
        soup = bs(r.content, "html5lib")
        
        udemyLink = soup.find("a", href=re.compile("www.udemy.com"))
        link = udemyLink["href"]
        #link = soup.find("a", id="couponLink")
        if link is not None and link != "":
            du_links.append(title + "|:|" + link)
    print("Discudemy Courses: " + str(len(du_links)))
    main_window["pDiscudemy"].update(0, visible=False)
    main_window["iDiscudemy"].update(visible=True)

def udemy_freebies():
    global uf_links
    uf_links = []
    big_all = []
    head = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    }
    backoff_time = 3  # start with a delay of 3 seconds
    for page in range(1, 3):
        for _ in range(5):  # try up to 5 times
            try:
                r = requests.get("https://www.udemyfreebies.com/free-udemy-courses/" + str(page), headers=head)
                break  # if the request is successful, break the loop
            except Exception as e:
                time.sleep(backoff_time)  # wait for 3 second before trying again
                backoff_time *= 2  # double the delay for the next retry
        # r = requests.get(
        #     "https://www.udemyfreebies.com/free-udemy-courses/" + str(page), headers=head
        # )
        soup = bs(r.content, "html5lib")
        small_all = soup.find_all("a", {"class": "theme-img"})
        big_all.extend(small_all)
        main_window["pUdemy Freebies"].update(page)
    main_window["pUdemy Freebies"].update(0, max=len(big_all))

    for index, item in enumerate(big_all):
        main_window["pUdemy Freebies"].update(index + 1)
        title = item.img["alt"]
        backoff_time = 3  # start with a delay of 3 seconds
        for _ in range(5):  # try up to 5 times
            try:
                link = requests.get("https://www.udemyfreebies.com/out/" + item["href"].split("/")[4], headers=head).url
                break  # if the request is successful, break the loop
            except Exception as e:
                time.sleep(backoff_time)  # wait for 3 second before trying again
                backoff_time *= 2  # double the delay for the next retry
        # link = requests.get(
        #     "https://www.udemyfreebies.com/out/" + item["href"].split("/")[4]
        # ).url
        uf_links.append(title + "|:|" + link)
    print("Udemy Freebies Courses: " + str(len(uf_links)))
    main_window["pUdemy Freebies"].update(0, visible=False)
    main_window["iUdemy Freebies"].update(visible=True)

def tutorialbar():

    global tb_links
    tb_links = []
    big_all = []
    head = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    }
    
    for page in range(1, 4):
        backoff_time = 3  # start with a delay of 3 seconds
        for _ in range(5):  # try up to 5 times
            try:
                r = requests.get("https://www.tutorialbar.com/all-courses/page/" + str(page), headers=head)
                break  # if the request is successful, break the loop
            except Exception as e:
                time.sleep(backoff_time)  # wait for 3 second before trying again
                backoff_time *= 2  # double the delay for the next retry

        #r = requests.get("https://www.tutorialbar.com/all-courses/page/" + str(page), headers=head)
        soup = bs(r.content, "html5lib")
        small_all = soup.find_all(
            "h3", class_="mb15 mt0 font110 mobfont100 fontnormal lineheight20"
        )
        big_all.extend(small_all)
        main_window["pTutorial Bar"].update(page)
    main_window["pTutorial Bar"].update(0, max=len(big_all))

    for index, item in enumerate(big_all):
        main_window["pTutorial Bar"].update(index + 1)
        title = item.a.string
        url = item.a["href"]
        backoff_time = 3  # start with a delay of 3 seconds
        for _ in range(5):  # try up to 5 times
            
            try:
                r = requests.get(url, headers=head)
                break  # if the request is successful, break the loop
            except Exception as e:
                time.sleep(backoff_time)  # wait for 3 second before trying again
                backoff_time *= 2  # double the delay for the next retry

        #r = requests.get(url, headers=head)
        soup = bs(r.content, "html5lib")
        link = soup.find("a", class_="btn_offer_block re_track_btn")["href"]
        if "www.udemy.com" in link:
            tb_links.append(title + "|:|" + link)
    print("Tutorial Bar Courses: " + str(len(tb_links)))
    main_window["pTutorial Bar"].update(0, visible=False)
    main_window["iTutorial Bar"].update(visible=True)

def real_discount():

    global rd_links
    rd_links = []
    big_all = []
    head = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    }
    for page in range(1, 3):
        backoff_time = 3  # start with a delay of 3 seconds
        for _ in range(5):  # try up to 5 times
            try:
                r = requests.get("https://real.discount/stores/Udemy?page=" + str(page), headers=head)
                break  # if the request is successful, break the loop
            except Exception as e:
                time.sleep(backoff_time)  # wait for 3 second before trying again
                backoff_time *= 2  # double the delay for the next retry

        #r = requests.get("https://real.discount/stores/Udemy?page=" + str(page), headers=head)
        soup = bs(r.content, "html5lib")
        small_all = soup.find_all("div", class_="col-xl-4 col-md-6")
        big_all.extend(small_all)
    main_window["pReal Discount"].update(page)
    main_window["pReal Discount"].update(0, max=len(big_all))

    for index, item in enumerate(big_all):
        main_window["pReal Discount"].update(index + 1)
        title = item.a.h3.string
        url = "https://real.discount" + item.a["href"]
        backoff_time = 3  # start with a delay of 3 seconds
        for _ in range(5):  # try up to 5 times
            try:
                r = requests.get(url, headers=head)
                break  # if the request is successful, break the loop
            except Exception as e:
                time.sleep(backoff_time)  # wait for 3 second before trying again
                backoff_time *= 2  # double the delay for the next retry

        #r = requests.get(url, headers=head)

        soup = bs(r.content, "html5lib")
        # link = soup.find("div", class_="col-xs-12 col-md-12 col-sm-12 text-center").a[
        #     "href"
        # ]
        #rakesh
        #we have multiple divs with same class name, i want to find divs with class name "col-xs-12 col-md-12 col-sm-12 card p-4" and then find a tag inside it and then href attribute of a tag
        links = soup.find_all("div", class_="col-xs-12 col-md-12 col-sm-12 card p-4")
        for link in links:
            if link.a is not None:
                link = link.a["href"]
                break
        #rakesh
        if link.startswith("http://click.linksynergy.com") or link.startswith("https://click.linksynergy.com"):
            if "RD_PARM1" in link:
                link = parse_qs(link)["RD_PARM1"][0]
            elif "murl" in link:
                link = parse_qs(link)["murl"][0]

        rd_links.append(title + "|:|" + link)
    print("Real Discount Courses: " + str(len(rd_links)))
    main_window["pReal Discount"].update(0, visible=False)
    main_window["iReal Discount"].update(visible=True)

def coursevania():
    
    global cv_links
    nonce = ""
    cv_links = []
    head = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    }
    backoff_time = 3  # start with a delay of 3 seconds
    for _ in range(5):  # try up to 5 times
        try:
            r = requests.get("https://coursevania.com/courses/", headers=head)
            break  # if the request is successful, break the loop
        except Exception as e:
            time.sleep(backoff_time)  # wait for 3 second before trying again
            backoff_time *= 2  # double the delay for the next retry
                
    #r = requests.get("https://coursevania.com/courses/", headers=head)
    soup = bs(r.content, "html5lib")
  
    nonce = ""
    for script in soup.find_all("script"):
        if script.string and "load_content" in script.string:
            content = script.string.replace("var stm_lms_nonces =", "").strip().rstrip(";")
            #print(content)  # Debugging line
            try:
                jsonObj = json.loads(content)
                nonce = json.loads(content)["load_content"]
                break
            except json.JSONDecodeError:
                print("Invalid JSON string")
                break
    backoff_time = 3  # start with a delay of 3 seconds            
    for _ in range(5):  # try up to 5 times
        try:
            r =  requests.get(
        "https://coursevania.com/wp-admin/admin-ajax.php?offset=0&template=courses/grid&args={'image_size':'750x422','per_row':'4','posts_per_page':'30','class':'archive_grid'}&action=stm_lms_load_content&nonce="+nonce+"&sort=date_high", headers=head
    ).json()
            break  # if the request is successful, break the loop
        except Exception as e:
            time.sleep(backoff_time)  # wait for 3 second before trying again
            backoff_time *= 2  # double the delay for the next retry

    # r = requests.get(
    #     "https://coursevania.com/wp-admin/admin-ajax.php?offset=0&template=courses/grid&args={'image_size':'750x422','per_row':'4','posts_per_page':'30','class':'archive_grid'}&action=stm_lms_load_content&nonce="+nonce+"&sort=date_high", headers=head
    # ).json()


    soup = bs(r["content"], "html5lib")
    small_all = soup.find_all("div", {"class": "stm_lms_courses__single--title"})
    main_window["pCourse Vania"].update(0, max=len(small_all))

    for index, item in enumerate(small_all):
        main_window["pCourse Vania"].update(index + 1)
        title = item.h5.string
        backoff_time = 3  # start with a delay of 3 seconds
        for _ in range(5):  # try up to 5 times
            try:
                r = requests.get(item.a["href"], headers=head)
                break  # if the request is successful, break the loop
            except Exception as e:
                time.sleep(backoff_time)  # wait for 3 second before trying again
                backoff_time *= 2  # double the delay for the next retry

        #r = requests.get(item.a["href"], headers=head)
        soup = bs(r.content, "html5lib")
        cv_links.append(
            title + "|:|" + soup.find("div", {"class": "stm-lms-buy-buttons"}).a["href"]
        )
    print("Course Vania Courses: " + str(len(cv_links)))
    main_window["pCourse Vania"].update(0, visible=False)
    main_window["iCourse Vania"].update(visible=True)

def idcoupons_Old():

    global idc_links
    idc_links = []
    big_all = []
    head = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    }
    for page in range(1, 3):
        backoff_time = 3  # start with a delay of 3 seconds
        for _ in range(5):  # try up to 5 times
            try:
                r = requests.get(
                    "https://idownloadcoupon.com/product-category/100off/page/" +
                    str(page), headers=head
                )
                break  # if the request is successful, break the loop
            except Exception as e:
                time.sleep(backoff_time)  # wait for 3 second before trying again
                backoff_time *= 2  # double the delay for the next retry

        # r = requests.get(
        #     "https://idownloadcoupon.com/product-category/100off/page/" +
        #     str(page), headers=head
        # )
        soup = bs(r.content, "html5lib")
        # small_all = soup.find_all("a", attrs={"class": "button product_type_external"})
        small_all = soup.find_all("a", attrs={
                                  "class": "button wp-element-button product_type_external"})
        big_all.extend(small_all)
    main_window["pIDownloadCoupons"].update(0, max=len(big_all))

    for index, item in enumerate(big_all):
        main_window["pIDownloadCoupons"].update(index + 1)
        title = item["aria-label"]
        link = unquote(item["href"])
        if link.startswith("https://ad.admitad.com"):
            link = parse_qs(link)["ulp"][0]
        elif link.startswith("https://click.linksynergy.com"):
            link = parse_qs(link)["murl"][0]
        idc_links.append(title + "|:|" + link)
    print("IDownloadCoupons Courses: " + str(len(idc_links)))
    main_window["pIDownloadCoupons"].update(0, visible=False)
    main_window["iIDownloadCoupons"].update(visible=True)

def idcoupons():
    global idc_links
    idc_links = []
    big_all = []
    head = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    }
    try:
        for page in range(1, 3):
            backoff_time = 3  # start with a delay of 3 seconds
            for _ in range(5):  # try up to 5 times
                try:
                    r = requests.get(
                            "https://idownloadcoupon.com/product-category/udemy/page/"
                            + str(page), headers=head
                        )
                    break  # if the request is successful, break the loop
                except Exception as e:
                    time.sleep(backoff_time)  # wait for 3 second before trying again
                    backoff_time *= 2  # double the delay for the next retry


            # r = requests.get(
            #     "https://idownloadcoupon.com/product-category/udemy/page/"
            #     + str(page), headers=head
            # )
            soup = bs(r.content, "html5lib")
            small_all = soup.find_all(
                "a",
                attrs={"class": "button product_type_external"},
            )
            big_all.extend(small_all)
        idc_length = len(big_all)
        main_window["pIDownloadCoupons"].update(0, max=len(big_all))

        for index, item in enumerate(big_all):
            main_window["pIDownloadCoupons"].update(index + 1)
            idc_progress = index
            title = item["aria-label"][5:][:-1].strip()
            backoff_time = 3  # start with a delay of 3 seconds
            #r = requests.get(item["href"], headers=head, allow_redirects=False)
            for _ in range(5):  # try up to 5 times
                try:
                    r = requests.get(item["href"], headers=head, allow_redirects=False)
                    break  # if the request is successful, break the loop
                except Exception as e:
                    time.sleep(backoff_time)  # wait for 3 second before trying again
                    backoff_time *= 2  # double the delay for the next retry


            link = unquote(r.headers["Location"])
            if link.startswith("https://ad.admitad.com"):
                link = parse_qs(link)["ulp"][0]
            # elif link.startswith("https://click.linksynergy.com"):
            #     link = link.split("murl=")[1]

            elif link.startswith("http://click.linksynergy.com") or link.startswith("https://click.linksynergy.com"):
                if "RD_PARM1" in link:
                    link = parse_qs(link)["RD_PARM1"][0]
                elif "murl" in link:
                    link = parse_qs(link)["murl"][0]
            # else:
            #     print(link)
            idc_links.append(title + "|:|" + link)
        print("IDownloadCoupons Courses: " + str(len(idc_links)))
        main_window["pIDownloadCoupons"].update(0, visible=False)
        main_window["iIDownloadCoupons"].update(visible=True)
    except:
        idc_error = traceback.format_exc()
        idc_length = -1
    idc_done = True

def onlinecoursesooo():
    global ooo_links
    ooo_links = []
    big_all = []
    head = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    }
    try:
        for page in range(1, 3):
            backoff_time = 3  # start with a delay of 3 seconds
            for _ in range(5):  # try up to 5 times
                try:
                    r = requests.get(
                            "https://www.onlinecourses.ooo/page/"
                            + str(page), headers=head
                        )
                    break  # if the request is successful, break the loop
                except Exception as e:
                    time.sleep(backoff_time)  # wait for 3 second before trying again
                    backoff_time *= 2  # double the delay for the next retry
                    
            # r = requests.get(
            #     "https://www.onlinecourses.ooo/page/"
            #     + str(page), headers=head
            # )
            soup = bs(r.content, "html5lib")
            small_all = soup.find_all(
                "a",
                attrs={"class": "img-centered-flex rh-flex-center-align rh-flex-justify-center re_track_btn"},
            )
            big_all.extend(small_all)
        ooo_length = len(big_all)
        main_window["ponlinecoursesooo"].update(0, max=len(big_all))

        for index, item in enumerate(big_all):
            main_window["ponlinecoursesooo"].update(index + 1)
            ooo_progress = index


            url = item["href"]
            if "onlinecourses.ooo" not in url:
                continue
            #r = requests.get(url, headers=head)
            backoff_time = 3  # start with a delay of 3 seconds
            for _ in range(5):  # try up to 5 times
                try:
                    r = requests.get(url, headers=head)
                    break  # if the request is successful, break the loop
                except Exception as e:
                    time.sleep(backoff_time)  # wait for 3 second before trying again
                    backoff_time *= 2  # double the delay for the next retry

            soup = bs(r.content, "html5lib")
            #find anchor tag containing "GET COUPON CODE" text and get href attribute
            
            #find h1 tag contains class "clearbox" and get text, h1 tag inside div tag contains class "lineheight20 rh-flex-center-align mobileblockdisplay"
            title=soup.find("h1", class_="clearbox").text

            udemyRedirectLink = soup.find("a", class_="btn_offer_block re_track_btn")
            #get href attribute of anchor tag
            link = unquote(udemyRedirectLink["href"])
            
            if link.startswith("https://ad.admitad.com"):
                link = parse_qs(link)["ulp"][0]
            elif link.startswith("http://click.linksynergy.com") or link.startswith("https://click.linksynergy.com"):
                if "RD_PARM1" in link:
                    link = parse_qs(link)["RD_PARM1"][0]
                elif "murl" in link:
                    link = parse_qs(link)["murl"][0]
            # else:
            #     print(link)
            ooo_links.append(title + "|:|" + link)
        print("onlinecoursesooo Courses: " + str(len(ooo_links)))
        main_window["ponlinecoursesooo"].update(0, visible=False)
        main_window["ionlinecoursesooo"].update(visible=True)
    except:
        ooo_error = traceback.format_exc()
        ooo_length = -1
    ooo_done = True

def smartybro():
    global smbro_links
    smbro_links = []
    big_all = []
    head = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    }
    try:
        for page in range(1, 3):
            backoff_time = 3  # start with a delay of 3 seconds
            for _ in range(5):  # try up to 5 times
                try:
                    r = requests.get(
                            "https://smartybro.com/category/udemy-coupon-100-off/page/"
                            + str(page), headers=head
                        )
                    break  # if the request is successful, break the loop
                except Exception as e:
                    time.sleep(backoff_time)  # wait for 3 second before trying again
                    backoff_time *= 2  # double the delay for the next retry

            # r = requests.get(
            #     "https://smartybro.com/category/udemy-coupon-100-off/page/"
            #     + str(page), headers=head
            # )
            soup = bs(r.content, "html5lib")

            #find anchor tag href with in h2 tag contains class "entry-title" and get href attribute
            anchorDivs = soup.find_all(
                "h2",
                attrs={"class": "grid-tit"},
            )

            small_all = [div.find("a") for div in anchorDivs]
                   
            big_all.extend(small_all)
        smbro_length = len(big_all)
        main_window["psmartybro"].update(0, max=len(big_all))

        for index, item in enumerate(big_all):
            main_window["psmartybro"].update(index + 1)
            smbro_progress = index


            url = item["href"]
            if "smartybro.com" not in url:
                continue
            backoff_time = 3  # start with a delay of 3 seconds        
            for _ in range(5):  # try up to 5 times
                try:
                    r = requests.get(url, headers=head)
                    break  # if the request is successful, break the loop
                except Exception as e:
                    time.sleep(backoff_time)  # wait for 3 second before trying again
                    backoff_time *= 2  # double the delay for the next retry      

            #r = requests.get(url, headers=head)
            soup = bs(r.content, "html5lib")
            #find anchor tag containing "GET COUPON CODE" text and get href attribute
            
            #find h1 tag contains class "clearbox" and get text, h1 tag inside div tag contains class "lineheight20 rh-flex-center-align mobileblockdisplay"
            title=soup.find("span", class_="entry-title").text

            udemyRedirectLink = soup.find("a", class_="fasc-button fasc-size-xlarge fasc-type-flat")
            #get href attribute of anchor tag
            link = unquote(udemyRedirectLink["href"])
            #remove all attributes except coupon code
            #link = link.split("?couponCode=")[0] + "?couponCode=" + link.split("?couponCode=")[1].split("&")[0]
            if link.startswith("https://ad.admitad.com"):
                link = parse_qs(link)["ulp"][0]
            elif link.startswith("http://click.linksynergy.com") or link.startswith("https://click.linksynergy.com"):
                if "RD_PARM1" in link:
                    link = parse_qs(link)["RD_PARM1"][0]
                elif "murl" in link:
                    link = parse_qs(link)["murl"][0]
            # else:
            #     print(link)
            smbro_links.append(title + "|:|" + link)
        print("smartybro Courses: " + str(len(smbro_links)))
        main_window["psmartybro"].update(0, visible=False)
        main_window["ismartybro"].update(visible=True)
    except:
        smbro_error = traceback.format_exc()
        smbro_length = -1
    smbro_done = True

def bestcouponhunter():
    global bch_links
    bch_links = []
    big_all = []
    head = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    }
    try:

        for page in range(1, 3):
            
            # r = requests.get(
            #     "https://bestcouponhunter.com/page/"
            #     + str(page), headers=head
            # )
            backoff_time = 3  # start with a delay of 3 seconds
            for _ in range(5):  # try up to 5 times
                try:
                    r = requests.get(
                            "https://bestcouponhunter.com/page/"
                            + str(page), headers=head
                        )
                    break  # if the request is successful, break the loop
                except Exception as e:
                    time.sleep(backoff_time)  # wait for 3 second before trying again
                    backoff_time *= 2  # double the delay for the next retry


            soup = bs(r.content, "html5lib")

            #find anchor tag href with in h2 tag contains class "entry-title" and get href attribute
            small_all = soup.find_all(
                "a",
                attrs={"class": "img-centered-flex rh-flex-center-align rh-flex-justify-center"},
            )

            #small_all = [div.find("a") for div in anchorDivs]
                   
            big_all.extend(small_all)
        bch_length = len(big_all)
        main_window["pbestcouponhunter"].update(0, max=len(big_all))

        for index, item in enumerate(big_all):
            main_window["pbestcouponhunter"].update(index + 1)
            bch_progress = index


            url = item["href"]
            if "bestcouponhunter.com" not in url:
                continue
            backoff_time = 3  # start with a delay of 3 seconds
            for _ in range(5):  # try up to 5 times
                try:
                    r = requests.get(url, headers=head)
                    break  # if the request is successful, break the loop
                except Exception as e:
                    time.sleep(backoff_time)  # wait for 3 second before trying again
                    backoff_time *= 2  # double the delay for the next retry
                    

            #r = requests.get(url, headers=head)
            soup = bs(r.content, "html5lib")
            #find anchor tag containing "GET COUPON CODE" text and get href attribute
            
            #find h1 tag contains class "clearbox" and get text, h1 tag inside div tag contains class "lineheight20 rh-flex-center-align mobileblockdisplay"
            titleDiv = soup.find("div", class_="single_top_main")
            title = titleDiv.find("h1").text


            udemyRedirectLink = soup.find("a", class_="btn_offer_block re_track_btn medium")
            #get href attribute of anchor tag
            link = unquote(udemyRedirectLink["href"])
            #remove all attributes except coupon code
            #link = link.split("?couponCode=")[0] + "?couponCode=" + link.split("?couponCode=")[1].split("&")[0]
            if link.startswith("https://ad.admitad.com"):
                link = parse_qs(link)["ulp"][0]
            elif link.startswith("http://click.linksynergy.com") or link.startswith("https://click.linksynergy.com"):
                if "RD_PARM1" in link:
                    link = parse_qs(link)["RD_PARM1"][0]
                elif "murl" in link:
                    link = parse_qs(link)["murl"][0]
            # else:
            #     print(link)
            bch_links.append(title + "|:|" + link)
        print("bestcouponhunter Courses: " + str(len(bch_links)))
        main_window["pbestcouponhunter"].update(0, visible=False)
        main_window["ibestcouponhunter"].update(visible=True)
    except:
        bch_error = traceback.format_exc()
        bch_length = -1
    bch_done = True

def cursosdev():
    global cd_links
    cd_links = []
    big_all = []
    head = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    }
    try:
        for page in range(1, 3):
            backoff_time = 3  # start with a delay of 3 seconds
            for _ in range(5):  # try up to 5 times
                try:
                    r = requests.get(
                            "https://www.cursosdev.com/?page="
                            + str(page), headers=head
                        )
                    break  # if the request is successful, break the loop
                except Exception as e:
                    time.sleep(backoff_time)  # wait before trying again
                    backoff_time *= 2  # double the delay for the next retry


            # r = requests.get(
            #     "https://www.cursosdev.com/?page="
            #     + str(page), headers=head
            # )

            soup = bs(r.content, "html5lib")

            coursesDiv = soup.find(
                "div",
                attrs={"class": "w-screen sm:w-full md:full lg:w-full xl:w-full mx-auto grid grid-cols-1 px-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4"},
            )
            #find anchor tag href with in h2 tag contains class "entry-title" and get href attribute
            small_all = coursesDiv.find_all(
                "a",
                attrs={"class": "c-card block bg-white shadow-md hover:shadow-xl rounded-lg overflow-hidden"},
            )
                   
            big_all.extend(small_all)
        cd_length = len(big_all)
        main_window["pcursosdev"].update(0, max=len(big_all))

        for index, item in enumerate(big_all):
            main_window["pcursosdev"].update(index + 1)
            cd_progress = index


            url = item["href"]
            if "cursosdev.com" not in url:
                continue

            try:
                backoff_time = 3  # start with a delay of 3 seconds
                for _ in range(5):  # try up to 5 times
                    try:
                        r = requests.get(url, headers=head)
                        break  # if the request is successful, break the loop
                    except Exception as e:
                        time.sleep(backoff_time)  # wait before trying again
                        backoff_time *= 2  # double the delay for the next retry


                #r = requests.get(url, headers=head)
                r.raise_for_status()  # This will raise an exception if the status code is not 200
            except requests.exceptions.RequestException as e:
                if r.status_code == 508:
                    print("Resource Limit Is Reached for URL:", url)
                    continue  # Skip this URL and continue with the next one
                else:
                    #raise  # Re-raise the exception if the status code is not 508
                    print("Some Exception Occered "+r.status_code+ " for URL:", url)

            soup = bs(r.content, "html5lib")
            # find anchor tag containing "GET COUPON CODE" text and get href attribute

            # find h1 tag contains class "clearbox" and get text, h1 tag inside div tag contains class "lineheight20 rh-flex-center-align mobileblockdisplay"
            title = soup.find("a", class_="text-4xl text-gray-700 font-bold hover:underline").text
            #title = titleDiv.find("h1").text

            udemyRedirectLink = soup.find("a", class_="border border-purple-800 bg-indigo-900 hover:bg-indigo-500 my-8 mr-2 text-white block rounded-sm font-bold py-4 px-6 ml-2 flex text-center items-center")
            # get href attribute of anchor tag
            link = unquote(udemyRedirectLink["href"])

            if link.startswith("https://ad.admitad.com"):
                link = parse_qs(link)["ulp"][0]
            elif link.startswith("http://click.linksynergy.com") or link.startswith("https://click.linksynergy.com"):
                if "RD_PARM1" in link:
                    link = parse_qs(link)["RD_PARM1"][0]
                elif "murl" in link:
                    link = parse_qs(link)["murl"][0]
            # else:
            #     print(link)
            cd_links.append(title + "|:|" + link)

        print("cursosdev Courses: " + str(len(cd_links)))
        main_window["pcursosdev"].update(0, visible=False)
        main_window["icursosdev"].update(visible=True)
    except:
        cd_error = traceback.format_exc()
        cd_length = -1
    cd_done = True

def freebiesglobal():
    global fg_links
    fg_links = []
    big_all = []
    head = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    }
    try:
        for page in range(1, 3):
            backoff_time = 3  # start with a delay of 3 seconds
            for _ in range(5):  # try up to 5 times
                try:
                    r = requests.get(
                        "https://freebiesglobal.com/page/"
                        + str(page), headers=head
                    )
                    break  # if the request is successful, break the loop
                except Exception as e:
                    time.sleep(backoff_time)  # wait before trying again
                    backoff_time *= 2  # double the delay for the next retry


            # r = requests.get(
            #     "https://freebiesglobal.com/page/"
            #     + str(page), headers=head
            # )
            soup = bs(r.content, "html5lib")

            coursesDiv = soup.find(
                "div",
                attrs={"class": "vc_row wpb_row vc_row-fluid centered-container"},
            )
            #find anchor tag href with in h2 tag contains class "entry-title" and get href attribute
            small_all = coursesDiv.find_all(
                "a",
                attrs={"class": "img-centered-flex rh-flex-center-align rh-flex-justify-center"},
            )
                   
            big_all.extend(small_all)
        fg_length = len(big_all)
        main_window["pfreebiesglobal"].update(0, max=len(big_all))

        for index, item in enumerate(big_all):
            main_window["pfreebiesglobal"].update(index + 1)
            fg_progress = index


            url = item["href"]
            if "freebiesglobal.com" not in url:
                continue

            try:
                backoff_time = 3  # start with a delay of 3 seconds
                for _ in range(5):  # try up to 5 times
                    try:
                        r = requests.get(url, headers=head)
                        break  # if the request is successful, break the loop
                    except Exception as e:
                        time.sleep(backoff_time)  # wait before trying again
                        backoff_time *= 2  # double the delay for the next retry


                # r = requests.get(url, headers=head)
                r.raise_for_status()  # This will raise an exception if the status code is not 200
            except requests.exceptions.RequestException as e:
                if r.status_code == 508:
                    print("Resource Limit Is Reached for URL:", url)
                    continue  # Skip this URL and continue with the next one
                else:
                    #raise  # Re-raise the exception if the status code is not 508
                    print("Some Exception Occered "+r.status_code+ " for URL:", url)

            soup = bs(r.content, "html5lib")
            # find anchor tag containing "GET COUPON CODE" text and get href attribute

            # find h1 tag contains class "clearbox" and get text, h1 tag inside div tag contains class "lineheight20 rh-flex-center-align mobileblockdisplay"
            titleDiv = soup.find("div", class_="rh_post_layout_compare_holder mb25")
            titleSubDiv = titleDiv.find("div", class_="title_single_area")
            title = titleDiv.find("h1").text

            udemyRedirectLink = soup.find("a", class_="re_track_btn btn_offer_block")
            # get href attribute of anchor tag
            link = unquote(udemyRedirectLink["href"])

            if link.startswith("https://ad.admitad.com"):
                link = parse_qs(link)["ulp"][0]
            elif link.startswith("http://click.linksynergy.com") or link.startswith("https://click.linksynergy.com"):
                if "RD_PARM1" in link:
                    link = parse_qs(link)["RD_PARM1"][0]
                elif "murl" in link:
                    link = parse_qs(link)["murl"][0]
            # else:
            #     print(link)
            if link.startswith("https://www.udemy.com"):
                fg_links.append(title + "|:|" + link)

        print("freebiesglobal Courses: " + str(len(fg_links)))
        main_window["pfreebiesglobal"].update(0, visible=False)
        main_window["ifreebiesglobal"].update(visible=True)
    except:
        fg_error = traceback.format_exc()
        fg_length = -1
    fg_done = True

def coursefolder():
    global cf_links
    cf_links = []
    big_all = []
    head = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        }
    try:
        backoff_time = 3  # start with a delay of 3 seconds
        for _ in range(5):  # try up to 5 times
            try:
                r = requests.get("https://coursefolder.net/live-free-udemy-coupon.php", headers=head)
                break  # if the request is successful, break the loop
            except Exception as e:
                time.sleep(backoff_time)  # wait before trying again
                backoff_time *= 2  # double the delay for the next retry
        # r = requests.get("https://coursefolder.net/live-free-udemy-coupon.php", headers=head)


        soup = bs(r.content, "html5lib")


        # coursesDiv = soup.find(
        #     "div",
        #     attrs={"class": "vc_row wpb_row vc_row-fluid centered-container"},
        # )
        #find anchor tag href with in h2 tag contains class "entry-title" and get href attribute
        small_all = soup.find_all(
            "a",
            attrs={"class": "edu-btn btn-secondary btn-small"},
        )
                
        big_all.extend(small_all)
        cf_length = len(big_all)
        main_window["pcoursefolder"].update(0, max=len(big_all))

        for index, item in enumerate(big_all):
            main_window["pcoursefolder"].update(index + 1)
            cf_progress = index


            url = item["href"]
            if "coursefolder.net" not in url:
                continue

            try:
                backoff_time = 3  # start with a delay of 3 seconds
                for _ in range(5):  # try up to 5 times
                    try:
                        r = requests.get(url, headers=head)
                        break  # if the request is successful, break the loop
                    except Exception as e:
                        time.sleep(backoff_time)  # wait before trying again
                        backoff_time *= 2  # double the delay for the next retry
                # r = requests.get(url, headers=head)
                r.raise_for_status()  # This will raise an exception if the status code is not 200
            except requests.exceptions.RequestException as e:
                if r.status_code == 508:
                    print("Resource Limit Is Reached for URL:", url)
                    continue  # Skip this URL and continue with the next one
                else:
                    #raise  # Re-raise the exception if the status code is not 508
                    print("Some Exception Occered "+r.status_code+ " for URL:", url)

            soup = bs(r.content, "html5lib")
            # find anchor tag containing "GET COUPON CODE" text and get href attribute

            # find h1 tag contains class "clearbox" and get text, h1 tag inside div tag contains class "lineheight20 rh-flex-center-align mobileblockdisplay"
            titleDiv = soup.find("div", class_="page-title")
            # titleSubDiv = titleDiv.find("div", class_="title_single_area")
            title = titleDiv.find("h1").text

            udemyRedirectLink = soup.find("a", href=re.compile("www.udemy.com"))
            if udemyRedirectLink is not None:
                link = unquote(udemyRedirectLink["href"])

                if link.startswith("https://ad.admitad.com"):
                    link = parse_qs(link)["ulp"][0]
                elif link.startswith("http://click.linksynergy.com") or link.startswith("https://click.linksynergy.com"):
                    if "RD_PARM1" in link:
                        link = parse_qs(link)["RD_PARM1"][0]
                    elif "murl" in link:
                        link = parse_qs(link)["murl"][0]
                # else:
                #     print(link)
                if link.startswith("https://www.udemy.com"):
                    cf_links.append(title + "|:|" + link)

        print("coursefolder Courses: " + str(len(cf_links)))
        main_window["pcoursefolder"].update(0, visible=False)
        main_window["icoursefolder"].update(visible=True)
    except:
        cf_error = traceback.format_exc()
        cf_length = -1
    cf_done = True

def techlinks():
    global tl_links
    tl_links = []
    big_all = []
    head = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    }
    try:

        urls = [
            "https://techlinks.in/udemy-free-coupons?offset=0&limit=21",
            "https://techlinks.in/udemy-free-coupons?offset=21&limit=21",
            "https://techlinks.in/udemy-free-coupons?offset=42&limit=21",
            # add more URLs as needed
        ]

        for url in urls:
            backoff_time = 3  # start with a delay of 3 seconds
            for _ in range(5):  # try up to 5 times
                try:
                    r = requests.get(url, headers=head)
                    break  # if the request is successful, break the loop
                except Exception as e:
                    time.sleep(backoff_time)  # wait before trying again
                    backoff_time *= 2  # double the delay for the next retry

            # r = requests.get(url, headers=head)
            soup = bs(r.content, "html5lib")

            coursesDiv = soup.find(
                "div",
                attrs={"class": "row text-center justify-content-around"},
            )
            #find anchor tag href with in h2 tag contains class "entry-title" and get href attribute
            small_all = coursesDiv.find_all(
                "a",
                attrs={"class": "btn btn-primary"},
            )
                   
            big_all.extend(small_all)
        tl_length = len(big_all)
        main_window["ptechlinks"].update(0, max=len(big_all))

        for index, item in enumerate(big_all):
            main_window["ptechlinks"].update(index + 1)
            tl_progress = index


            url = "https://techlinks.in/"+item["href"]
            if "techlinks.in" not in url:
                continue

            try:
                backoff_time = 3  # start with a delay of 3 seconds
                for _ in range(5):  # try up to 5 times
                    try:
                        r = requests.get(url, headers=head)
                        break  # if the request is successful, break the loop
                    except Exception as e:
                        time.sleep(backoff_time)  # wait before trying again
                        backoff_time *= 2  # double the delay for the next retry

                # r = requests.get(url, headers=head)
                r.raise_for_status()  # This will raise an exception if the status code is not 200
            except requests.exceptions.RequestException as e:
                if r.status_code == 508:
                    print("Resource Limit Is Reached for URL:", url)
                    continue  # Skip this URL and continue with the next one
                else:
                    #raise  # Re-raise the exception if the status code is not 508
                    print("Some Exception Occered "+r.status_code+ " for URL:", url)

            soup = bs(r.content, "html5lib")
            # find anchor tag containing "GET COUPON CODE" text and get href attribute

            # find h1 tag contains class "clearbox" and get text, h1 tag inside div tag contains class "lineheight20 rh-flex-center-align mobileblockdisplay"
            titleDiv = soup.find("div", class_="container mt-3")
            # titleSubDiv = titleDiv.find("div", class_="title_single_area")
            title = titleDiv.find("h1").text

            udemyRedirectLink = soup.find("a", class_="btn btn-primary btn-lg")
            # get href attribute of anchor tag
            link = unquote(udemyRedirectLink["href"])

            if link.startswith("https://ad.admitad.com"):
                link = parse_qs(link)["ulp"][0]
            elif link.startswith("http://click.linksynergy.com") or link.startswith("https://click.linksynergy.com"):
                if "RD_PARM1" in link:
                    link = parse_qs(link)["RD_PARM1"][0]
                elif "murl" in link:
                    link = parse_qs(link)["murl"][0]
            # else:
            #     print(link)
            if link.startswith("https://www.udemy.com"):
                tl_links.append(title + "|:|" + link)

        print("techlinks Courses: " + str(len(tl_links)))
        main_window["ptechlinks"].update(0, visible=False)
        main_window["itechlinks"].update(visible=True)
    except:
        tl_error = traceback.format_exc()
        tl_length = -1
    tl_done = True

def freewebcart():
    
    global fwc_links
    nonce = ""
    fwc_links = []
    head = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    }
    backoff_time = 3  # start with a delay of 3 seconds
    for _ in range(5):  # try up to 5 times
        try:
            r = requests.get("https://www.freewebcart.com/course/100-off-udemy-coupons/", headers=head)
            break  # if the request is successful, break the loop
        except Exception as e:
            time.sleep(backoff_time)  # wait before trying again
            backoff_time *= 2  # double the delay for the next retry    

    #r = requests.get("https://www.freewebcart.com/course/100-off-udemy-coupons/", headers=head)
    soup = bs(r.content, "html5lib")
    
    nonce = ""
    for script in soup.find_all("script"):
        if script.string and "load_content" in script.string:
            content = script.string.replace("var stm_lms_nonces =", "").strip().rstrip(";")
            #print(content)  # Debugging line
            try:
                jsonObj = json.loads(content)
                nonce = json.loads(content)["load_content"]
                break
            except json.JSONDecodeError:
                print("Invalid JSON string")
                break
    backoff_time = 3  # start with a delay of 3 seconds            
    for _ in range(5):  # try up to 5 times
        try:
            r = requests.get(
        "https://www.freewebcart.com/wp-admin/admin-ajax.php?offset=0&template=courses/grid&args={'per_row':'4','posts_per_page':'12','tax_query':[{'taxonomy':'stm_lms_course_taxonomy','field':'term_id','terms':46}],'class':'archive_grid'}&action=stm_lms_load_content&nonce="+nonce+"&sort=date_high"
    , headers=head).json()
            break  # if the request is successful, break the loop
        except Exception as e:
            time.sleep(backoff_time)  # wait before trying again
            backoff_time *= 2  # double the delay for the next retry


    # r = requests.get(
    #     "https://www.freewebcart.com/wp-admin/admin-ajax.php?offset=0&template=courses/grid&args={'per_row':'4','posts_per_page':'12','tax_query':[{'taxonomy':'stm_lms_course_taxonomy','field':'term_id','terms':46}],'class':'archive_grid'}&action=stm_lms_load_content&nonce="+nonce+"&sort=date_high"
    # , headers=head).json()



    soup = bs(r["content"], "html5lib")
    small_all = soup.find_all("div", {"class": "stm_lms_courses__single--title"})
    main_window["pfreewebcart"].update(0, max=len(small_all))

    for index, item in enumerate(small_all):
        main_window["pfreewebcart"].update(index + 1)
        title = item.h5.string
        backoff_time = 3  # start with a delay of 3 seconds
        for _ in range(5):  # try up to 5 times
            try:
                r = requests.get(item.a["href"], headers=head)
                break  # if the request is successful, break the loop
            except Exception as e:
                time.sleep(backoff_time)  # wait before trying again
                backoff_time *= 2  # double the delay for the next retry


        # r = requests.get(item.a["href"], headers=head)
        soup = bs(r.content, "html5lib")
        fwc_links.append(
            title + "|:|" + soup.find("div", {"class": "stm-lms-buy-buttons"}).a["href"]
        )
    #write fwc_links length to console
    print("freewebcart Courses: " + str(len(fwc_links)))
    main_window["pfreewebcart"].update(0, visible=False)
    main_window["ifreewebcart"].update(visible=True)

def enext() -> list:
    en_links = []
    big_all = []
    head = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.84",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    }
    backoff_time = 3  # start with a delay of 3 seconds
    for _ in range(5):  # try up to 5 times
        try:
            r = requests.get("https://jobs.e-next.in/course/udemy", headers=head)
            break  # if the request is successful, break the loop
        except Exception as e:
            time.sleep(backoff_time)  # wait before trying again
            backoff_time *= 2  # double the delay for the next retry
    # r = requests.get("https://jobs.e-next.in/course/udemy", headers=head)
    soup = bs(r.content, "html5lib")
    #rakesh
    backoff_time = 3  # start with a delay of 3 seconds
    for _ in range(5):  # try up to 5 times
        try:
            json_response = requests.get("https://jobs.e-next.in/public/assets/data/udemy.json", headers=head).json()
            break  # if the request is successful, break the loop
        except Exception as e:
            time.sleep(backoff_time)  # wait before trying again
            backoff_time *= 2  # double the delay for the next retry
    #fetch json from url
    #json_response = requests.get("https://jobs.e-next.in/public/assets/data/udemy.json", headers=head).json()
    #push all item in big_all
    #loop first 50 items
    for item in json_response[:30]:
        big_all.append(item['title'] + "|:|"  + "https://jobs.e-next.in/course/udemy/" + item['url'])


    #make sure big_all is not None
    if big_all is not None:
        main_window["pE-next"].update(0, max=len(big_all))
        for i in big_all:
            main_window["pE-next"].update(index + 1)

            #split i with |:| and get title and link
            link = i.split("|:|")[1]
            title = i.split("|:|")[0]
            #rakesh
            backoff_time = 3  # start with a delay of 3 seconds
            for _ in range(5):  # try up to 5 times
                try:
                    r = requests.get(link, headers=head)
                    break  # if the request is successful, break the loop
                except Exception as e:
                    time.sleep(backoff_time)  # wait before trying again
                    backoff_time *= 2  # double the delay for the next retry          
            # r = requests.get(link, headers=head)
            soup = bs(r.content, "html5lib")
            #find anchor tag containing "Enroll Now free" text and get href attribute
            i = soup.find("a", string="Enroll Now free")
            #rakesh
            if i is not None and i != "":
                #append title and href attribute of anchor tag
                en_links.append(title + "|:|" + i["href"])
        
            # title = i.text[11:].strip().removesuffix("Enroll Now free").strip()
            # link = i.a["href"]
            # en_links.append(title + "|:|" + link)
        print("E-next Courses: " + str(len(en_links)))
        main_window["pE-next"].update(0, visible=False)
        main_window["iE-next"].update(visible=True)




########################### Constants

version = "v1.7"


def create_scrape_obj():
    funcs = {
        
        "LocalFile": threading.Thread(target=LocalFile, daemon=True),
        "Discudemy": threading.Thread(target=discudemy, daemon=True),
        "Udemy Freebies": threading.Thread(target=udemy_freebies, daemon=True),
        "Tutorial Bar": threading.Thread(target=tutorialbar, daemon=True),
        "Real Discount": threading.Thread(target=real_discount, daemon=True),
        "Course Vania": threading.Thread(target=coursevania, daemon=True),
        "IDownloadCoupons": threading.Thread(target=idcoupons, daemon=True),
        "E-next": threading.Thread(target=enext, daemon=True),
        "onlinecoursesooo": threading.Thread(target=onlinecoursesooo, daemon=True),
        "bestcouponhunter": threading.Thread(target=bestcouponhunter, daemon=True),
        "cursosdev": threading.Thread(target=cursosdev, daemon=True),
        "freewebcart": threading.Thread(target=freewebcart, daemon=True),
        "freebiesglobal": threading.Thread(target=freebiesglobal, daemon=True),
        "techlinks": threading.Thread(target=techlinks, daemon=True),
        "coursefolder": threading.Thread(target=coursefolder, daemon=True),
        "smartybro": threading.Thread(target=smartybro, daemon=True),
    }
    return funcs


################
def cookiejar(
    client_id,
    access_token,
    csrf_token,
):
    cookies = dict(
        client_id=client_id,
        access_token=access_token,
        csrf_token=csrf_token,
    )
    return cookies

def load_settings():
    try:
        os.rename("duce-settings.json", "duce-gui-settings.json")
    except:
        pass
    try:
        with open("duce-gui-settings.json") as f:
            settings = json.load(f)
    except FileNotFoundError:
        settings = dict(
            requests.get(
                "https://raw.githubusercontent.com/techtanic/Discounted-Udemy-Course-Enroller/master/duce-gui-settings.json"
            ).json()
        )

    title_exclude = "\n".join(settings["title_exclude"])
    instructor_exclude = "\n".join(settings["instructor_exclude"])

    settings.setdefault("save_txt", True)  # v1.3
    settings["sites"].setdefault("E-next", True)  # v1.4
    settings.setdefault("discounted_only", False)  # v1.4

    return settings, instructor_exclude, title_exclude

def save_settings():
    with open("duce-gui-settings.json", "w") as f:
        json.dump(settings, f, indent=4)

def fetch_cookies():
    cookies = browser_cookie3.load(domain_name="www.udemy.com")
    return requests.utils.dict_from_cookiejar(cookies), cookies

def get_course_id(url):

    backoff_time = 3  # start with a delay of 3 seconds
    for _ in range(5):  # try up to 5 times
        try:
            r = requests.get(url, headers=head, allow_redirects=False)
            r.raise_for_status()  # raise an exception if the response contains an HTTP error status code
            break  # if the request is successful, break the loop
        except Exception as e:
            func_name = sys._getframe().f_code.co_name
            print(f"An error occurred in function {func_name}: {e}. Retrying in {backoff_time} seconds...")
            time.sleep(backoff_time)  # wait before trying again
            backoff_time *= 2  # double the delay for the next retry

    # r = requests.get(url, headers=head, allow_redirects=False)
    if r.status_code in (404, 302, 301):
        return False
    if "/course/draft/" in url:
        return False
    soup = bs(r.content, "html5lib")

    try:
        courseid = soup.find(
            "div",
            attrs={"data-content-group": "Landing Page"},
        )["data-course-id"]
    except:
        courseid = soup.find(
            "body", attrs={"data-module-id": "course-landing-page"}
        )["data-clp-course-id"]
        
        # courseid = soup.find(
        #     "body", attrs={"data-module-id": "course-landing-page/udlite"}
        # )["data-clp-course-id"]
        # with open("problem.txt","w",encoding="utf-8") as f:
        # f.write(str(soup))
    return courseid

def get_course_coupon(url):
    query = urlsplit(url).query
    params = parse_qs(query)
    try:
        params = {k: v[0] for k, v in params.items()}
        return params["couponCode"]
    except:
        return ""

def affiliate_api(courseid):

    backoff_time = 3  # start with a delay of 3 seconds
    for _ in range(5):  # try up to 5 times
        try:
            r = s.get(
                "https://www.udemy.com/api-2.0/courses/"
                + courseid
                + "/?fields[course]=locale,primary_category,avg_rating_recent,visible_instructors",
            ).json()
            #r.raise_for_status()  # raise an exception if the response contains an HTTP error status code
            break  # if the request is successful, break the loop
        except Exception as e:
            func_name = sys._getframe().f_code.co_name
            print(f"An error occurred in function {func_name}: {e}. Retrying in {backoff_time} seconds...")
            time.sleep(backoff_time)  # wait before trying again
            backoff_time *= 2  # double the delay for the next retry

    # ... existing code ...

    # r = s.get(
    #     "https://www.udemy.com/api-2.0/courses/"
    #     + courseid
    #     + "/?fields[course]=locale,primary_category,avg_rating_recent,visible_instructors",
    # ).json()

    instructor = (
        r["visible_instructors"][0]["url"].replace("/user/", "").rstrip("/")
    )
    return (
        r["primary_category"]["title"],
        r["locale"]["simple_english_title"],
        round(r["avg_rating_recent"], 1),
        instructor,
    )

def course_landing_api(courseid):
    

    # ... existing code ...

    backoff_time = 3  # start with a delay of 3 seconds
    for _ in range(5):  # try up to 5 times
        try:
            r = s.get(
                "https://www.udemy.com/api-2.0/course-landing-components/"
                + courseid
                + "/me/?components=purchase"
            ).json()
            #r.raise_for_status()  # raise an exception if the response contains an HTTP error status code
            break  # if the request is successful, break the loop
        except Exception as e:
            func_name = sys._getframe().f_code.co_name
            print(f"An error occurred in function {func_name}: {e}. Retrying in {backoff_time} seconds...")
            time.sleep(backoff_time)  # wait before trying again
            backoff_time *= 2  # double the delay for the next retry

    # ... existing code ...

    # r = s.get(
    #     "https://www.udemy.com/api-2.0/course-landing-components/"
    #     + courseid
    #     + "/me/?components=purchase"
    # ).json()

    try:
        purchased = r["purchase"]["data"]["purchase_date"]
    except:
        purchased = False

    try:
        amount = r["purchase"]["data"]["list_price"]["amount"]
    except:
        print(r["purchase"]["data"])
    return purchased, Decimal(amount)


# def remove_duplicates(l):
#     l = l[::-1]
#     for i in l:
#         while l.count(i) > 1:
#             l.remove(i)
#     return l[::-1]

#rakesh
def remove_duplicates(l):
    print("Before removing duplicates: ", len(l))
    seen = set()
    result = []
    for item in l:
        url = item.split('|:|')[1].lower()  # Get the URL part
        if url not in seen:
            seen.add(url)
            result.append(item)
    print("After removing duplicates: ", len(result))
    return result

def update_courses():
    while True:
        r = s.get("https://www.udemy.com/api-2.0/users/me/subscribed-courses/").json()
        new_menu = [
            ["Help", ["Support", "Github", "Discord"]],
            [f'Total Courses: {r["count"]}'],
        ]
        main_window["mn"].Update(menu_definition=new_menu)
        time.sleep(10)  # So that Udemy's api doesn't get spammed.

def update_available():
    release_version = requests.get(
        "https://api.github.com/repos/techtanic/Discounted-Udemy-Course-Enroller/releases/latest"
    ).json()["tag_name"]
    if version.lstrip("v") < release_version.lstrip("v"):
        return (
            f" Update {release_version} Availabe",
            f"Update {release_version} Availabe",
        )
    else:
        return f"Login {version}", f"Discounted-Udemy-Course-Enroller {version}"

def manual_login():
    for retry in range(0, 2):

        s = cloudscraper.CloudScraper()
        
        r = s.get(
            "https://www.udemy.com/join/signup-popup/",
        )
        soup = bs(r.text, "html5lib")
        
        csrf_token = soup.find("input", {"name": "csrfmiddlewaretoken"})["value"]
        data = {
            "csrfmiddlewaretoken": csrf_token,
            "locale": "en_US",
            "email": settings["email"],
            "password": settings["password"],
        }

        s.headers.update({"Referer": "https://www.udemy.com/join/signup-popup/"})
        r = s.get("https://www.udemy.com/join/login-popup/?locale=en_US")
        try:
            r = s.post(
                "https://www.udemy.com/join/login-popup/?locale=en_US",
                data=data,
                allow_redirects=False,
            )
        except cloudscraper.exceptions.CloudflareChallengeError:
            continue
        if r.status_code == 302:
            return "", r.cookies["client_id"], r.cookies["access_token"], csrf_token
        else:
            soup = bs(r.content, "html5lib")
            with open("test.txt", "w") as f:
                f.write(r.text)
            txt = soup.find(
                "div", class_="alert alert-danger js-error-alert"
            ).text.strip()
            if txt[0] == "Y":
                return "Too many logins per hour try later", "", "", ""
            elif txt[0] == "T":
                return "Email or password incorrect", "", "", ""
            else:
                return txt, "", "", ""

    return "Cloudflare is blocking your requests try again after an hour", "", "", ""

def check_login(client_id, access_token, csrf_token):
    head = {
        "authorization": "Bearer " + access_token,
        "accept": "application/json, text/plain, */*",
        "x-requested-with": "XMLHttpRequest",
        "x-forwarded-for": str(
            ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
        ),
        "x-udemy-authorization": "Bearer " + access_token,
        "content-type": "application/json;charset=UTF-8",
        "origin": "https://www.udemy.com",
        "referer": "https://www.udemy.com/",
        "dnt": "1",
    }

    r = requests.get(
        "https://www.udemy.com/api-2.0/contexts/me/?me=True&Config=True", headers=head
    ).json()
    currency = r["Config"]["price_country"]["currency"]
    user = r["me"]["display_name"]

    s = requests.session()
    cookies = cookiejar(client_id, access_token, csrf_token)
    s.cookies.update(cookies)
    s.headers.update(head)
    s.keep_alive = False

    return head, user, currency, s

def title_in_exclusion(title, t_x):
    title_words = title.casefold().split()
    for word in title_words:
        word = word.casefold()
        if word in t_x:
            return True
    return False


# -----------------
def free_checkout(coupon, courseid):
    payload = (
        '{"checkout_environment":"Marketplace","checkout_event":"Submit","shopping_info":{"items":[{"discountInfo":{"code":"'
        + coupon
        + '"},"buyable":{"type":"course","id":'
        + str(courseid)
        + ',"context":{}},"price":{"amount":0,"currency":"'
        + currency
        + '"}}]},"payment_info":{"payment_vendor":"Free","payment_method":"free-method"}}'
    )

    for _ in range(5):  # try up to 5 times
        try:
            
            r = s.post(
                "https://www.udemy.com/payment/checkout-submit/",
                data=payload,
                verify=False,
            )
            #r.raise_for_status()  # raise an exception if the response contains an HTTP error status code
            break  # if the request is successful, break the loop
        except Exception as e:
            func_name = sys._getframe().f_code.co_name
            print(f"An error occurred in function {func_name}: {e}. Retrying in {backoff_time} seconds...")
            time.sleep(backoff_time)  # wait before trying again
            backoff_time *= 2  # double the delay for the next retry


    # r = s.post(
    #     "https://www.udemy.com/payment/checkout-submit/",
    #     data=payload,
    #     verify=False,
    # )
    return r.json()

def free_enroll(courseid):
    backoff_time = 3  # start with a delay of 3 seconds
    for _ in range(5):  # try up to 5 times
        try:
            s.get(
                "https://www.udemy.com/course/subscribe/?courseId=" + str(courseid),
                verify=False,
            )
            #s.raise_for_status() 
            r = s.get(
                "https://www.udemy.com/api-2.0/users/me/subscribed-courses/"
                + str(courseid)
                + "/?fields%5Bcourse%5D=%40default%2Cbuyable_object_type%2Cprimary_subcategory%2Cis_private",
                verify=False,
            )
            #r.raise_for_status()  # raise an exception if the response contains an HTTP error status code
            break  # if the request is successful, break the loop
        except Exception as e:
            func_name = sys._getframe().f_code.co_name
            print(f"An error occurred in function {func_name}: {e}. Retrying in {backoff_time} seconds...")
            time.sleep(backoff_time)  # wait before trying again
            backoff_time *= 2  # double the delay for the next retry

    # s.get(
    #     "https://www.udemy.com/course/subscribe/?courseId=" + str(courseid),
    #     verify=False,
    # )

    # r = s.get(
    #     "https://www.udemy.com/api-2.0/users/me/subscribed-courses/"
    #     + str(courseid)
    #     + "/?fields%5Bcourse%5D=%40default%2Cbuyable_object_type%2Cprimary_subcategory%2Cis_private",
    #     verify=False,
    # )
    return r.json()


# -----------------


def auto(list_st):
    main_window["pout"].update(0, max=len(list_st))
    se_c, ae_c, e_c, ex_c, as_c = 0, 0, 0, 0, 0
    if settings["save_txt"]:
        if not os.path.exists("Courses/"):
            os.makedirs("Courses/")
        txt_file = open(f"Courses/" + time.strftime("%Y-%m-%d--%H-%M"), "w")
    for index, combo in enumerate(list_st):
        tl = combo.split("|:|")
        main_window["out"].print(str(index) + " " + tl[0], text_color="yellow", end=" ")
        link = tl[1]
        link = link.replace('\n', '')
        main_window["out"].print(link, text_color="blue")
        try:
            course_id = get_course_id(link)
            if course_id:
                coupon_id = get_course_coupon(link)
                cat, lang, avg_rating, instructor = affiliate_api(course_id)
                purchased, amount = course_landing_api(course_id)
                
                if (
                    # instructor in instructor_exclude
                    # or title_in_exclusion(tl[0], title_exclude)
                    # or cat not in categories
                    # or lang not in languages
                    # or 
                    avg_rating < min_rating
                ):
                    # if instructor in instructor_exclude:
                    #     main_window["out"].print(
                    #         f"Instructor excluded: {instructor}",
                    #         text_color="light blue",
                    #     )
                    # elif title_in_exclusion(tl[0], title_exclude):
                    #     main_window["out"].print(
                    #         "Title Excluded", text_color="light blue"
                    #     )
                    # elif cat not in categories:
                    #     main_window["out"].print(
                    #         f"Category excluded: {cat}", text_color="light blue"
                    #     )
                    # elif lang not in languages:
                    #     main_window["out"].print(
                    #         f"Languages excluded: {lang}", text_color="light blue"
                    #     )
                    # elif avg_rating < min_rating:
                    if avg_rating < min_rating:
                        main_window["out"].print(
                            f"Poor rating: {avg_rating}", text_color="light blue"
                        )
                    main_window["out"].print()
                    ex_c += 1

                else:

                    if not purchased:

                        if coupon_id:
                            slp = ""

                            js = free_checkout(coupon_id, course_id)
                            try:
                                if js["status"] == "succeeded":
                                    main_window["out"].print(
                                        "Successfully Enrolled To Course :)",
                                        text_color="green",
                                    )
                                    main_window["out"].print()
                                    se_c += 1
                                    as_c += amount
                                    if settings["save_txt"]:
                                        txt_file.write(combo + "\n")
                                        txt_file.flush()
                                        os.fsync(txt_file.fileno())
                                elif js["status"] == "failed":
                                    # print(js)
                                    main_window["out"].print(
                                        "Coupon Expired :(", text_color="red"
                                    )
                                    main_window["out"].print()
                                    e_c += 1

                            except:
                                try:
                                    msg = js["detail"]
                                    main_window["out"].print(
                                        f"{msg}", text_color="dark blue"
                                    )
                                    main_window["out"].print()
                                    print(js)
                                    slp = int(re.search(r"\d+", msg).group(0))
                                except:
                                    # print(js)
                                    main_window["out"].print(
                                        "Expired Coupon", text_color="red"
                                    )
                                    main_window["out"].print()
                                    e_c += 1

                            if slp != "":
                                slp += 3
                                main_window["out"].print(
                                    ">>> Pausing execution of script for "
                                    + str(slp)
                                    + " seconds",
                                    text_color="red",
                                )
                                time.sleep(slp)
                                main_window["out"].print()
                            else:
                                time.sleep(3.5)

                        elif not coupon_id:
                            if settings["discounted_only"]:
                                main_window["out"].print(
                                    "Free course excluded", text_color="light blue"
                                )
                                ex_c += 1
                                continue
                            js = free_enroll(course_id)
                            try:
                                if js["_class"] == "course":
                                    main_window["out"].print(
                                        "Successfully Subscribed", text_color="green"
                                    )
                                    main_window["out"].print()
                                    se_c += 1
                                    as_c += amount

                                    if settings["save_txt"]:
                                        txt_file.write(combo + "\n")
                                        txt_file.flush()
                                        os.fsync(txt_file.fileno())

                            except:
                                main_window["out"].print(
                                    "COUPON MIGHT HAVE EXPIRED", text_color="red"
                                )
                                main_window["out"].print()
                                e_c += 1

                    elif purchased:
                        main_window["out"].print(purchased, text_color="light blue")
                        main_window["out"].print()
                        ae_c += 1

            elif not course_id:
                main_window["out"].print(".Course Expired.", text_color="red")
                e_c += 1
            main_window["pout"].update(index + 1)
        except:
            e = traceback.format_exc()
            print(e)
    main_window["done_col"].update(visible=True)

    main_window["se_c"].update(value=f"Successfully Enrolled: {se_c}")
    main_window["as_c"].update(value=f"Amount Saved: ${round(as_c,2)}")
    main_window["ae_c"].update(value=f"Already Enrolled: {ae_c}")
    main_window["e_c"].update(value=f"Expired Courses: {e_c}")
    main_window["ex_c"].update(value=f"Excluded Courses: {ex_c}")


##########################################


def main1():
    try:
        links_ls = []
        for key in funcs:
            main_window[f"pcol{key}"].update(visible=True)
        main_window["main_col"].update(visible=False)
        main_window["scrape_col"].update(visible=True)
        for key in funcs:
            funcs[key].start()
        for t in funcs:
            funcs[t].join()
        main_window["scrape_col"].update(visible=False)
        main_window["output_col"].update(visible=True)

        for link_list in [
            "local_links",
            "du_links",
            "uf_links",
            "tb_links",
            "rd_links",
            "cv_links",
            "idc_links",
            "en_links",
            "ooo_links",
            "bch_links",
            "cd_links",
            "fwc_links",
            "fg_links",
            "tl_links",
            "cf_links",
            "smbro_links",
        ]:
            try:
                links_ls += eval(link_list)
            except:
                pass

        auto(remove_duplicates(links_ls))

    except:
        e = traceback.format_exc()
        sg.popup_scrolled(e, title=f"Unknown Error {version}")

    main_window["output_col"].Update(visible=False)


settings, instructor_exclude, title_exclude = load_settings()
login_title, main_title = update_available()


############## MAIN ############# MAIN############## MAIN ############# MAIN ############## MAIN ############# MAIN ###########
menu = [["Help", ["Support", "Github", "Discord"]]]

login_error = False
try:
    if settings["stay_logged_in"]["auto"]:
        # my_cookies, cookies = fetch_cookies()
        # head, user, currency, s = check_login(
        #     my_cookies["client_id"], my_cookies["access_token"], my_cookies["csrftoken"]
        # )
        
        client_id = "bd2565cb7b0c313f5e9bae44961e8db2"
        access_token = "3Mk2xLcQ5oQaGIrMFSRlxTOffncSlg2nGB6Zmcl8"
        csrftoken = "yeiV0LzFB9DfFC2efUyKipdI42mQZh02gRfP6CdXzfmG7uvSGZhSPC7Iuuvfzbsb"
        head, user, currency, s = check_login(client_id,access_token,csrftoken)

    elif settings["stay_logged_in"]["manual"]:
        txt, client_id, access_token, csrf_token = manual_login()
        if not txt:
            head, user, currency, s = check_login(client_id, access_token, csrf_token)

except:
    login_error = True
if (
    not settings["stay_logged_in"]["auto"] and not settings["stay_logged_in"]["manual"]
) or login_error:

    c1 = [
        [
            sg.Button(key="a_login", image_data=auto_login),
            sg.T(""),
            sg.B(key="m_login", image_data=manual_login_),
        ],
        [
            sg.Checkbox(
                "Stay logged-in",
                default=settings["stay_logged_in"]["auto"],
                key="sli_a",
            )
        ],
    ]
    c2 = [
        [
            sg.T("Email"),
            sg.InputText(
                default_text=settings["email"], key="email", size=(20, 1), pad=(5, 5)
            ),
        ],
        [
            sg.T("Password"),
            sg.InputText(
                default_text=settings["password"],
                key="password",
                size=(20, 1),
                pad=(5, 5),
                password_char="*",
            ),
        ],
        [
            sg.Checkbox(
                "Stay logged-in",
                default=settings["stay_logged_in"]["manual"],
                key="sli_m",
            )
        ],
        [
            sg.B(key="Back", image_data=back),
            sg.T("                     "),
            sg.B(key="Login", image_data=login),
        ],
    ]

    login_layout = [
        [sg.Menu(menu)],
        [sg.Column(c1, key="col1"), sg.Column(c2, visible=False, key="col2")],
    ]

    login_window = sg.Window(login_title, login_layout)

    while True:
        event, values = login_window.read()

        if event in (None,):
            login_window.close()
            sys.exit()

        elif event == "a_login":
            try:
                #my_cookies, cookies = fetch_cookies()
                try:
                    # client_id = "bd2565cb7b0c313f5e9bae44961e8db2"
                    # access_token = "zGvbYjA5ORRyHHYdcXydVkw444s0G6a1DWlUteME"
                    # csrftoken = "q1KtUPzFjfzfPFUC5izNk2JOC1sQq0c3cUgQC6kwDGhsvHnOJxIbOcrcjnU8MvJb"
                    client_id = "bd2565cb7b0c313f5e9bae44961e8db2"
                    access_token = "3Mk2xLcQ5oQaGIrMFSRlxTOffncSlg2nGB6Zmcl8"
                    csrftoken = "yeiV0LzFB9DfFC2efUyKipdI42mQZh02gRfP6CdXzfmG7uvSGZhSPC7Iuuvfzbsb"
        
                    head, user, currency, s = check_login(client_id,access_token,csrftoken)
                    
                    # head, user, currency, s = check_login(
                    #     my_cookies["client_id"],
                    #     my_cookies["access_token"],
                    #     my_cookies["csrftoken"],
                    # )
                    settings["stay_logged_in"]["auto"] = values["sli_a"]
                    save_settings()
                    login_window.close()
                    break

                except Exception as e:
                    
                    e = traceback.format_exc()
                    print(e)
                    sg.popup_auto_close(
                        "Make sure you are logged in to udemy.com in chrome browser",
                        title="Error",
                        auto_close_duration=5,
                        no_titlebar=True,
                    )

            except Exception as e:
                e = traceback.format_exc()
                sg.popup_scrolled(e, title=f"Unknown Error {version}")

        elif event == "m_login":
            login_window["col1"].update(visible=False)
            login_window["col2"].update(visible=True)

            login_window["email"].update(value=settings["email"])
            login_window["password"].update(value=settings["password"])

        elif event == "Github":
            web("https://github.com/techtanic/Discounted-Udemy-Course-Enroller")

        elif event == "Support":
            web("https://techtanic.github.io/duce/")

        elif event == "Discord":
            web("https://discord.gg/wFsfhJh4Rh")

        elif event == "Back":
            login_window["col1"].update(visible=True)
            login_window["col2"].update(visible=False)

        elif event == "Login":

            settings["email"] = values["email"]
            settings["password"] = values["password"]
            try:
                txt, client_id, access_token, csrf_token = manual_login()
                if not txt:
                    head, user, currency, s = check_login(
                        client_id, access_token, csrf_token
                    )
                    settings["stay_logged_in"]["manual"] = values["sli_m"]
                    save_settings()
                    login_window.close()
                    break
                else:
                    sg.popup_auto_close(
                        txt,
                        title="Error",
                        auto_close_duration=5,
                        no_titlebar=True,
                    )

            except:
                e = traceback.format_exc()
                sg.popup_scrolled(e, title=f"Unknown Error {version}")

# checkbox_lo = []
# for key in settings["sites"]:
#     checkbox_lo.append([sg.Checkbox(key, key=key, default=settings["sites"][key])])

#rakesh
checkbox_lo = []
checkbox_k = list(settings["sites"].keys())
checkbox_v = list(settings["sites"].values())
for index, _ in enumerate(settings["sites"]):
    if index % 3 == 0:
        try:
            checkbox_lo.append(
                [
                    sg.Checkbox(
                        checkbox_k[index],
                        default=checkbox_v[index],
                        key=checkbox_k[index],
                        size=(16, 1),
                    ),
                    sg.Checkbox(
                        checkbox_k[index + 1],
                        default=checkbox_v[index + 1],
                        key=checkbox_k[index + 1],
                        size=(16, 1),
                    ),
                    sg.Checkbox(
                        checkbox_k[index + 2],
                        default=checkbox_v[index + 2],
                        key=checkbox_k[index + 2],
                        size=(15, 1),
                    ),
                ]
            )
        except:
            temp = []
            for i in range(index, len(settings["sites"])):
                temp.append(
                    sg.Checkbox(
                        checkbox_k[i],
                        default=checkbox_v[i],
                        key=checkbox_k[i],
                        size=(16, 1),
                    )
                )
                index += 1

            checkbox_lo.append(temp)


categories_lo = []
categories_k = list(settings["categories"].keys())
categories_v = list(settings["categories"].values())
for index, _ in enumerate(settings["categories"]):
    if index % 3 == 0:
        try:
            categories_lo.append(
                [
                    sg.Checkbox(
                        categories_k[index],
                        default=categories_v[index],
                        key=categories_k[index],
                        size=(16, 1),
                    ),
                    sg.Checkbox(
                        categories_k[index + 1],
                        default=categories_v[index + 1],
                        key=categories_k[index + 1],
                        size=(16, 1),
                    ),
                    sg.Checkbox(
                        categories_k[index + 2],
                        default=categories_v[index + 2],
                        key=categories_k[index + 2],
                        size=(15, 1),
                    ),
                ]
            )
        except:
            categories_lo.append(
                [
                    sg.Checkbox(
                        categories_k[index],
                        default=categories_v[index],
                        key=categories_k[index],
                        size=(17, 1),
                    )
                ]
            )

languages_lo = []
languages_k = list(settings["languages"].keys())
languages_v = list(settings["languages"].values())
for index, _ in enumerate(settings["languages"]):
    if index % 3 == 0:
        try:
            languages_lo.append(
                [
                    sg.Checkbox(
                        languages_k[index],
                        default=languages_v[index],
                        key=languages_k[index],
                        size=(8, 1),
                    ),
                    sg.Checkbox(
                        languages_k[index + 1],
                        default=languages_v[index + 1],
                        key=languages_k[index + 1],
                        size=(8, 1),
                    ),
                    sg.Checkbox(
                        languages_k[index + 2],
                        default=languages_v[index + 2],
                        key=languages_k[index + 2],
                        size=(8, 1),
                    ),
                ]
            )
        except IndexError:
            languages_lo.append(
                [
                    sg.Checkbox(
                        languages_k[index],
                        default=languages_v[index],
                        key=languages_k[index],
                        size=(8, 1),
                    ),
                    sg.Checkbox(
                        languages_k[index + 1],
                        default=languages_v[index + 1],
                        key=languages_k[index + 1],
                        size=(8, 1),
                    ),
                ]
            )

main_tab = [
    [
        sg.Frame(
            "Websites",
            checkbox_lo,
            "#4deeea",
            border_width=4,
            title_location="n",
            key="fcb",
        ),
        sg.Frame(
            "Language",
            languages_lo,
            "#4deeea",
            border_width=4,
            title_location="n",
            key="fl",
        ),
    ],
    [
        sg.Frame(
            "Category",
            categories_lo,
            "#4deeea",
            border_width=4,
            title_location="n",
            key="fc",
        )
    ],
]

instructor_ex_lo = [
    [
        sg.Multiline(
            default_text=instructor_exclude, key="instructor_exclude", size=(15, 10)
        )
    ],
    [sg.Text("Paste instructor(s)\nusername in new lines")],
]
title_ex_lo = [
    [sg.Multiline(default_text=title_exclude, key="title_exclude", size=(20, 10))],
    [sg.Text("Keywords in new lines\nNot cAsE sensitive")],
]

rating_lo = [
    [
        sg.Spin(
            [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0],
            initial_value=settings["min_rating"],
            key="min_rating",
            font=25,
        ),
        sg.Text("0.0 <-> 5.0", font=15),
    ]
]

advanced_tab = [
    [
        sg.Frame(
            "Exclude Instructor",
            instructor_ex_lo,
            "#4deeea",
            border_width=4,
            title_location="n",
            font=25,
        ),
        sg.Frame(
            "Title Keyword Exclusion",
            title_ex_lo,
            "#4deeea",
            border_width=4,
            title_location="n",
            font=25,
        ),
    ],
    [
        sg.Frame(
            "Minimum Rating",
            rating_lo,
            "#4deeea",
            border_width=4,
            title_location="n",
            key="f_min_rating",
            font=25,
        )
    ],
    [
        sg.Checkbox(
            "Save enrolled courses in txt", key="save_txt", default=settings["save_txt"]
        )
    ],
    [
        sg.Checkbox(
            "Enroll in Discounted courses only",
            key="discounted_only",
            default=settings["discounted_only"],
        )
    ],
]


scrape_col = []
for key in settings["sites"]:
    scrape_col.append(
        [
            sg.pin(
                sg.Column(
                    [
                        [
                            sg.Text(key, size=(12, 1)),
                            sg.ProgressBar(
                                3,
                                orientation="h",
                                key=f"p{key}",
                                bar_color=("#1c6fba", "#000000"),
                                border_width=1,
                                size=(20, 20),
                            ),
                            sg.Image(data=check_mark, visible=False, key=f"i{key}"),
                        ]
                    ],
                    key=f"pcol{key}",
                    visible=False,
                )
            )
        ]
    )

output_col = [
    [sg.Text("Output")],
    [sg.Multiline(size=(69, 12), key="out", autoscroll=True, disabled=True)],
    [
        sg.ProgressBar(
            3,
            orientation="h",
            key="pout",
            bar_color=("#1c6fba", "#000000"),
            border_width=1,
            size=(46, 20),
        )
    ],
]

done_col = [
    [sg.Text("       Stats", text_color="#FFD700")],
    [
        sg.Text(
            "Successfully Enrolled:             ",
            key="se_c",
            text_color="#7CFC00",
        )
    ],
    [
        sg.Text(
            "Amount Saved: $                                         ",
            key="as_c",
            text_color="#00FA9A",
        )
    ],
    [sg.Text("Already Enrolled:              ", key="ae_c", text_color="#00FFFF")],
    [sg.Text("Expired Courses:           ", key="e_c", text_color="#FF0000")],
    [sg.Text("Excluded Courses:          ", key="ex_c", text_color="#FF4500")],
]

main_col = [
    [
        sg.TabGroup(
            [[sg.Tab("Main", main_tab), sg.Tab("Advanced", advanced_tab)]],
            border_width=2,
            font=25,
        )
    ],
    [
        sg.Button(
            key="Start",
            tooltip="Once started will not stop until completed",
            image_data=start,
        )
    ],
]

if settings["stay_logged_in"]["auto"] or settings["stay_logged_in"]["manual"]:
    logout_btn_lo = sg.Button(key="Logout", image_data=logout)
else:
    logout_btn_lo = sg.Button(key="Logout", image_data=logout, visible=False)

main_lo = [
    [
        sg.Menu(
            menu,
            key="mn",
        )
    ],
    [sg.Text(f"Logged in as: {user}", key="user_t"), logout_btn_lo],
    [
        sg.pin(sg.Column(main_col, key="main_col")),
        sg.pin(sg.Column(output_col, key="output_col", visible=False)),
        sg.pin(sg.Column(scrape_col, key="scrape_col", visible=False)),
        sg.pin(sg.Column(done_col, key="done_col", visible=False)),
    ],
    [sg.Button(key="Exit", image_data=exit_)],
]

# ,sg.Button(key='Dummy',image_data=back)

global main_window
main_window = sg.Window(main_title, main_lo, finalize=True)
threading.Thread(target=update_courses, daemon=True).start()
update_available()
while True:

    event, values = main_window.read()
    if event == "Dummy":
        print(values)

    if event in (None, "Exit"):
        break

    elif event == "Logout":
        settings["stay_logged_in"]["auto"], settings["stay_logged_in"]["manual"] = (
            False,
            False,
        )
        save_settings()
        break

    elif event == "Support":
        web("https://techtanic.github.io/duce/support/#")

    elif event == "Github":
        web("https://github.com/techtanic/Discounted-Udemy-Course-Enroller")

    elif event == "Discord":
        web("https://discord.gg/wFsfhJh4Rh")

    elif event == "Start":

        for key in settings["languages"]:
            settings["languages"][key] = values[key]
        for key in settings["categories"]:
            settings["categories"][key] = values[key]
        for key in settings["sites"]:
            settings["sites"][key] = values[key]
        settings["instructor_exclude"] = values["instructor_exclude"].split()
        settings["title_exclude"] = list(
            filter(None, values["title_exclude"].split("\n"))
        )
        settings["min_rating"] = float(values["min_rating"])
        settings["save_txt"] = values["save_txt"]
        settings["discounted_only"] = values["discounted_only"]
        save_settings()

        all_functions = create_scrape_obj()
        funcs = {}
        sites = {}
        categories = []
        languages = []
        instructor_exclude = settings["instructor_exclude"]
        title_exclude = settings["title_exclude"]
        min_rating = settings["min_rating"]
        user_dumb = True

        for key in settings["sites"]:
            if values[key]:
                funcs[key] = all_functions[key]
                sites[key] = settings["sites"][key]
                user_dumb = False

        for key in settings["categories"]:
            if values[key]:
                categories.append(key)

        for key in settings["languages"]:
            if values[key]:
                languages.append(key)

        if user_dumb:
            sg.popup_auto_close(
                "What do you even expect to happen!",
                auto_close_duration=5,
                no_titlebar=True,
            )
        if not user_dumb:
            # for key in all_functions:
            # main_window[f"p{key}"].update(0, visible=True)
            # main_window[f"img{index}"].update(visible=False)
            # main_window[f"pcol{index}"].update(visible=False)
            threading.Thread(target=main1, daemon=True).start()

main_window.close()
