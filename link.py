import sqlite3

zanyatost = '&employment=part'
massive_time = ['&part_time=employment_part',
                '&part_time=from_four_to_six_hours_in_a_day',
                '&part_time=start_after_sixteen',
                '&part_time=only_saturday_and_sunday']

massive_experience = ['',
                      '&experience=noExperience',
                      '&experience=between1And3',
                      '&experience=between3And6',
                      '&experience=moreThan6']

massive_disability = ['&label=accept_handicapped', '']

massive_specialization = [
    '&professional_role=22&professional_role=90&professional_role=95&professional_role=116&professional_role=120',
    '&professional_role=8&professional_role=21&professional_role=23&professional_role=32&professional_role=58&professional_role=89&professional_role=90&professional_role=130',
    '&professional_role=156&professional_role=160&professional_role=10&professional_role=12&professional_role=150&professional_role=25&professional_role=165&professional_role=34&professional_role=36&professional_role=73&professional_role=155&professional_role=96&professional_role=164&professional_role=104&professional_role=157&professional_role=107&professional_role=112&professional_role=113&professional_role=148&professional_role=114&professional_role=116&professional_role=121&professional_role=124&professional_role=125&professional_role=126',
    '&professional_role=12&professional_role=13&professional_role=20&professional_role=25&professional_role=34&professional_role=41&professional_role=55&professional_role=98&professional_role=103&professional_role=139',
    '&professional_role=8&professional_role=15&professional_role=19&professional_role=24&professional_role=29&professional_role=42&professional_role=168&professional_role=64&professional_role=65&professional_role=79&professional_role=151&professional_role=133',
    '&professional_role=5&professional_role=21&professional_role=31&professional_role=52&professional_role=59&professional_role=63&professional_role=173&professional_role=78&professional_role=85&professional_role=86&professional_role=102&professional_role=109&professional_role=111&professional_role=115&professional_role=128&professional_role=131&professional_role=143',
    '&professional_role=9&professional_role=35&professional_role=77&professional_role=97&professional_role=99&professional_role=123&professional_role=127',
    '&professional_role=8&professional_role=56&professional_role=60&professional_role=61&professional_role=70&professional_role=92&professional_role=138',
    '']

massive_industry = ['&industry=15',
                    '&industry=50',
                    '&industry=51',
                    '&industry=7',
                    '&industry=48',
                    '&industry=37',
                    '&industry=27',
                    '&industry=388',
                    '&industry=41',
                    '&industry=13',
                    '&industry=42',
                    '&industry=8',
                    '']

dict_region = {'moscow': '&L_save_area=true&area=1',
               'moscow_region': '&L_save_area=true&area=2019',
               'petersburg': '&L_save_area=true&area=2',
               'leningrad': '&L_save_area=true&area=145',
               'sevastopol': '&L_save_area=true&area=130',
               'krasnodar': '&L_save_area=true&area=1438',
               'tatarstan': '&L_save_area=true&area=1624',
               'nizhny_novgorod': '&L_save_area=true&area=1679',
               'yaroslavl': '&L_save_area=true&area=1806',
               }


def get_link(userid):
    link = 'https://hh.ru/search/vacancy?hhtmFrom=students&hhtmFromLabel=for_users&search_field=name&search_field=company_name&search_field=description&enable_snippets=false'
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Users WHERE userid = ?', (userid,))
    result = cursor.fetchone()
    connection.close()
    link += (f'{zanyatost}{massive_time[result[4]]}'
             f'{massive_specialization[result[5]]}{massive_industry[result[6]]}'
             f'{massive_experience[result[7]]}{massive_disability[result[8]]}{dict_region[result[3]]}')
    return link
