import requests
from bs4 import BeautifulSoup


base_url = "https://remoteok.io"
request_header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
}


def extract_job(html):
    try:
        link = html.find("a", {"itemprop": "url"})["href"]
        company = html['data-company']
        title = html.find("h2", {"itemprop": "title"}).get_text()
        if html.find("div", {"class": "location"}) is None:
            location = 'No office location'
        else:
            location = html.find("div", {"class": "location"}).get_text()
        if html.find("span", {"class": "closed"}):  # except closed
            return
        return {
            'title': title,
            'company': company,
            'location': location,
            'apply_link': f"{base_url}{link}"
        }
    except AttributeError:  # filter view-all button
        return


def extract_jobs(url):
    response = requests.get(url, headers=request_header)
    soup = BeautifulSoup(response.text, "html.parser")
    container = soup.find("table", {"id": "jobsboard"})
    results = container.find_all("tr", {"class": "job"})
    jobs = []
    for result in results:
        job = extract_job(result)
        if job:
            jobs.append(job)
    return jobs


def get_jobs(word):
    url = f"{base_url}/remote-{word}-jobs"
    jobs = extract_jobs(url)
    print("remoteok finished")
    return jobs
