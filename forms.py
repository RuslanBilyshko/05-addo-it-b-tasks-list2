from wtforms import Form, StringField, PasswordField, TextAreaField, SelectField, HiddenField
import validators
from models import User

required_mess = "Поле обязательно для заполнения"

class LoginForm(Form):
    username = StringField(
        'Имя пользователя',
        [
            validators.DataRequired(
                message=required_mess
            )
        ]
    )

    password = PasswordField(
        'Пароль',
        [
            validators.DataRequired(
                message=required_mess
            )
        ])


class RegisterForm(Form):
    username = StringField(
        'Имя пользователя',
        [
            validators.DataRequired(
                message=required_mess
            ),
            validators.Length(
                min=4, max=25,
                message="Поле должно содержать 4-6 симфолов"
            ),
            validators.Regexp(
                '[A-Za-z0-9]+',
                message="Поле должно содержать буквы латинского алфавита и цыфры"
            ),
            validators.Unique(
                User,
                "username",
                message="Это имя уже занято, придумайте другое"
            )
        ]
    )

    password = PasswordField(
        'Пароль',
        [
            validators.DataRequired(
                message=required_mess
            ),
            validators.Regexp(
                '[A-Za-z0-9]+',
                message="Пароль должен содержать буквы латинского алфавита и цыфры"
            ),
            validators.EqualTo(
                'confirm',
                message='Пароли должны совпадать')
        ])

    confirm = PasswordField('Пароль еще раз')



class TaskForm(Form):
    title = StringField(
        'Название',
        [
            validators.DataRequired(
                message=required_mess
            )
        ]
    )

    description = TextAreaField(
        'Описание',
        [
            validators.DataRequired(
                message=required_mess
            )
        ]
    )

    date = StringField(
        'Дата',
        [
            validators.DataRequired(
                message=required_mess
            ),
            validators.Regexp(
                '^(0?[1-9]|[12][0-9]|3[01])-(0?[1-9]|1[0-2])-\d\d\d\d$',
                message="Дата должна иметь формат \"ДД-ММ-ГГГГ Ч:М\""
            ),
            validators.DatePast(
                message="Дата не может быть в прошлом времени"
            )
        ]
    )

    time = StringField(
        'Время',
        [
            validators.DataRequired(
                message=required_mess
            ),
            validators.Regexp(
                '^(00|[0-9]|1[0-9]|2[0-3]):([0-9]|[0-5][0-9])$',
                message="Время должно иметь формат \"Ч:М\""
            ),

            validators.TimePast(
                message="Время должно быть в будущем"
            )
        ])

class TaskStatusForm(Form):
    status = SelectField(
        'Статус',
        choices=[("0", 'В ожидании'), ("1", 'Выполнено')],
        default="0"
    )


class TaskDeleteForm(Form):
    id = HiddenField()




