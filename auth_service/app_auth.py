import models


class UserMgmt():
    def __init__(self, database):
        self.session = database.session()

    def find_user(self, phone):
        owner = self.session.query(models.User).filter_by(
            phone_number=phone).first()
        return owner



class AppAuth():
    def __init__(self, database):
        self.user_mgmt = UserMgmt(database)

    def login(self, phone):
        # [TODO]: Validate
        user = self.user_mgmt.find_user(phone)
        if not user:
            return "Phone number {} is not exist!!".format(phone)
        return "Correct"

        