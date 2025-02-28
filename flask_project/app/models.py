from app import db
import sqlalchemy as sa
import sqlalchemy.orm as so
    
class User(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), unique=True, nullable=False)
    password: so.Mapped[str] = so.mapped_column(sa.String(128), nullable=False) ### 
    tasks: so.Mapped[list['Task']] = so.relationship(back_populates='user')
    
    def __repr__(self):
        return f'<User {self.username}>'    
    

class Task(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    title: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    description: so.Mapped[str] = so.mapped_column(sa.Text, nullable=True)
    done: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('user.id'))
    user: so.Mapped['User'] = so.relationship(back_populates='tasks')

    def __repr__(self):
        return f'<Task id={self.id}, title={self.title}>'
    