from flask.views import MethodView
import requests
import re


class LolSkinView(MethodView):
    """换肤大师接口"""

    def get(self):
        url = 'https://lol.qq.com/act/AutoCMS/publish/LOLWeb/OfficialWebsite/website_cfg.js?v='
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        }
        try:
            request = requests.get(url=url, headers=headers)
            ver = re.search('Ver \d+.\d+', request.text).group()

            url2 = 'http://skin.lolhfds.com/a/chajian/4.html'
            request = requests.get(url=url2, headers=headers)
            date = re.search('\d+-\d+-\d+', request.text).group()
        except Exception as e:
            return {"code": 500, "msg": "换肤大师服务器异常"}
        data = {"lol_ver": ver, "lolskin_date": date, "lolskin_url": "http://down3.lolhfds.com/LolCallSkin.7z"}
        return {"code": 200, "data": data}
