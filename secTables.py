'''
Author: Denis Lima e Alves, PhD
Developed in: Python 3.7, macOS, iPython

The SEC Edgar system (Securities and Exchange Comission Electronic Data Gathering, Analysis and Retrieval)
is a huge source of information regarding information from companies that, for some reason, are required to 
disclose them to their shareholders and general public. This happens through the publication of forms
generally named "filings" and they are several. The most common among them are the 10-K, 10-Q, 8-K and 
DEF 14A and they are filed when some specific event happens and the company has to make that information 
available. For instance, the 10-Ks bring audited financial statement and are disclosed one every year.

Many times, researchers like myself don't have access to most of the mainstream paid databases. However,
much of the data they sell comes from the SEC Edgar system and there is no reason why we couldn't do the
same.

This script is part of my initiative to get all data I need for my research from "free" sources, that is,
where we do not need to pay a subscription to get access. It uses the modules edgar, requests and 
beautifulsoup to access, connect and parse the pages. The requests are done in a way that it is very 
unlikely that they will be denied by the SEC systems. Therefore, there are no treatment for exceptions.

Probably, the most obvious application of this package is to generate a file like the file test1.csv,
available in this repository as an illustration. The variables' descriptions are available in the function
get_metaData's docstring. Just type get_metaData?? (after importing the package, of course) you will see
the documentation. You can do it for all functions in this package, for additional details regarding their
use.

Hence, With this first part, you will be able to download some data from SEC's 10-K filings, such as SIC 
codes and description, IRS number, company's addresses, reporting date and state of incorporation and 
location. This is the information needed to carry on one of my projects in empirical accounting and tax 
research. In the next days, more information will be available to download from financial statements 
using XBRL.

The basic usage is as follows.

The function get_indices downloads the addresses from SEC Edgar. You need to suply the destination folder
where the files (.tsv) will be placed and the starting year. After those are downloaded, the function
write_edgarIndex creates a csv file with the filtered information needed for the download of data. This is
the one similar to the test1.csv file available in this repository as example. The output will consist of a 
bigger csv file with the filing type you need, but only those reported in the year you supplied to this 
function. This file can be used in many other applications, however. You need to supply the arguments as well.

To check which information you need to give each function, type: "function"??

If you have any questions, contact ufudenis@gmail.com
'''

def fix_cik(source,column):
    return ['0' * (10 - len(str(i))) + str(i) for i in source[column]]

def get_indices(destFolder,startYear):
    '''Where 'year' is the starting year to download Edgar's indices.
    Arguments: destFolder,startYear'''
    import edgar # https://pypi.org/project/edgar/
    edgar.download_index(destFolder,startYear)
    print(f"Indices have been downloaded. Build the dataframe using write_edgarIndex({destFolder}) as parameter.")

def write_edgarIndex(sourceFolder,destFolder,cikList=None,filingType=['10-K'],filingYear=[2000,2001]):
    '''Arguments: sourceFolder,destFolder,filingType,filingYear.
    Leave filingType blank for 10-K and filingYear blank for [2000,2001]. If not blank, filingYear must be a list of integers.
    In the case this list of years has length of one, it will use the range of years between the single year in the list
    and the current year.
    cikList must be a list. Leave it blank for all CIKs, which is not recommended if filingYear is 2000.
    There will be a lot of observations.'''
    import glob,re,os,datetime
    from tqdm import tqdm
    import pandas as pd
    '''Where sourceFolder is the folder where the .tsv files (from SEC Edgar) are located.
    fileName should not have any extensions and will be a CSV file in desfFolder.'''
    if len(filingYear) == 1:
        filingYear = [x for x in range(filingYear[0],datetime.datetime.today().date().year + 1)]
    list_files = [f for f in glob.glob(sourceFolder+'/*.tsv') if any(str(yr) in f for yr in filingYear)]
    def fix_cik(source,column):
        return ['0' * (10 - len(str(i))) + str(i) for i in source[column]]
    header = True
    #os.system('cls' if os.name == 'nt' else 'clear')
    print(f'Saving file to {destFolder}. File type is {filingType}.')
    with tqdm(total=len(list_files)) as bar1:
        for file_sec in list_files:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f'Reading {file_sec}.')
            bar1.update()
            try:
                x = pd.read_csv(file_sec, sep='|',header=None,dtype=str)
                x.columns = ['cik', 'firm_name','file_type','report_date','file_url_txt','file_url_html']
                x['report_date'] = pd.to_datetime(x.report_date,errors='coerce')
                x['report_year'] = [dt.date().year for dt in x.report_date]
                if fix_cik(x,'cik') is not None:
                    x.cik = fix_cik(x,'cik')
                else:
                    print('Failed to convert CIK.',file_sec)
                    break
                if cikList is None:
                    x = x.query("file_type in @filingType and report_year in @filingYear").copy(deep=True)
                elif isinstance(cikList,list):
                    x = x.query("file_type in @filingType and report_year in @filingYear and cik in @cikList").copy(deep=True)
                else:
                    print(f'Your cikList {cikList} is not valid.')
                    break
                if len(x) == 0:
                    bar1.update(1)
                    continue
                for col in ['file_url_txt','file_url_html']:
                    try:
                        x[col] = ['https://sec.gov/Archives/' + str(u) for u in x[col]]
                    except Exception as ex:
                        print(str(type(ex).__name__),str(ex.args))
                x.to_csv(destFolder+'/'+','.join(filingType)+'_index.csv',mode='a',header=header,index=False)
                header = False
            except Exception as ex:
                print('Can\'t read this file: ' + str(file_sec))
                print(str(type(ex).__name__),str(ex.args))


def get_metaData(sourceFile,destFolder,tupleList=None):
    from bs4 import BeautifulSoup as bs
    from tqdm import tqdm
    import pandas as pd
    import re,gc,csv,os,unicodedata
    # Next function adapted from https://www.programcreek.com/python/example/18310/requests.Session
    def requests_retry_session(
        retries=5,
        backoff_factor=0.3,
        status_forcelist=(500, 502, 503, 504),
        session=None,):
        if __name__ == '__main__':
            pass
        import requests
        from requests.adapters import HTTPAdapter
        #from requests.packages.urllib3.util.retry import Retry
        from urllib3.util.retry import Retry
        session = session or requests.Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist,
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session
    '''sourceFile is the full path to the file created and stored previously with the write_edgarIndex function. 
    In the case you want to use only the filings from specific dates for each CIK, enter the argument tupleList as a
    list of tuples like [(CIK,DATE)]. Otherwise, all filings will be included.
    The data consists of a CSV file and contains: CIK number, current firm name, filing date, filing type, SIC code 
    and label, IRS number, State of incorporation, State of location, business address, mailing address, 
    a list with former names (if any) and the url to the index of the respective index page.'''
    def fix_cik(source,column):
        return ['0' * (10 - len(str(i))) + str(i) for i in source[column]]
    gc.collect()
    metadata = pd.DataFrame(columns=['cik','currName','fDate','fType','irsNum','sicDesc','sic','sInc','sLoc',
        'bAddress','mAddress','fUrl'])
    metadata.to_csv(destFolder+'/SEC_datafile.csv',index=False)
    print('start')
    for chunk in pd.read_csv(sourceFile,chunksize=10000,dtype={'cik':str},parse_dates=['report_date']):
        if fix_cik(chunk,'cik') is not None:
            chunk.cik = fix_cik(chunk,'cik')
        if tupleList is not None:
            # chunk = chunk.query("cik in [x[0] for x in @tupleList] and report_date.date().year in [y[1] for y in @tupleList]").reset_index(
            #     drop=True).copy(deep=True) # There's some bug here.
            ciks,years = list(set([x[0] for x in tupleList])),list(set([y[1] for y in tupleList]))
            chunk = chunk.query("cik in @ciks and report_year in @years")
        os.system('cls' if os.name == 'nt' else 'clear')
        with open(destFolder+'/SEC_datafile.csv','a') as csvFile:
            writer = csv.writer(csvFile, delimiter = ',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            print(f'Writer ok.',len(chunk))
            with tqdm(total=len(chunk)) as bar1:
                for row,col in chunk.iterrows():
                    try:
                        indexurl = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK='+str(
                            col['cik'])+'&owner=exclude'
                        _10kUrl = col['file_url_html']
                        soup1 = bs(requests_retry_session().get(indexurl).content,'lxml')
                        soup2 = bs(requests_retry_session().get(_10kUrl).content,'lxml')
                        identText1 = soup1.find('p',{'class':'identInfo'}).text
                        identText2 = soup2.find('p',{'class':'identInfo'}).text
                        thisRow = [
                        col['cik'],col['firm_name'],col['report_date'].date(),col['file_type'],
                        re.search(r'[0-9]{4}',identText1).group(),
                        re.search(r'(?<= \- ).+?(?=State location)',identText1).group(),
                        re.search(r'(?<=IRS No.: )[0-9]+',identText2).group(),
                        re.search(r'(?<=State of Inc.: )[A-Z0-9]{2}',identText1).group(),
                        re.search(r'(?<=State location: )[A-Z0-9]{2}',identText1).group(),
                        [address.strip().replace('Business Address ','') for address in [re.sub(r' {2,999}',' ',tt.replace('\n',' ')) for tt in [unicodedata.normalize('NFKD',t.text) for t in soup1.findAll('div',{'class':'mailer'})]] if 'usiness' in address][0],
                        [address.strip().replace('Mailing Address ','') for address in [re.sub(r' {2,999}',' ',tt.replace('\n',' ')) for tt in [unicodedata.normalize('NFKD',t.text) for t in soup1.findAll('div',{'class':'mailer'})]] if 'ailing' in address][0],
                        'https://sec.gov/Archives/'+col['file_url_html']
                        ]
                    except:
                        thisRow = [col['cik'],col['firm_name'],col['report_date'].date(),col['file_type'],'','','','','','','','http://sec.gov/Archives/'+col['file_url_html']]
                    writer.writerow(thisRow)
                    bar1.update(1)

def get_xbrl_10k():
    '''To be implemented.'''

def get_cikList(pathtoFile,sheetName,cikColumn):
    '''To be implemented.'''
