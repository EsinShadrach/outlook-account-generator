from bose import (BaseTask, BoseDriver, BrowserConfig, Profile, TaskConfig,
                  UserAgent, Wait, WindowSize)
from bose.account_generator import AccountGenerator
from bose.ip_utils import find_ip_details
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from .config import config


class OutlookSignUpTask(BaseTask):
    def get_task_config(self):
        accounts_created_len = len(Profile.get_profiles())
        is_min_3_accounts_created = accounts_created_len >= 3

        return TaskConfig(
            target_website='microsoft.com',
            prompt_to_close_browser=is_min_3_accounts_created,
            change_ip=is_min_3_accounts_created,
        )

    def get_browser_config(self, data):
        return BrowserConfig(
            profile=data['username'],
            is_tiny_profile=True,
            window_size=WindowSize.RANDOM,
            user_agent=UserAgent.REAL,
        )

    def get_data(self):
        country_code = find_ip_details()['country']
        accounts = AccountGenerator.generate_accounts(
            config['number_of_accounts_to_generate'], country=country_code)
        return accounts

    def run(self, driver: BoseDriver, account):
        first_name = account['first_name']
        last_name = account['last_name']
        username = account['username']
        password = account['password']
        dob_year = str(account['dob']['year'])
        dob_day = str(account['dob']['day'])
        dob_month = str(account['dob']['month'])
        account['email'] = username + '@outlook.com'
        email = account['email']
        ip_details = find_ip_details()
        country_name = ip_details['country_name']

        def press_next_btn():
            driver.get_element_by_id('iSignupAction', Wait.LONG).click()

        def sign_up():

            # Fill in the email and check if it's already taken
            emailInput = driver.get_element_by_id('MemberName', Wait.LONG)
            emailInput.send_keys(email)

            driver.long_random_sleep()
            press_next_btn()

            # with suppress(Exception):
            if driver.get_element_by_id('MemberNameError', Wait.SHORT) is not None:
                print(driver.get_element_by_id(
                    'MemberNameError', Wait.SHORT).text)
                print("Username is already taken. So this account was not created.")
                raise Exception()

            driver.short_random_sleep()
            # Fill in the password and proceed
            passwordinput = driver.get_element_by_id(
                'PasswordInput', Wait.LONG)
            passwordinput.send_keys(password)

            driver.long_random_sleep()
            press_next_btn()

            driver.short_random_sleep()

            # Fill in the personal information
            first = driver.get_element_by_id('FirstName', Wait.LONG)
            first.send_keys(first_name)

            driver.short_random_sleep()

            last = driver.get_element_by_id('LastName', Wait.LONG)
            last.send_keys(last_name)

            driver.short_random_sleep()
            press_next_btn()

            driver.short_random_sleep()

            birthMonth = driver.get_element_by_id('BirthMonth', Wait.LONG)
            objectMonth = Select(birthMonth)
            objectMonth.select_by_value(str(dob_month))

            driver.short_random_sleep()

            # Fill in the date of birth
            birthYear = driver.get_element_by_id('BirthYear', Wait.LONG)
            birthYear.send_keys(str(dob_year))

            driver.short_random_sleep()

            # Select the country from the dropdown
            dropdown = driver.get_element_by_id('Country', Wait.LONG)
            dropdown.find_element(
                By.XPATH, f"//option[. = '{country_name}']").click()

            driver.short_random_sleep()

            birthDay = driver.get_element_by_id('BirthDay', Wait.LONG)
            objectDay = Select(birthDay)
            objectDay.select_by_value(str(dob_day))

            driver.short_random_sleep()
            press_next_btn()

            # Prompt to solve the CAPTCHA
            driver.prompt_to_solve_captcha(more_rules=[
                                           ' - If you are using Residential IP AND Microsoft Captcha is too Tough. Solve via Audio Captcha.'])

            yes_button = driver.get_element_or_none_by_selector(
                '[value="Yes"]', Wait.LONG)
            if yes_button is None:
                # Agree to Privacy Policy if it appears
                if driver.is_in_page('privacynotice.account.microsoft.com/notice', Wait.LONG):
                    continue_button = driver.get_element_or_none_by_selector(
                        '[id="id__0"]', Wait.LONG)
                    continue_button.click()
                yes_button = driver.get_element_or_none_by_selector(
                    '[value="Yes"]', Wait.LONG)

                if yes_button is None:
                    if driver.is_in_page('privacynotice.account.microsoft.com/notice', Wait.LONG):
                        continue_button = driver.get_element_or_none_by_selector(
                            '[id="id__0"]', Wait.LONG)
                        continue_button.click()
                    yes_button = driver.get_element_or_none_by_selector(
                        '[value="Yes"]', Wait.LONG)

            # Click "Yes" button if it appears
            yes_button.click()

        def is_bot_detected():
            blocked_el = driver.get_element_or_none_by_text(
                'The request is blocked.')
            return blocked_el is not None

        # Open the sign-up page via Google
        driver.organic_get("https://signup.live.com/")

        if is_bot_detected():
            print('Bot is Blocked by Microsoft. Possibly because Microsoft has flagged the IP. You can try running the Bot after few minutes or you change your IP address to bypass the IP Ban.')
            driver.long_random_sleep()
            return

        sign_up()

        Profile.set_profile(account)
        driver.get_by_current_page_referrer('https://account.microsoft.com/')

        # Uncomment following line if you want to browse things after account is created.
        # driver.prompt()
