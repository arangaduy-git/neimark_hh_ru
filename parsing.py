from urllib.request import urlopen
from bs4 import BeautifulSoup


def get_vacs(link):
    page = urlopen(link)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    soup = BeautifulSoup(html, features="html.parser")
    s = soup.find_all("div", {"class": "magritte-redesign"})
    vacs = []
    for i in range(0, 3):
        try:
            vac = []
            vac.append(s[i].find_all_next('h2', {"class": "bloko-header-section-2"})[0].text)
            try:
                vac.append(s[i].find_all_next('span', {
                    "data-sentry-component": 'Compensation'})[
                               0].text)
            except:
                vac.append('Не указана')
            vac.append(s[i].find_all_next('div', {"class": 'magritte-tag__label___YHV-o_3-0-18'})[0].text)
            vac.append(s[i].find_all_next('span', {"data-qa": 'vacancy-serp__vacancy-employer-text'})[1].text)
            vac.append(s[i].find_all_next('span', {
                "class": 'magritte-text___pbpft_3-0-16 magritte-text_style-primary___AQ7MW_3-0-16 magritte-text_typography-label-3-regular___Nhtlp_3-0-16'})[
                           1].text)
            vac.append(s[i].find_all('a', {
                'data-qa': 'serp-item__title'})[
                           0].get("href").replace('https://nn.hh.ru', 'https://hh.ru'))
            vac[1] = vac[1].replace('\u202f', '')
            vac[1] = vac[1].replace('\xa0', ' ')
            vacs.append(vac)
        except Exception as e:
            print(e)
    return vacs
