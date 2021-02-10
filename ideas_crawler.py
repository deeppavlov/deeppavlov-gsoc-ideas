import os

from bs4 import BeautifulSoup
from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(executable_path=r'chromedriver.exe',
                          options=chrome_options)

repo_path = "oserikov/deeppavlov-contrib-drafts"
# repo_path = "deepmipt/DeepPavlov"
issues_url = f"https://github.com/{repo_path}/issues?q=label%3Agsoc"

driver.get(issues_url)
htmlSource = driver.page_source

soup = BeautifulSoup(htmlSource, features="html.parser")
content_html = soup.find("div", attrs={"class": "repository-content"})

to_extract_classes = [
    "d-flex flex-justify-between mb-md-3 flex-column-reverse flex-md-row flex-items-end",
    "bg-gray-light pt-3 hide-full-screen mb-5",
    "position-relative js-header-wrapper ",
    "position-relative js-header-wrapper",
    "js-pinned-issues-reorder-container",
    "paginate-container d-none d-sm-flex flex-sm-justify-center",
    "footer container-xl width-full p-responsive",
    "protip",
    "paginate-container d-sm-none mb-5",
    "Box-header d-flex flex-justify-between",
    "ml-2 pl-2 d-none d-md-flex",
    "ml-3 d-flex flex-justify-between width-full width-md-auto",
    "issues-reset-query-wrapper",
    "d-block d-lg-none no-wrap"
]
for issues_section in to_extract_classes:
    c_elem = soup.find("div", attrs={"class": issues_section})
    if c_elem:
        c_elem.extract()

next_pages_issues = []
next_pages_soups = []
for pageNum in range(10):
    driver.get(issues_url + f"?page={pageNum}")
    htmlSource2 = driver.page_source
    next_page_soup = BeautifulSoup(htmlSource2, features="html.parser")
    next_pages_soups.append(next_page_soup)

for next_page_soup in next_pages_soups:
    for issues_section in next_page_soup.findAll("div", attrs={"aria-label": "Issues"}):
        for issues_subsection in issues_section.findAll("div", attrs={
            "class": "js-navigation-container js-active-navigation-container"}):
            for issue in issues_subsection.children:
                next_pages_issues.append(issue)

for issue in next_pages_issues:
    soup.find("div",
              attrs={"class": "js-navigation-container js-active-navigation-container"}) \
        .append(issue)

soup_pretty = str(soup)

soup_pretty = soup_pretty.replace(f'"/{repo_path}/issues', f'"https://github.com/{repo_path}/issues')
soup_pretty = soup_pretty.replace('"/users', '"https://github.com/users')

with open("gsoc_ideas.html", 'w', encoding="utf-8") as f:
    print(soup_pretty, file=f)
