import streamlit as st
import json
import os
import gspread
from datetime import datetime
import pytz

# 環境変数からサービスアカウントのJSON情報を読み込む
gcp_service_account_info = json.loads(os.environ['GCP_SERVICE_ACCOUNT_JSON'])

# gspreadに認証情報を渡してクライアントを初期化
gc = gspread.service_account_from_dict(gcp_service_account_info)

# titleの表示
st.title('Wanna Wear Kimono?')

st.header('About Soraie Miyabi Kimono Service')
# 画像の表示
kimono_image = st.image("kimono_nine.png", caption="Kimono Image")
# 動画の表示
kimono_video = st.video("kimono_ig.mp4", format="video/mp4")

st.header('Q&A')

# 着付けについて
with st.expander("About Dressing"):
    st.markdown("""
    - **Can I receive dressing services even if I bring my own clothes or accessories?**
        - We do not provide dressing services for items brought in by customers.
    - **From what age are children's sizes available?**
        - Kimono experiences are available for children from 95cm to 140cm tall.
    - **Can pregnant women experience wearing a kimono?**
        - We regret to inform you that we do not offer kimono dressing services to pregnant customers.
    - **Is it okay to come empty-handed?**
        - Yes, it is. Kimonos, yukatas, dressing tools, and accessories can all be rented. If customers have any accessories or decorations they would like to add to their kimono, they are welcome to bring them, and we can assist with the dressing.
    - **Are hair ornaments available for rent?**
        - Yes, they are available for rent.
    - **How long does it take to change clothes?**
        - Typically, female customers require about 30 minutes, while male customers require about 10 minutes.
""")

# 返却について
with st.expander("About Returns"):
    st.markdown("""
    - **What should I do if rented kimonos or accessories get dirty or damaged?**
        - We will not charge compensation for removing stains or repairing damages that can be handled directly by our store. However, if stains cannot be removed immediately or if the item becomes unusable due to damage, compensation will be charged depending on the item.
    - **What should I do if I cannot return the items on time or if I want to borrow them until the next day?**
        - If you cannot return the items on time, a late fee of 3000 yen per person will be charged for every 30 minutes delayed. If you wish to return the items the next day, please inform the staff in advance, pay the extension fee of 1000 yen per person and the deposit, and you can return the items by 11 a.m. the next day.
""")

# レンタルについて
with st.expander("About Rentals"):
    st.markdown("""
    - **How long is the rental period?**
        - Usually from 9 a.m. to 5 p.m. Please check with the staff on the day as it may change depending on the situation.
    - **Until what time is reception available?**
        - Due to the impact of COVID-19, please return by 5 p.m. The final reception time is 3:30 p.m. Customers borrowing until the next day will be accepted until 5 p.m. If you have any other requests, please contact us in advance.
    - **Are there any special size considerations?**
        - Customers with hip sizes of less than 110cm are eligible. (For children, the height should be 95cm or above.)
    - **Can credit cards be used?**
        - Yes, various electronic money options in addition to credit cards are accepted.
    - **If I prepay or make a reservation and need to change plans, can I get a refund?**
        - Full refunds are possible up to 7 days before the reservation date, but not within 7 days. However, changes to the schedule are possible. Please contact us as soon as possible if you wish to cancel. Please note that cancellations and refunds are not possible once the schedule has been changed. (Up to two schedule changes only.)
""")

# 価格、場所について
with st.expander("Price / Location"):
    st.markdown("""
    - **How much is the cost?**
        - Usually it costs 8,000 yen per person (plus 10% Tax). It includes basic kimono options. You can add hair accessories options etc when you arrive at the store.
    - **Can credit cards be used?**
        - Yes, various electronic money options in addition to credit cards are accepted.
    - **If I prepay or make a reservation and need to change plans, can I get a refund?**
        - Full refunds are possible up to 7 days before the reservation date, but not within 7 days. However, changes to the schedule are possible. Please contact us as soon as possible if you wish to cancel. Please note that cancellations and refunds are not possible once the schedule has been changed. (Up to two schedule changes only.)
    - **Where should I go meet you on the reservation date?**
        - Primavera 2F, 2-20-8 Kaminarimon Taito-ku Tokyo
""")

# 予約フォーム
with st.form('Reservation Form'):
    st.header('Reservation Form')
    name = st.text_input('Name')
    address = st.text_input('Address')
    phone = st.text_input('Phone')
    email = st.text_input('Email')
    people_count = st.number_input('How many people', min_value=1)
    reservation_date = st.date_input('Reservation Date')
    
    # 予約時間の選択
    st.subheader('Reservation Time')
    reservation_time = st.selectbox('Select reservation time', options=[
        '9:00', '9:30', '10:00', '10:30',
        '11:00', '11:30', '12:00', '12:30',
        '13:00', '13:30', '14:00', '14:30',
        '15:00', '15:30', '16:00', '16:30'
    ])
    
    # 入力値のバリデーション
    all_fields_filled = name and address and phone and email
    today = datetime.now().date()
    valid_date = reservation_date >= today
    
    submitted = st.form_submit_button('SUBMIT')
    
    if submitted:
        if not all_fields_filled or not valid_date:
            if not all_fields_filled:
                st.error('Please fill in all the fields.')
            if not valid_date:
                st.error('Reservation Date must be today or later.')
        else:
            # 予約情報をスプレッドシートに記録
            # 以下のコードは、実際のGoogle Sheets APIの使用例です
            # 実際のアプリケーションでは、Google Sheets APIを設定し、認証を行う必要があります
            sh = gc.open("soraiekimono")
            worksheet = sh.sheet1
            worksheet.append_row([
                name, address, phone, email, str(people_count), 
                str(reservation_date), reservation_time
            ])
            st.success('NOT DONE YET! Please Pay below to Reserve your spot. Your spots will not be confirmed until payment is made.')
            
            # 送信後に表示されるリンク(https://buy.stripe.com/7sIeWWbmA0oy6SQfZd)
            st.markdown('Please [CLICK HERE](https://buy.stripe.com/7sIeWWbmA0oy6SQfZd) to make a payment. (Our staff will contact you after your payment.)')