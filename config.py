import requests
from bs4 import BeautifulSoup


TOKEN_BOT = '6626305859:AAHBWHuV_-lhP6EhU8AR5Qrvzs8nthV9ciY'



with open('TEXT/manual_student.txt', 'r', encoding='utf-8') as doc:
    ManStud = doc.read()

with open('TEXT/manual_teacher.txt', 'r', encoding='utf-8') as doc:
    ManTeach = doc.read()

with open('TEXT/operating_mode.txt', 'r', encoding='utf-8') as doc:
    OperatingMode = doc.read()

with open('TEXT/bells.txt', 'r', encoding='utf-8') as doc:
    bells = doc.read()



def StudentParser(user_id, NumGroup):
    cookies = {
        'user': '76f5cc75ce2a35789670e25f51a7133f',
        '_ym_uid': '1684606312857245203',
        '_ym_d': '1684606312',
        'user': '76f5cc75ce2a35789670e25f51a7133f',
        'PHPSESSID': '4qbba8qq12npqhv928e0j6oq44',
        '_ym_isad': '2',
        '_ym_visorc': 'w',
        'mygroup': '%D0%98%D0%A1-26',
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        # 'Cookie': 'user=76f5cc75ce2a35789670e25f51a7133f; _ym_uid=1684606312857245203; _ym_d=1684606312; user=76f5cc75ce2a35789670e25f51a7133f; PHPSESSID=4qbba8qq12npqhv928e0j6oq44; _ym_isad=2; _ym_visorc=w; mygroup=%D0%98%D0%A1-26',
        'Origin': 'https://www.rksi.ru',
        'Referer': 'https://www.rksi.ru/schedule',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36',
        'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
    }

    data = {
        'group': f'{NumGroup}',
        'stt': 'Показать!',
    }


    response = requests.post('https://www.rksi.ru/schedule', cookies=cookies, headers=headers, data=data)
    with open(f'result/{user_id}.txt', 'wb') as doc:
        doc.write(response.content)

    with open(f'result/{user_id}.txt', encoding='utf-8') as doc:
        src = doc.read()

    a = src.split('</table>')[-1].split('</main>')[0].replace('<h3>', '\n').replace('<p>', '\n').replace('<b>', '\n')
    b = a.replace('</h3>', '\n').replace('</p>', '\n').replace('</b>', '\n').replace('<br />', ' ').replace('<hr>', ' ').replace('<div style="clear: both;"></div>', ' ')

    with open(f'result/{user_id}.txt', 'w', encoding='utf-8') as doc:
        doc.write(b)




def ParserTeacher(user_id, fullname):
    cookies = {
    'user': '76f5cc75ce2a35789670e25f51a7133f',
    '_ym_uid': '1684606312857245203',
    '_ym_d': '1684606312',
    'user': '76f5cc75ce2a35789670e25f51a7133f',
    'PHPSESSID': '4qbba8qq12npqhv928e0j6oq44',
    '_ym_isad': '2',
    'mygroup': '%D0%98%D0%A1-26',
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        # 'Cookie': 'user=76f5cc75ce2a35789670e25f51a7133f; _ym_uid=1684606312857245203; _ym_d=1684606312; user=76f5cc75ce2a35789670e25f51a7133f; PHPSESSID=4qbba8qq12npqhv928e0j6oq44; _ym_isad=2; mygroup=%D0%98%D0%A1-26',
        'Origin': 'https://www.rksi.ru',
        'Referer': 'https://www.rksi.ru/schedule',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36',
        'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
    }

    data = {
        'teacher': f'{fullname}.',
        'stp': 'Показать!',
    }

    response = requests.post('https://www.rksi.ru/schedule', cookies=cookies, headers=headers, data=data)
    with open(f'result/{user_id}.txt', 'wb') as doc:
        doc.write(response.content)

    with open(f'result/{user_id}.txt', encoding='utf-8') as doc:
        src = doc.read()

    a = src.split('</table>')[-1].split('</main>')[0].replace('<h3>', '\n').replace('<p>', '\n').replace('<b>', '\n')
    b = a.replace('</h3>', '\n').replace('</p>', '\n').replace('</b>', '\n').replace('<br />', ' ').replace('<hr>', ' ').replace('<div style="clear: both;"></div>', ' ')

    with open(f'result/{user_id}.txt', 'w', encoding='utf-8') as doc:
        doc.write(b.replace('УП', ''))