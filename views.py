from datetime import datetime

from flask import Flask, flash
from flask import abort
from flask import g, request, redirect, url_for, render_template
from flask_login import LoginManager, current_user, login_user, logout_user
from var_dump import var_dump
from wtforms import HiddenField

from helpers import dateformat, render_form, render_content, is_not_auth, render_tasks_list_as_table, render_url
from models import User, initialize_database, Task

from forms import RegisterForm, TaskForm, TaskStatusForm, TaskDeleteForm, LoginForm

app = Flask("TaskList")
app.secret_key = 'super secret key'

login_manager = LoginManager(app)
login_manager.login_view = 'login'


@app.before_request
def before_request():
    g.user = current_user


@login_manager.user_loader
def load_user(id):
    return User.get(id=int(id))


@app.route('/', methods=['GET'])
def index():
    if current_user.is_authenticated:

        tasks = Task.filter(
            Task.user == current_user.id,
            Task.date == datetime.today().strftime(dateformat)
        )

        var_dump(tasks)
        var_dump(datetime.today())

        content = render_tasks_list_as_table(tasks)
        title = "Список дел на сегодня"

    else:
        content = render_template("_index_anonimus.html")
        title = "Добро пожаловать"

    return render_content(content, title)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():

        username = request.form['username']
        password = request.form['password']

        registered_user = User.filter(User.username == username).first()

        if registered_user is None or not registered_user.password.check_password(password):
            flash('Ошибка ввода логина или пароля', "danger")
            return redirect(url_for('login'))  # redirect back to login page if can't wasn't found

        login_user(registered_user)
        return redirect(request.args.get('next') or url_for('index'))

    content = render_form(
        form=form,
        action=url_for("login"),
        button="Вход",
        button_class="success"
    )
    return render_content(content=content, title="Авторизация")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegisterForm(request.form)

    if request.method == 'POST' and form.validate():
        username = request.form['username']
        password = request.form['password']

        User.create(
            username=username,
            password=password
        )

        flash('Спасибо за регистрацию. Теперь вы можете авторизироваться и начать работу')
        return redirect(url_for('login'))

    content = render_form(
        form=form,
        action=url_for("registration"),
        button="Регистрация",
        button_class="primary"
    )

    return render_content(content, "Регистрация")


@app.route("/task/create", methods=['GET', 'POST'])
def task_create():

    if not current_user.is_authenticated:
        return is_not_auth()

    form = TaskForm(request.form)

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        description = request.form['description']
        date = request.form['date']
        time = request.form['time']

        Task.create(
            title=title,
            description=description,
            date=date,
            user=current_user.id,
            time=time
        )

        flash('Задание успешно добавлено', 'success')
        return redirect(url_for('task_list'))

    content = render_form(
        form=form,
        action=url_for("task_create"),
        button="Создать"
    )

    return render_content(content, "Создать задание")


@app.route('/task/edit/<int:task_id>', methods=['GET', 'POST'])
def task_edit(task_id):
    if not current_user.is_authenticated:
        return is_not_auth()

    task = Task.get(Task.id == task_id)

    form = TaskForm(formdata=request.form, obj=task)

    if request.method == "GET":
        content = render_form(
            form=form,
            action=url_for("task_edit", task_id=task_id),
            button="Обновить")

        return render_content(content, "Редактировать - {}".format(task.title))

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        description = request.form['description']
        date = request.form['date']
        time = request.form['time']

        task.title = title
        task.description = description
        task.date = date
        task.user = current_user.id
        task.time = time
        task.save()

        flash('Задание <b><em>{}</em></b> успешно обновлено'.format(title), 'success')
        return redirect(url_for('task_list'))


@app.route('/task/edit/status/<int:task_id>', methods=['GET', 'POST'])
def task_change_status(task_id):
    if not current_user.is_authenticated:
        return is_not_auth()

    task = Task.get(Task.id == task_id)

    form = TaskStatusForm(formdata=request.form, obj=task)

    if request.method == "GET":
        content = render_form(
            form=form,
            action=url_for("task_change_status", task_id=task_id),
            button="Обновить")

        return render_content(content, "Изменить статус - {}".format(task.title))

    if request.method == 'POST' and form.validate():
        status = request.form['status']
        task.status = status
        task.save()

        flash('Статус <b><em>{}</em></b> успешно обновлен'.format(task.title), 'success')
        return redirect(url_for('task_list'))


@app.route('/task/delete', methods=['POST'], defaults={"task_id": None})
@app.route('/task/delete/<int:task_id>', methods=['GET'])
def task_delete(task_id):
    if not current_user.is_authenticated:
        return is_not_auth()

    # if False:
    #     abort(404)

    if request.method == "GET":
        task = Task.filter(Task.id == task_id).first()

        if task is None:
            return abort(404)

        form = TaskDeleteForm(formdata=request.form, obj=task)
        content = render_form(
            form=form,
            action=url_for("task_delete"),
            delete=True
        )

        return render_content(content, "Вы уверены что хотите удалить - {}?".format(task.title))

    if request.method == 'POST':
        task = Task.get(Task.id == request.form["id"])
        var_dump(task)
        task.delete()
        flash('Событие <b><em>{}</em></b> успешно удалено'.format(task.title), 'success')
        return redirect(url_for('task_list'))


@app.route("/task/list", methods=['GET'])
def task_list():
    if not current_user.is_authenticated:
        return is_not_auth()

    tasks = Task.select() \
        .order_by(Task.date) \
        .where(Task.user == current_user.id)

    content = render_tasks_list_as_table(tasks)
    return render_content(content, "Список дел")


if __name__ == "__main__":
    initialize_database()
    app.debug = True
    app.run()
