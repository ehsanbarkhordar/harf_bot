class ReadyMessage:
    initiate = "چه کاری برات انجام بدم؟"
    start_conversation = "شما می‌توانید صورت حساب های بانک ملی خود براساس روز، هفته، " \
                         "ماه جاری یا بازه زمانی مشخصی را مشاهده کنبد."
    info = "A fun yet helpful game.\n" \
           "Let people you know to tell you what's on their mind about you, anonymously!\n\n\n" \
           "یه بازی مفید و جالب\n" \
           "از دوستانتون بخواید بدون اینکه شناخته بشن انتقاد یا هرچی تو دلشونه رو به صورت ناشناس بهتون بگن\n\n\n"


class Regex:
    number_only = '^([0-9]+|[۰-۹]+)$'
    eight_digits_number = "^[0-9]{8}$|^[۰-۹]{8}$"
    numbers = '([0-9]+|[۰-۹]+)'
    persian_regex = "[ء|\s|آ-ی]+"
    any_match = "(.*)"
    payment_pattern = "{}-{}-{}".format(numbers, numbers, numbers)


class TMessage:
    cancel = "لغو"
    start = "شروع"
    back = "بازگشت به منو اصلی"
    help = "راهنما"
    # ===========================
    want_to_get_anonymously_message = "می‌خوام پیام ناشناس دریافت کنم"
    inbox = "پیام های دریافت شده"
    send_direct = "ارسال مستقیم ناشناس"


class LogMessage:
    success_send_message = "success send message"
    fail_send_message = "success send message"
    max_fail_retried = "max fails retried"
    location_sent = "location sent to client"
    upload_failure = "upload was failed"
    upload_success = "upload was successful"
    info = "info showed"
