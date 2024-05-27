from datetime import datetime, timedelta, timezone

def hanoi_time():
    # Lấy ngày giờ hiện tại
    now_utc = datetime.now(timezone.utc)

    # Chuyển múi giờ từ UTC sang Hanoi (+7)
    hanoi_offset = timedelta(hours=7)
    hanoi_time = now_utc + hanoi_offset

    # Định dạng ngày tháng năm
    date_format = "%d/%m/%Y"
    formatted_date = hanoi_time.strftime(date_format)

    # Định dạng giờ phút giây
    time_format = "%H:%M:%S"
    formatted_time = hanoi_time.strftime(time_format)

    return formatted_date, formatted_time

if __name__ == "__main__":
    date, time = hanoi_time()
    print("Ngày hôm nay là:", date)
    print("Giờ theo múi giờ Hanoi là:", time)
