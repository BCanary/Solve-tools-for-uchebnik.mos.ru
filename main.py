from selenium import webdriver

#CONST
GECKODRIVER_PATH = "/home/kali/Downloads/geckodriver"

UCHEBNIK_MOS_URL = "https://uchebnik.mos.ru/"

ENG_LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
RUS_LETTERS = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ь', 'Ы', 'Ъ', 'Э', 'Ю', 'Я']
NUMBERS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
#input constants

login_method = input("1. Ввести логин и пароль\n2. Загрузить логин и пароль из файла logindata (login:password)\nВвод: ")

if login_method == "1":
	LOGIN = input("Введите логин от вашего mos.ru: ")
	PASSWORD = input("Введите пароль от вашего mos.ru: ")
elif login_method == "2":
	#check file
	with open("logindata", "r") as file:
		text = file.read()
		data = text.split(":")

		LOGIN = data[0]
		PASSWORD = data[1]
else:
	print("Ошибка ввода!")
CROSSWORD_URL = input("Введите url кроссворда: ")

chouse = input("Какой словарь использовать?\n1. Русский\n2. Английский\nВвод: ")
if chouse == "1":
	LETTERS = RUS_LETTERS
elif chouse == "2":
	LETTERS = ENG_LETTERS
else:
	print("Ошибка ввода!")


#get driver
driver = webdriver.Firefox(executable_path=GECKODRIVER_PATH)
driver.get(UCHEBNIK_MOS_URL)

#find login button and click it
login_btn = driver.find_element_by_tag_name("button")
login_btn.click()


#click to login by mos ru button
mos_ru_btn = driver.find_element_by_css_selector("button.rectangleButton-44.buttonWithLeftIcon-63.simple-47")
mos_ru_btn.click()

#login into mos ru
form = driver.find_element_by_css_selector('form#loginFm')
login = driver.find_element_by_css_selector('input#login')
password = driver.find_element_by_css_selector('input#password')
#button = driver.find_element_by_css_selector('button#bind') #it doesnt work very well

login.send_keys(LOGIN)
password.send_keys(PASSWORD)
#button.click()
form.submit()

#Go to crossword url
driver.get(CROSSWORD_URL)

# driver.implicitly_wait(2)

# button = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div/div[1]/div/div/div[2]/div[5]/div/div/div/div/button")
# button.click()

driver.implicitly_wait(5)

#switch to crossword frame

iframe = driver.find_element_by_tag_name('iframe')
driver.switch_to.frame(iframe)

iframe = driver.find_element_by_tag_name('iframe')
driver.switch_to.frame(iframe)

iframe = driver.find_element_by_tag_name('iframe')
driver.switch_to.frame(iframe)

#wait for button
driver.implicitly_wait(2)

#get ok button, and click on it
ok_btn = driver.find_element_by_xpath("/html/body/div[5]/div[2]/button")
driver.execute_script("arguments[0].click();", ok_btn) # idk how its work, just normal click() not working, thanks stackoverflow

#get elements
table = driver.find_elements_by_xpath("//table[@id='crossword']//table[1]/tbody//div[@class='field filled']") #get all boxes
check_btn = driver.find_element_by_xpath("//*[@id='checkSolutionBtn']") #get checks solution button

#parse all crossword boxes
for element in table:
	for letter in LETTERS:
		driver.execute_script(f"arguments[0].innerHTML='{letter}'", element) #change div value
		check_btn.click()
		if element.value_of_css_property('color') == "rgb(0, 128, 0)": #if color green
			break #stop itterating letters