import streamlit as st
import pickle
import pandas as pd
import sklearn
import time
from model import final_model
model = final_model

    
def setup_quesion(title='title'):
    value = st.radio(title,['無','有'], horizontal=True, key=title)
    if value == '無':
        value = 0
    else:
        value = 1 
    return value

def predict():
    features = pd.DataFrame({
    '是否有高血壓':[high_blood_pressure],
    '是否有高血脂':[high_blood_oil], 
    '是否有糖尿病':[high_blood_sugar], 
    '是否有骨質疏鬆症':[bone_lack], 
    '是否有肝臟疾病':[liver_problem],  
    '是否有子宮卵巢疾病':[womon_proble],
    '是否關節疼痛':[joint_pain], 
    '是否下背部疼痛或腰痛':[back_pain], 
    '是否坐骨神經痛':[sit_pain], 
    '是否頭痛或偏頭痛':[head_pain], 
    '是否痛風':[gout], 
    '是否使用慢性處方籤':[longterm_drug],
    '是否曾吸菸':[smoke], 
    '年齡':[age]})
    result = model.predict(features)[0]
    prob = model.predict_proba(features)[:,1][0]
    if result:
        st.error(f'預測為可能有慢性腎臟病，患病機率:{prob:.0%}，表示您對於上述危險因子具有高度曝險，但不一定有患病，建議您到醫院做進一步檢查')
        hospital(region)
        health_info()
    else:
        st.success(f'預測為健康狀態，健康機率:{1-prob:.0%}')
        health_info()
            
def health_info():
    st.warning('衛教資訊(有效預防與延緩慢性腎臟病)')
    st.text(
    """
    1.運動：
    (1)有氧運動：一周3~5天，一天20~60分鐘，如游泳、騎腳踏車、走路
    (2)阻力運動：一周2~3天，一組10~15反覆，要練習到8~10種肌群，如彈力帶、機器
    
    2.飲食：
    (1)注意鈉、蛋白、脂肪含量。選擇低飽和脂肪，反式脂肪，膽固醇，鹽(鈉)和添加糖的食物
    (2)避免醃漬類食品、避免罐頭、冷凍食品等加工食品
    (3)不吃高鹽高脂速食如漢堡、炸雞、鹹酥雞、披薩、泡麵、火鍋、滷味
    (4)每天飲食限鹽少於2,300毫克
    (5)限蛋白飲食
    (6)低鉀、低磷飲食(大部分包裝食品或飲料都含有磷)
    
    *推薦甜品選擇：愛玉、仙草、粉粿等食用前添加少量蜂蜜；果凍、粉圓、西谷米、涼圓
    
    *推薦食物選擇：炒冬粉、水晶餃、地瓜
    
    *小心高磷食物：麵筋、毛豆、蠶豆、花生、杏仁、巧克力、碳酸飲料、奶製品
    
    *小心高鉀食物：低鈉或薄鹽醬油 (因減少的鈉會由鉀代替，鉀易過高)、高湯、果汁、香蕉、香瓜
                 榴槤，奇異果、草莓、柑橘、咖啡、茶、運動飲料、堅果類、巧克力、梅子汁、蕃茄醬
                 九層塔、木耳、菠菜、空心菜、海帶
    
    *小心高鈉食物：各種醃製食品，如：醬菜、豆腐乳、肉鬆、麵線、鹽、味增、沙茶醬、烏醋、蕃茄醬
                 豆瓣醬等調味料，蘇打餅乾、培根、熱狗、香腸、芹菜、菠菜、罐頭食品、汽水
    """)

def hospital(region):
    lookup_table = {
        '基隆市':[('基隆長庚','https://www.cgmh.org.tw/tw/Services/DeptInfo/2/21000/21500'),
                 ('基隆醫院', 'https://www.kln.mohw.gov.tw/?aid=51&pid=114')],
        '台北市':[('台北醫院', 'https://www.tph.mohw.gov.tw/?aid=51&pid=7'),
                 ('台北馬偕', 'https://www.mmh.org.tw/departmain.php?id=4')],
        '新北市':[('土城醫院', 'https://www.cgmh.org.tw/tw/Services/DeptInfo/V/V1000/V1500'),
                 ('亞東醫院', 'https://www.femh.org.tw/doctor/doctor?t=2')],
        '桃園市':[('桃園榮總', 'https://www.tyvh.gov.tw/team/'),
                 ('桃園醫院', 'https://www.tygh.mohw.gov.tw/?aid=51&pid=132')],
        '新竹縣':[('台大醫院新竹分院', 'https://www.hch.gov.tw/?aid=51&pid=8'),
                 ('中國醫藥大學新竹附設醫院', 'https://www.cmu-hch.cmu.edu.tw/Doctor/Department?detail=7&current=1&source=dep')],
        '新竹市':[('新竹馬偕', 'https://www.hc.mmh.org.tw/departmain.php?depid=4#staff'),
                 ('國軍桃園總醫院新竹分院', 'https://813.mnd.gov.tw/department/sn5/')],
        '苗栗縣':[('苗栗醫院', 'https://www.mil.mohw.gov.tw/?aid=51&pid=51')],
        '台中市':[('台中榮總','https://www.vghtc.gov.tw/APIPage/DoctorInfoList?WebMenuID=dc264319-1d78-4ad8-a7ba-647440dbad6b&SECTION_ID=NEPH&SECTION=%E8%85%8E%E8%87%9F%E7%97%85%E7%A7%91'),
                 ('台中慈濟醫院','https://taichungsub.tzuchi.com.tw/12/doctors')],
        '彰化縣':[('彰化基督教醫院', 'https://www.cch.org.tw/NEPHRO/'),
                 ('彰化醫院', 'https://www.chhw.mohw.gov.tw/?aid=51&pid=31')],
        '雲林縣':[('台大醫院雲林分院', 'https://www.ylh.gov.tw/?aid=51&pid=35'),
                 ('雲林基督教醫院', 'https://yl.cch.org.tw/doctor_1_detial.aspx?cID=74&key=0105')],
        '嘉義縣':[('朴子醫院', 'https://www.puzih.mohw.gov.tw/?aid=51&pid=41&page_name=list&pageNo=2'),
                 ('嘉義長庚', 'https://www.cgmh.org.tw/tw/Systems/AreaInfo/9')],
        '嘉義市':[('嘉義醫院', 'https://www.chyi.mohw.gov.tw/list.asp?orcaid={850945D1-5D12-4D84-AE32-8C8B0E26D923}'),
                 ('台中榮總嘉義分院', 'https://www.vhcy.gov.tw/PageView/RowView?WebMenuID=25cadfcc-5a2d-4b5b-a1b5-eb11cbb21f7b')],
        '台南市':[('台南醫院', 'https://www.tnhosp.mohw.gov.tw/list.asp?orcaid={850945D1-5D12-4D84-AE32-8C8B0E26D923}'),
                 ('奇美醫院', 'http://sub.chimei.org.tw/57340/index.php/members/')],
        '高雄市':[('高雄醫學大學附設醫院', 'https://www.kmuh.org.tw/KMUHInterWeb/InterWeb/InnerPage/1001124056'),
                 ('高雄榮總', 'https://org.vghks.gov.tw/neph/')],
        '屏東縣':[('屏東醫院', 'https://www.pntn.mohw.gov.tw/?aid=51&pid=90'),
                 ('屏東榮總', 'https://org.ptvgh.gov.tw/nephro/')],
        '南投縣':[('竹山秀傳醫院', 'https://www.csshow.org.tw/new_cssummary/cssummary_04_01_08.asp'),
                 ('南投醫院', 'https://www.nant.mohw.gov.tw/?aid=51&pid=63')],
        '宜蘭縣':[('陽明交通大學附設醫院', 'https://www.hosp.nycu.edu.tw/departments/health-care/internal/kidney/member.html'),
                 ('羅東博愛醫院', 'https://www.pohai.org.tw/doctor.php?Class1=7&Class2=17&Sort=2#sidebar_2')],
        
        '花蓮縣':[('花蓮醫院', 'https://webreg.hwln.mohw.gov.tw/OINetReg.WebRwd/Reg/Dept'),
                 ('花蓮慈濟醫院', 'https://hlm.tzuchi.com.tw/neph/')],
        '台東縣':[('台東醫院', 'https://www.tait.mohw.gov.tw/?aid=51&pid=41&page_name=detail&iid=659'),
                 ('台東馬偕', 'https://ttw3.mmh.org.tw/departmain.php?id=4')],
        '金門縣':[('金門醫院', 'https://netreg.kmhp.mohw.gov.tw/OINetReg.WebRwd/')],
        '澎湖縣':[('三軍總醫院澎湖分院', 'https://wwwv.tsgh.ndmctsgh.edu.tw/Docdetaillist/195/40123/25218'),
                 ('澎湖醫院', 'https://www.pngh.mohw.gov.tw/?aid=51&pid=41')],
        '連江縣':[('連江縣立醫院', 'https://ljc.matsuh.gov.tw/OINetReg/OINetReg.Reg/Reg_NetReg.aspx')]}

    data = lookup_table[region]
    st.info('在您地區提供腎臟檢查之醫院')
    for i, (name, ref) in enumerate(data,1):
        st.markdown(f"{i}. [{name}]({ref})")


# app section
st.title('問卷快篩')
st.caption('本預測模型是由「腎敗難免」團隊利用衛生福利部國民健康署 \
           (前身：衛生署國民健康局) 於民國 91 年所施行的「台灣地區國民健康促進知識、態度與行為調查」作為原始資料進行機器學習訓練而得\
            ，預測結果僅為參考仍應以醫師診斷結果為主，模型表現數據如下：')

with st.expander("查看更多關於模型表現"):
    st.text("""
            原始資料經整理後共有 11283 個有效樣本，其中患有腎臟病者為 494 人，佔有效樣本數 4%
            團隊將資料進行 8:2 切割分成訓練集與驗證集，以下數據為模型訓練完成後在驗證集的表現
            (採 bootstrap 法建構之 95% 信賴區間)
            Accuracy(整體預測正確率): [0.7356, 0.7398]
            Sensitivity(實際有病者中預測為有病比率): [0.5756, 0.6267]
            Specificity(實際沒病者中預測為沒病比率): [0.7420, 0.7461]
            """)

with st.expander("查看更多認識慢性腎臟病"):
    st.text("""
疾病簡介

腎臟組織因疾病遭受無法恢復的損壞時，腎功能就會逐漸衰退，當腎臟組織長期受損達三個月以上
無法恢復原有的功能，稱為慢性腎臟病

腎臟功能：

1. 形成尿液，排除水分
2. 調節血壓
3. 排泄體內代謝後的廢物
4. 維持人體內水分與電解質及酸鹼度的平衡
5. 製造紅血球生成素，刺激紅血球的生長和成熟，維持血色素的濃度
6. 產生活性維生素D，調節鈣與磷的代謝
7. 腎臟與內分泌有關，假如腎臟損傷也會出現內分泌失調
8. 慢性腎臟病早期常常沒有明顯的症狀，等到發現時已經有相當程度的受損

以下為慢性腎臟病的十大高危險群：

1. 糖尿病患者：長期高血糖會造成腎臟病變及血管病變
2. 高血壓患者：血壓控制不好會影響腎臟血管及腎絲球硬化
3. 心血管疾病患者：心臟衰竭容易導致腎功能惡化
4. 蛋白尿患者：蛋白尿的出現已屬於慢性腎臟病且是心血管疾病的危險因子
5. 痛風患者：血液尿酸濃度過高時，尿酸會沉積在腎組織影響腎功能
6. 65歲以上老年人：老年人身體器官隨年齡增加而退化，容易合併腎功能退化
7. 長期服用藥物患者
8. 有腎臟病家族史：家族中有多囊性腎病變、遺傳性腎炎及透析患者
9. 抽菸者：抽菸會刺激交感神經，升高血壓造成腎臟負擔而影響腎功能
10.代謝症候群的病人：男生腰圍＞35吋(90公分)，女生腰圍＞31吋(80公分)

慢性腎臟疾病分期：

第一期：腎功能正常併有尿液或影像學檢查的異常；腎絲球過濾率(GFR)≧90mL/min/1.73㎡
第二期：輕度腎功能損傷併有尿液或影像學檢查的異常；腎絲球過濾率(GFR)60-89mL/min/1.73㎡
第三期：中度腎功能損傷；腎絲球過濾率(GFR)30-59 mL/min/1.73㎡
第四期：重度腎功能損傷；腎絲球過濾率(GFR)15-29 mL/min/1.73㎡
第五期：末期腎衰竭；腎絲球過濾率(GFR)＜15mL/min/1.73㎡

慢性腎臟病早期的症狀是：泡、水、高、貧、倦
1. 泡：小便有泡「泡」
2. 水：「水」腫
3. 高：「高」血壓
4. 貧：「貧」血
5. 倦：「倦」怠

慢性腎臟病常見症狀：

1. 水腫：腎臟病人最常見的臨床症狀就是水腫，常出現於眼瞼、踝部、後背。水腫時均伴有尿少及體重增加
2. 高血壓：腎臟病人就醫時應注意檢查血壓，血壓升高常是病情加重的表現
3. 尿頻、尿急、尿痛。尿頻（次數多，每次尿一點）、急（憋不住尿）、痛（排尿時小腹疼痛、有下墜感），總稱為”尿路刺激症”是膀胱疾病的表現，常見於膀胱炎
4. 腰痛：間斷發作的劇烈腰痛，常沿側腹部向會陰部放射，伴嘔吐。常見於腎盂、輸尿管結石
5. 少尿或無尿：尿量每天少於400毫升叫做少尿，少於100毫升的叫無尿，此時腎臟已不能從尿液中排出代謝物，無法調節水和其他內在環境的穩定和平衡
6. 多尿：每天尿量大於2500毫升的稱為多尿。同時應注意夜尿（入睡至起床間的尿量）與晝尿的比例（正常為1:2或1:3）
7. 血尿：血尿可能是嚴重疾病的信號，應及時就診查明原因，做出適當的處理
8. 尿中泡沫增多：可能是尿中出現大量蛋白的表現，應及時作尿液檢查
9. 其他：原因不明的食慾不振、乏力、貧血等，也可能是腎臟疾症引起的
            """)
st.write("---")

st.markdown('#### 以下共有十五題，請依實際狀況回答')
st.markdown('##### 居住地與年齡')

region = st.selectbox('您目前居住在哪裡',
                      ['基隆市','台北市','新北市','桃園市','新竹縣','新竹市','苗栗縣','台中市',
                       '彰化縣','雲林縣','嘉義縣','嘉義市','台南市','高雄市','屏東縣','南投縣'
                       '宜蘭縣','花蓮縣','台東縣','金門縣','澎湖縣','連江縣'])
age = st.number_input('您目前的年齡',
                      min_value=1,max_value=100,value=80)

st.markdown('##### 三高病史 (須為經醫師診斷)')
high_blood_pressure = setup_quesion('您是否有高血壓')
high_blood_sugar = setup_quesion('您是否有糖尿病')
high_blood_oil = setup_quesion('您是否有高血脂')

st.markdown('##### 其他疾病 (須為經醫師診斷)')
bone_lack = setup_quesion('您是否有骨質疏鬆')
liver_problem = setup_quesion('您是否有肝臟疾病')
gout = setup_quesion('您是否有痛風')
womon_proble = setup_quesion('您是否有子宮卵巢疾病(男性填無)')


st.markdown('##### 身體不適 (自我評估)')
joint_pain = setup_quesion('您是否關節疼痛')
back_pain = setup_quesion('您是否有下背部疼痛或是腰痛')
sit_pain = setup_quesion('您是否有坐骨神經痛')
head_pain = setup_quesion('您是否有頭痛或偏頭痛')

st.markdown('##### 其他')
longterm_drug = setup_quesion('您是否有使用慢性處方籤')
smoke = setup_quesion('您是否有或有過長期吸菸的經驗')


pred = st.button('Predict')
if pred:
    my_bar = st.progress(0)
    time.sleep(0.1)
    for i in range(0,100, 10):
        if i < 5:
            time.sleep(0.1)
        elif i < 8:
            time.sleep(0.03)
        else:
            time.sleep(0.01)
        my_bar.progress(i + 10)
    time.sleep(0.01)
    result = predict()

