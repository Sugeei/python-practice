from bs4 import BeautifulSoup
import os
from config.base import root_path


class FeedBase():
    def __init__(self):
        pass

    def get_soup(self, page):
        # url = params.paramsget('url')
        # header = params.get('header')
        # source = requests.get(url, headers=header)
        soup = BeautifulSoup(page, 'lxml')
        return soup

    def transform(self, df, flag):
        # df = pd.read_csv(os.path.join(root_path, 'interface', 'InterFaceListedCompany'))
        df = df[['id', 'key', 'value']]
        df = df.drop_duplicates()
        dft = df.pivot(index='id', columns='key')
        dft.to_csv(os.path.join(root_path, 'output', "%s.csv" % (flag)))
        pass

