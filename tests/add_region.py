import cpca


def add_region_msg():
    import pandas as pd
    import pymysql as mysql

    csv = pd.read_csv("E:\\python-work\\chinese_province_city_area_mapper\\cpca\\resources\\pca.csv")

    res = csv.tail(5000)
    frame = pd.DataFrame(res)
    frame.itertuples()
    a = []
    db = mysql.connect("localhost", "root", "757671834", "spider")
    cursor = db.cursor()
    # country,sheng,shi,qu,lat,lng
    for row in frame.itertuples():
        country = getattr(row, 'country')
        province = getattr(row, 'sheng')
        city = getattr(row, 'shi')
        county = getattr(row, 'qu')
        x = getattr(row, 'lat')
        y = getattr(row, 'lng')
        region = getattr(row, 'region')
        print(country, province, city, county, x, y, region)
        if city != None:
            sql = "select address_geoid from ipregion where address_detail ='{}'".format(city)
            print(sql)
            cursor.execute(sql)
            ip = cursor.fetchone()
            if ip is not None and len(ip) > 0:
                print(ip[0])
                ip = ip[0]
            a.append(
                {"country": country, "province": province, "city": city, "county": county, "x": x, "y": y,
                 "region": ip})
    result = pd.DataFrame(a)
    result.to_csv("ip.csv", index=False, columns=["country", "province", "city", "county", "x", "y", "region"])


def test_region():
    location_str = ["厦门市湖里区"]
    df = cpca.transform(location_str, need_region_code=True)
    print(df)


if __name__ == '__main__':
    test_region()
