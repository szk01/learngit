from flask_login import LoginManager

login_manager = LoginManager()

# 通过用户id拿到相应的用户对象
@login_manager.user_loader
def load_user(user_id):
    from models.user import User
    user = User.query.get(int(user_id))
    return user