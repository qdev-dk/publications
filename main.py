import arxivtodf
import dftohtml


search_queries = ['rn:NBI+AND+rn:QDEV', 'au:+kjaergaard_m', 'au:Nygaard_J+OR+au:Nygard_J','au:Marcus_C_M','au:+flensberg_k','au:+kuemmeth_f','au:+paaske_j','au:+rudner_m','au:+jespersen_T', 'au:+krogstrup_P', 'au:+chatterjee_a']
names = ['output', 'kjaergaard', 'nygard','marcus','flensberg','kuemmeth','paaske','rudner','jespersen', 'krogstrup', 'chatterjee']
fullnames = ['All QDev staff', 'Morten Kjaergaard',u'Jesper Nyg\xe5rd', 'Charles M. Marcus', 'Karsten Flensberg', 'Ferdinand Kuemmeth', 'Jens Paaske', 'Mark Spencer Rudner', 'Thomas Sand Jespersen', 'Peter Krogstrup', 'Anasua Chatterjee']
homepageids = ['', '181096', '67039', '379494', '185400', '440362', '126929', '440016', '136147', '276614','109873']

basehref = '/var/publications/data/'
basehref2 = '/var/publications/web/'

for n in range(len(names)):
    try:
        df = arxivtodf.df_from_query(search_queries[n], start=0, max_results=500)
        df.to_csv(basehref+names[n]+'.csv')
        dftohtml.df_to_html_file(homepageids[n], fullnames[n], df, names, basehref2+names[n]+'.html')
    except Exception as e:
        print(e)
        pass
