import streamlit as st 
import pandas as pd 
from classes.analytics.analytics_state import Analytics_state
from classes.analytics.analytics_data import Analytics_data
import pydeck as pdk
from snowflake.snowpark.context import get_active_session
from numpy.random import default_rng as rng

def analytics():
    analytics_state = Analytics_state() 
    analytics_state.setup_check()
    
    st.title('🔍 Analytics')
    
    if not analytics_state.setup_check_flg:
        st.warning("Setup is not Completed", icon="🚨")
        st.write("Go back to ⚙️SETUP Page and setup rest of the parameters")
        return
    else:
        analytics_data = Analytics_data()
        
    st.title("📈 Logistics Simulator")
    origin_country = analytics_state.get_value('origin_country')
    destination_country = analytics_state.get_value('destination_country')
        
    route_html = f"""
    <div style="
        display: flex; 
        align-items: center; 
        justify-content: space-around;
        width: 100%;
        gap: 15px; 
        font-family: sans-serif;
        margin: 20px auto;
    ">
        <div style="
            border: 2px solid #1E3A8A; 
            background-color: #F0FDF4; 
            padding: 10px 20px; 
            border-radius: 8px; 
            font-weight: bold; 
            font-size: 1.2rem;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
        ">
            {origin_country}
        </div>
    
        <div style="
            font-size: 1.8rem; 
            color: #4B5563;
            font-weight: bold;
        ">
            ➔
        </div>
    
        <div style="
            border: 2px solid #1E3A8A; 
            background-color: #EFF6FF; 
            padding: 10px 20px; 
            border-radius: 8px; 
            font-weight: bold; 
            font-size: 1.2rem;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
        ">
            {destination_country}
        </div>
    </div>
    """
    st.html(f"{route_html}")   

    with st.form("form_analytics_params"):
        st.subheader("Cost Factor")
        fuel_increase_param = st.slider("Fuel Cost Increasing Factor", 0.0, 5.0, 1.0,step=0.5, key='_fuel_increase_param')
        risk_avoidance_param = st.slider("Risk Avoidance Factor", 0.0, 5.0, 1.0, step=0.5, key='_risk_avoidance_param')
        weight_t = st.slider("Weight Of Cargo", 0, 100, 20, step=20, key='_weight_t')
        submitted = st.form_submit_button("Submit", key = 'f_analytics_params')
    if st.session_state['f_analytics_params']:
        analytics_state.store_value('fuel_increase_param')
        analytics_state.store_value('risk_avoidance_param')
        analytics_state.store_value('weight_t')


    tmp_df = pd.DataFrame({
        "Transport Mode": ["Airplane", "Airplane", "Airplane", "Ship"],
        "Cost(Money)": [123000, 123000, 123000, 123000],
        "Cost(Environment)": [4000, 4000, 4000, 4000],
        "Weather": ["Rain", "Fog", "Clear", "Hurricane"]
    })
    
    st.subheader("The Most efficient Transport")
    tmp_df = pd.DataFrame({
        "Transport Mode": ["AirPlane", "Ship", "Rail"],
        "Fixed Cost": [100, 200, 300],
        "Risk(Environment)": [200, 300, 200],
        "Total": [300, 500, 500],
    })
    
    
    st.bar_chart(data=tmp_df, x = "Transport Mode", y="Total", horizontal=True)
    
    a, b = st.columns(2)
    a.bar_chart(data=tmp_df, x = "Transport Mode", y="Fixed Cost", horizontal=True)
    b.bar_chart(data=tmp_df, x = "Transport Mode", y="Risk(Environment)", horizontal=True)
    
    
    st.dataframe(tmp_df)
    
    
    
    st.write("---")
    
    
    
    # changes = list(rng(4).standard_normal(20))
    # data = [sum(changes[:i]) for i in range(20)]
    # delta = round(data[-1], 2)
    
    
    # # --- 1. 状態（State）の初期化 ---
    # # 何もクリックされていない状態（None）、または "Late", "Cancel" を保持する
    # if "selected_detail" not in st.session_state:
    #     st.session_state.selected_detail = None
    
    # # (ユーザーの元コードのパラメータやマップ部分は省略)
    
    # # サンプル用の実績データ
    # tmp_df = pd.DataFrame({
    #     "DATE": ["2026-01-01", "2026-01-02", "2026-01-03", "2026-01-04"],
    #     "Transport":["Airplane", "Airplane", "Airplane", "Ship"],
    #     "Product": ["Electricity", "Food", "Electricity", "Food"],
    #     "Weight(mt)": [10, 200, 30, 100],
    #     "Status": ["On Time", "Late", "Late", "Cancelled"],  # フィルタ用に分かりやすく追加
    #     "ElapsedDate": ["+0", "+2", "+3", "-"],
    #     "Weather": ["Clear", "Hurricane", "Fog", "Clear"],
    #     "Cancelation": ["", "", "", "Suspend"],
    #     "CancelationFactor": ["", "", "", "Weather"],
    #     "Actual Cost(KUSD)": [100, 120, 110, 30],
    # })
    
    # st.subheader("Past metrics")
    # filter_list = ["3month", "6month", "1year", "3year"]
    # st.selectbox("DateRange", filter_list)
    
    # # メトリクスとボタンを縦に並べるためのコンテナ
    # row1 = st.columns(3)
    # delta = 0.5
    
    # with row1[0]:
    #     st.metric("BadWeather", 10, delta, border=True)
    #     # 必要に応じてここにもボタンを配置可能
    
    # with row1[1]:
    #     st.metric("Late", 2, delta, border=True)
    #     # トグルボタンの配置（クリックするたびに状態が切り替わる）
    #     if st.button("🔍 View Late Details", key="btn_late", use_container_width=True):
    #         if st.session_state.selected_detail == "Late":
    #             st.session_state.selected_detail = None  # 既に開いていたら閉じる
    #         else:
    #             st.session_state.selected_detail = "Late"
    
    # with row1[2]:
    #     st.metric("Cancel", 1, delta, border=True)
    #     if st.button("🔍 View Cancel Details", key="btn_cancel", use_container_width=True):
    #         if st.session_state.selected_detail == "Cancel":
    #             st.session_state.selected_detail = None  # 既に開いていたら閉じる
    #         else:
    #             st.session_state.selected_detail = "Cancel"
    
    # st.write("---")
    
    # # --- 2. 条件付きレンダリング（クリック時のみ表示） ---
    # if st.session_state.selected_detail == "Late":
    #     st.subheader("⚠️ Detailed Log: Late Shipments")
    #     # StatusがLateのデータのみをフィルタリング
    #     filtered_df = tmp_df[tmp_df["Status"] == "Late"]
    #     st.dataframe(filtered_df, use_container_width=True)
    
    # elif st.session_state.selected_detail == "Cancel":
    #     st.subheader("🚫 Detailed Log: Canceled Shipments")
    #     # CancelationがSuspendのデータのみをフィルタリング
    #     filtered_df = tmp_df[tmp_df["Cancelation"] == "Suspend"]
    #     st.dataframe(filtered_df, use_container_width=True)
    
    # tmp_df = pd.DataFrame({
    #     "DATE": ["2020-01-01", "2020-01-01", "2020-01-01", "2020-01-01"],
    #     "Transport":["Airplane", "Airplane", "Airplane", "Ship"],
    #     "Product": ["Electricity", "Food", "Electricity", "Food"],
    #     "Weight(mt)": ["10", "200", "30", "100"],
    #     "ElapsedDate": ["+3", "+2", "-1", "+3"],
    #     "Weather": ["Clear", "Hurricane", "Fog", "Clear"],
    #     "Cancelation": ["Suspend", "", "Suspend", ""],
    #     "CancelationFactor": ["Weather", "", "Weather", ""],
    #     "Actual Cost(KUSD)": ["100", "100", "20", "30"],
    #     "Report": ["URL", "URL", "URL", "URL"]
    # })
    
    # import pandas as pd
    # import pydeck as pdk
    # import streamlit as st
    
    # # 1. 1つの目的地に対して、輸送モード（mode）ごとにレコードを3つに分解
    # # ※ 同じ座標だと完全に重なるため、targetの緯度経度に微小な値（例: 1.0度）を足し引きして並走させます
    # route_data = [
    #     # --- 成田 (NRT) 行き ---
    #     {
    #         "destination": "成田 (NRT)",
    #         "source": [-73.7781, 40.6413],
    #         "target": [140.3929, 35.7720],  # Air (基準位置)
    #         "mode": "Air",
    #         "risk": "Low",  # 安全なので太い緑線になる
            
    #     },
    #     {
    #         "destination": "成田 (NRT)",
    #         "source": [-73.7781, 40.6413],
    #         "target": [
    #             140.3929 + 1.0,
    #             35.7720 - 1.0,
    #         ],  # Sea (少し右下にずらす)
    #         "mode": "Sea",
    #         "risk": "High",  # 危険なので細い赤線になる
    #     },
    #     {
    #         "destination": "成田 (NRT)",
    #         "source": [-73.7781, 40.6413],
    #         "target": [
    #             140.3929 - 1.0,
    #             35.7720 + 1.0,
    #         ],  # Rail (少し左上にずらす)
    #         "mode": "Rail",
    #         "risk": "Middle",  # 中間の太さのオレンジ線
    #     },
    #     # --- シンガポール (SIN) 行き ---
    #     {
    #         "destination": "シンガポール (SIN)",
    #         "source": [-73.7781, 40.6413],
    #         "target": [103.9915, 1.3502],  # Air
    #         "mode": "Air",
    #         "risk": "High",
    #     },
    #     {
    #         "destination": "シンガポール (SIN)",
    #         "source": [-73.7781, 40.6413],
    #         "target": [103.9915 + 1.0, 1.3502 - 1.0],  # Sea
    #         "mode": "Sea",
    #         "risk": "Low",
    #     },
    #     {
    #         "destination": "シンガポール (SIN)",
    #         "source": [-73.7781, 40.6413],
    #         "target": [103.9915 - 1.0, 1.3502 + 1.0],  # Rail
    #         "mode": "Rail",
    #         "risk": "Middle",
    #     },
    # ]
    
    # df = pd.DataFrame(route_data)
    
    
    # # 2. リスクに応じて色(RGB)を返す関数
    # def get_color_by_risk(risk):
    #     if risk == "Low":
    #         return [0, 255, 0, 200]  # 緑 (安全)
    #     elif risk == "Middle":
    #         return [255, 165, 0, 200]  # オレンジ
    #     elif risk == "High":
    #         return [255, 0, 0, 200]  # 赤 (危険)
    #     return [128, 128, 128, 200]
    
    
    # # 3. リスクに応じて線の太さを返す関数
    # # ※ 「健康なものは太く、リスクが高いものは細く」の要件に合わせて数値を調整
    # def get_width_by_risk(risk):
    #     if risk == "Low":
    #         return 2 # 安全ルートは「極太」で推奨
    #     elif risk == "Middle":
    #         return 2  # 通常
    #     elif risk == "High":
    #         return 2  # 危険ルートは「極細」で警告
    #     return 2
    
    
    # # データフレームにカラムを適用
    # df["color"] = df["risk"].apply(get_color_by_risk)
    # df["width"] = df["risk"].apply(get_width_by_risk)
    
    # # 4. ArcLayer の定義
    # layer = pdk.Layer(
    #     "ArcLayer",
    #     df,
    #     get_source_position="source",
    #     get_target_position="target",
    #     get_source_color="color",
    #     get_target_color="color",
    #     get_width="width",
    # )
    
    # # 5. 視点の設定
    # view_state = pdk.ViewState(latitude=30.0, longitude=180.0, zoom=1, pitch=40)
    
    # # 6. 目的地のドット描画
    # target_layer = pdk.Layer(
    #     "ScatterplotLayer",
    #     df,
    #     get_position="target",
    #     get_color="color",
    #     get_radius=200000,
    # )
    
    # # 7. マップの描画
    # st.pydeck_chart(
    #     pdk.Deck(
    #         layers=[layer, target_layer],
    #         initial_view_state=view_state,
    #         map_style=None,
    #     )
    # )