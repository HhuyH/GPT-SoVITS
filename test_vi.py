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
        "Chào bạn, lại là vun đây từ Góc Nhỏ mang tên Được Khỏe Vui.",
        "để ở đâu rồi? Chắc hẳn bạn cũng đã quen với cái cảnh này.",
        "Hoặc là mở suy nghĩ trong đầu, tạo cái file mới đặt tên là đơn xin nghỉ việc.",
        "Cái cảm giác kiệt sức cứ triền miên. Nỗi ám ảnh tối chủ nhật chuẩn bị cho sáng thứ hai nó lại quay lại.",
        "Thì chào mừng bạn, hôm nay chúng ta sẽ nói thật với nhau",
        "Nhưng lại đóng băng vì sợ hãi. Nhưng trước tiên, mình cần bạn biết:",
        "Đó là trách nhiệm của người lớn đang đè nặng.",
        "Hãy thở sâu. Bạn không đơn độc. Và quan trọng,",
        "Và bây giờ, trước khi mà bạn có thể nghỉ việc",
        "Thì chúng ta cần can đảm gọi tên những cái sợi xích tâm lý vô hình đang kìm hãm bạn lại. Vì đôi khi,",
        "Vậy thì, mắt xích đầu tiên: nỗi sợ mất đi bản sắc.",
        "cái sự đào sâu hơn một chút ấy thì bạn sẽ thấy rằng",
        "Anh chị làm nghề gì? gần như là câu cửa miệng. Nó thành một phần định nghĩa con người của mình luôn rồi.",
        "Identity fusion, khi mà mình vô tình hòa quyện toàn bộ giá trị bản thân vào công việc."
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