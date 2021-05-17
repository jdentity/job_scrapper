import requests
from bs4 import BeautifulSoup


base_url = "https://weworkremotely.com/remote-jobs"
request_header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
}


def extract_job(html):
    try:
        result = html.find("a", recursive=False)
        link = result['href']
        company = result.find(
            "span", {"class": "company"}, recursive=False).get_text()
        title = result.find("span", {"class": "title"}).get_text()
        location = result.find("span", {"class": "region"}).get_text()
        return {
            'title': title,
            'company': company,
            'location': location,
            'apply_link': f"{base_url}{link}"
        }
    except AttributeError:  # filter view-all button
        return
    except TypeError:
        return


def extract_jobs(url):
    response = requests.get(url, headers=request_header)
    soup = BeautifulSoup(response.text, "html.parser")
    container = soup.find("div", {"class": "jobs-container"})
    results = container.find_all("li")
    jobs = []
    for result in results:
        job = extract_job(result)
        if job:
            jobs.append(job)
    return jobs


def get_jobs(word):
    url = f"{base_url}/search?term={word}"
    jobs = extract_jobs(url)
    print("wework finished")
    return jobs
