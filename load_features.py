from app.data import user, activity
from app.features import timestamp, web, device, pc

if __name__ == "__main__":
    timestamp.run_scoring(activity.all)
    web.run_scoring(activity.http)
    dev_120 = activity.filter_by_date(activity.dev, 50)
    device.run_scoring(user.join_on_uid(dev_120))
    all_50 = activity.filter_by_date(activity.all, 50)
    pc.run_scoring(user.join_on_uid(all_50))

    