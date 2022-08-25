from socket import timeout
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from xml.dom.minidom import Element
import time
import math
import userData
import logging

logging.basicConfig(  # Set up logging
    filename="EasyApplyBot.log",
    level=logging.INFO,
    format="%(levelname)s | %(asctime)s | %(message)s",
    datefmt="%m/%d %H:%M:%S",
)


class Linkedin:
    def __init__(self):
        service = FirefoxService(
            executable_path=GeckoDriverManager().install())

        ffOptions = Options()
        ffOptions.add_argument("-profile")
        ffOptions.add_argument(userData.FFPATH)
        self.driver = Firefox(service=service, options=ffOptions)

        # self.driver.maximize_window()  # For maximizing window
        self.driver.get(
            "https://www.linkedin.com/feed/"
        )  # opens the linkedin feed page

    def Link_job_apply(self):

        count_application = 0
        count_job = 0
        jobs_per_page = 25

        # gives an implicit wait for 10 seconds
        self.driver.implicitly_wait(10)

        # that's where the magic begins
        for indexpag in range(len(userData.keywords)):  # loops through the keywords

            # url that contains the combinations of all the user input above
            url = (
                f"https://www.linkedin.com/jobs/search/{userData.easy_apply}&f_TPR=r{userData.date_posted}"
                f"{userData.remote}&keywords={userData.keywords[indexpag]}&location={userData.location}"
            )
            # opens the linkedin job search page # https://www.linkedin.com/jobs/search/?f_AL=true&f_TPR=r604800&keywords=QA&location=United%20States
            self.driver.get(url)
            numofjobs = self.driver.find_element(
                "xpath", "//*[@id='main']/div/section[1]/header/div[1]/small"
            ).text  # get number of results

            space_ind = numofjobs.index(
                " "
            )  # get index of space between | number and word "results" |
            total_jobs = numofjobs[0:space_ind]  # get "number" of results
            total_jobs_int = int(
                total_jobs.replace(",", "")
            )  # convert "number" to integer
            logging.info(
                "Number of Results: " + str(total_jobs_int)
            )  # print total jobs
            number_of_pages = math.ceil(
                total_jobs_int / jobs_per_page
            )  # calculate number of pages
            # print number of pages
            logging.info(f"Number of Pages: {number_of_pages}")

            for i in range(
                number_of_pages
            ):  # cycles through pages and runs the below code for each page
                cons_page_mult = 25 * i
                url = (
                    f"https://www.linkedin.com/jobs/search/{userData.easy_apply}&f_TPR=r{userData.date_posted}"
                    f"{userData.remote}&keywords={userData.keywords[indexpag]}&location={userData.location}&start={str(cons_page_mult)}"
                )
                self.driver.get(url)  # get url of each page page of results
                time.sleep(5)  # wait 10 seconds
                # needs to be scrolled down to get all the jobs on the page, couldn't write the code yet. Workaround is to set the default zoom of the browser to lowest.
                links = self.driver.find_elements(  # finds all job elements on the page by their job id
                    "xpath", "//div[@data-job-id]"
                )
                logging.info(
                    f"Number of Job Elements: {str(len(links))}"
                )  # number job elements

                IDs = []
                for link in links:  # get job id for each job element
                    temp = link.get_attribute("data-job-id")
                    jobID = temp.split(":")[-1]
                    IDs.append(int(jobID))
                IDs = set(IDs)
                jobIDs = [x for x in IDs]

                for jobID in jobIDs:  # loop through job ids and apply to each job
                    job_page = f"https://www.linkedin.com/jobs/view/{jobID}"
                    self.driver.get(job_page)  # get specific job page
                    count_job += 1
                    logging.info(f"Job number: {count_job}")

                    # WORKING ON IT ------------------------------------------------
                    # wait = WebDriverWait(self.driver, 15)
                    # logging.warning("Breakpoint | 1")
                    # button = wait.until(
                    #     EC.presence_of_all_elements_located(
                    #         (
                    #             By.XPATH,
                    #             "//button[contains(@class, 'jobs-apply')]/span[1]",
                    #         )
                    #     )
                    # )
                    # logging.warning("Breakpoint | 2")
                    # wait.until(EC.element_to_be_selected(button[0]))
                    # logging.warning("Breakpoint | 3")

                    # if button[0].text in "Easy Apply":
                    #     EasyApplyButton = button[0]
                    #     logging.warning("Breakpoint | 4")

                    # else:
                    #     EasyApplyButton = False
                    #     logging.warning("Breakpoint | 5")

                    # button = EasyApplyButton
                    # logging.warning("Breakpoint | 6")
                    # -----------------------------------------------------------------

                    # ORIGINAL-ISH ---------------------------------------------------------
                    time.sleep(15)
                    try:
                        button = self.driver.find_elements(
                            "xpath", '//button[contains(@class, "jobs-apply")]/span[1]'
                        )
                        if button[0].text in "Easy Apply":
                            EasyApplyButton = button[0]
                    except:
                        EasyApplyButton = False
                    button = EasyApplyButton
                    # --------------------------------------------------------

                    if button is not False:
                        button.click()
                        time.sleep(3)
                        try:
                            self.driver.find_element(
                                By.CSS_SELECTOR,
                                "button[aria-label='Submit application']",
                            ).click()
                            time.sleep(3)
                            count_application += 1
                            print("* Just Applied to this job!")
                        except:
                            try:
                                button = self.driver.find_element(
                                    By.CSS_SELECTOR,
                                    "button[aria-label='Continue to next step']",
                                ).click()
                                time.sleep(3)
                                percen = self.driver.find_element(
                                    "xpath",
                                    "/html/body/div[3]/div/div/div[2]/div/div/span",
                                ).text
                                percen_numer = int(
                                    percen[0: percen.index("%")])
                                if int(percen_numer) < 25:
                                    print(
                                        "*More than 5 pages,wont apply to this job! Link: "
                                        + job_page
                                    )
                                elif int(percen_numer) < 30:
                                    try:
                                        self.driver.find_element(
                                            By.CSS_SELECTOR,
                                            "button[aria-label='Continue to next step']",
                                        ).click()
                                        time.sleep(3)
                                        self.driver.find_element(
                                            By.CSS_SELECTOR,
                                            "button[aria-label='Continue to next step']",
                                        ).click()
                                        time.sleep(3)
                                        self.driver.find_element(
                                            By.CSS_SELECTOR,
                                            "button[aria-label='Review your application']",
                                        ).click()
                                        time.sleep(3)
                                        self.driver.find_element(
                                            By.CSS_SELECTOR,
                                            "button[aria-label='Submit application']",
                                        ).click()
                                        count_application += 1
                                        print("* Just Applied to this job!")
                                    except:
                                        print(
                                            "*4 Pages,wont apply to this job! Extra info needed. Link: "
                                            + job_page
                                        )
                                elif int(percen_numer) < 40:
                                    try:
                                        self.driver.find_element(
                                            By.CSS_SELECTOR,
                                            "button[aria-label='Continue to next step']",
                                        ).click()
                                        time.sleep(3)
                                        self.driver.find_element(
                                            By.CSS_SELECTOR,
                                            "button[aria-label='Review your application']",
                                        ).click()
                                        time.sleep(3)
                                        self.driver.find_element(
                                            By.CSS_SELECTOR,
                                            "button[aria-label='Submit application']",
                                        ).click()
                                        count_application += 1
                                        print("* Just Applied to this job!")
                                    except:
                                        print(
                                            "*3 Pages,wont apply to this job! Extra info needed. Link: "
                                            + job_page
                                        )
                                elif int(percen_numer) < 60:
                                    try:
                                        self.driver.find_element(
                                            By.CSS_SELECTOR,
                                            "button[aria-label='Review your application']",
                                        ).click()
                                        time.sleep(3)
                                        self.driver.find_element(
                                            By.CSS_SELECTOR,
                                            "button[aria-label='Submit application']",
                                        ).click()
                                        count_application += 1
                                        print("* Just Applied to this job!")
                                    except:
                                        print(
                                            "* 2 Pages,wont apply to this job! Unknown.  Link: "
                                            + job_page
                                        )
                            except:
                                print("* Cannot apply to this job!!")
                    else:
                        print(
                            "* Already applied! ---------------------------------------------"
                        )
                    time.sleep(3)
            print(
                "Category: ",
                userData.keywords,
                " ,applied: "
                + str(count_application)
                + " jobs out of "
                + str(count_job)
                + ".",
            )


start_time = time.time()
ed = Linkedin()
ed.Link_job_apply()
end = time.time()

print("---Took: " + str(round((time.time() - start_time) / 60)) + " minute(s).")
