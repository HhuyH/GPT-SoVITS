# coding=utf-8

from text.vietnamese import g2p


def run_test():

    test_cases = [
        # ================= DATE =================
        # "Hôm nay là 12/03/2024.",
        # "Deadline: 2024-04-01.",
        # "Sự kiện diễn ra ngày 1/1/2023.",
        # "Ngày phát hành 2023/12/25.",

        # ================= TIME =================
        # "Họp lúc 08:05.",
        # "Thời gian thi từ 8:30-10:45.",
        # "Chương trình bắt đầu lúc 23:59:30.",
        # "Mở cửa 07:00 sáng.",

        # ================= PERCENT =================
        # "Giảm giá 50%.",
        # "Tăng 12.5%.",
        # "Lãi suất là 7.25%.",

        # # ================= FRACTION =================
        # "Phân số là 3/4.",
        # "Tỉ lệ 1/2 dân số.",
        # "Công thức 5/10.",

        # # ================= PHONE =================
        # "Gọi ngay 0987654321.",
        # "Liên hệ 0912345678 để biết thêm chi tiết.",
        # "Hotline 19001234 hoạt động 24/7.",
        # "Số bàn 024-12345678.",

        # # ================= TEMPERATURE =================
        # "Nhiệt độ hôm nay là 32°C.",
        # "Trời lạnh -5°C vào ban đêm.",

        # # ================= UNITS =================
        # "Diện tích phòng là 25m2.",
        # "Chiều dài 3m.",
        # "Cân nặng 65kg.",
        # "Tốc độ 60km.",
        # "Thể tích 10cm3.",

        # # ================= MATH =================
        # "5 + 3 = 8.",
        # "10 - 2 = 8.",
        # "6 × 7 = 42.",
        # "8 ÷ 2 = 4.",

        # # ================= NEGATIVE & DECIMAL =================
        "Nhiệt độ là -10 độ.",
        "Số pi xấp xỉ 3.14.", # bug
        "Giá là 1000000 đồng.",
        "Phiên bản v2.1 phát hành hôm nay.", # bug

        # # ================= MIXED =================
        # "Meeting lúc 09:30 ngày 15/08/2024 tại TP.HCM.",
        # "CPU chạy ở 3.5GHz.",
        # "Tăng trưởng GDP 8.2% trong năm 2023.",
        # "Kết quả là 1/3 tổng số 300 người.",
    ]
    print("=" * 70)
    print("FULL G2P PIPELINE TEST")
    print("=" * 70)

    for i, text in enumerate(test_cases, 1):
        print(f"\nTest {i}")
        print("INPUT :", text)

        try:
            phones, word2ph = g2p(text)

            print("PHONES :", phones)
            print("WORD2PH:", word2ph)
            print("TOTAL PHONES:", len(phones))

        except Exception as e:
            print("❌ ERROR:", e)


if __name__ == "__main__":
    run_test()
