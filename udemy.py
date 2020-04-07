import requests, urllib, json
from bs4 import BeautifulSoup


def coupon_data():
    sorgu = "inurl:udemy.com/course/ \"inurl:couponCode site:udemy.com"
    # Bu kısımda Google'da arama yapıyoruz.
    tbs = "d" 
    URL = f"https://google.com/search?q={sorgu}&tbs=qdr:{tbs}"


    # Sanal tarayıcı oluşturuyoruz.
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
    ACCEPT_ENCODING = "gzip, deflate, br"

    headers = { 'User-Agent' : USER_AGENT, 'Content-Type': "text/plain" }

    resp = requests.get(URL, headers=headers)
    try:
        #Bağlantı sorunsuz olursa yani dönüş kodumuz 200 olursa BeatufiulSoup ile sayfayı parçalıyoruz.
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, "html.parser")

        link, title, coupon = [], [], []
        for g in soup.find_all('div', class_='r'):
            anchors = g.find_all('a')
            if anchors:
                title.append(g.find('h3').text)
                link.append(anchors[0]['href'])
                coupon.append((anchors[0]['href']).partition("?couponCode=")[2]) 

        results = [{"Title": t, "Link": l, "Coupon": c} for t, l, c in zip(title, link, coupon)]

        data_list = []

        for i in range(len(results)): 
            resp = requests.get(results[i]["Link"], headers=headers)

            if resp.status_code == 200:
                course_code = BeautifulSoup(resp.content, "html.parser").body['data-clp-course-id']
                
                CodeCheck_URL = f"https://www.udemy.com/api-2.0/course-landing-components/{course_code}/me/?components=buy_button,purchase,redeem_coupon,discount_expiration,gift_this_course&discountCode="+results[i]["Coupon"]
                resp = requests.request("GET",CodeCheck_URL, headers=headers).json()
                

                # Kuponları listeye ekliyoruz.
                if (resp)["purchase"]["data"]["pricing_result"]["price"]["amount"] == 0:
                    course_list = []
                    course_list.append(results[i]["Title"])
                    course_list.append(results[i]["Link"])
                    course_list.append(results[i]["Coupon"])
                    course_list.append(resp["purchase"]["data"]["pricing_result"]["campaign"]["uses_remaining"])
                    course_list.append(resp["purchase"]["data"]["pricing_result"]["campaign"]["end_time"][:-9])
                    data_list.append(course_list)

        return data_list
    except KeyError:
        pass