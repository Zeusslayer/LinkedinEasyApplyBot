from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
from xml.dom.minidom import Element
import time
import math
import data


class Linkedin:
    def __init__(self):
        service = FirefoxService(executable_path=GeckoDriverManager().install())

        ffOptions = Options()
        ffOptions.add_argument("-profile")
        ffOptions.add_argument(data.FFPATH)
        self.driver = Firefox(service=service, options=ffOptions)

        # self.driver.maximize_window()  # For maximizing window
        self.driver.get(
            "https://www.linkedin.com/feed/"
        )  # opens the linkedin feed page

    def Link_job_apply(self):
        count_application = 0
        count_job = 0
        jobs_per_page = 25
        easy_apply = "?f_AL=true"
        location = "Germany"  # "Worldwide" - European%20Union - United%20States - Norway - Istanbul - United%20States
        keywords = ["QA", "Test Engineer", "Test Automation"]
        # in the last x seconds | day = 86400, week = 604800, month = 2592000
        date_posted = "604800"
        self.driver.implicitly_wait(10)  # gives an implicit wait for 10 seconds
        for indexpag in range(len(keywords)):  # loops through the keywords
            self.driver.get(  # opens the linkedin job search page using parameters below # https://www.linkedin.com/jobs/search/?f_AL=true&f_TPR=r604800&keywords=QA&location=United%20States
                "https://www.linkedin.com/jobs/search/"
                + easy_apply  # easy apply
                + "&f_TPR=r"
                + date_posted  # in the last x seconds
                + "&keywords="
                + keywords[indexpag]  # keywords
                + "&location="
                + location  # location
            )
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
            print("Number of Results: " + str(total_jobs_int))  # print total jobs
            number_of_pages = math.ceil(
                total_jobs_int / jobs_per_page
            )  # calculate number of pages
            print("Number of Pages: ", number_of_pages)  # print number of pages

            for i in range(
                number_of_pages
            ):  # cycles through pages and runs the below code for each page
                cons_page_mult = 25 * i
                url = (
                    "https://www.linkedin.com/jobs/search/"
                    + easy_apply
                    + "&f_TPR=r"
                    + date_posted
                    + "&keywords="
                    + keywords[indexpag]
                    + "&location="
                    + location
                    + "&start="
                    + str(cons_page_mult)
                )
                self.driver.get(url)  # get url of each page page of results
                time.sleep(10)
                # needs to be scrolled down to get all the jobs on the page, couldn't write the code yet. Workaround is to set the default zoom of the browser to lowest.
                links = self.driver.find_elements(  # finds all job elements on the page by their job id
                    "xpath", "//div[@data-job-id]"
                )
                print(
                    "Number of Job Elements: " + str(len(links))
                )  # print number job elements

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
                    time.sleep(10)
                    try:
                        button = self.driver.find_elements(
                            "xpath", '//button[contains(@class, "jobs-apply")]/span[1]'
                        )
                        if button[0].text in "Easy Apply":
                            EasyApplyButton = button[0]
                    except:
                        EasyApplyButton = False

                    button = EasyApplyButton
                    if button is not False:
                        button.click()
                        time.sleep(10)
                        try:
                            self.driver.find_element(
                                By.CSS_SELECTOR,
                                "button[aria-label='Submit application']",
                            ).click()
                            time.sleep(7)
                            count_application += 1
                            print("* Just Applied to this job!")
                        except:
                            try:
                                button = self.driver.find_element(
                                    By.CSS_SELECTOR,
                                    "button[aria-label='Continue to next step']",
                                ).click()
                                time.sleep(7)
                                percen = self.driver.find_element(
                                    "xpath",
                                    "/html/body/div[3]/div/div/div[2]/div/div/span",
                                ).text
                                percen_numer = int(percen[0 : percen.index("%")])
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
                                        time.sleep(7)
                                        self.driver.find_element(
                                            By.CSS_SELECTOR,
                                            "button[aria-label='Continue to next step']",
                                        ).click()
                                        time.sleep(7)
                                        self.driver.find_element(
                                            By.CSS_SELECTOR,
                                            "button[aria-label='Review your application']",
                                        ).click()
                                        time.sleep(7)
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
                                        time.sleep(7)
                                        self.driver.find_element(
                                            By.CSS_SELECTOR,
                                            "button[aria-label='Review your application']",
                                        ).click()
                                        time.sleep(7)
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
                                        time.sleep(7)
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
                        print("* Already applied!")
                    time.sleep(1)
            print(
                "Category: ",
                keywords,
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
