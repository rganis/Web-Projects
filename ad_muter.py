import time
from selenium import webdriver
from selenium.webdriver.common.by import By
driver = webdriver.Chrome() # change this to your chromedriver path, or empty if in PATH
driver.get(r'https://accounts.spotify.com/en/login?continue=https%3A%2F%2Fopen.spotify.com%2F')
time.sleep(2)
driver.find_element(By.CSS_SELECTOR, '#login-username').send_keys('user@web.com') # change this to your spotify username
driver.find_element(By.CSS_SELECTOR, '#login-password').send_keys('P@ssw0rd') # change this to your spotify password
driver.find_element(By.CSS_SELECTOR, '#login-button').click()
while True: # checks if anything is playing, if so break and continue. otherwise wait 5 seconds and try again. if this didnt exist, the program would break if you started it while nothing was playing
    try:
        volume_mute = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[3]/footer/div/div[3]/div/div[3]/button')
        div_element = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[3]/footer/div/div[1]/div/div[2]/div[1]/div/div/div/div/span/a')
        break
    except: time.sleep(5)
while True: # its super annoying to have to refresh the div element every time, but if we dont it will throw a StaleElement error
    if len(driver.window_handles) == 0: break # if the window is closed, break and end the program
    if volume_mute.get_attribute('aria-label') == "Unmute": volume_mute.click() #unmutes if still muted from inner loop
    time.sleep(2)
    try: # check if div element for song still exists and refreshes it if it does, otherwise it will go to ad logic
        div_element = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[3]/footer/div/div[1]/div/div[2]/div[1]/div/div/div/div/span/a').get_attribute('href') 
    except: # if the div element is not found, it means an ad is playing
        volume_mute.click() # mutes the volume if href is an ad
        while True:
            try: # checks to see if the new div element is an ad, if so, refreshes the div element and continues. if not, breaks and returns to main loop
                div_element = driver.find_element(By.XPATH, '//*[@id="main"]/div/div[2]/div[3]/footer/div/div[1]/div/div[2]/div[1]/div/div/div/div/a').get_attribute('href')
                time.sleep(2)
            except: break # breaks if the ad is over and returns to main loop