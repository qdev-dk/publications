
import urllib.request as libreq
import feedparser
import re
import pandas as pd
import xml.etree.ElementTree as ET


def df_from_query(query: str, start: int = 0, max_results: int = 5):
    entrys = get_arxiv_feed_entries_list(query, start, max_results)
    df = df_from_arxiv_feed(entrys)
    return df


def get_arxiv_feed_entries_list(query: str, start: int = 0, max_results: int = 5):
    base_url = 'http://export.arxiv.org/api/query?'
    query_url = f'search_query={query}&start={start}&max_results={max_results}'

    with libreq.urlopen(base_url+query_url) as url:
        response = url.read()
    feed = feedparser.parse(response)
    return feed['entries']


def df_from_arxiv_feed(entrys):
    column_list = ['arxiv_id', 'idnr', 'Ver', 'updated', 'Year', 'journal_ref', 'DOI', 'title', 'summary', 'authors', 'ref_link', 'pdf_link', 'arxiv_abstract']
    my_list = [entry_list(ent) for ent in entrys]
    df = pd.DataFrame(my_list, columns=column_list)
    df['title'] = df.apply(lambda x: update_tile(x.DOI, x.arxiv_id, x.title), axis=1)
    return df


def update_tile(doi: str, arxiv_id: str, title: str):
    if doi is not None and arxiv_id is not None:
        return get_title_from_crossref(doi)
    else:
        return title


def get_title_from_crossref(doi: str):
    basehref_crossref = f'http://doi.crossref.org/servlet/query?usr=guenevere.p@gmail.com&format=unixref&qdata={doi}'
    with libreq.urlopen(basehref_crossref) as url:
        response = url.read()
    root = ET.fromstring(response)
    for title in root.iter('title'):
        title_str = title.text
    return title_str


def entry_list(entry):
    idtuple = get_id_and_version(entry)
    year = get_year(entry)
    author_list = [author['name'] for author in entry.authors ]
    ref_link = get_link(entry, 'doi')
    pdf_link = get_pdf_link(entry)
    arxiv_abstract = get_arxiv_abstract(entry)
    entrylist = [idtuple[0], idtuple[1], idtuple[2],
                 entry.updated,
                 year,
                 has_key_else_none(entry, 'arxiv_journal_ref'),
                 has_key_else_none(entry, 'arxiv_doi'),
                 entry.title,
                 entry.summary,
                 author_list,
                 ref_link,
                 pdf_link,
                 arxiv_abstract]
    return entrylist


def get_id_and_version(entry):
    arxiv_id = entry['id']
    last_slash_index = arxiv_id.rindex('/')
    idv = arxiv_id[last_slash_index+1:]
    v_index = idv.rindex('v')
    idnr = idv[:v_index]
    version = idv[v_index+1:]
    return (arxiv_id, idnr, version)


def get_year(entry):
    year_arxiv_updated = entry.updated_parsed.tm_year
    if 'arxiv_journal_ref' in entry:
        ref = entry.arxiv_journal_ref
        year_re = re.search("\(20[0-5][0-9]\)", ref)
        if year_re is not None:
            year = year_re.group()[1:-1]
        else:
            year = year_arxiv_updated  #'1950'
    else:
        year = year_arxiv_updated
    return str(year)


def get_link(entry, link_title):
    for link in entry.links:
        if link.rel != 'alternate':
            if link.title == link_title:
                link = link.href
                return link
    return None


def get_arxiv_abstract(entry):
    for link in entry.links:
        if link.rel == 'alternate':
            link = link.href
            return link


def get_pdf_link(entry):
    basehref_pdfs = 'http://qdev-data.nbi.ku.dk/pdfs'
    pdf_link = basehref_pdfs+'/'+entry.id.split('/abs/')[-1]+'.pdf'
    try:
        tryopen = libreq.urlopen(pdf_link)
        return pdf_link
    except:
        try:
            pdf_link = get_link(entry, 'pdf')
            #tryopen = libreq.urlopen(pdf_link)
            return pdf_link
        except:
            return None


def has_key_else_none(entry, key):
    if key in entry:
        return entry[key]
    else:
        return None
