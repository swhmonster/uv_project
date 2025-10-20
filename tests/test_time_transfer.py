#!/usr/bin/env python3
"""
time_transfer.py 的单元测试

测试时间转换工具的各个功能模块，包括：
- 时间戳验证
- 日期字符串解析
- 时区检测
- 时间戳与日期的相互转换
- 当前时间信息获取
"""

import unittest
import datetime
import pytz
from unittest.mock import patch, MagicMock
import sys
import os

# 添加 src 目录到 Python 路径，以便导入被测试的模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from tools.time_transfer import (
    validate_timestamp,
    parse_date_string,
    detect_timezone_from_abbr,
    timestamp_to_date,
    date_to_timestamp,
    get_current_time_info,
    TIME_ZONES,
    DATE_FORMATS
)


class TestValidateTimestamp(unittest.TestCase):
    """测试 validate_timestamp 函数"""

    def test_valid_timestamp_integer(self):
        """测试有效的整数时间戳"""
        result = validate_timestamp("1697049600")
        self.assertEqual(result, 1697049600.0)

    def test_valid_timestamp_float(self):
        """测试有效的浮点数时间戳"""
        result = validate_timestamp("1697049600.123")
        self.assertEqual(result, 1697049600.123)

    def test_valid_timestamp_milliseconds(self):
        """测试毫秒级时间戳"""
        result = validate_timestamp("1697049600000")
        self.assertEqual(result, 1697049600000.0)

    def test_timestamp_with_whitespace(self):
        """测试带空格的时间戳"""
        result = validate_timestamp("  1697049600  ")
        self.assertEqual(result, 1697049600.0)

    def test_invalid_timestamp_string(self):
        """测试无效的字符串时间戳"""
        with self.assertRaises(ValueError) as context:
            validate_timestamp("not_a_number")
        self.assertIn("无效的时间戳格式", str(context.exception))

    def test_negative_timestamp(self):
        """测试负数时间戳"""
        with self.assertRaises(ValueError) as context:
            validate_timestamp("-1")
        self.assertIn("时间戳超出合理范围", str(context.exception))

    def test_future_timestamp_out_of_range(self):
        """测试超出范围的未来时间戳"""
        with self.assertRaises(ValueError) as context:
            validate_timestamp("5000000000000")  # 超过2100年
        self.assertIn("时间戳超出合理范围", str(context.exception))

    def test_zero_timestamp(self):
        """测试零时间戳（1970年1月1日）"""
        result = validate_timestamp("0")
        self.assertEqual(result, 0.0)


class TestParseDateString(unittest.TestCase):
    """测试 parse_date_string 函数"""

    def test_standard_format(self):
        """测试标准日期格式"""
        dt, tz = parse_date_string("2023-10-11 12:34:56")
        expected = datetime.datetime(2023, 10, 11, 12, 34, 56)
        self.assertEqual(dt, expected)
        self.assertIsNone(tz)

    def test_iso_format(self):
        """测试 ISO 8601 格式"""
        dt, tz = parse_date_string("2023-10-11T12:34:56")
        expected = datetime.datetime(2023, 10, 11, 12, 34, 56)
        self.assertEqual(dt, expected)
        self.assertIsNone(tz)

    def test_date_only(self):
        """测试仅日期格式"""
        dt, tz = parse_date_string("2023-10-11")
        expected = datetime.datetime(2023, 10, 11, 0, 0, 0)
        self.assertEqual(dt, expected)
        self.assertIsNone(tz)

    def test_slash_format(self):
        """测试斜杠分隔格式"""
        dt, tz = parse_date_string("2023/10/11 12:34:56")
        expected = datetime.datetime(2023, 10, 11, 12, 34, 56)
        self.assertEqual(dt, expected)
        self.assertIsNone(tz)

    def test_us_format(self):
        """测试美式日期格式"""
        dt, tz = parse_date_string("10/11/2023 12:34:56")
        expected = datetime.datetime(2023, 10, 11, 12, 34, 56)
        self.assertEqual(dt, expected)
        self.assertIsNone(tz)

    def test_chinese_format(self):
        """测试中文日期格式"""
        dt, tz = parse_date_string("2023年10月11日 12:34:56")
        expected = datetime.datetime(2023, 10, 11, 12, 34, 56)
        self.assertEqual(dt, expected)
        self.assertIsNone(tz)

    def test_compact_format(self):
        """测试紧凑格式"""
        dt, tz = parse_date_string("20231011123456")
        expected = datetime.datetime(2023, 10, 11, 12, 34, 56)
        self.assertEqual(dt, expected)
        self.assertIsNone(tz)

    def test_timezone_abbreviation(self):
        """测试带时区缩写的格式"""
        dt, tz = parse_date_string("2023-10-11 12:34:56 CST")
        expected = datetime.datetime(2023, 10, 11, 12, 34, 56)
        self.assertEqual(dt, expected)
        self.assertEqual(tz, "CST")

    def test_timezone_offset(self):
        """测试带时区偏移的格式"""
        dt, tz = parse_date_string("2023-10-11 12:34:56 +0800")
        expected = datetime.datetime(2023, 10, 11, 12, 34, 56)
        self.assertEqual(dt, expected)
        self.assertIsNotNone(tz)

    def test_invalid_date_format(self):
        """测试无效的日期格式"""
        with self.assertRaises(ValueError) as context:
            parse_date_string("invalid_date")
        self.assertIn("无法解析日期格式", str(context.exception))

    def test_whitespace_handling(self):
        """测试空格处理"""
        dt, tz = parse_date_string("  2023-10-11 12:34:56  ")
        expected = datetime.datetime(2023, 10, 11, 12, 34, 56)
        self.assertEqual(dt, expected)
        self.assertIsNone(tz)


class TestDetectTimezoneFromAbbr(unittest.TestCase):
    """测试 detect_timezone_from_abbr 函数"""

    def test_cst_with_shanghai_target(self):
        """测试 CST 缩写，目标时区为上海"""
        result = detect_timezone_from_abbr("CST", "Asia/Shanghai")
        self.assertEqual(result, "Asia/Shanghai")

    def test_cst_with_chicago_target(self):
        """测试 CST 缩写，目标时区为芝加哥"""
        result = detect_timezone_from_abbr("CST", "America/Chicago")
        self.assertEqual(result, "America/Chicago")

    def test_cst_with_other_target(self):
        """测试 CST 缩写，目标时区为其他"""
        result = detect_timezone_from_abbr("CST", "UTC")
        self.assertEqual(result, "Asia/Shanghai")  # 默认返回第一个匹配

    def test_pst_abbreviation(self):
        """测试 PST 缩写"""
        result = detect_timezone_from_abbr("PST", "UTC")
        self.assertEqual(result, "America/Los_Angeles")

    def test_jst_abbreviation(self):
        """测试 JST 缩写"""
        result = detect_timezone_from_abbr("JST", "UTC")
        self.assertEqual(result, "Asia/Tokyo")

    def test_utc_abbreviation(self):
        """测试 UTC 缩写"""
        result = detect_timezone_from_abbr("UTC", "Asia/Shanghai")
        self.assertEqual(result, "UTC")

    def test_unknown_abbreviation(self):
        """测试未知缩写"""
        result = detect_timezone_from_abbr("XYZ", "Asia/Shanghai")
        self.assertEqual(result, "Asia/Shanghai")  # 返回目标时区


class TestTimestampToDate(unittest.TestCase):
    """测试 timestamp_to_date 函数"""

    def test_timestamp_to_shanghai_time(self):
        """测试时间戳转换为上海时间"""
        # 2023-10-11 20:00:00 UTC = 2023-10-12 04:00:00 CST
        timestamp = 1697054400000  # 毫秒时间戳
        result = timestamp_to_date(timestamp, "Asia/Shanghai")
        self.assertIn("2023-10-12 04:00:00", result)
        self.assertIn("CST", result)

    def test_timestamp_to_utc_time(self):
        """测试时间戳转换为 UTC 时间"""
        timestamp = 1697054400000
        result = timestamp_to_date(timestamp, "UTC")
        self.assertIn("2023-10-11 20:00:00", result)
        self.assertIn("UTC", result)

    def test_timestamp_to_los_angeles_time(self):
        """测试时间戳转换为洛杉矶时间"""
        timestamp = 1697054400000
        result = timestamp_to_date(timestamp, "America/Los_Angeles")
        self.assertIn("2023-10-11 13:00:00", result)
        # 可能是 PDT 或 PST，取决于夏令时

    def test_zero_timestamp(self):
        """测试零时间戳"""
        result = timestamp_to_date(0, "UTC")
        self.assertIn("1970-01-01 00:00:00", result)

    def test_invalid_timezone(self):
        """测试无效时区"""
        with self.assertRaises(ValueError):
            timestamp_to_date(1697054400000, "Invalid/Timezone")


class TestDateToTimestamp(unittest.TestCase):
    """测试 date_to_timestamp 函数"""

    def test_shanghai_date_to_timestamp(self):
        """测试上海时间转时间戳"""
        # 2023-10-12 04:00:00 CST = 2023-10-11 20:00:00 UTC
        result = date_to_timestamp("2023-10-12 04:00:00", "Asia/Shanghai")
        expected = 1697054400000  # 毫秒时间戳
        self.assertEqual(result, expected)

    def test_utc_date_to_timestamp(self):
        """测试 UTC 时间转时间戳"""
        result = date_to_timestamp("2023-10-11 20:00:00", "UTC")
        expected = 1697054400000
        self.assertEqual(result, expected)

    def test_date_with_timezone_info(self):
        """测试带时区信息的日期转时间戳"""
        result = date_to_timestamp("2023-10-12 04:00:00 CST", "Asia/Shanghai")
        expected = 1697054400000
        self.assertEqual(result, expected)

    def test_date_only_format(self):
        """测试仅日期格式转时间戳"""
        result = date_to_timestamp("2023-10-11", "UTC")
        # 应该是当天 00:00:00 UTC 的时间戳
        expected_dt = datetime.datetime(2023, 10, 11, 0, 0, 0)
        expected_timestamp = int(pytz.utc.localize(expected_dt).timestamp() * 1000)
        self.assertEqual(result, expected_timestamp)

    def test_various_date_formats(self):
        """测试各种日期格式转时间戳"""
        formats_and_dates = [
            "2023/10/11 12:34:56",
            "10/11/2023 12:34:56",
            "2023年10月11日 12:34:56",
            "20231011123456"
        ]
        
        for date_str in formats_and_dates:
            result = date_to_timestamp(date_str, "UTC")
            self.assertIsInstance(result, int)
            self.assertGreater(result, 0)

    def test_invalid_date_format(self):
        """测试无效日期格式"""
        with self.assertRaises(ValueError):
            date_to_timestamp("invalid_date", "UTC")

    def test_invalid_timezone(self):
        """测试无效时区"""
        with self.assertRaises(ValueError):
            date_to_timestamp("2023-10-11 12:34:56", "Invalid/Timezone")


class TestGetCurrentTimeInfo(unittest.TestCase):
    """测试 get_current_time_info 函数"""

    @patch('tools.time_transfer.time.time')
    @patch('tools.time_transfer.datetime.datetime')
    def test_current_time_info_format(self, mock_datetime, mock_time):
        """测试当前时间信息格式"""
        # Mock 当前时间
        mock_time.return_value = 1697054400  # 秒级时间戳
        mock_utc_time = datetime.datetime(2023, 10, 11, 20, 0, 0, tzinfo=datetime.timezone.utc)
        mock_datetime.now.return_value = mock_utc_time

        result = get_current_time_info()
        
        # 检查返回格式
        self.assertIn("当前时间戳:", result)
        self.assertIn("1697054400000", result)  # 毫秒时间戳
        
        # 检查包含各个时区
        for tz_info in TIME_ZONES.values():
            self.assertIn(tz_info['name'], result)

    def test_current_time_info_structure(self):
        """测试当前时间信息结构"""
        result = get_current_time_info()
        lines = result.split('\n')
        
        # 第一行应该是时间戳
        self.assertTrue(lines[0].startswith("当前时间戳:"))
        
        # 后续行应该包含时区信息
        self.assertEqual(len(lines), len(TIME_ZONES) + 1)


class TestConstants(unittest.TestCase):
    """测试常量定义"""

    def test_time_zones_structure(self):
        """测试时区常量结构"""
        self.assertIsInstance(TIME_ZONES, dict)
        
        for key, value in TIME_ZONES.items():
            self.assertIsInstance(key, str)
            self.assertIsInstance(value, dict)
            self.assertIn('tz', value)
            self.assertIn('name', value)
            self.assertIsInstance(value['tz'], str)
            self.assertIsInstance(value['name'], str)

    def test_date_formats_structure(self):
        """测试日期格式常量结构"""
        self.assertIsInstance(DATE_FORMATS, list)
        self.assertGreater(len(DATE_FORMATS), 0)
        
        for fmt in DATE_FORMATS:
            self.assertIsInstance(fmt, str)
            self.assertIn('%', fmt)  # 应该包含格式化符号

    def test_timezone_coverage(self):
        """测试时区覆盖范围"""
        expected_timezones = [
            'Asia/Shanghai',
            'America/Los_Angeles', 
            'Asia/Riyadh',
            'Europe/Madrid',
            'UTC',
            'America/New_York',
            'Asia/Tokyo',
            'Europe/London'
        ]
        
        actual_timezones = [info['tz'] for info in TIME_ZONES.values()]
        
        for tz in expected_timezones:
            self.assertIn(tz, actual_timezones)


class TestEdgeCases(unittest.TestCase):
    """测试边界情况和异常情况"""

    def test_leap_year_handling(self):
        """测试闰年处理"""
        # 2024年是闰年，2月29日应该有效
        dt, tz = parse_date_string("2024-02-29 12:00:00")
        self.assertEqual(dt.month, 2)
        self.assertEqual(dt.day, 29)

    def test_daylight_saving_time(self):
        """测试夏令时处理"""
        # 测试夏令时期间的时间转换
        summer_date = "2023-07-15 12:00:00"
        winter_date = "2023-12-15 12:00:00"
        
        summer_ts = date_to_timestamp(summer_date, "America/Los_Angeles")
        winter_ts = date_to_timestamp(winter_date, "America/Los_Angeles")
        
        # 夏令时和标准时间的时间戳应该不同（相同本地时间）
        self.assertNotEqual(summer_ts, winter_ts)

    def test_extreme_timestamps(self):
        """测试极端时间戳"""
        # 测试接近边界的时间戳
        early_timestamp = 1000  # 1970年附近
        late_timestamp = 4102444800000 - 1000  # 接近2100年
        
        result1 = timestamp_to_date(early_timestamp, "UTC")
        result2 = timestamp_to_date(late_timestamp, "UTC")
        
        self.assertIn("1970", result1)
        self.assertIn("2099", result2)

    def test_microsecond_precision(self):
        """测试微秒精度处理"""
        dt, tz = parse_date_string("2023-10-11T12:34:56.123456")
        self.assertEqual(dt.microsecond, 123456)

    def test_empty_string_handling(self):
        """测试空字符串处理"""
        with self.assertRaises(ValueError):
            parse_date_string("")
        
        with self.assertRaises(ValueError):
            validate_timestamp("")


if __name__ == '__main__':
    # 配置测试运行器
    unittest.main(verbosity=2, buffer=True)