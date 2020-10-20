from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import random

#do no judge paradigm search at bottom
print("Input Judge Page URL: ")
URL = input()
print("Input Number of Judges: ")
NUM_JUDGES = int(input())
CHROME_DRIVER = "/Users/child/Desktop/001 - WMDs/driver/chromedriver"
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(executable_path=CHROME_DRIVER, options=options)
STATUS = "K"
FILE = "systems.txt"
CONFLICTS = ["Matthew Tan", "Kevin Lu","Debayan Sen", "Matt Schnall", "Ruth Zheng","Chris Jun", "Nick Lepp", "Sheryl Kaczmarek", "Brendon Morris", "Talia Blatt", "Janet Novack", "Magi Ortiz"]
Nums = [[0 for x in range (2)] for y in range(NUM_JUDGES)]
f = open(FILE, 'r')
T = f.readlines()
f.close()

def percentValue(i):
    Kteam = ["Iyer &amp; Kinikar", "Kinikar &amp; Iyer", "Berhe &amp; Yang", "Yang &amp; Berhe", "Ahmed &amp; Cai", "Cai &amp; Ahmed", "Jun &amp; Raghavan", "Raghavan &amp; Jun", "Lu &amp; Gunnala", "Gunnala &amp; Lu", "Raghavan &amp; Zheng", "Zheng &amp; Raghavan", "Tang &amp; Chakravarti", "Chakravarti &amp; Tang", "Tang &amp; Bhandarkar", "Bhandarkar &amp; Tang"]
    flexTeam = ["Sreeprakash &amp; Yang", "Yang &amp; Sreeprakash", "Ahmed &amp; Ahmed", "Cai &amp; Mukherjee", "Mukherjee &amp; Cai"]
    elem = driver.find_element_by_xpath("//div[@class='main']")
    name = elem.get_attribute('innerHTML')
    start = name.find("for")+4
    end = name.find("</h4>")
    name = name[start:end]
    Nums[i][1] = name
    print(name)
    all_spans = driver.find_elements_by_xpath("//td[@class='last smallish padless']")
    if len(all_spans) == 0:
        Nums[i][0] = 999
        return 0
    count = 0
    isK = False
    isFlex = False
    percent = 0
    totalTimes = 0
    for span in all_spans:
        #team name
        if count%5 == 0:
            isK = False
            isFlex = False
            count += 1
        elif count%5 == 1:
            name = span.get_attribute('innerHTML')
            name = name.strip()
            if name in Kteam:
                isK = True
            if name in flexTeam:
                isFlex = True
            count += 1
        elif count%5 == 4:
            val = span.get_attribute('innerHTML')
            val = val.strip()
            if val == "":
                tournament = all_spans[count-4].get_attribute('innerHTML')
                tournament = tournament.strip()
                tournament = tournament + '\n'
                if tournament in T:
                    tier = all_spans[count-2].get_attribute('innerHTML')
                    tier = tier.strip()
                    totalTier = T[T.index(tournament)+1]
                    val = float(int(tier)/int(totalTier))*100.0-float(1/(2*int(totalTier)))
                    if isK and STATUS == "K":
                        totalTimes += 1
                        percent += val
                    elif isFlex and STATUS == "K":
                        totalTimes += 1
                        percent += val
                    elif isFlex and STATUS == "P":
                        totalTimes += 1
                        percent += val
                    elif not isK and STATUS == "P":
                        totalTimes += 1
                        percent += val
                    count += 1
                    continue         
                else:    
                    count += 1
                    continue
            else:
                if isK and STATUS == "K":
                    totalTimes += 1
                    percent += float(val)
                elif isFlex and STATUS == "K":
                    totalTimes += 1
                    percent += float(val)
                elif isFlex and STATUS == "P":
                    totalTimes += 1
                    percent += float(val)
                elif not isK and STATUS == "P":
                    totalTimes += 1
                    percent += float(val)
                count += 1
                continue
        else:
            count += 1
            continue
    if totalTimes == 0:
        Nums[i][0] = 999
        return 0
    Nums[i][0] = percent/totalTimes+50/(totalTimes*totalTimes)
    return 0

driver.get(URL)
driver.find_element_by_xpath("//a[@class='login-window']").click()
time.sleep(1)
elem = driver.find_element_by_name("username")
elem.send_keys("LevelRvstudios@gmail.com")
elem = driver.find_element_by_name("password")
elem.send_keys("")
elem.send_keys(Keys.ENTER)
driver.get(URL)
for i in range(0, NUM_JUDGES):
    try:
        span = driver.find_elements_by_xpath("//a[@class='buttonwhite bluetext fa fa-sm fa-file-text-o']")[i]
        span.click()
    except Exception as e:
        continue
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[1])
    try:
        driver.find_element_by_xpath("//a[@class='blue full']").click()
        percentValue(i)
    except Exception as e:
        print("ERROR")
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    driver.get(URL)
Nums.sort()
print(" ")
print(" ")
print("PREFS")
print(" ")
c = 1
for j in range(0, NUM_JUDGES):
    if Nums[j][1] in CONFLICTS:
        continue
    if Nums[j][0] == 0:
        continue
    if Nums[j][0]  == 999:
        print("NO DATA -- " + Nums[j][1])
        continue
    print(c)
    c += 1
    print(Nums[j][1] + " - " + str(Nums[j][0]))
    print(" ")

driver.quit()



    
    
