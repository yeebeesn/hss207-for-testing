from PIL import Image, ImageDraw, ImageFont
import io
import math
import base64
from js import document
import pandas as pd

yearSelect = document.getElementById('yearSelect')
monthSelect = document.getElementById('monthSelect')
monthRange = document.getElementById('monthRange')
imageContainer = document.getElementById('subwayImageContainer')
stationInfo = document.getElementById('stationInfo')

def populate_years():
    years = [2012, 2013, 2014, 2015, 2016, 2018, 2019, 2020, 2021, 2022, 2023, 2024]
    for year in years:
        option = document.createElement('option')
        option.value = year
        option.textContent = year
        yearSelect.appendChild(option)

def update_months(*args):
    monthSelect.innerHTML = ''  # Clear previous options
    selectedYear = int(yearSelect.value)
    maxMonth = 4 if selectedYear == 2024 else 12
    monthRange.max = maxMonth  # Update range slider max value

    for month in range(1, maxMonth + 1):
        option = document.createElement('option')
        option.value = month
        option.textContent = month
        monthSelect.appendChild(option)

    if int(monthSelect.value) > maxMonth:
        monthSelect.value = maxMonth

    monthRange.value = monthSelect.value
file_path = "통합 문서1.xlsx"


station_coords = {'1호선':{'서울역':(1170,424), '시청':(1201,347), '종각':(1241,302), '종로3가':(1295,282), '종로5가':(1362,295), '동대문':(1408,293), '동묘앞':(1451,279), '신설동':(1501,257), '제기동':(1574,223), '청량리':(1641,220)}, '2호선':{'시청': (1201,347),'을지로입구':(1234,336),'을지로3가':(1303,333),'을지로4가':(1338,330),'동대문역사문화공원':(1396,349),'신당':(1454,341),'상왕십리':(1540,350),'왕십리':(1582,375),'한양대':(1632,420),'뚝섬':(1656,489),'성수':(1707,509),'건대입구':(1805,548),'구의':(1906,571),'강변':(1961,588),'잠실나루':(2020,705),'잠실':(2011,759),'잠실새내':(1911,779),'종합운동장':(1841,780),'삼성':(1757,801),'선릉':(1666,837),'역삼':(1584,869),'강남':(1527,890),'교대':(1438,925),'서초':(1399,940),'방배':(1334,1024),'사당':(1231,1065),'낙성대':(1113,1060),'서울대입구':(1044,1027),'봉천':(972,1016),'신림':(895,1002),'신대방':(790,975),'구로디지털단지':(713,995),'대림':(674,939),'신도림':(645,802),'문래':(670,727),'영등포구청':(680,678),'당산':(716,598),'합정':(790,473),'홍대입구':(871,399),'신촌':(941,424),'이대':(1002,411),'아현':(1066,405),'충정로':(1113,387),'용답':(1678,368),'신답':(1653,305),'용두':(1598,271),'신설동':(1501,257),'도림천':(591,756),'양천구청':(482,773),'신정네거리':(399,709)},'3호선':{'녹번':(935,52), '홍제':(989,150), '무악재':(1028,202), '독립문':(1077,267), '경복궁':(1179,255), '안국':(1256,250), '종로3가':(1295,282), '을지로3가':(1303,333), '충무로':(1313,374), '동대입구':(1386,393), '약수':(1419,427), '금호':(1452,480), '옥수':(1468,546),'압구정':(1534,659),'신사':(1476,742),'잠원':(1421,770),'고속터미널':(1382,835),'교대':(1438,925),'남부터미널':(1455,996),'양재':(1570,1000),'매봉':(1653,979),'도곡':(1707,949),'대치':(1760,918),'학여울':(1812,900),'대청':(1863,926),'일원':(1894,1002),'수서':(2007,977),'가락시장':(2116,934),'경찰병원':(2152,909),'오금':(2177,857)},'4호선':{'길음':(1510,32),'성신여대입구':(1456,118),'한성대입구':(1390,153),'혜화':(1362,204),'동대문':(1408,293),'동대문역사문화공원':(1396,349), '충무로':(1313,374), '명동':(1262,377),'회현':(1211,395), '서울역':(1170,424), '숙대입구':(1169,511),'삼각지':(1182,584),'신용산':(1143,636),'이촌':(1182,690),'동작':(1230,862),'총신대입구(이수)':(1233,994),'사당':(1231,1065)},'5호선':{'신정':(420,670),'목동':(474,661),'오목교':(543,674),'양평':(615,665),'영등포구청':(680,678),'영등포시장':(736,689),'신길':(813,732),'여의도':(859,698),'여의나루':(917,652),'마포':(1000,552),'공덕':(1034,515),'애오개':(1071,437),'충정로':(1113,387),'서대문':(1134,337),'광화문':(1198,290),'종로3가':(1295,282), '을지로4가':(1338,330), '동대문역사문화공원':(1396,349), '청구':(1438,383),'신금호':(1485,430),'행당':(1541,406),'왕십리':(1582,375),'마장':(1627,335),'답십리':(1688,327),'장한평':(1767,373),'군자':(1863,408),'아차산':(1928,450),'광나루':(2019,504),'천호':(2147,560),'강동':(2204,581),'길동':(2254,566),'굽은다리':(2274,503),'명일':(2280,456),'고덕':(2345,425),'상일동':(2422,412),'둔촌동':(2230,649),'올림픽공원':(2195,741),'방이':(2163,804),'오금':(2177,857),'개롱':(2222,890),'거여':(2279,928),'마천':(2337,914)},'6호선':{'역촌':(851,9),'응암':(804,71),'새절':(792,131),'증산':(767,190),'디지털미디어시티':(710,253),'월드컵경기장':(699,306),'마포구청':(726,357),'망원':(769,416),'합정':(790,473),'상수':(848,484),'광흥창':(910,486),'대흥':(977,485),'공덕':(1034,515),'효창공원앞':(1110,559),'삼각지':(1182,584),'녹사평':(1264,592),'이태원':(1314,592),'한강진':(1361,549),'버티고개':(1396,481),'약수':(1419,427),'청구':(1438,383),'신당':(1454,341),'동묘앞':(1451,279),'창신':(1448,227),'보문':(1475,178),'안암':(1538,170),'고려대':(1581,137),'월곡':(1618,42),'상월곡':(1665,4)},'7호선':{'중화': (1862,37), '상봉': (1901,85), '면목': (1915,150), '사가정': (1921,214), '용마산': (1911,272), '중곡': (1893,340), '군자': (1863,408), '어린이대공원': (1832,483), '건대입구': (1805,548), '뚝섬유원지': (1780,617), '청담': (1698,715), '강남구청': (1616,734), '학동': (1554,775), '논현': (1487,784), '반포': (1425,806), '고속터미널': (1382,835), '내방': (1308,975), '총신대입구': (1233,994), '남성': (1163,998), '숭실대입구': (1052,908), '상도': (1015,853), '장승배기': (956,834), '신대방삼거리': (885,876), '보라매': (836,874), '신풍': (765,873), '대림': (674,939), '남구로': (621,987), '가산디지털단지': (594,1032), '철산': (499,1067), '광명사거리': (412,1042), '천왕': (308,981),'온수': (206,937)},'8호선':{'암사': (2174,465), '천호': (2147,560), '강동구청': (2128,625), '몽촌토성': (2078,730), '잠실': (2011,759), '석촌': (2042,831), '송파': (2076,876), '가락시장': (2116,934), '문정': (2141,988), '장지': (2165,1047)},'9호선':{'언주':(1568,813),'선정릉':(1633,790),'삼성중앙':(1691,767),'봉은사':(1738,757),'종합운동장':(1841,780),'삼전':(1915,837),'석촌고분':(1977,854),'석촌': (2042,831),'송파나루':(2075,789),'한성백제':(2101,740),'올림픽공원':(2195,741),'둔촌오륜':(2247,716),'중앙보훈병원':(2309,639)}}

class Station:
    def __init__(self, name, line, location):
        self.name = name
        self.line = []
        self.line.append(line)
        self.ussage = 0
        self.location = location
        self.transfer = False
    def add(self, ussage):
        
        self.ussage = self.ussage+ussage
    def hierachy(self, line):
        self.transfer = True
        self.line.append(line)

def make_class():
    for line in station_coords:
        for station_name in station_coords[line]:
            if station_in_done_station(station_name):
                station = return_station(station_name)
                station.hierachy(line)
            else:
                new_station = Station(station_name,line,station_coords[line][station_name])
                done_stations.append(new_station)


def get_ussage(year, month):
    
    
    sheet_name = year + "승차"
    data = pd.read_excel(file_path, sheet_name=sheet_name)
    
    if int(year) ==2018 or int(year) >2020:
        a=2
    else:
        a=1
    for station in done_stations:
        station_name = [station.name]
        if station_name == '총신대입구(이수)':
            station_name.append('이수')
        for line in station.line:
            station_name.append(station.name+"("+line[0]+")")
            
        for i in range(1, len(data), 1):
            if data.iloc[i,0] in station_name:
                
                station.add(data.iloc[i,month+a])

def return_station(station_name):
    for station in done_stations:
        if station_name == station.name:
            
            return station
        
def station_in_done_station(station_name):
    for station in done_stations:
        if station_name == station.name:
            return True
    return False    

def check_line(line, last_station, station):
    if line == '5호선':
        if last_station == '상일동':
            return '강동'
        else:
            return last_station
    elif line == '2호선':
        if station == '도림천':
            return '신도림'
        elif station == '용답':
            return '성수'
        else:
            return last_station
    else:
        return last_station
        
def determine_color(line):
    if line == '1호선':
        color = 'navy'
    elif line == '2호선':
        color = 'green'
    elif line == '3호선':
        color = 'orange'
    elif line == '4호선':
        color = 'dodgerblue'
    elif line == '5호선':
        color = 'purple'
    elif line == '6호선':
        color = 'chocolate'
    elif line == '7호선':
        color = 'olive'
    elif line == '8호선':
        color = 'hotpink'
    elif line == '9호선':
        color = 'gold'
    return color 




def draw_river(drawmap):
    drawmap.line(((454,304),(764,544),(910,572),(1083,729),(1233,780),(1327,745),(1437,660),(1488,588),(1576,579),(1718,629),(1884,692),(1942,675),(2082,524),(2135,369),(2427,358)), fill = 'skyblue',width = 40)
    for cor in [(454,304),(764,544),(910,572),(1083,729),(1233,780),(1327,745),(1437,660),(1488,588),(1576,579),(1718,629),(1884,692),(1942,675),(2082,524),(2135,369),(2427,358)]:
        a, b = cor
        drawmap.ellipse((a-20,b-20,a+20,b+20), outline='skyblue',width=20)



def draw_line(line, drawmap):
    last_station = "없"
    color = determine_color(line)
    for station in station_coords[line]:
        a, b = station_coords[line][station]
        last_station = check_line(line,last_station,station)
        if not last_station == "없":
            last_station = check_line(line,last_station,station)
            drawmap.line((station_coords[line][last_station], station_coords[line][station]), fill=color,width=5)
            if station == '시청':
                drawmap.line(((1201,347), (1113,387)), fill='green',width=5)
        
        last_station = station






def draw_station(line, drawmap):
    color = determine_color(line)
    for station in station_coords[line]:
        a, b = station_coords[line][station]
        
        for station_done in done_stations:
            if station == station_done.name:
                ussage = station_done.ussage
                break
        #r = target_station_ussage
        r = round(math.sqrt(ussage)/20)
        
        drawmap.ellipse((a-r,b-r,a+r,b+r), outline=(255,0,0,255),width=1)
        new_station = Station(station, line, station_coords[line][station] )
        done_stations.append(new_station)

lines = ['1호선','2호선','3호선','4호선','5호선','6호선','7호선','8호선','9호선']
def generate_image(year, month):
    
    global done_stations
    done_stations = []
    make_class()
    get_ussage(year, month)
    map = Image.new('RGBA', (2427,1093), 'white')
    drawmap = ImageDraw.Draw(map)
    draw_river(drawmap)
    text_position = (200,100)
    
    for line in lines:
        draw_line(line, drawmap)
    
    for line in lines:
        draw_station(line, drawmap)


  
    # Save the image to a string in base64 format
    buf = io.BytesIO()
    image.save(buf, format='PNG')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    return img_str

def update_image(*args):
    selectedYear = yearSelect.value
    selectedMonth = int(monthSelect.value)
    img_str = generate_image(selectedYear, selectedMonth)
    
    imageContainer.innerHTML = f'<img src="data:image/png;base64,{img_str}" alt="Subway Usage {selectedYear}-{selectedMonth:02d}">'

def update_month_range(*args):
    selectedMonth = monthRange.value
    monthSelect.value = selectedMonth
    update_image()

# Populate years and set initial values
populate_years()
yearSelect.value = 2023  # Set default year
monthSelect.value = 1    # Set default month
update_image()

# Add event listeners
yearSelect.addEventListener('change', update_months)
yearSelect.addEventListener('change', update_image)
monthSelect.addEventListener('change', update_image)
monthRange.addEventListener('input', update_month_range)
