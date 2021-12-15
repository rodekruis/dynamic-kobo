#Full script
#Karla Peña Ramírez. 510 global. Project (T12890) Web crawler.

#Driver for Firefox
from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
import os.path
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

#Get the proper browser driver. In my case Firefox for MacOSarch32. Available here: https://github.com/mozilla/geckodriver/releases/tag/v0.30.0
driver = Firefox()
#driver = Firefox(executable_path='/Users/kpr/Documents/agora/510global/geckodriver')

####
#Drop files function
# JavaScript: HTML5 File drop
# source            : https://gist.github.com/florentbr/0eff8b785e85e93ecc3ce500169bd676
# param1 WebElement : Drop area element
# param2 Double     : Optional - Drop offset x relative to the top/left corner of the drop area. Center if 0.
# param3 Double     : Optional - Drop offset y relative to the top/left corner of the drop area. Center if 0.
# return WebElement : File input
JS_DROP_FILES = "var k=arguments,d=k[0],g=k[1],c=k[2],m=d.ownerDocument||document;for(var e=0;;){var f=d.getBoundingClientRect(),b=f.left+(g||(f.width/2)),a=f.top+(c||(f.height/2)),h=m.elementFromPoint(b,a);if(h&&d.contains(h)){break}if(++e>1){var j=new Error('Element not interactable');j.code=15;throw j}d.scrollIntoView({behavior:'instant',block:'center',inline:'center'})}var l=m.createElement('INPUT');l.setAttribute('type','file');l.setAttribute('multiple','');l.setAttribute('style','position:fixed;z-index:2147483647;left:0;top:0;');l.onchange=function(q){l.parentElement.removeChild(l);q.stopPropagation();var r={constructor:DataTransfer,effectAllowed:'all',dropEffect:'none',types:['Files'],files:l.files,setData:function u(){},getData:function o(){},clearData:function s(){},setDragImage:function i(){}};if(window.DataTransferItemList){r.items=Object.setPrototypeOf(Array.prototype.map.call(l.files,function(x){return{constructor:DataTransferItem,kind:'file',type:x.type,getAsFile:function v(){return x},getAsString:function y(A){var z=new FileReader();z.onload=function(B){A(B.target.result)};z.readAsText(x)},webkitGetAsEntry:function w(){return{constructor:FileSystemFileEntry,name:x.name,fullPath:'/'+x.name,isFile:true,isDirectory:false,file:function z(A){A(x)}}}}}),{constructor:DataTransferItemList,add:function t(){},clear:function p(){},remove:function n(){}})}['dragenter','dragover','drop'].forEach(function(v){var w=m.createEvent('DragEvent');w.initMouseEvent(v,true,true,m.defaultView,0,0,0,b,a,false,false,false,false,0,null);Object.setPrototypeOf(w,null);w.dataTransfer=r;Object.setPrototypeOf(w,DragEvent.prototype);h.dispatchEvent(w)})};m.documentElement.appendChild(l);l.getBoundingClientRect();return l"

def drop_files(element, files, offsetX=0, offsetY=0):
    driver = element.parent
    isLocal = not driver._is_remote or '127.0.0.1' in driver.command_executor._url
    paths = []

    # ensure files are present, and upload to the remote server if session is remote
    for file in (files if isinstance(files, list) else [files]) :
        if not os.path.isfile(file) :
            raise FileNotFoundError(file)
        paths.append(file if isLocal else element._upload(file))

    value = '\n'.join(paths)
    elm_input = driver.execute_script(JS_DROP_FILES, element, offsetX, offsetY)
    elm_input._execute('sendKeysToElement', {'value': [value], 'text': value})

WebElement.drop_files = drop_files
####

####
#CRAWLER
#Login credentials and new form path
url = "https://kobo.humanitarianresponse.info/"
username = "kpenaramirez"
password = "testKPR@rodekruisnl"
old_form = "#/forms/ae2c3mPS5E6XAD9XaUH25R"
new_form = "/Users/kpr/Documents/agora/510global/modified.xlsx"
#Go to the webpage
driver.get(url)
#Wait to load the webpage to send the fields
#Username
go = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, "registration__action")))
user = driver.find_element(By.ID, "id_username")
user.clear()
user.send_keys(username)
#Password
pwd = driver.find_element(By.ID, "id_password")
pwd.clear()
pwd.send_keys(password)
#Login
go.send_keys(Keys.RETURN)
#Go to the form
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "asset-row__link-overlay")))
forms = driver.find_elements_by_class_name('asset-row__link-overlay')
form = driver.find_element(By.XPATH, "//a[@href='" + old_form + "']")
form.click()
time.sleep(3)
#Replace the form
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".k-icon-replace")))
replace = driver.find_element(By.CSS_SELECTOR, ".k-icon-replace")
replace.click()
time.sleep(3)
#Upload new form
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".form-modal__item > button:nth-child(1)")))
upload = driver.find_element(By.CSS_SELECTOR, ".form-modal__item > button:nth-child(1)")
upload.click()
time.sleep(3)
dropzone = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "kobo-dropzone")))
dropzone.drop_files(new_form)
#Redeploy
time.sleep(15)
redeploy = driver.find_element(By.CSS_SELECTOR, "a.kobo-button")
redeploy.click()
time.sleep(3)
#Confirm
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.ajs-button:nth-child(1)")))
ok = driver.find_element(By.CSS_SELECTOR, "button.ajs-button:nth-child(1)")
ok.click()
#Close
driver.quit()
