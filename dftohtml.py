import re
from unidecode import unidecode


def df_to_html_file(homepageid: str, fullname, df, prof_names, file_path):
    stringhtml = make_html_string(homepageid, fullname, df, prof_names)    
    html_string_to_file(file_path, stringhtml)


def html_string_to_file(file_path, html_string):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(html_string)


def make_html_string(homepageid: str, fullname, df, prof_names):
    stringhtml = output_html_string_top(homepageid, fullname)
    stringhtml += entrys_by_years_to_html(df, prof_names)
    stringhtml += '</body></html>'
    return stringhtml


def output_html_string_top(homepageid: str, fullname):
    output_html_string_top = '<html><head>\n'
    output_html_string_top += '<meta http-equiv="content-type" content="text/html;charset=utf-8" />\n'
    output_html_string_top += '<link href="http://qdev.nbi.ku.dk/css/style.css" rel="stylesheet" type="text/css" media="screen, print" />\n'
    output_html_string_top += '<link rel="stylesheet" type="text/css" href="http://qdev-data.nbi.ku.dk/publications/simpletree.css" />'
    output_html_string_top += '</head><body>\n'
    output_html_string_top += '<script type="text/javascript" src="http://qdev-data.nbi.ku.dk/publications/simpletreemenu.js"></script>\n'
    output_html_string_top += '<script type="text/javascript"\n'
    output_html_string_top += '  src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">\n'
    output_html_string_top += '</script>\n'
    output_html_string_top += '<script type="text/x-mathjax-config">\n'
    output_html_string_top += 'MathJax.Hub.Config({\n'
    output_html_string_top += '  tex2jax: {inlineMath: [["$","$"], ["{","}"]]}\n'
    output_html_string_top += '});\n'
    output_html_string_top += '</script>\n'
    # If NOT all profs, write his name with a link to his page
    if homepageid.isdigit():
        output_html_string_top += f'<h2>Publications by <a href="http://www.nbi.ku.dk/english/staff/?id={homepageid}&vis=medarbejder">{fullname}</a></h2>'
    # If it IS all profs, write name (with no link), which is all QDev staff
    else:
        output_html_string_top += f'<h2>Publications by {fullname}</h2>'
#    output_html_string_top += '<p><img src="%s" style="width:100px;">' %qdev_logo
    output_html_string_top += '</p>\n'
    return output_html_string_top


def entrys_by_years_to_html(df, prof_names):
    years_list = list(set(df.Year.to_list()))
    years_list.sort(reverse=True)
    output_html_string = ''
    for year in years_list:
        df_year = df.loc[df['Year'] == year]
        output_html_string += entrys_year_to_html(year, df_year, prof_names)

    return output_html_string


def entrys_year_to_html(year, df, prof_names):
    output_html_string = f'<ul id="{year}" class="treeview">\n'
    output_html_string += f'<li><a href="javascript:void(0)" onClick="return false;" style="font-size: 12px; font-weight:bold; line-height: 3em">{year}</a>\n<ul rel="open">\n'

    output_html_string += entrys_to_html(df, prof_names)

    output_html_string += '</ul>\n</li></ul>\n'
    output_html_string += '<script type="text/javascript">\n'
    output_html_string += '//ddtreemenu.createTree(treeid, enablepersist, opt_persist_in_days (default is 1))\n'
    output_html_string += f'ddtreemenu.createTree("{year}", false)\n'
    output_html_string += "</script>\n"
    return output_html_string


def entrys_to_html(df, prof_names):
    stringhtml = ''
    df_dict = df.to_dict('records')
    for i in range(df.shape[0]):
        entry = df_dict[i]
        stringhtml += output_html_string_entry(entry, prof_names)
    return stringhtml


def output_html_string_entry(entry, prof_names):
    output_html_string = '<li>\n'
    output_html_string += '<b>\n'
    output_html_string += entry['title']
    output_html_string += '</b> - \n'
    output_html_string += '<a href="javascript:void(0)" onClick="return false;" rel="closed">Abstract</a>\n'
    output_html_string += '<ul rel="closed"><li>\n'
    output_html_string += entry['summary']
    output_html_string += '</li></ul></li><li>'
    output_html_string += '<table><tr>\n'
    output_html_string += '<td>\n'
    output_html_string += '</td></tr><tr><td>\n'

    output_html_string += author_links_to_html(entry['authors'], prof_names)

    output_html_string += journal_link_to_html(entry)

    if entry['DOI']:
        output_html_string += '<tr><td>DOI: '+entry['DOI']
        output_html_string += '</td></tr><tr><td>\n'

    if not(entry['journal_ref']):
        if entry['arxiv_abstract']:
            idv = entry['arxiv_id'].split('/abs/')[-1]
            output_html_string += '<a href='+entry['arxiv_abstract']+' target="_blank" title="Abstract">'+idv+'</a> '
        if entry['pdf_link']:
            output_html_string += '[<a href="{}" title="Download PDF">pdf</a>]'.format(entry['pdf_link'])

        output_html_string += '</td></tr>'

    output_html_string += '</table><hr>\n'
    output_html_string += '</li>\n'

    return output_html_string


def author_links_to_html(authors, prof_names):
    output_html_string = ''
    for i, author in enumerate(authors):
        linkaddr = '<a href="http://arxiv.org/find/cond-mat/1/au:+' + re.sub('[^A-Za-z0-9-_]+', '', re.sub('-', '_', unidecode(author[author.rfind(' ')+1:]))) + '_' + unidecode(author[0]) + '/0/1/0/all/0/1" target="_blank">' + author + '</a>'
        for prof_name in author.lower().split():
            if prof_name in prof_names:
                linkaddr = '<a href="http://qdev.nbi.ku.dk/publications/' + prof_name + '">' + author + '</a>'
        if i != 0:
            output_html_string += ', '
        output_html_string += linkaddr
    output_html_string += '</td></tr><tr><td>\n'
    return output_html_string


def journal_link_to_html(entry):
    journal_ref = ''
    if entry['journal_ref'] and entry['ref_link']:
        journal_ref += '<tr><td>Journal reference: '
        journal_ref += '<a href="javascript:void(0)" onclick="window.open('
        journal_ref += "'"
        journal_ref += entry['ref_link']
        journal_ref += "', 'newwindow', 'width=800, height=800'); return false;"
        journal_ref += '">'
        journal_ref += entry['journal_ref']
        journal_ref += '</a>\n'

    if entry['pdf_link']:
        journal_ref += ' [<a href='+entry['pdf_link']+' title="Download PDF">pdf</a>]'
    #else:
        #output_html_string += '<font color=#fff> [ %s ]</font>' %entry.id.split('/abs/')[-1]
    journal_ref += '</td></tr>\n'
    return journal_ref
