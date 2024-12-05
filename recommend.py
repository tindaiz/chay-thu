import pandas as pd
import streamlit as st
from unidecode import unidecode  # Thư viện để chuẩn hóa chuỗi không dấu

def recommend_hotels(df, address, price_range, min_score):
    """
    Lọc khách sạn theo địa chỉ, giá, và điểm đánh giá.
    """
    # Xử lý dữ liệu
    df['price'] = df['price'].apply(lambda x: ''.join(filter(str.isdigit, str(x)))).astype(int)
    df['score'] = df['score'].str.extract('(\d+)').astype(float)  # Trích xuất điểm số
    df['address'] = df['address'].str.strip().str.lower().apply(unidecode)  # Chuẩn hóa địa chỉ thành không dấu
    address = unidecode(address.strip().lower())  # Chuẩn hóa giá trị nhập vào thành không dấu

    # Lọc theo từng tiêu chí
    address_filter = df['address'].str.contains(address, na=False)
    if price_range == "Nhỏ hơn 500.000 đ/ Đêm":
        price_filter = df['price'] < 500000
    elif price_range == "500-1tr đ/ Đêm":
        price_filter = (df['price'] >= 500000) & (df['price'] <= 1000000)
    elif price_range == "Lớn hơn 1tr đ/ Đêm":
        price_filter = df['price'] > 1000000
    else:
        price_filter = pd.Series([True] * len(df))
    score_filter = df['score'] >= min_score

    # Áp dụng bộ lọc
    filtered_df = df[address_filter & price_filter & score_filter]
    recommended_df = (
        filtered_df.sort_values(by=['score', 'price'], ascending=[False, True])
        .drop_duplicates(subset=['hotel'], keep='first')  # Loại bỏ khách sạn trùng
    )
    return recommended_df

def display_hotel_card(row):
    """
    Hiển thị giao diện đẹp cho từng khách sạn.
    """
    formatted_price = f"{row['price']:,}".replace(",", ".")  # Định dạng giá với dấu chấm phân cách
    image_url = row['image_url'] if 'image_url' in row and pd.notna(row['image_url']) else \
        'https://cf.bstatic.com/xdata/images/hotel/max1024x768/175975039.jpg?k=a6e79350b9425673945744d2315561b0afcd5f9dc5d2021565d2b3d4301e51e8&o=&hp=1'
    st.markdown(f"""
        <div style='background-color: rgba(230, 245, 255, 0.9); border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;'>
            <h3 style='color: #1E3A8A; text-align: center; margin-bottom: 15px;'>{row['hotel']}</h3>
            <div style='display: flex; justify-content: center; margin-bottom: 15px;'>
                <img src='{image_url}' style='width: 100%; max-width: 400px; border-radius: 10px;' alt='Hotel Image'>
            </div>
            <p style='color: #1E3A8A;'><b>⭐ Rating:</b> <span style='color: black;'> {row['score']}</span></p>
            <p style='color: #1E3A8A;'><b>🗺️ Địa chỉ:</b> <span style='color: black;'>{row['address']}</span></p>
            <p style='color: #1E3A8A;'><b>💵 Giá:</b> <span style='color: black;'>{formatted_price} VND</span></p>
            <div style='text-align: center; margin-top: 20px;'>
                <a href='{row['url']}' target='_blank' style='text-decoration: none; background-color: #1E3A8A; color: white; padding: 12px 24px; border-radius: 5px; display: inline-block; text-align: center; transition: background-color 0.3s;'>Đặt phòng</a>
            </div>
        </div>
    """, unsafe_allow_html=True)


def main():
    # Load dữ liệu khách sạn từ file CSV
    df = pd.read_csv('E:\\hk7\\5.CMPM\\chay thu\\hotels_list.csv')

    # Tạo tiêu đề
    st.title("Khách sạn được đề xuất")
    st.write("Tìm kiếm khách sạn phù hợp với bạn.")

    # Bộ lọc
    st.sidebar.header("Bộ lọc tìm kiếm")
    
    with st.sidebar.form(key='search_form'):
        address = st.text_input("Nhập địa điểm:", "")
        price_range = st.selectbox("Chọn mức giá:", ["Mọi mức giá", "Nhỏ hơn 500.000 đ/ Đêm", "500-1tr đ/ Đêm", "Lớn hơn 1tr đ/ Đêm"])
        min_score = st.slider("Điểm đánh giá tối thiểu (thang điểm 10):", min_value=1, max_value=10, value=5)
        submit_button = st.form_submit_button("Tìm kiếm")
    
    # Tìm kiếm khách sạn
    if submit_button:  # Khi nhấn Enter hoặc nút "Tìm kiếm"
        recommended_hotels_df = recommend_hotels(df, address, price_range, min_score)
        if not recommended_hotels_df.empty:
            for _, row in recommended_hotels_df.iterrows():
                display_hotel_card(row)
        else:
            st.write("Không có khách sạn nào phù hợp với tiêu chí của bạn.")
    else:
        st.write("Vui lòng sử dụng bộ lọc để tìm kiếm khách sạn phù hợp.")

if __name__ == "__main__":
    main()
