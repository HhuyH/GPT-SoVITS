import sys
import os

# Thêm đường dẫn để Python tìm thấy module text
sys.path.append(os.getcwd())

# Import hàm g2p từ file vietnamese.py ông vừa tạo
try:
    from text.vietnamese import g2p
    print("✅ Đã kết nối được với 'pháp sư' Vietnamese.py")
except Exception as e:
    print(f"❌ Lỗi Import: {e}")
    sys.exit()

def run_test():
    # Câu test đầy đủ "đồ chơi": Tiếng Việt + Số + Đơn vị + Dấu câu
    text = "Chào ông giáo, hôm nay ngày 03/02 tôi mua 5kg gạo hết 150.000 đồng."
    
    print(f"\n--- ĐANG XỬ LÝ VĂN BẢN ---")
    print(f"Gốc: {text}")
    
    try:
        # Chạy hàm g2p (nó sẽ gọi cả normalize bên trong)
        phones, word2ph = g2p(text)
        
        print(f"\n--- KẾT QUẢ ---")
        print(f"Âm vị (Phones): {phones}")
        print(f"Số lượng âm vị mỗi từ (Word2ph): {word2ph}")
        
        # Kiểm tra xem có dấu câu nào bị rơi rụng không
        if "," in phones and "." in phones:
            print("\n✅ Dấu câu được giữ lại chuẩn xác.")
            
        # Kiểm tra số đã biến thành chữ chưa
        phones_str = " ".join(phones)
        if "tram" in phones_str or "nghin" in phones_str:
            print("✅ Hệ thống Normalization đã biến '150.000' thành chữ chuẩn Việt.")
            
    except Exception as e:
        print(f"❌ Lỗi khi chạy g2p: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_test()