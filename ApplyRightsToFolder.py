import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from pathlib import Path
import codecs
import tkinter as tk
from tkinter import ttk
import pathlib
import sys
sys.path.insert(1, str(pathlib.Path(__file__).parent.resolve()))
import settings
import rsa
import os



###############################################################################
###
###  Created:
### Автоматическая проставновка прав в папках PAW ITarasov 08.08.2023
###
###  Redacted:
###
##################################################

####Создание директории для вывода
errCreate=0
try:
    os.mkdir(str(pathlib.Path(__file__).parent.resolve())+'\\'+'_Output')
except:
    errCreate=1


privateKey =rsa.PrivateKey(7281075739009287806768015752209289410271044883918960917421685723948455653573907533938176545280783174258024727956939943035074077775603237316239961159714417, 65537, 5583043152912610283557579620607800490323799053230687138306482943765838254135388927196204216857504275576667732487857215715449721044439107147675453478162497, 5925588345364238942707904166368032881819419170042580107042886845837205044139089513, 1228751528901849264223582414182081329648943767399792869199027630000977609)

def wait_for_element_to_load(driver,text):
    err=1
    while(err==1):
        try:
            driver.find_element(By.XPATH, text)
            err=0
        except:
            err=1
            time.sleep(0.1)
        #print(text)
    return

def element_exists(driver,text):
    exist=0
    try:
        driver.find_element(By.XPATH, text)
        exist=1
    except:
        exist=0
    return exist

def find_text_in_element(element,textstrings):
    for text in textstrings:
        found_text=element.get_attribute("title")
        if(found_text.find(text)>-1):
            break
    return found_text.find(text)

def get_book_name_from_path(path_text):
    sindextext=path_text.rfind("/")+1
    return path_text[sindextext:]

def array_to_string(array):
    outputText=''
    for text in array:
        outputText=outputText+text+'\n'
    return outputText

def remove_elements_from_one_array_that_in_another(arr1,arr2):
    for i in arr2:
        for k in arr1:
            if i in arr1:
                arr1.remove(i)
    return arr1

def text_to_array(text):
    arr=[]
    arr=text.split('\n')
    while('' in arr):
        arr.remove('')   
    return arr

def setPermissionsToAllInsideFolder(driver,sleepArray):
        wait_for_element_to_load(driver,"//*[@class='bx--overflow-menu']")
        menuElementNameClasses=driver.find_elements(By.XPATH, "//*[@class='bx--overflow-menu']")
        numMenu=0
        for menuElementNameClass in menuElementNameClasses:
            menuElementNameClass.click()
            ######Ждем подгрузки подменю, там нажимаем Set Permissions
            wait_for_element_to_load(driver,"//*[@class='bx--overflow-menu-options__option-content']")
            setPermissionsMenu=driver.find_element(By.XPATH, "//div[text()='Set Permissions']")
            setPermissionsMenu.click()
            ####Смотрим проставлен ли чекбокс, если нет, то проставляем
            wait_for_element_to_load(driver,"//*[@class='user-icon-and-name bx--col']")
            checkboxPermissions=driver.find_element(By.XPATH, "//input[@id='permission-dialog-inherit-permissions']")
            #################!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            if(not checkboxPermissions.get_attribute("checked")):
                checkboxText=driver.find_element(By.XPATH, "//*[@class='bx--checkbox-label-text']")
                checkboxText.click()
                ####И нажимаем сохранить
            wait_for_element_to_load(driver,"//*[@class='bx--btn bx--btn--primary']")
            ####
            time.sleep(sleepArray[2])
            ####
            buttonSavePermissions=driver.find_element(By.XPATH, "//button[text()='Save']")
            buttonSavePermissions.click()
            ###Ждем как пропадет подменю
            while(element_exists(driver,"//*[@class='user-icon-and-name bx--col']")):
                time.sleep(0.3)
            wait_for_element_to_load(driver,"//*[@class='bx--overflow-menu']")
            numMenu+=1
            ######
            #Задержка, для того чтобы не ронять сервер
            time.sleep(sleepArray[1])
            ######

def leaveOnlyFolders(driver):
        ## Оставляем только папки
        wait_for_element_to_load(driver,"//button[@title='Filter view']")
        driver.find_element(By.XPATH, "//button[@title='Filter view']").click()
        ####Выбираем папки
        wait_for_element_to_load(driver,"//*[@class='bx--checkbox-label-text']")
        checkboxPermissions=driver.find_element(By.XPATH, "//input[@id='table-toolbar-filter-checkbox-favorite-folder']")
        if(not checkboxPermissions.get_attribute("checked")):
            driver.find_element(By.XPATH, "//span[text()='Folder']").click()
        ###Закрываем подменю
        wait_for_element_to_load(driver,"//button[@title='Filter view']")
        driver.find_element(By.XPATH, "//button[@title='Filter view']").click()
        wait_for_element_to_load(driver,"//*[@class='bx--link bx--truncation-middle content-no-wrap icon_pading']")

def leaveAll(driver):
        ## Показываем все
        wait_for_element_to_load(driver,"//button[@title='Filter view']")
        driver.find_element(By.XPATH, "//button[@title='Filter view']").click()
        ####Выбираем ALL
        wait_for_element_to_load(driver,"//*[@class='bx--checkbox-label-text']")
        checkboxPermissions=driver.find_element(By.XPATH, "//input[@id='table-toolbar-filter-checkbox-favorite-all']")
        if(not checkboxPermissions.get_attribute("checked")):
            driver.find_element(By.XPATH, "//span[text()='All']").click()
        ###Закрываем подменю
        wait_for_element_to_load(driver,"//button[@title='Filter view']")
        driver.find_element(By.XPATH, "//button[@title='Filter view']").click()
    
def getCurrentFolderName(driver):
    ###Из списка сверху получаем имя с помощью ссылок /Наша папка, она первая и единственная из данного типа
    parentLink = driver.find_element(By.XPATH, "//li[@class='bx--breadcrumb-item bx--breadcrumb-item--current']")
    currentFolderElements=parentLink.find_elements(By.XPATH, '*')
    for currentFolderElement in currentFolderElements:
        return currentFolderElement.text
    
def goUpFolder(driver):
    ####По ссылкам над папками поднимаемся на одну вверх(последняя не из текущих)
    parentLinks = driver.find_elements(By.XPATH, "//li[@class='bx--breadcrumb-item']")
    numLink=0
    for parentLink in parentLinks:
        numLink+=1
        if(numLink==len(parentLinks)):
            parentLink.click()
            return



def main():
    
    #Работа с входными переменными
    url = settings.url
    urlTest=settings.urlTest
    urlProd=settings.urlProd
    folder= varTextFolder.get()
    userLogin =varTextLogin.get()
    userPassword=varTextPassword.get()
    #inputFilePath=varTextPath.get()
    sleepArray=settings.sleepArray
    sleepArray[0]=int(varTextSleep1.get())
    sleepArray[1]=int(varTextSleep2.get())
    sleepArray[2]=int(varTextSleep3.get())
    rememberMe=varRememberMe.get()
    servers=settings.servers
    chosenServer=comboboxServer.get()

        


    publicKey =rsa.PublicKey(7281075739009287806768015752209289410271044883918960917421685723948455653573907533938176545280783174258024727956939943035074077775603237316239961159714417,65537)
    ###перекладываем стандартные переменные в файл
    settingsFile=codecs.open(str(pathlib.Path(__file__).parent.resolve())+'\\'+'settings.py','w','utf-8')
    settingsFile.write("%s = '%s'\n" %("url",url))
    settingsFile.write("%s = '%s'\n" %("urlTest",urlTest))
    settingsFile.write("%s = '%s'\n" %("urlProd",urlProd))
    settingsFile.write("%s = '%s'\n" %("folder",folder))
    if(varRememberMe.get()):
        settingsFile.write("%s = '%s'\n" %("userLogin",userLogin))
        settingsFile.write("%s = %s\n" %("userPassword",rsa.encrypt(userPassword.encode(),publicKey)))
    else:
        settingsFile.write("%s = '%s'\n" %("userLogin",''))
        settingsFile.write("%s = %s\n" %("userPassword",b''))
    settingsFile.write("%s = %s\n" %("sleepArray",sleepArray))
    settingsFile.write("%s = %s\n" %("rememberMe",rememberMe))
    settingsFile.write("%s = %s\n" %("servers",servers))
    settingsFile.write("%s = '%s'\n" %("chosenServer",chosenServer))
    settingsFile.close()





############Начало, настройка вебдрайвера
    #service = Service(ChromeDriverManager(version="114.0.5735.90").install())
    service = Service()
    options = webdriver.ChromeOptions()
    #options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})
    #options.add_argument("--headless")
    #options.add_argument("--disable-gpu")
    options.add_argument("--allow-insecure-localhost")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--no-sandbox")
    options.add_argument("--lang=en")
    #
    #options.add_experimental_option("detach", True)
    options.set_capability("acceptInsecureCerts", True)
    driver = webdriver.Chrome(options=options)
    
############################################################################################################################################################   
    # Если дев     
    if(chosenServer=='Dev'):
        # Opening the URL
        driver.get(url)
        username = driver.find_element(By.ID, "username")
        username.send_keys(userLogin)

        password = driver.find_element(By.ID, "password")
        password.send_keys(userPassword)
        driver.find_element(By.ID, "loginButton").click()

    #Если авторизация CAM(тест/прод)
    if(chosenServer=='Test'):
        completeUrlTest='http://'+userLogin+':'+userPassword+'@'+urlTest
        driver.get(completeUrlTest)
    
    if(chosenServer=='Prod'):
        completeUrlTest='http://'+userLogin+':'+userPassword+'@'+urlProd
        driver.get(completeUrlTest)

       
    ##Выбираем нужную ПАПКУ и находим ее , нажимаем
    wait_for_element_to_load(driver,"//a[@class='bx--link bx--truncation-middle content-no-wrap icon_pading']")
    folderElementNameClasses=driver.find_elements(By.XPATH, "//a[@class='bx--link bx--truncation-middle content-no-wrap icon_pading']")
    isFound=0
    for folderElementNameClass in folderElementNameClasses:
        #####Если название слишком длинное, то оно сокращается, а полное пишется в title
        if((folderElementNameClass.get_attribute("title")!='' and folderElementNameClass.get_attribute("title").find(folder)>-1) or (folderElementNameClass.text==folder)):
            folderElementNameClass.click()
            isFound=1
            break

    if(not isFound):
         sys.exit()
    


    level=1
    checkedFolders=[]
    currentFolderName=''
    ####Идем по графу сверху вниз, начинаем с нижней папки, потом поднимаемся по методу уровня воды в графе, до нашей исходной папки
    while(currentFolderName!=folder):
        leaveOnlyFolders(driver)
        exitFolder=0
        while(element_exists(driver, "//*[@class='bx--link bx--truncation-middle content-no-wrap icon_pading']") and (not exitFolder)):
                ####Идем по папочкам, выбираем ту где еще не все проверили
                wait_for_element_to_load(driver,"//*[@class='bx--link bx--truncation-middle content-no-wrap icon_pading']")
                folderElementNameChecks=driver.find_elements(By.XPATH, "//*[@class='bx--link bx--truncation-middle content-no-wrap icon_pading']")
                numFolder=0
                for folderElementNameCheck in folderElementNameChecks:
                    numFolder+=1
                    #####Если название слишком длинное, то оно сокращается, а полное пишется в title
                    if(not ((folderElementNameCheck.get_attribute("title")!='' and (folderElementNameCheck.get_attribute("title") in checkedFolders)) or (folderElementNameCheck.text in checkedFolders))):
                        folderElementNameCheck.click()
                        ###
                        time.sleep(sleepArray[0])
                        ###
                        ####Проходим на уровень ниже, ждем пока загрузится
                        wait_for_element_to_load(driver,"//div[@class='assets-table-container bx--data-table-container bx--data-table--max-width']")
                        break
                    #####Если папки в папке все проверены то мы в них не спускаемся
                    if(len(folderElementNameChecks)==numFolder):
                        exitFolder=1
                        break
        ###Сохраняем папку в уже просмотренных
        currentFolderName=getCurrentFolderName(driver)
        checkedFolders.append(currentFolderName)
        ###Выбираем все обьекты и проставляем права
        leaveAll(driver)
        setPermissionsToAllInsideFolder(driver,sleepArray)
        ####Поднимаемся на уровень выше
        goUpFolder(driver)
        wait_for_element_to_load(driver,"//*[@class='bx--link bx--truncation-middle content-no-wrap icon_pading']")

 

###Часть 2 GUI
# Define the function to be called when the Start button is clicked
def start():
    main()


# Create the main window
root = tk.Tk()

# Set the window title and size
root.title("Python_Rights_Apply_Script")
root.geometry("400x280")

notebook = ttk.Notebook(root)


tab1 = tk.Frame(notebook)
notebook.add(tab1, text="Настройка прав")

tab2 = tk.Frame(notebook)
notebook.add(tab2, text="Настройки")


text_Hint_Server = tk.Label(tab1,text="Выберите Сервер", width=50)
text_Hint_Server.grid(row=0, column=0)


comboboxServer = ttk.Combobox(tab1,textvariable=settings.chosenServer, values=settings.servers)
comboboxServer.grid(row=1, column=0)

varRememberMe=tk.BooleanVar(value=settings.rememberMe)
checkbox4 = tk.Checkbutton(tab1, text="Запомнить Меня?",variable=varRememberMe)
checkbox4.grid(row=6, column=0)

text_Login = tk.Label(tab1,text="Логин", width=50)
text_Login.grid(row=2, column=0, columnspan=2)

text_Password = tk.Label(tab1,text="Пароль", width=50)
text_Password.grid(row=4, column=0, columnspan=2)

if(varRememberMe.get()):
    varTextPassword=tk.StringVar(value=rsa.decrypt(settings.userPassword,privateKey).decode())
    varTextLogin=tk.StringVar(value=settings.userLogin)
else:
    varTextPassword=tk.StringVar(value='')
    varTextLogin=tk.StringVar(value='')


input_text_box_Password = tk.Entry(tab1, width=50,textvariable=varTextPassword)
input_text_box_Password.grid(row=5, column=0, columnspan=2)

input_text_box_Login = tk.Entry(tab1, width=50,textvariable=varTextLogin)
input_text_box_Login.grid(row=3, column=0, columnspan=2)


text_BD = tk.Label(tab1,text="Папка", width=50)
text_BD.grid(row=9, column=0, columnspan=2)

varTextFolder=tk.StringVar(value=settings.folder)
input_text_box_BD = tk.Entry(tab1, width=50,textvariable=varTextFolder)
input_text_box_BD.grid(row=10, column=0, columnspan=2)

text_Empt = tk.Label(tab1,text="", width=50)
text_Empt.grid(row=11, column=0, columnspan=2)

# Create the Start button
start_button = tk.Button(tab1, text="Начать", width=10, command=start)
start_button.grid(row=14, column=0, columnspan=2)




####### Вкладка 2
text_Sleep1 = tk.Label(tab2,text="Если программа останавливается до завершения простановки", width=50)
text_Sleep1.grid(row=1, column=0, columnspan=1)

text_Sleep2 = tk.Label(tab2,text="прав, попробуйте увеличить это число(1 - 5)", width=50)
text_Sleep2.grid(row=2, column=0, columnspan=1)

varTextSleep1=tk.StringVar(value=settings.sleepArray[0])
input_text_box_Sleep = tk.Entry(tab2, width=50,textvariable=varTextSleep1)
input_text_box_Sleep.grid(row=3, column=0, columnspan=2)

text_Sleep3 = tk.Label(tab2,text="Задержка между проставлением прав(5 - 20)", width=50)
text_Sleep3.grid(row=4, column=0, columnspan=1)

varTextSleep2=tk.StringVar(value=settings.sleepArray[1])
input_text_box_Sleep2 = tk.Entry(tab2, width=50,textvariable=varTextSleep2)
input_text_box_Sleep2.grid(row=5, column=0, columnspan=2)

text_Sleep4 = tk.Label(tab2,text="Задержка перед сохранением(1-5)", width=50)
text_Sleep4.grid(row=6, column=0, columnspan=1)

varTextSleep3=tk.StringVar(value=settings.sleepArray[2])
input_text_box_Sleep3 = tk.Entry(tab2, width=50,textvariable=varTextSleep3)
input_text_box_Sleep3.grid(row=7, column=0, columnspan=2)

notebook.pack()
# Start the GUI event loop
root.mainloop()







