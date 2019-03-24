import platform
import datetime


def test_platform():
    print(platform.system())
    print(datetime.date.today().year)
    print(datetime.date.today().month)
    print(datetime.date.today().day)


if __name__ == "__main__":
    test_platform()
