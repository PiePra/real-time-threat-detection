from app.data import user_data, activity_data
from app.features import timestamp, web, device, pc, user

if __name__ == "__main__":
    user.update(user_data.user)
    timestamp.update(activity_data.all)
    web.update(activity_data.http)
    dev_120 = activity_data.filter_by_date(activity_data.dev, 50)
    device.update(user_data.join_on_uid(dev_120))
    all_50 = activity_data.filter_by_date(activity_data.all, 50)
    pc.update(user_data.join_on_uid(all_50))