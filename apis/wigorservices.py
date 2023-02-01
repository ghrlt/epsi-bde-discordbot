import requests
import bs4

class WigorServices:
    logged_url = "https://ws-edt-cd.wigorservices.net/WebPsDyn.aspx"
    unlogged_url = "https://edtmobiliteng.wigorservices.net/WebPsDyn.aspx"

    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"

    class ClassObject:
        def __init__(self):
            pass

    class UnableToLogin(Exception):
        pass
    class CurrentlyOnHoliday(Exception):
        pass
    class InvalidToken(Exception):
        pass

    def __init__(self):
        self.s = requests.Session()
        self.s.headers['User-Agent'] = self.user_agent

    def login(self, username: str, password: str=None):
        if not password:
            self.usingLoggedVersion = False
            self.url = self.unlogged_url

            self.username = username

            self.s.params.update({
                "action": "posEDTBEECOME",
                "serverid": "C",
                "Tel": self.username
            })

        else:
            self.usingLoggedVersion = True
            self.url = self.logged_url

            self.username = username
            self.password = password

            self.s.params.update({
                "action": "posEDTLMS",
                "serverID": "C",
                "Tel": self.username
            })

            r = self.s.get(
                "https://cas-p.wigorservices.net/cas/login",
                params={"service": "https://ws-edt-cd.wigorservices.net/WebPsDyn.aspx"}
            )
            rSoup = bs4.BeautifulSoup(r.content, "html.parser")
            executionToken = rSoup.find('input', {"name": "execution"}).get('value')

            r = self.s.post(
                "https://cas-p.wigorservices.net/cas/login",
                params={"service": "https://ws-edt-cd.wigorservices.net/WebPsDyn.aspx"}, #In order for wigor to identify your school
                headers={
                    "Accept": "text/html",
                    "Content-Type": "application/x-www-form-urlencoded",
                    **self.s.headers
                },
                data={
                    "username": username,
                    "password": password,
                    "execution": executionToken,
                    "_eventId": "submit",
                    "geolocation": "" 
                }
            )

            if r.status_code == 200:
                return True

            raise self.UnableToLogin(self.getLoginErrMsg(r))

    def getLoginErrMsg(self, req: requests.Request):
        html = bs4.BeautifulSoup(req.content, "html.parser")
        err = html.find('div', id='loginErrorsPanel')

        return err.text.strip()


    def fetch(self, date: str):
        self.s.params.update({
            "date": date
        })
        r = self.s.get(self.url)

        return r.content

    def parse(self, htmlpage: str):
        soup = bs4.BeautifulSoup(htmlpage, 'html.parser')

        allClasses = soup.find_all('div', class_='Case')
        classOrdered = {}

        for _class in allClasses:
            if _class.text == "Pas de cours cette semaine": #holiday
                raise self.CurrentlyOnHoliday("No classes this week")

            if _class.get('id') == 'After': continue

            _classStyle = _class['style'].split(';')
            classStyle = {i.split(':')[0]: i.split(':')[-1] for i in _classStyle}

            if not classStyle.get('left').split('.')[0] in classOrdered:
                classOrdered[classStyle.get('left').split('.')[0]] = []

            classOrdered[classStyle.get('left').split('.')[0]].append(_class)

        allDays = soup.find_all('div', class_='Jour')
        daysOrdered = {}

        for day in allDays:
            _dayStyle = day['style'].split(';')
            dayStyle = {i.split(':')[0]: i.split(':')[-1] for i in _dayStyle}

            daysOrdered[dayStyle.get('left').split('.')[0]] = day.text

        classes = {i: [] for i in daysOrdered.values()}

        for key, value in classOrdered.items():
            if key in daysOrdered:
                for _class in value:
                    classes[daysOrdered[key]].append(_class)

        return classes

    def parseClass(self, _class):
        classObj = self.ClassObject()

        classObj.informations = _class.find('td', class_='TCProf').text

        classObj.startTime = _class.find('td', class_='TChdeb').text.split('-')[0].strip()
        classObj.endTime = _class.find('td', class_='TChdeb').text.split('-')[1].strip()

        br = _class.find('td', class_='TCProf').find('br')
        if br:
            if isinstance(br.previousSibling, bs4.element.NavigableString):
                professor = br.previousSibling.title().split()
                professor.reverse()
                classObj.professor = ' '.join(professor)
            else:
                classObj.professor = 'None'
        else:
            classObj.professor = 'You'


        if _class.find('td', class_='TCSalle').text == "Salle:Aucune":
            classObj.place = ""
            classObj.room = ""
        else:
            classObj.place = _class.find('td', class_='TCSalle').text.split('(')[1].strip(')')
            classObj.room = _class.find('td', class_='TCSalle').text.split('(')[0].split(':')[1].strip('.')

            if classObj.place == "Apothicair":
                classObj.place = "Apothicaire"
                classObj.room = classObj.room[1:]

            elif classObj.place == "PISE & SIE":
                if classObj.room.startswith('P'):
                    classObj.place = "PISE"
                elif classObj.room.startswith('S'):
                    classObj.place = "SIENNE"

            elif classObj.place == "DISTANCIEL":
                classObj.place = "Distanciel"
                classObj.room = ''

            if classObj.room:
                for i in classObj.room:
                    if not i.isdigit():
                        classObj.room = classObj.room.replace(i, '')
                classObj.room = str(int(classObj.room)) # Strip the leading 0

        
        rawSubject = _class.find('td', class_='TCase').text or '???'
        if rawSubject.split()[-1] == classObj.room and rawSubject.split()[-2].startswith(classObj.place):
            classObj.fullSubject = ' '.join(rawSubject.split()[:-2])
        else:
            classObj.fullSubject = rawSubject

        classObj.fullSubject = ' '.join([w.title() if w.islower() else w for w in classObj.fullSubject.split()])

        classObj.subject = classObj.fullSubject.split('-')
        if len(classObj.subject) > 1:
            classObj.subject = '-'.join(classObj.subject[1:]).strip()
        else:
            classObj.subject = classObj.subject[0]


        classObj.isAutonomie = classObj.fullSubject != classObj.subject

        classObj.teamsLink = _class.find('td', class_='TCase').find('div', class_='Teams')
        if classObj.teamsLink:
            if classObj.teamsLink.find('a'):
                classObj.teamsLink = classObj.teamsLink.find('a').get('href')



        return classObj

    def fetchAndParse(self, date: str, toJson: bool=False):
        _parsed =  self.parse(self.fetch(date))
        parsed = {day: [] for day in _parsed.keys()}

        for day, classes in _parsed.items():
            for _class in classes:
                if toJson:
                    parsed[day].append(self.parseClass(_class).__dict__)
                else:
                    parsed[day].append(self.parseClass(_class))

        return parsed

