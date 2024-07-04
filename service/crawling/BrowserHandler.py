from selenium import webdriver


class BrowserHandler:
    init = ''
    driver = None

    wait_time = 3

    def chrome(self, headless=None):
        options = webdriver.ChromeOptions()
        if headless is 'background':
            options.add_argument('--headless=new')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--blink-settings=imagesEnabled=false')

        # service = Service(executable_path=config.executable_path)
        # driver = webdriver.Chrome()
        # self.driver = webdriver.Chrome(options, service)
        self.driver = webdriver.Chrome(options)
        self.driver.implicitly_wait(self.wait_time)

    def browser_exit(self):
        self.driver.quit()
