#!/usr/bin/env python3
"""
时间转换工具

支持时间戳和日期之间的相互转换，支持多个时区。
可以处理毫秒级时间戳，支持多种日期格式。
"""

import argparse
import datetime
import pytz
import time
import sys
from typing import Dict, Optional

# 定义时区映射
TIME_ZONES: Dict[str, Dict[str, str]] = {
    '1': {'tz': 'Asia/Shanghai', 'name': '上海/北京时区 (UTC+8)'},
    '2': {'tz': 'America/Los_Angeles', 'name': '美西时区 (UTC-8/-7)'},
    '3': {'tz': 'Asia/Riyadh', 'name': '沙特阿拉伯时区 (UTC+3)'},
    '4': {'tz': 'Europe/Madrid', 'name': '西班牙马德里时区 (UTC+1/+2)'},
    '5': {'tz': 'UTC', 'name': 'UTC时区 (UTC+0)'},
    '6': {'tz': 'America/New_York', 'name': '美东时区 (UTC-5/-4)'},
    '7': {'tz': 'Asia/Tokyo', 'name': '东京时区 (UTC+9)'},
    '8': {'tz': 'Europe/London', 'name': '伦敦时区 (UTC+0/+1)'}
}

# 支持的日期格式
DATE_FORMATS = [
    '%Y-%m-%d %H:%M:%S',
    '%Y/%m/%d %H:%M:%S',
    '%Y-%m-%d %H:%M',
    '%Y/%m/%d %H:%M',
    '%Y-%m-%d',
    '%Y/%m/%d'
]

def validate_timestamp(timestamp_str: str) -> float:
    """验证并转换时间戳"""
    try:
        timestamp = float(timestamp_str.strip())
        # 检查是否为合理的时间戳范围（1970-2100年）
        if timestamp < 0 or timestamp > 4102444800000:  # 2100年的毫秒时间戳
            raise ValueError("时间戳超出合理范围")
        return timestamp
    except ValueError as e:
        raise ValueError(f"无效的时间戳格式: {e}")

def parse_date_string(date_str: str) -> datetime.datetime:
    """尝试解析多种日期格式"""
    date_str = date_str.strip()
    
    for fmt in DATE_FORMATS:
        try:
            return datetime.datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    raise ValueError(f"无法解析日期格式，支持的格式: {', '.join(DATE_FORMATS)}")

def timestamp_to_date(timestamp: float, timezone_str: str) -> str:
    """
    将时间戳转换为指定时区的日期字符串
    
    Args:
        timestamp: 毫秒级时间戳
        timezone_str: 时区字符串
    
    Returns:
        格式化的日期字符串
    """
    try:
        # 将时间戳转换为UTC时间
        utc_time = datetime.datetime.utcfromtimestamp(timestamp / 1000).replace(tzinfo=pytz.utc)
        
        # 获取目标时区
        target_timezone = pytz.timezone(timezone_str)
        
        # 将UTC时间转换为目标时区时间
        target_time = utc_time.astimezone(target_timezone)
        
        return target_time.strftime('%Y-%m-%d %H:%M:%S %Z')
    except Exception as e:
        raise ValueError(f"时间戳转换失败: {e}")

def date_to_timestamp(date_str: str, timezone_str: str) -> int:
    """
    将日期字符串转换为毫秒级时间戳
    
    Args:
        date_str: 日期字符串
        timezone_str: 时区字符串
    
    Returns:
        毫秒级时间戳
    """
    try:
        # 获取目标时区
        target_timezone = pytz.timezone(timezone_str)
        
        # 解析日期字符串
        target_time = parse_date_string(date_str)
        
        # 本地化到目标时区
        target_time = target_timezone.localize(target_time)
        
        # 转换为UTC时间戳并返回毫秒级时间戳
        timestamp = int(target_time.astimezone(pytz.utc).timestamp() * 1000)
        
        return timestamp
    except Exception as e:
        raise ValueError(f"日期转换失败: {e}")

def get_current_time_info() -> str:
    """获取当前时间的详细信息"""
    current_timestamp = int(time.time() * 1000)
    current_utc = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
    
    info_lines = [f"当前时间戳: {current_timestamp}"]
    
    # 显示各个时区的当前时间
    for tz_key, tz_info in TIME_ZONES.items():
        tz = pytz.timezone(tz_info['tz'])
        local_time = current_utc.astimezone(tz)
        info_lines.append(f"{tz_key}. {tz_info['name']}: {local_time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    
    return '\n'.join(info_lines)

def print_timezone_help():
    """打印时区帮助信息"""
    print("可用时区:")
    for key, info in TIME_ZONES.items():
        print(f"  {key}: {info['name']}")

def main():
    parser = argparse.ArgumentParser(
        description='时间转换工具 - 支持时间戳和日期之间的相互转换',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  获取当前时间戳:
    python time_transfer.py
    
  时间戳转日期 (上海时区):
    python time_transfer.py -m to_date -v 1697049600000 -t 1
    
  日期转时间戳 (美西时区):
    python time_transfer.py -m to_timestamp -v "2023-10-11 12:34:56" -t 2
    
  显示当前各时区时间:
    python time_transfer.py --current-time
    
  显示时区列表:
    python time_transfer.py --list-timezones
        """
    )
    
    parser.add_argument('-m', '--mode', choices=['to_date', 'to_timestamp'],
                        help='转换模式: to_date (时间戳转日期) 或 to_timestamp (日期转时间戳)')
    parser.add_argument('-v', '--value', help='要转换的时间戳或日期字符串')
    parser.add_argument('-t', '--timezone', choices=TIME_ZONES.keys(),
                        help='时区选择 (使用 --list-timezones 查看所有可用时区)')
    parser.add_argument('--current-time', action='store_true',
                        help='显示当前各时区时间')
    parser.add_argument('--list-timezones', action='store_true',
                        help='显示所有可用时区')

    args = parser.parse_args()

    # 处理特殊参数
    if args.list_timezones:
        print_timezone_help()
        return

    if args.current_time:
        print(get_current_time_info())
        return

    # 如果没有传入任何参数，返回当前时间戳（毫秒级）
    if not args.mode and not args.value and not args.timezone:
        print(int(time.time() * 1000), end='')
        return

    # 验证必需参数
    if not args.mode or not args.value or not args.timezone:
        print('错误: 缺少必需参数', file=sys.stderr)
        print('使用 --help 查看帮助信息', file=sys.stderr)
        sys.exit(1)

    # 获取时区信息
    timezone_info = TIME_ZONES[args.timezone]
    timezone_str = timezone_info['tz']

    try:
        if args.mode == 'to_date':
            # 时间戳转日期
            timestamp = validate_timestamp(args.value)
            converted_value = timestamp_to_date(timestamp, timezone_str)
            print(converted_value, end='')
        elif args.mode == 'to_timestamp':
            # 日期转时间戳
            converted_value = date_to_timestamp(args.value, timezone_str)
            print(converted_value, end='')
    except ValueError as e:
        print(f'错误: {e}', file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f'未知错误: {e}', file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()