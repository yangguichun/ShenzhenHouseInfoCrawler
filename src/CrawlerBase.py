
class CrawlerBase:
    form_data = {'ctl00$ContentPlaceHolder1$scriptManager1': '',
                   '__EVENTTARGET': '',
                   '__EVENTARGUMENT': '',
                   '__LASTFOCUS': '',
                   '__VIEWSTATE': '',
                   '__VIEWSTATEGENERATOR': '',
                   '__VIEWSTATEENCRYPTED': '',
                   '__EVENTVALIDATION': '',
                   'ctl00$ContentPlaceHolder1$radSelect': 0}

    areas = {'全市': {'ctl00$ContentPlaceHolder1$scriptManager1': '',
                     '__EVENTTARGET': ''},
              '宝安':
                  {
                      'ctl00$ContentPlaceHolder1$scriptManager1': 'ctl00$ContentPlaceHolder1$updatepanel1|ctl00$ContentPlaceHolder1$hypBa',
                      '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$hypBa'},
              '福田':
                  {
                      'ctl00$ContentPlaceHolder1$scriptManager1': 'ctl00$ContentPlaceHolder1$updatepanel1|ctl00$ContentPlaceHolder1$hypFt',
                      '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$hypFt'},
             '龙岗':
                  {
                      'ctl00$ContentPlaceHolder1$scriptManager1': 'ctl00$ContentPlaceHolder1$updatepanel1|ctl00$ContentPlaceHolder1$hypLg',
                      '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$hypLg'},
             '罗湖':
                  {
                      'ctl00$ContentPlaceHolder1$scriptManager1': 'ctl00$ContentPlaceHolder1$updatepanel1|ctl00$ContentPlaceHolder1$hypLh',
                      '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$hypLh'},
             '南山':
                  {
                      'ctl00$ContentPlaceHolder1$scriptManager1': 'ctl00$ContentPlaceHolder1$updatepanel1|ctl00$ContentPlaceHolder1$hypNs',
                      '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$hypNs'},
             '盐田':
                  {
                      'ctl00$ContentPlaceHolder1$scriptManager1': 'ctl00$ContentPlaceHolder1$updatepanel1|ctl00$ContentPlaceHolder1$hypYt',
                      '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$hypYt'}}

    def extract_formdata_from_newpage(self, node):
        '''
        从新页面的html中提取fromdata数据，便于访问下一页
        :param node:
        :return:
        '''
        input_list = node.find_all('input', type='hidden')
        for input in input_list:
            if input['name'] == 'ctl00$ContentPlaceHolder1$radSelect':
                continue
            try:
                name = input['name']
                value = input['value']
                self.form_data[name] = value
            except:
                pass
