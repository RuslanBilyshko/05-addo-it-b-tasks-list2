import peewee as pw
from playhouse.fields import PasswordField

db = pw.SqliteDatabase('database.db')


def initialize_database():
    User.create_table(fail_silently=True)
    Task.create_table(fail_silently=True)

    try:
        User.create(
            username='root',
            password='123'
        )
    except pw.IntegrityError:
        pass


class BaseModel(pw.Model):
    class Meta:
        database = db


class User(BaseModel):
    username = pw.CharField(max_length=70, unique=True)
    password = PasswordField()
    state = pw.BooleanField(default=True)

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.state

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)


class Task(BaseModel):
    title = pw.CharField(max_length=100)
    description = pw.TextField()
    date = pw.DateField()
    time = pw.TimeField()
    status = pw.IntegerField(default=0)
    user = pw.ForeignKeyField(User)
