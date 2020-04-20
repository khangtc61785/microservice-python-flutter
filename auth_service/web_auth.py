import models


class OwnerMgmt():
    def __init__(self, database):
        self.session = database.session()

    def find_owner(self, username):
        owner = self.session.query(models.Owner).filter_by(
            username=username).first()
        return owner



class WebAuth():
    def __init__(self, database):
        self.owner_mgmt = OwnerMgmt(database)

    def login(self, username, password):
        # [TODO]: Validate
        owner = self.owner_mgmt.find_owner(username)
        if not owner:
            return "Owner {} is not exist!!".format(username)
        if owner.password != password:
            return "Password is incorrect"
        return "Correct"

        

