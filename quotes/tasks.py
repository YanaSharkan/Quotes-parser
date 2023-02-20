from django.core.mail import send_mail
from celery.schedules import crontab

from bs4 import BeautifulSoup
import requests

from core.celery import app
from .models import Quote, Author


@app.task
def get_quotes():
    quotes_finished = False
    current_page = 1
    created_quotes = 0
    host = 'http://quotes.toscrape.com'
    while created_quotes < 5:
        try:
            quotes_r = requests.get(f'{host}/page/{current_page}')
        except requests.exceptions.RequestException:
            break

        quotes_doc = BeautifulSoup(quotes_r.content, features='html.parser')
        quotes_blk = quotes_doc.find_all('div', class_='quote')

        if len(quotes_blk) == 0:
            quotes_finished = True
            break

        current_page += 1
        for q_blk in quotes_blk:
            q_text = q_blk.find('span', class_='text')
            if q_text:
                q_body = q_text.get_text()
                try:
                    Quote.objects.get(body=q_body)
                except Quote.DoesNotExist:
                    author_name = q_blk.find('small', class_='author').get_text()

                    try:
                        author_m = Author.objects.get(full_name=author_name)
                    except Author.DoesNotExist:
                        q_author_link = q_blk.find('a').get('href')
                        author_r = requests.get(f'{host}{q_author_link}')
                        author_doc = BeautifulSoup(author_r.content, features='html.parser')
                        author_born = author_doc.find('span', class_='author-born-date').get_text()
                        author_loc = author_doc.find('span', class_='author-born-location').get_text()
                        author_about = author_doc.find('div', class_='author-description').get_text()
                        author_m = Author.objects.create(full_name=author_name,
                                                         born=author_born, location=author_loc,
                                                         about=author_about)

                    Quote.objects.create(body=q_body, author=author_m)

                    created_quotes += 1

    if quotes_finished and created_quotes < 5:
        send_mail(
            'No quotes left',
            'No quotes left',
            'test@test.com',
            ['test@test.com'],
            fail_silently=False,
        )


app.conf.beat_schedule = {
    'scraping': {
        'task': 'quotes.tasks.get_quotes',
        'schedule': crontab(minute=0, hour='1,3,5,7,9,11,13,15,17,19,21,23')
    }
}
