import requests
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader


def fetch_one(year):
  print(f'Downloading the statistics for IMO {year} ...')

  url = f'https://www.imo-official.org/year_statistics.aspx?year={year}'

  ses = requests.session()

  res = ses.get(url)

  if res.status_code != 200:
    print(f'Failed to download the statistics for IMO {year}')
    return
  else:
    soup = BeautifulSoup(res.text, 'html.parser')
    means = soup.select('td:contains("Mean") ~ td')
    maxs = soup.select('td:contains("Max") ~ td')
    for i, (me, ma) in enumerate(zip(means, maxs)):
      score = float(me.get_text(strip=True)) / float(ma.get_text(strip=True))
      yield round(score*7, 2), year, i


def fetch_all():
  res = []
  for year in range(1959, 2020):
    for record in fetch_one(year):
      res.append(record)
  res.sort(key=lambda x: (-x[0], x[1], x[2]))
  return res


def make_html():
  with open("./index.html", "w", encoding="utf8") as dest:
    env = Environment(loader=FileSystemLoader("."))
    temp = env.get_template('template.html')
    dest.write(str(temp.render(records=fetch_all())))


if __name__ == '__main__':
  make_html()