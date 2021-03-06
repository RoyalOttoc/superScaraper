import requests
from bs4 import BeautifulSoup

start_page= 1


def get_last_page(url):
  result = requests.get(url)
  soup = BeautifulSoup(result.text, "html.parser")
  pagination = soup.find("p", {"class": "mRR2Am8"})
  links = pagination.find_all('a')

  pages = []
  for link in links[:-1]:
    pages.append(int(link.string))

  max_page = pages[-1]
  return max_page

def extract_job(html):
    title = html.find("a", {"class": "_2S5REPk"}).string
    company = html.find("a", {"class": "_17sHMz8"}).string

    company = company.string
    company = company.strip()
    
    location_box = html.find("strong", {"class": "_7ZnNccT"})
    location =  location_box.find("a", {"class": "_17sHMz8"}).string
    job_id = html["data-job-id"]
    return {"title": title, "company": company, "location": location, "link": f"https://www.seek.com.au/job/{job_id}"} 

def extract_seek_jobs(last_page, word):
    jobs = []
    for page in range(last_page):
      print(f"scrapping page {page}")
      result = requests.get(f"https://www.seek.com.au/{word}-jobs?page={start_page*page}")
      soup = BeautifulSoup(result.text, "html.parser")
      results = soup.find_all("article", {"class":"_37iADb_ uUfGKHq"})
      
      for result in results:
          job = extract_job(result)
          jobs.append(job)
    return jobs

def get_jobs(word):
  url = f"https://www.seek.com.au/{word}-jobs?page={start_page}"
  last_page = get_last_page(url)
  jobs = extract_seek_jobs(last_page, word)
  return jobs
  
  
