from db.dal.base import BaseDAL
from db.models import users as db_users
from schemas import users


class Users(BaseDAL[db_users.User, users.UserCreate, users.UserCreate]):
    model = db_users.User
    readable_object_name = "user"
