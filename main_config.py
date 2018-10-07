import logging
import os


class Config:
    request_timeout = int(os.environ.get('REQUEST_TIMEOUT', 5))
    # 0:print to output        1:use graylog       2:both 0 and 1
    use_graylog = os.environ.get('USE_GRAYLOG', "2")
    source = os.environ.get('SOURCE', "bot_source")
    graylog_host = os.environ.get('GRAYLOG_HOST', "localhost")
    graylog_port = int(os.environ.get('GRAYLOG_PORT', "12201"))
    log_level = int(os.environ.get('LOG_LEVEL', logging.DEBUG))
    log_facility_name = os.environ.get('LOG_FACILITY_NAME', "python_bale_bot")
    real_time_fetch_updates = os.environ.get('REAL_TIME_FETCH_UPDATES', True)
    continue_last_processed_seq = os.environ.get('CONTINUE_LAST_PROCESSED_SEQ', False)
    max_total_send_failure = int(os.environ.get('MAX_TOTAL_FAILURE', 20))
    max_retries = int(os.environ.get('MAX_RETRIES', 1))
    check_interval = float(os.environ.get('CHECK_INTERVAL', 0.5))
    time_sleep = float(os.environ.get('TIME_SLEEP', 0.5))
    bot_token = os.environ.get('TOKEN', "8b44d740b78ac33894be616f4e7ff0946e4cea09")
    bot_user_id = os.environ.get('BOT_USER_ID', "41")
    admin_user_id_list = ["1497526823", "1341381900"]
