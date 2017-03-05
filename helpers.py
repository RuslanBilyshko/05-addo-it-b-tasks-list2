from datetime import datetime

from flask import flash
from flask import redirect
from flask import render_template
from flask import url_for
from var_dump import var_dump

from models import BaseModel

dateformat = '%d-%m-%Y'
timeformat = '%H:%M'


def render_form(
        action,
        form=None,
        method="POST",
        button="Submit",
        button_class="default",
        delete=False
):
    template = 'form/form.html'

    if delete:
        template = "form/delete_form.html"

    return render_template(
        template,
        **{
            'form': form,
            "action": action,
            "method": method,
            "button": button,
            "button_class": button_class

        }
    )


def render_content(content, title="No title"):
    return render_template(
        "content.html",
        **{
            "title": title,
            "content": content
        }
    )


def render_tasks_list_as_table(tasks):
    header = ['Название', "Описание", "Дата", "Время", "Статус", "Правка", ""]

    rows = []

    for task in tasks:

        text = ""
        class_attr = ""

        if task.status == 0:
            text = "В ожидании"
            class_attr = "warning"


        if task.status == 1:
            class_attr = "success"
            text = "Выполнено"

        status = render_url(url_for("task_change_status", task_id=task.id), text=text, class_attr=class_attr)

        row = [
            task.title,
            task.description,
            task.date,
            task.time.strftime("%H:%M"),
            status,
            render_url(url_for("task_edit", task_id=task.id), text="Редактировать"),
            render_url(url_for("task_delete", task_id=task.id), text="Удалить", class_attr="danger")
        ]

        rows.append(row)

    return render_template(
        "table.html",
        **{
            "header": header,
            "rows": rows
        }
    )


def render_url(url, text=None, class_attr=None, title=None) -> str:
    if text is None:
        text = url

    if class_attr is None:
        class_attr = 'default'

    if title is None:
        title = ''

    return "<a href='{}' class='btn btn-{}' title='{}'>{}</a>".format(url, class_attr, title, text)


def is_not_auth():
    flash('Чтобы управлять делами вы должны войти или зарегистрироваться', 'danger')
    return redirect(url_for("index"))


def is_date_past(date, format=dateformat) -> bool:
    date_now_start = today_start()

    date_check = datetime.strptime(date, format)
    return date_now_start > date_check


def is_date_now(date, format=dateformat) -> bool:
    date_now_start = today_start()
    date_check = datetime.strptime(date, format)
    return date_now_start == date_check

def is_date_future(date, format=dateformat) -> bool:
    date_now_start = today_start()
    date_check = datetime.strptime(date, format)
    return date_now_start < date_check


def today_start() -> datetime:
    date_now = datetime.today()
    today_intro_str = "{}-{}-{}".format(date_now.day, date_now.month, date_now.year)
    return datetime.strptime(today_intro_str, '%d-%m-%Y')


def is_time_past(time, format=timeformat):
    tt = datetime.today().time().strftime(format)
    return tt > time
