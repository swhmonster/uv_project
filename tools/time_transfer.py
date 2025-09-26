import argparse
import datetime
import pytz
import time

# 定义时区映射
TIME_ZONES = {
    '1': 'Asia/Shanghai',  # 上海时区/北京时区（与上海时区相同）
    '2': 'America/Los_Angeles',  # 美西时区
    '3': 'Asia/Riyadh',  # 沙特阿拉伯时区
    '4': 'Europe/Madrid'  # 西班牙马德里时区
}


def timestamp_to_date(timestamp, timezone_str):
    # 将时间戳转换为UTC时间
    utc_time = datetime.datetime.utcfromtimestamp(timestamp / 1000).replace(tzinfo=pytz.utc)

    # 获取目标时区
    target_timezone = pytz.timezone(timezone_str)

    # 将UTC时间转换为目标时区时间
    target_time = utc_time.astimezone(target_timezone)

    return target_time.strftime('%Y-%m-%d %H:%M:%S')


def date_to_timestamp(date_str, timezone_str):
    # 获取目标时区
    target_timezone = pytz.timezone(timezone_str)

    # 将日期字符串解析为目标时区的时间
    target_time = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    target_time = target_timezone.localize(target_time)

    # 转换为UTC时间戳并返回毫秒级时间戳
    timestamp = int(target_time.astimezone(pytz.utc).timestamp() * 1000)

    return timestamp


def main():
    parser = argparse.ArgumentParser(description='Convert between timestamp and date with timezone support.')
    parser.add_argument('-m', '--mode', choices=['to_date', 'to_timestamp'],
                        help='Conversion mode: to_date or to_timestamp')
    parser.add_argument('-v', '--value', help='The timestamp or date string to convert')
    parser.add_argument('-t', '--timezone', choices=TIME_ZONES.keys(),
                        help='Timezone: 1 for Shanghai, 2 for Los Angeles, 3 for Beijing')

    args = parser.parse_args()

    if not args.mode and not args.value and not args.timezone:
        # 如果没有传入任何参数，返回当前时间戳（毫秒级）
        # print('Current Timestamp (ms):', int(time.time() * 1000))
        print(int(time.time() * 1000), end='')
        return

    if not args.mode or not args.value or not args.timezone:
        print('Error: Missing required arguments')
        parser.print_help()
        return

    timezone_str = TIME_ZONES[args.timezone]

    if args.mode == 'to_date':
        # 时间戳转日期
        try:
            timestamp = float(args.value.strip())
            converted_value = timestamp_to_date(timestamp, timezone_str)
            print(converted_value, end='')
        except ValueError:
            print('Error: Invalid timestamp value')
    elif args.mode == 'to_timestamp':
        # 日期转时间戳
        try:
            date_str = args.value.strip()
            converted_value = date_to_timestamp(date_str, timezone_str)
            print(converted_value, end='')
        except ValueError:
            print('Error: Invalid date string format. Use YYYY-MM-DD HH:MM:SS')


if __name__ == '__main__':
    main()

# 时间戳转日期（上海时区）：python convert.py -m to_date -v 1697049600 -t 1
# 日期转时间戳（美西时区）：python convert.py -m to_timestamp -v "2023-10-11 12:34:56" -t 2
# 不传参数时返回当前时间戳
