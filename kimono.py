import streamlit as st
import json
import os
import gspread

# 環境変数からサービスアカウント情報を取得
gcp_service_account_info = json.loads(os.environ['GCP_SERVICE_ACCOUNT_JSON'])
# gspreadの認証
gc = gspread.service_account_info(gcp_service_account_info)


# titleの表示
st.title('Wanna Wear Kimono?')

st.header('About Soraie Miyabi Kimono Service')
# 画像の表示
kimono_image = st.image("kimono_nine.png", caption="Kimono Image")
# 動画の表示
kimono_video = st.video("kimono_ig.webm", format="video/webm")

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
    - **Other Notes**
        - Can you store clothes or belongings?
            - Yes, we offer free luggage storage, so please feel free to ask. We can also store large items. However, please store valuables such as accessories and bags yourself, as we cannot take responsibility for any loss or damage.
        - Are there any special considerations for wearing kimonos in winter?
            - In winter, customers can wear their own Heattech (except for turtlenecks) during the experience. However, please refrain from wearing tights that cover the feet as tabi socks need to be worn.
    """)

# 価格、場所について
with st.expander("Price / Location"):
    st.markdown("""
    - **How much is the cost?**
        - Usually it costs 8,000 yen per person. You need 3000 yen to reserve your spot and pay the remaining as you choose your option at the store.**    
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
    
    submit_button = st.form_submit_button('Submit & Pay to Reserve')

# Googleスプレッドシートへの書き込み
if submit_button:
    gc = gspread.service_account(filename=r'C:\Users\ume27\my_app_kimono\kimono-2843949effac.json')
    sheet = gc.open('soraiekimono').sheet1
    sheet.append_row([name, address, phone, email, people_count, reservation_date.strftime('%Y-%m-%d'), reservation_time])
    st.success('Reservation submitted successfully!')
