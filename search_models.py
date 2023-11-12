import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tkinter as tk
import tkinter.font as tkFont
import threading
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import requests
import json


def fetch_pdp_Extra(driver, url,check_once):
            model_id = ""
            try:
                if check_once == 0:
                    driver.execute_script("window.open('');")
                    check_once+=1
                driver.switch_to.window(driver.window_handles[1])
                driver.get(url)
                time.sleep(10)
                # driver.set_page_load_timeout(30)
                
                try:
            
                    ids = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='head-attributes svelte-16a8elv']"))
                    ).get_attribute("textContent")
                    
                    print("this is ids:",ids)
                    model_sku = ids.replace("Model No: ","")
                    model_sku = model_sku.replace("SKU: ","")
                    model_sku = model_sku.split(" ")
                    # print(model_sku)
                    model_id = model_sku[0]
                    
                except:
                    # driver.close()
                    # driver.switch_to.window(driver.window_handles[0])
                    model_id = ""
                   
                print("Model ID:",model_id)
                # driver.close()
                driver.switch_to.window(driver.window_handles[0])
                return model_id,check_once
            except:
                driver.switch_to.window(driver.window_handles[0])
                return model_id,check_once
    
def fetch_pdp_Almanea(driver, url,check_once):
            model_id = ""

            
            try:
                if check_once == 0:
                    driver.execute_script("window.open('');")
                    check_once+=1
                driver.switch_to.window(driver.window_handles[1])
                driver.get(url)
                time.sleep(10)
                # driver.set_page_load_timeout(30)
                
                try:
                
                    model_id = driver.find_element(By.CSS_SELECTOR,"td[data-th='Model']").text

                
                except:
                    # driver.close()
                    # driver.switch_to.window(driver.window_handles[0])
                    model_id = ""
                

        


                
                

                # driver.close()
                driver.switch_to.window(driver.window_handles[0])
                return model_id,check_once
            except:
                return model_id,check_once
    

def Extra_Web(driver,list_of_categories,data,Sharaf_DG):
        output_df = pd.DataFrame(columns=['Model','Extra'])
        
        for cate in list_of_categories:
            df = data[data['Category'] == cate]
            # print(df)
            list_of_models = df["Models"]
            # We got the models of one category
            check_once = 0

            for models in list_of_models:
                # if check_once == 0:
                print("Model: ",models)
                df_link = Sharaf_DG[Sharaf_DG['Category'] == cate]
                keyword = models
                # print(df_link["Links"])
                # dyno_link = df_link["Links"].iloc[0]
                # print(dyno_link)
                
                model_ids :list = []
                driver.get(f"https://www.extra.com/en-sa/search/?q={models}:relevance:brandEn:LG&text={models}&pageSize=96&pg=0&sort=relevance")
                # going to first page 
                # get number of pages
                
                # go to each page
                # go to each product then 
                # compare the model number 
                # if its matched 
                # print o 
                # else 
                # print x 
                total_pages = 1
                
                time.sleep(5)
                try:
                    # all_divs = driver.find_elements(By.CSS_SELECTOR,".main-section.svelte-dthlku")
                    # Fetching all the divs with product link
                    # 
                    # for div in all_divs:
                    #     product_link = div.find_element(By.TAG_NAME,"a").get_attribute("href")
                    #     print(product_link)
                    #     driver.get(product_link)
                        
                    all_pages_ul = driver.find_element(By.CSS_SELECTOR,".nav.ul_container.svelte-khdy6u")
                    # ul for getting pages numbers. 
                    list_of_li = all_pages_ul.find_elements(By.TAG_NAME,"li")
                    # print(int(list_of_li[-2].text))
                    total_pages = int(list_of_li[len(list_of_li)-2].text)
                    print(total_pages)
                    
                except:
                    total_pages = 1
                print("Total Pages:",total_pages)
                each_page = 0
                while each_page < total_pages:
                    
                    page_number = str(each_page)
                    url_ = str(f"https://www.extra.com/en-sa/search/?q={models}:relevance:brandEn:LG&text={models}&pageSize=96&pg={page_number}&sort=relevance")
                    # url_ = str(f"https://www.extra.com/en-sa/search/?q={models}:relevance:productFeaturesEn.Brand%20Name:LG&text={models}&pageSize=96&pg={page_number}&sort=relevance")
                    driver.get(url_)
                    # driver.get(each_page_url)
                    time.sleep(10)
                    # ids = WebDriverWait(driver, 10).until(
                    #     EC.presence_of_element_located((By.CSS_SELECTOR,".product-list"))
                    # )
                
    
                    all_divs  = driver.find_elements(By.CSS_SELECTOR,".main-section.svelte-dthlku")
                    
                    for div in all_divs:
                        product_link = div.find_element(By.TAG_NAME,"a").get_attribute("href")
                        print("Product Link:",product_link)
                        model_id,check_once = fetch_pdp_Extra(driver,product_link,check_once)
                        print(model_id)
                        # Save this model id in the list and use it later 
                        # 
                        model_ids.append(model_id)
                
                    each_page += 1
            
                # Compare here now
                total_models = len(model_ids)
                counter = 0
                for each_model in model_ids: 
                    if each_model.find(models) != -1 or models in each_model:
                        output_df = output_df.append({
                                "Model":models,
                                "Extra": "o",
                        },ignore_index=True)
                        print(models,"Found")
                        break
                    counter+=1

                if counter == total_models:
                    output_df = output_df.append({
                            "Model":models,
                            "Extra": "x",
      
                    },ignore_index=True)
                    print(models,"Not Found")


        
            
                    
                
            


        with pd.ExcelWriter("output.xlsx",mode="a",if_sheet_exists='replace') as writer:
            output_df.to_excel(writer,sheet_name="Extra")

def InfiniteScrolling(driver):
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(4)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height


def FetchProduct(model):

    # Fetch the category
    url = "https://www.almanea.sa/api/search"

    payload = json.dumps({
    "word": f"{model}"
    })
    headers = {
    'Cookie': 'wp_ga4_customerGroup=NOT%20LOGGED%20IN; __Host-next-auth.csrf-token=a0c6833a1127baf2ffd76713967f090081b75661570a0efb97352bdbb28780fd%7C3a9d6435a226bb2beaaff4b1c1658b684d5e1bba0aafe4746605bee585e8b8f1; __Secure-next-auth.callback-url=https%3A%2F%2Fwww.almanea.sa; handshake=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdG9yZSI6ImFyIiwic2Vzc2lvbklEIjoibnhKRnZDV3hQai1mR19yZ294eFd5bU1GclFDeGloTTQiLCJpYXQiOjE2OTQwODQzNjcsImV4cCI6MTY5NjY3NjM2N30.MCIpTx4Y0k7v6JNwnjl-vQi6aKtBgWdif6xanLLSX7E',
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    final_response = response.json()

    total_products = final_response['totalProduct']
    

    if total_products == 1:   
        product_link = "https://www.almanea.sa/product/"+final_response['products'][0]['_source']['rewrite_url']
        product_name = final_response['products'][0]['_source']['name'][0]
        # print(product_name)
        # Compare this name with the model 
        # If it matches then do output o 
        # Else output x
        if product_name.find(model) != -1:
            # If model is found store the output with o and break the loop
            return ({
                    "Model":model,
                    "Almanea": "o",
                    "Product Link": product_link
                    
            })
        else:
             return ({
                    "Model":model,
                    "Almanea": "x",
                    "Product Link": ""
                    
            })
    elif total_products > 1:
        product_link = "https://www.almanea.sa/product/"+final_response['products'][0]['_source']['rewrite_url']
        product_name = "https://www.almanea.sa/product/"+final_response['products'][0]['_source']['name']
        # Compare this name with the model 
        # If it matches then do output o 
        # Else output x
        if product_name.find(model) != -1:
            # If model is found store the output with o and break the loop
            return ({
                    "Model":model,
                    "Almanea": "o",
                    "Product Link": product_link
                    
            })
        else:
             return ({
                    "Model":model,
                    "Almanea": "x",
                    "Product Link": ""
                    
            })
            

    else:
        return ({
                    "Model":model,
                    "Almanea": "x",
                    "Product Link": ""
                    
        })
    

# def Almanea_Web(driver,list_of_categories,data,Sharaf_DG):
def Almanea_Web(list_of_categories,data,Sharaf_DG):
        output_df = pd.DataFrame(columns=['Model','Almanea'])
        for cate in list_of_categories:
            df = data[data['Category'] == cate]
            # print(df)
            list_of_models = df["Models"]
            
            for models in list_of_models:
                 
            
                output_df = output_df.append(FetchProduct(models),ignore_index=True)
               

        with pd.ExcelWriter("output.xlsx",mode="a",if_sheet_exists='replace') as writer:
            output_df.to_excel(writer,sheet_name="Almanea")


def Almanea_WebT20(driver,list_of_categories,data,Sharaf_DG):
        output_df = pd.DataFrame(columns=['Model','Almanea'])
        for cate in list_of_categories:
            df = data[data['Category'] == cate]
            # print(df)
            list_of_models = df["Models"]
            # We got the models of one category
            check_once = 0
          
            for models in list_of_models:
                if check_once == 0:
                    print("Model: ",models)
                    df_link = Sharaf_DG[Sharaf_DG['Category'] == cate]
                    keyword = models
                    # print(df_link["Links"])
                    dyno_link = df_link["Links"].iloc[0]
                    # print(dyno_link)
           
                    model_ids :list = []
                    # driver.get(dyno_link)
                    # # Get scroll height
                    # InfiniteScrolling(driver)
                    
                    driver.get(dyno_link)
                    time.sleep(5)
                    ids = driver.find_element(By.CSS_SELECTOR, ".products.list.items.product-items")
                    all_divs  = ids.find_elements(By.TAG_NAME, "li")
                    # print(len(all_divs))
      
                    for div in all_divs:
                        
                        link = div.find_element(By.CSS_SELECTOR,".product-item-link").get_attribute("href")
                        model_id,check_once = fetch_pdp_Almanea(driver,link,check_once)
                        print(model_id)
                        # Save this model id in the list and use it later 
                        # 
                        model_ids.append(model_id)
                


                total_models = len(model_ids)
                counter = 0
                for each_model in model_ids: 
                    if each_model.find(models) != -1:
                        output_df = output_df.append({
                                "Model":models,
                                "Almanea": "O",
                               
                                
                        },ignore_index=True)
                        print(models,"Found")
                        break
                    counter+=1

                if counter == total_models:
                    output_df = output_df.append({
                            "Model":models,
                            "Almanea": "X",
                            
      
                    },ignore_index=True)
                    print(models,"Not Found")
                
                # Compare here now

        with pd.ExcelWriter("output.xlsx",mode="a",if_sheet_exists='replace') as writer:
            output_df.to_excel(writer,sheet_name="AlmaneaTop20")
   


def Jumbo_Web(driver,list_of_categories,data):

        for cate in list_of_categories:
            df = data[data['Category'] == cate]
            # print(df)
            list_of_models = df["Model"]
            # We got the models of one category
            check_once = 0
            for models in list_of_models:
                if check_once == 0:
                    print("Model: ",models)
                    df_link = Sharaf_DG[Sharaf_DG['Category'] == cate]
                    keyword = models
                    # print(df_link["Links"])
                    dyno_link = df_link["Links"].iloc[0]
                    # print(dyno_link)
                    each_page = 0
                    model_ids :list = []
                    driver.get(dyno_link)
                    time.sleep(5)
                    try:
                        all_pages_ul = driver.find_element(By.ID,"hits-pagination")
                        # Pagination id = "hits-pagination"
                        list_of_li = all_pages_ul.find_elements(By.TAG_NAME,"li")
                        # print(int(list_of_li[-2].text))
                        total_pages = int(list_of_li[len(list_of_li)-2].text)
                        print(total_pages)

                        
                    except:
                        
                        total_pages = 1
                    
                    while each_page < total_pages:
                        Pages = f"&page_number={each_page+1}"
                        driver.get(dyno_link+Pages)
                        time.sleep(5)
                        ids = driver.find_element(By.ID,"hits")
                
                        all_divs  = ids.find_elements(By.CSS_SELECTOR, ".slide")
                        
                        for div in all_divs:
                            link = div.find_element(By.TAG_NAME,"a").get_attribute("href")
                            model_id,check_once = fetch_pdp(driver,link,check_once)
                            print(model_id)
                            # Save this model id in the list and use it later 
                            # 
                            model_ids.append(model_id)


                    
                        each_page += 1
                
                # Compare here now
                if models in model_ids:
                    print(models,"Found")
                else:
                    print(models,"Not Found")


        
            
                    
                
            # Get total number of pages 
                # Open each page 
                # Get all the products links
                # Open one by one and compare the model number with the product model number
                # If found, save O 
                # Else save X
                # Move to next page


            # driver.get(dyno_link)
            # time.sleep(5)
            # try:
            #     ids = driver.find_element(By.ID,"hits")
            #     all_divs  = ids.find_elements(By.CSS_SELECTOR, ".slide")
            #     number_of_products = len(all_divs)
            #     sharaf_dg_output = "O"
            #     print("Sharf dg Found")

            # except:
            #     sharaf_dg_output = "X"
            #     print("Sharf dg Not Found")
            
            # # Lulu From here 
            # df_link = LULU[LULU['Category'] == cate]
            # keyword = models
            # # print(df_link["Links"])
            # dyno_link = df_link["Links"].iloc[0].format(keyword=keyword)
            # # print(dyno_link)
            # driver.get(dyno_link)
            # time.sleep(5)
            # # try:
            # ids = driver.find_element(By.ID,"moreLoadedProducts")
            # all_divs  = ids.find_elements(By.CSS_SELECTOR, ".product__list--item")
            # # print(len(all_divs))
            # if len(all_divs) <=0:
            #     lulu_output = "X"
            #     print("Lulu Not Found")
            # else:
            #     lulu_output = "O"
            #     print("Lulu Found")
            # # except:
            # #     lulu_output = "X"
            # #     print("Lulu Not Found")

            # # Jumbo From here 
            # df_link = Jumbo[Jumbo['Category'] == cate]
            # keyword = models
            # # print(df_link["Links"])
            # dyno_link = df_link["Links"].iloc[0].format(keyword=keyword)
            # # print(dyno_link)
            # driver.get(dyno_link)
            # time.sleep(5)
            # try:
            #     ids=  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".col-lg-9.border-box.products-list.products-list-en")))
            #     # ids = ids.find_elements(By.CSS_SELECTOR,".list-view")
            #     all_divs  = ids.find_elements(By.CSS_SELECTOR, ".flex.gap-0.flex-col.w-full")
            #     if len(all_divs) <=0:
            #         jumbo_output = "X"
            #         print("Jumbo Not Found")
            #     else:
            #         jumbo_output = "O"
            #         print("Jumbo Found")
                
            #     output_df = output_df.append({
            #             "Model":keyword,
                        
            #             "Sharaf_DG": sharaf_dg_output,
            #             "Lulu": lulu_output,
            #             "Jumbo": jumbo_output,
                        
            #     },ignore_index=True)
                
            # except:
            #     jumbo_output="X"
            #     output_df = output_df.append({
            #             "Model":keyword,
                        
            #             "Sharaf_DG": sharaf_dg_output,
            #             "Lulu": lulu_output,
            #             "Jumbo": jumbo_output,
                        
            #     },ignore_index=True)
            #     print("Jumbo Not Found")
 

def Run_Extra():




    # 0------------------------------------------------------------------------------
    # df_sharaf_dg_categories_keywords = pd.read_excel("search_keywords.xlsx")
    # df_sharaf_dg_brands = pd.read_excel("input.xlsx")
    data = pd.read_excel("models.xlsx",sheet_name="Models")
    Sharaf_DG = pd.read_excel("models.xlsx",sheet_name="Extra")
    # LULU = pd.read_excel("models.xlsx",sheet_name="LULU")
    # Jumbo = pd.read_excel("models.xlsx",sheet_name="Jumbo")
    # output_df = pd.DataFrame(columns=['Model','Sharaf_DG'])
    # print(data["Model"])
    
    # print(data["Category"].unique())
    # driver = webdriver.Chrome(options=chrome_options)
    driver = webdriver.Chrome("C:\Program Files\chromedriver.exe")
    list_of_categories = data["Category"].unique()

    Extra_Web(driver,list_of_categories,data,Sharaf_DG)
    # Lulu_Web(driver,list_of_categories,data,LULU)
    # Jumbo_Web(driver,list_of_categories,data,Jumbo)

        


        
            
                    
                
            # Get total number of pages 
                # Open each page 
                # Get all the products links
                # Open one by one and compare the model number with the product model number
                # If found, save O 
                # Else save X
                # Move to next page


            # driver.get(dyno_link)
            # time.sleep(5)
            # try:
            #     ids = driver.find_element(By.ID,"hits")
            #     all_divs  = ids.find_elements(By.CSS_SELECTOR, ".slide")
            #     number_of_products = len(all_divs)
            #     sharaf_dg_output = "O"
            #     print("Sharf dg Found")

            # except:
            #     sharaf_dg_output = "X"
            #     print("Sharf dg Not Found")
            
            # # Lulu From here 
            # df_link = LULU[LULU['Category'] == cate]
            # keyword = models
            # # print(df_link["Links"])
            # dyno_link = df_link["Links"].iloc[0].format(keyword=keyword)
            # # print(dyno_link)
            # driver.get(dyno_link)
            # time.sleep(5)
            # # try:
            # ids = driver.find_element(By.ID,"moreLoadedProducts")
            # all_divs  = ids.find_elements(By.CSS_SELECTOR, ".product__list--item")
            # # print(len(all_divs))
            # if len(all_divs) <=0:
            #     lulu_output = "X"
            #     print("Lulu Not Found")
            # else:
            #     lulu_output = "O"
            #     print("Lulu Found")
            # # except:
            # #     lulu_output = "X"
            # #     print("Lulu Not Found")

            # # Jumbo From here 
            # df_link = Jumbo[Jumbo['Category'] == cate]
            # keyword = models
            # # print(df_link["Links"])
            # dyno_link = df_link["Links"].iloc[0].format(keyword=keyword)
            # # print(dyno_link)
            # driver.get(dyno_link)
            # time.sleep(5)
            # try:
            #     ids=  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".col-lg-9.border-box.products-list.products-list-en")))
            #     # ids = ids.find_elements(By.CSS_SELECTOR,".list-view")
            #     all_divs  = ids.find_elements(By.CSS_SELECTOR, ".flex.gap-0.flex-col.w-full")
            #     if len(all_divs) <=0:
            #         jumbo_output = "X"
            #         print("Jumbo Not Found")
            #     else:
            #         jumbo_output = "O"
            #         print("Jumbo Found")
                
            #     output_df = output_df.append({
            #             "Model":keyword,
                        
            #             "Sharaf_DG": sharaf_dg_output,
            #             "Lulu": lulu_output,
            #             "Jumbo": jumbo_output,
                        
            #     },ignore_index=True)
                
            # except:
            #     jumbo_output="X"
            #     output_df = output_df.append({
            #             "Model":keyword,
                        
            #             "Sharaf_DG": sharaf_dg_output,
            #             "Lulu": lulu_output,
            #             "Jumbo": jumbo_output,
                        
            #     },ignore_index=True)
            #     print("Jumbo Not Found")
    # # list_of_categories = df_sharaf_dg_categories_keywords.Category.unique()
    # df  = pd.DataFrame(columns=['keywords'])
    # # print(df_sharaf_dg_models[0])
    # # print(len(df_sharaf_dg_models))
    # list_of_models = []
    # for each_model in df_sharaf_dg_models.iterrows():
    #     list_of_models.append(each_model[1]["Keywords"].split(".")[0])


    # chrome_options = Options()
    # # chrome_options.add_argument("--headless")  # Comment out this line if you want to see the browser window

    # driver = webdriver.Chrome(options=chrome_options)

    # output_df = pd.DataFrame(columns=['Model','Sharaf_DG'])
    # for keyword in list_of_models:
    #     link = f"https://uae.sharafdg.com/?q={keyword}&post_type=product"
    #     driver.get(link)
    #     time.sleep(5)
    #     try:
    #         ids = driver.find_element(By.ID,"hits")
    #         all_divs  = ids.find_elements(By.CSS_SELECTOR, ".slide")
    #         number_of_products = len(all_divs)
    #         sharaf_dg_output = "O"
    #         print("Sharf dg Found")

    #     except:
    #         sharaf_dg_output = "X"
    #         print("Sharf dg Not Found")
    #     link = f"https://www.luluhypermarket.com/en-ae/search/?text={keyword}%3Arelevance"
    #     driver.get(link)
    #     time.sleep(5)
    #     try:
    #         ids = driver.find_element(By.ID,"moreLoadedProducts")
    #         all_divs  = ids.find_elements(By.CSS_SELECTOR, ".product__list--item")
    #         lulu_output = "O"
    #         print("Lulu Found")
    #     except:
    #         lulu_output = "X"
    #         print("Lulu Not Found")

    #     link = f"https://www.jumbo.ae/search/{keyword}"
    #     driver.get(link)
    #     time.sleep(5)
    #     try:
    #         ids=  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".col-lg-9.border-box.products-list.products-list-en")))
    #         # ids = ids.find_elements(By.CSS_SELECTOR,".list-view")
    #         all_divs  = ids.find_elements(By.CSS_SELECTOR, ".flex.gap-0.flex-col.w-full")
    #         jumbo_output = "O"
    #         print("Jumbo Found")
    #     except:
    #         jumbo_output="X"
            
    #         print("Jumbo Not Found")
    #     link = f"https://uae.emaxme.com/search?q={keyword}"
    #     driver.get(link)
    #     time.sleep(5)

    #     try:
    #         ids = driver.find_element(By.ID,"search-list-layout")
    #         main_div  = ids.find_element(By.CSS_SELECTOR, ".MuiGrid-root.MuiGrid-container.MuiGrid-spacing-xs-2")

    #         emax_output = "O"

    #         print("Emax Found")
    #     except:
    #         emax_output="X"
    #         print("Emax Not Found")
        


        
    #     link = f"https://www.lg.com/ae/search/search-all?search={keyword}"
    #     driver.get(link)
    #     time.sleep(5)
    #     try:
    #         ids = driver.find_element(By.CSS_SELECTOR,"ul.list-box")
    #         all_divs  = ids.find_elements(By.TAG_NAME, "li")
            
    #         output_df = output_df.append({
    #             "Model":keyword,
    #             "LG.COM": "O",
    #             "Sharaf_DG": sharaf_dg_output,
    #             "Lulu": lulu_output,
    #             "Jumbo": jumbo_output,
    #             "EMax": emax_output
    #         },ignore_index=True)

    #         print("LG Found")
    #     except:
    #         output_df = output_df.append({
    #             "Model":keyword,
    #             "LG.COM": "X",
    #             "Sharaf_DG": sharaf_dg_output,
    #             "Lulu": lulu_output,
    #             "Jumbo": jumbo_output,
    #             "EMax": emax_output
    #         },ignore_index=True)
    #         print("LG Not Found")

    # with pd.ExcelWriter("output.xlsx",mode="a",if_sheet_exists='replace') as writer:
    #         output_df.to_excel(writer)
  

def Run_Almanea():




    # 0------------------------------------------------------------------------------
    # df_sharaf_dg_categories_keywords = pd.read_excel("search_keywords.xlsx")
    # df_sharaf_dg_brands = pd.read_excel("input.xlsx")
    data = pd.read_excel("models.xlsx",sheet_name="Models")
    
    LULU = pd.read_excel("models.xlsx",sheet_name="Almanea")
    
    # print(data["Model"])
    
    # print(data["Category"].unique())
    # driver = webdriver.Chrome(options=chrome_options)
    # driver = webdriver.Chrome("C:\Program Files\chromedriver.exe")
    list_of_categories = data["Category"].unique()

    # Sharaf_DG_Web(driver,list_of_categories,data,Sharaf_DG)
    # Almanea_Web(driver,list_of_categories,data,LULU)
    Almanea_Web(list_of_categories,data,LULU)
    # Jumbo_Web(driver,list_of_categories,data,Jumbo)

        


        
            
                    
         

# Main App 
class App:

    def __init__(self, root):
        #setting title
        root.title("KSA Model Check")
        ft = tkFont.Font(family='Arial Narrow',size=13)
        #setting window size
        width=640
        height=480
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        root.configure(bg='black')

        ClickBtnLabel=tk.Label(root)
       
      
        
        ClickBtnLabel["font"] = ft
        
        ClickBtnLabel["justify"] = "center"
        ClickBtnLabel["text"] = "KSA Model Check"
        ClickBtnLabel["bg"] = "black"
        ClickBtnLabel["fg"] = "white"
        ClickBtnLabel.place(x=120,y=190,width=150,height=70)
    

        
        Lulu=tk.Button(root)
        Lulu["anchor"] = "center"
        Lulu["bg"] = "#009841"
        Lulu["borderwidth"] = "0px"
        
        Lulu["font"] = ft
        Lulu["fg"] = "#ffffff"
        Lulu["justify"] = "center"
        Lulu["text"] = "START"
        Lulu["relief"] = "raised"
        Lulu.place(x=375,y=190,width=150,height=70)
        Lulu["command"] = self.start_func




  

    def ClickRun(self):

        running_actions = [
            Run_Extra,          
            # Run_Almanea,
            # Run_Jumbo
        ]

        thread_list = [threading.Thread(target=func) for func in running_actions]

        # start all the threads
        for thread in thread_list:
            thread.start()

        # wait for all the threads to complete
        for thread in thread_list:
            thread.join()
    
    def start_func(self):
        thread = threading.Thread(target=self.ClickRun)
        thread.start()

    
        

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()


# Run()
