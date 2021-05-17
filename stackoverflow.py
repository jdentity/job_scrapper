import requests
from bs4 import BeautifulSoup


def get_last_page(url):
    try:
        result = requests.get(url)
        soup = BeautifulSoup(result.text, "html.parser")
        pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
        last_page = pages[-2].get_text(strip=True)
        return int(last_page)
    except AttributeError:
        print("stackoverflow : No result")
        return 0


def extract_job(html):
    title = html.find("h2", {"class": "mb4"}).find("a")["title"]
    company, location = html.find(
        "h3", {"class": "fc-black-700 fs-body1 mb4"}).find_all("span", recursive=False)
    company = company.get_text(strip=True)
    location = location.get_text(strip=True)
    job_id = html["data-jobid"]
    return {
        'title': title,
        'company': company,
        'location': location,
        'apply_link': f"https://stackoverflow.com/jobs/{job_id}"
    }


def extract_jobs(last_page, url):
    jobs = []
    for page in range(last_page):
        print(f"Scraping StackOverflow : Page {page}")
        result = requests.get(f"{url}&pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "-job"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs(word):
    url = f"https://stackoverflow.com/jobs?q={word}"
    last_page = get_last_page(url)
    jobs = extract_jobs(last_page, url)
    print("stackoverflow finished")
    return jobs
