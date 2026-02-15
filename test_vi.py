import sys
import os

# Đảm bảo Python tìm thấy module text
sys.path.append(os.getcwd())

try:
    from text.vietnamese import g2p
    print("✅ Đã kết nối với 'pháp sư' Vietnamese.py mới.")
except Exception as e:
    print(f"❌ Lỗi Import: {e}")
    sys.exit()

def test_specific_lines():
    # Danh sách các câu ông giáo bị lỗi UNK lúc nãy
    test_cases = [
        "Càn khôn xoay chuyển, vạn vật thái bình. Thanh âm u huyền văng vẳng chốn thâm uyên.",
        "Bậc chính nhân quân tử, chí tại tứ phương, mưu đồ đại sự, xoay vần tạo hóa, định đoạt giang sơn xã tắc"
    ]

    print(f"\n{'='*20} BẮT ĐẦU KIỂM TRA BIẾN HÌNH {'='*20}")
    
    all_clean = True
    for i, text in enumerate(test_cases, 1):
        try:
            phones, word2ph = g2p(text)
            phones_str = " ".join(phones)
            
            print(f"\nCâu {i}: {text}")
            print(f"Result: {phones_str}")
            
            if "UNK" in phones_str:
                print(f"❌ VẪN CÒN LỖI UNK Ở ĐÂY!")
                all_clean = False
            else:
                print(f"✅ SẠCH BÓNG QUÂN THÙ!")
                
        except Exception as e:
            print(f"❌ Lỗi xử lý câu {i}: {e}")
            all_clean = False

    print(f"\n{'='*60}")
    if all_clean:
        print("🎉 CHÚC MỪNG ÔNG GIÁO! Không còn một chữ UNK nào trong đống câu lỗi cũ.")
    else:
        print("⚠️ Vẫn còn sót vài từ lạ, ông giáo hãy quăng log lên tôi xem lại.")

if __name__ == "__main__":
    test_specific_lines()