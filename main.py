import arxivtodf
import dftohtml
import pandas as pd

names_df  = pd.read_excel('names.xlsx',dtype={'names':str, 'fullnames':str, 'search_queries':str, 'homepageids':str})

search_queries = names_df['search_queries'].to_list()
names = names_df['names'].to_list()
fullnames =names_df['fullnames'].to_list()
homepageids = names_df['homepageids'].to_list()


basehref = '/var/publications/data/'
basehref2 = '/var/publications/web/'
static = 'X:\Publication list'
column_list = ['arxiv_id', 'idnr', 'Ver', 'updated', 'Year', 'journal_ref', 'DOI', 'title', 'summary', 'authors', 'ref_link', 'pdf_link', 'arxiv_abstract']

for n in range(len(names)):
    try:
        df_query = arxivtodf.df_from_query(search_queries[n], start=0, max_results=500)

        df_query.to_excel(basehref+names[n]+'.xlsx')
        df_static =  pd.read_excel(static+'static_'+names[n]+'.xlsx',index_col=0,dtype=str)
        merged = pd.merge(df_static[['idnr','DOI']], df_query[['idnr','DOI']], on=['idnr','DOI'], how='right', indicator=True)
        bool_df = merged._merge=='right_only'
        df_final = pd.concat([df_static,df_query[bool_df.to_list()]])

        dftohtml.df_to_html_file(str(homepageids[n]), fullnames[n], df_query, names, basehref2+names[n]+'.html')
    except Exception as e:
        print(e)
        pass
