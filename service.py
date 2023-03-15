import time


class Service():
    _api = ""

    async def sendUserData(space, login, password):
        # r = requests.post("http://bugs.python.org", data={'login': login, 'password':password})
        time.sleep(1)
        with open('session.txt', 'w') as f:
            f.write('auth')
        return True

    def checkUserSession(save):
        try:
            session = open("session.txt")
            return True
        except:
            return False