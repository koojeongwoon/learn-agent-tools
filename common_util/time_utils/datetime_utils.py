from datetime import datetime, timezone, timedelta

# 한국 시간대 설정 (KST = UTC + 9)
KST = timezone(timedelta(hours=9))

def now_kst() -> datetime:
    """현재 한국 시간을 반환합니다."""
    return datetime.now(KST)

def format_date(dt: datetime, fmt: str = "%Y-%m-%d") -> str:
    """날짜를 지정된 포맷의 문자열로 변환합니다."""
    return dt.strftime(fmt)

def format_datetime(dt: datetime, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """날짜와 시간을 지정된 포맷의 문자열로 변환합니다."""
    return dt.strftime(fmt)

def parse_date(date_str: str, fmt: str = "%Y-%m-%d") -> datetime:
    """문자열을 datetime 객체로 변환합니다. (KST 적용)"""
    dt = datetime.strptime(date_str, fmt)
    return dt.replace(tzinfo=KST)
