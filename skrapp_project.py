from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from wonderwords import RandomWord
import time
from typing import List

# options.add_experimental_option(name="detach", value=True)

r = RandomWord()

def wait(sec: float):
    '''
    Delay execution for a set amount of time in seconds.

    Arg:
    sec: Time to delay in seconds. Float number allows for millisecond delay.
    '''
    time.sleep(sec)

def load_file(file_name: str):
    '''
    Loads content of .txt file as list. Each line will become an element

    Arg:
    File_name: the name of the file to load, E.g. "file.txt"
    '''
    content = []
    with open (file_name, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for i in lines:
                clean = i.rstrip("\n")
                content.append(clean)
    return content

def create_skrapp_acct(directory: str):
    '''
    Create skrapp accounts with the emails from the directory inputed.
    Emails must be stored in a .txt file

    Arg:
    directory: A string of the directory containing the emails. 
    '''
    
    options = Options()
    options.add_argument("--incognito")
    driver = webdriver.Edge(options=options)
    driver.implicitly_wait(10)

    # driver.execute_script("window.localStorage.clear(); window.sessionStorage.clear();")

    emails = load_file(directory)

    logging = open("acct_logs.txt", "w")

    for i, email in enumerate(emails, start=1):
        driver.get('https://www.skrapp.io/campaign')

        wait(1)
        driver.find_element(By.ID,value="«R2knarla5ildm»").send_keys(r.word(word_min_length=5, word_max_length=10).capitalize())
        driver.find_element(By.ID,value="«R2l7arla5ildm»").send_keys(email)
        driver.find_element(By.CLASS_NAME,value="css-6afilt").click()
        
        wait(3)
        try:
            confirmation = driver.find_element(By.CLASS_NAME, "css-1hq0r99").text
            logging.write(f"{confirmation}\nAccount successfully created for email {i}: {email}\n\n")
        except:
            try:
                reason = driver.find_element(By.CLASS_NAME, "css-1o8o0xn").text
                logging.write(f"{reason}\nAccount not created for {email}\n\n")
            except:
                logging.write(f"Account not created for email {i}: {email}\n\n")

        wait(0.5)
        if i == len(emails):
            driver.quit()
        else:
            driver.refresh()
    logging.close()

def setup_passwords(directory: str):
    '''
    Complete accounts setup by creating password and completing signup questioneer and popups.
    Links must be stored in a .txt file

    Arg:
    directory: A string of the directory containing the links. 
    '''

    links = load_file(directory)

    s_logging = open ("setup_logs.txt", "w", encoding="utf-8")

    try:
        for i,link in enumerate(links, start=1):
            options = Options()
            driver = webdriver.Edge(options=options)
            #driver = webdriver.Chrome(options=options)
            options.add_argument("--incognito")
            driver.implicitly_wait(10)

            exp_wait = WebDriverWait(driver, timeout=30)

            password = "starlord76"

            try:
                driver.get(link)

                try:
                    driver.find_element(By.ID, "proceed-button").click()
                except:
                    pass
                
                driver.refresh()
                wait(0.5)
                #Setup Password
                driver.find_element(By.ID,value="pwd").send_keys(password)
                driver.find_element(By.ID,value="cpwd").send_keys(password)
                driver.find_element(By.XPATH,value='//*[@id="__next"]/div/div[1]/div/div/div[1]/div[2]/form/div/div[3]/div/div/div/div/button').click()
                print(f"--link {i}:password setup complete--")

                #info popup
                try:
                    acct_setup_popup_1 = exp_wait.until(
                        EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div[2]/div/div[1]/div/div/div/div[2]/button"))
                    )
                    acct_setup_popup_1.click()
                except:
                    pass


                #How did you hear about us popup
                acct_setup_popup_2 = exp_wait.until(
                    EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[2]/div/div[1]/div/div/div/form/div/div/div/div[1]"))
                )
                acct_setup_popup_2.click()
                driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div[1]/div/div/div/form/div/div/button").click()
                print("--Popup 1 complete--")

                #Provide details popup
                driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div[1]/div/div/div/form/div/div[1]/input").send_keys(r.word(word_min_length=5, word_max_length=10).capitalize())
                driver.find_element(By.ID, "rc_select_0").send_keys(Keys.ENTER, Keys.ENTER)
                driver.find_element(By.ID, "rc_select_1").send_keys(Keys.ENTER, Keys.ENTER)
                driver.find_element(By.ID, "rc_select_2").send_keys(Keys.ENTER, Keys.ENTER)
                driver.find_element(By.ID, "rc_select_3").send_keys(Keys.ENTER, Keys.ENTER)
                driver.find_element(By.XPATH, "/html/body/div[2]/div/div[2]/div/div[1]/div/div/div/form/div/div[6]/button[2]").submit()
                print("--Popup 2 complete--")

                #Welcome popups
                driver.find_element(By.XPATH, '//*[@id="react-joyride-step-0"]/div/div/div/div[2]/div/div/button').click()
                driver.find_element(By.XPATH, '//*[@id="react-joyride-step-1"]/div/div/div/div[2]/div/div/button').click()
                driver.find_element(By.XPATH, '//*[@id="react-joyride-step-2"]/div/div/div[1]/div[2]/div/div/button').click()
                driver.find_element(By.XPATH, '//*[@id="react-joyride-step-4"]/div/div/div[1]/div[2]/div/div/button').click()
                print(f"--link {i}: Welcome popups complete--")
                s_logging.write(f"✅ Setup Complete for:\nLink {i}\n\n")

                wait(1)
                driver.quit()
                # driver.delete_all_cookies()
                # driver.execute_script("window.localStorage.clear(); window.sessionStorage.clear();")
                # time.sleep(1)

            except Exception as e:
                s_logging.write(f"❌❌Error on link: \n{e!r}\n\n")
    finally:
        driver.quit()
        s_logging.close()


if __name__ == "__main__":

    create_skrapp_acct("email.txt")

    # setup_passwords("links.txt")