#Full script
#Karla Peña Ramírez. 510 global. Project (T12890) Web crawler.

#Driver for Firefox
from seleniumwire import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
import os.path
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import click
import warnings
from dotenv import load_dotenv
warnings.filterwarnings("ignore", category=DeprecationWarning)
load_dotenv()

# Drop files function
# JavaScript: HTML5 File drop
# source            : https://gist.github.com/florentbr/0eff8b785e85e93ecc3ce500169bd676
# param1 WebElement : Drop area element
# param2 Double     : Optional - Drop offset x relative to the top/left corner of the drop area. Center if 0.
# param3 Double     : Optional - Drop offset y relative to the top/left corner of the drop area. Center if 0.
# return WebElement : File input
JS_DROP_FILES = "var k=arguments,d=k[0],g=k[1],c=k[2],m=d.ownerDocument||document;for(var e=0;;){var f=d.getBoundingClientRect(),b=f.left+(g||(f.width/2)),a=f.top+(c||(f.height/2)),h=m.elementFromPoint(b,a);if(h&&d.contains(h)){break}if(++e>1){var j=new Error('Element not interactable');j.code=15;throw j}d.scrollIntoView({behavior:'instant',block:'center',inline:'center'})}var l=m.createElement('INPUT');l.setAttribute('type','file');l.setAttribute('multiple','');l.setAttribute('style','position:fixed;z-index:2147483647;left:0;top:0;');l.onchange=function(q){l.parentElement.removeChild(l);q.stopPropagation();var r={constructor:DataTransfer,effectAllowed:'all',dropEffect:'none',types:['Files'],files:l.files,setData:function u(){},getData:function o(){},clearData:function s(){},setDragImage:function i(){}};if(window.DataTransferItemList){r.items=Object.setPrototypeOf(Array.prototype.map.call(l.files,function(x){return{constructor:DataTransferItem,kind:'file',type:x.type,getAsFile:function v(){return x},getAsString:function y(A){var z=new FileReader();z.onload=function(B){A(B.target.result)};z.readAsText(x)},webkitGetAsEntry:function w(){return{constructor:FileSystemFileEntry,name:x.name,fullPath:'/'+x.name,isFile:true,isDirectory:false,file:function z(A){A(x)}}}}}),{constructor:DataTransferItemList,add:function t(){},clear:function p(){},remove:function n(){}})}['dragenter','dragover','drop'].forEach(function(v){var w=m.createEvent('DragEvent');w.initMouseEvent(v,true,true,m.defaultView,0,0,0,b,a,false,false,false,false,0,null);Object.setPrototypeOf(w,null);w.dataTransfer=r;Object.setPrototypeOf(w,DragEvent.prototype);h.dispatchEvent(w)})};m.documentElement.appendChild(l);l.getBoundingClientRect();return l"


def drop_files(element, files, offsetX=0, offsetY=0):
    """
    drop a file in upload area
    """
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


@click.command()
@click.option("--headless", is_flag=True, default=False, help="run headless (no GUI)")
@click.option('--koboserver', default="", help='URL of KoBo server, e.g. https://kobonew.ifrc.org/')
@click.option('--username', default="", help='username')
@click.option('--password', default="", help='password')
@click.option('--formid', default="", help='form (asset) ID')
@click.option('--newform', default="", help='absolute path to new form xlsx')
@click.option('--geckodriver', default="", help='absolute path to geckodriver')
def replace_redeploy(headless, koboserver, username, password, formid, newform, geckodriver):
    """
    replace KoBo form with a new one and redeploy
    """

    # initialize web driver
    # Get geckodriver, the Firefox browser driver, at https://github.com/mozilla/geckodriver/releases
    if "GECKODRIVER" in os.environ:
        geckodriver = os.getenv("GECKODRIVER")
    # set headless option, if requested
    options = Options()
    options.headless = headless
    driver = webdriver.Firefox(options=options, executable_path=geckodriver)
    WebElement.drop_files = drop_files

    # Login credentials and new form path
    if "KOBO_SERVER" in os.environ:
        koboserver = os.getenv("KOBO_SERVER")
    if "USERNAME" in os.environ:
        username = os.getenv("USERNAME").lower()  # WARNING: USERNAME MUST BE LOWER CASE
    if "PASSWORD" in os.environ:
        password = os.getenv("PASSWORD")
    if "FORM_ID" in os.environ:
        formid = os.getenv('FORM_ID')
    if "NEW_FORM" in os.environ:
        newform = os.getenv('NEW_FORM')

    # Go to the webpage
    driver.get(koboserver)
    # Wait to load the webpage to send the fields
    go = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, "kobo-button")))
    time.sleep(3)
    # Insert username
    user = driver.find_element(By.ID, "id_username")
    user.clear()
    user.send_keys(username)
    # Insert password
    pwd = driver.find_element(By.ID, "id_password")
    pwd.clear()
    pwd.send_keys(password)
    # Login
    go.send_keys(Keys.RETURN)
    # Go to the form
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "asset-row__link-overlay")))
    # forms = driver.find_elements_by_class_name('asset-row__link-overlay')
    try:
        form = driver.find_element(By.XPATH, "//a[@href='#/forms/" + formid + "']")
        form.click()
    except NoSuchElementException:
        driver.get(koboserver + "#/forms/" + formid + "/landing")
    time.sleep(3)
    # Replace the form
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "i.k-icon.k-icon-more")))
    more_popup = driver.find_element(By.CSS_SELECTOR, "i.k-icon.k-icon-more")
    more_popup.click()
    replace = driver.find_element(By.CSS_SELECTOR, "i.k-icon.k-icon-replace")
    replace.click()
    time.sleep(3)
    # Upload new form
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".form-modal__item > button:nth-child(1)")))
    upload = driver.find_element(By.CSS_SELECTOR, ".form-modal__item > button:nth-child(1)")
    upload.click()
    time.sleep(3)
    dropzone = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "kobo-dropzone")))
    dropzone.drop_files(newform)
    # Redeploy
    time.sleep(15)
    redeploy = driver.find_element(By.CSS_SELECTOR, "a.kobo-button")
    redeploy.click()
    time.sleep(3)
    # Confirm
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.ajs-button:nth-child(1)")))
    ok = driver.find_element(By.CSS_SELECTOR, "button.ajs-button:nth-child(1)")
    ok.click()
    # Close the webdriver
    driver.quit()


if __name__ == "__main__":
    replace_redeploy()
