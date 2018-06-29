from lxml import etree
from bs4 import BeautifulSoup
from urllib.request import urlopen

# vars to set
blogRootUrl = "https://coolwebsitedotcom.wordpress.com"
blogPosts = ["https://coolwebsitedotcom.wordpress.com/2018/06/27/cool-post/", "https://coolwebsitedotcom.wordpress.com/2018/06/18/post-2-selected-same-fi-as-post-1/"]
# TASK - CAN I SOMEHOW GET THE SELECTORS UP HERE?

index = 1  
authorList = []
rss = etree.Element('rss')
channel = etree.SubElement(rss, 'channel')
rootLink = etree.SubElement(channel, 'link') 
rootLink.text = blogRootUrl

for post in blogPosts:
    page = urlopen(post)
    soup = BeautifulSoup(page, "html.parser")
    
    # create <item>
    item = etree.SubElement(channel, "item")

    # set <content:encoded> 
    postBody = soup.select(".entry-content")[0]
    bodyStr = str(postBody)
    content = etree.SubElement(item, 'contentencoded') 
    content.text = etree.CDATA(bodyStr)

    # set <title>
    postTitle = soup.select(".entry-title")[0]
    title = etree.SubElement(item, "title")
    title.text = postTitle.text

    # set <pubDate>
    # TASK - FIGURE OUT HOW TO GET THE PUBLISH DATE WORKING WELL  
    date = etree.SubElement(item, 'pubDate') 
    date.text = 'Wed, 25 Apr 2018 13:19:35 +0000'

    # set <link>
    link = etree.SubElement(item, 'link') 
    link.text = post

    # set <wp:post_id>
    postId = etree.SubElement(item, 'wppost_id') 
    postId.text = str(index)

    # set <wp:status>
    status = etree.SubElement(item, 'wpstatus')
    status.text = "publish"

    # set <wp:post_type>
    status = etree.SubElement(item, 'wppost_type')
    status.text = "post"

    # set <dc:creator> and create <wp:author>
    # TASK - THIS FEELS REALLY SPECIFIC
    postAuthor = soup.find('a', attrs={'rel':'author'})
    author = etree.SubElement(item, 'dccreator')
    author.text = postAuthor.text
    if author.text not in authorList:
        authorList.append(author.text)
        authorPar = etree.SubElement(channel, 'wpauthor')
        rootLink.addnext(authorPar)
        authorParName = etree.SubElement(authorPar, 'wpauthor_display_name') 
        authorParName.text = etree.CDATA(postAuthor.text)
        authorParlog = etree.SubElement(authorPar, 'wpauthor_login') 
        authorParlog.text = etree.CDATA(postAuthor.text)

    # set <category>
    postTags = soup.find_all('a', attrs={'rel':'category tag'})
    for postTag in postTags:
        category = etree.SubElement(item, 'category')
        category.text = etree.CDATA(postTag.text)
        category.set("domain", "category")
        catSlug = category.text.replace(' ', '-')
        category.set("nicename", catSlug)

    # set <excerpt:encoded>
    postMetaD = soup.find('meta', attrs={'name':'description'})
    metaD = etree.SubElement(item, "excerptencoded")
    metaD.text = postMetaD["content"]

    # TASK - FIGURE OUT COMMENTS

    index += 1

etree.ElementTree(rss).write("blog.xml", pretty_print=True, xml_declaration=True, encoding='UTF-8')

def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

d = {
    'contentencoded':'content:encoded',
    'excerptencoded':'excerpt:encoded',
    'wppost_id':'wp:post_id',
    'wpstatus':'wp:status',
    'wppost_type':'wp:post_type',
    'dccreator':'dc:creator',
    'wpauthor_display_name':'wp:author_display_name',
    'wpauthor':'wp:author',
    'wpauthor_login':'wp:author_login'
    }

with open('blog.xml', 'r') as file:
    contents = file.read()
new_contents = replace_all(contents, d)
with open('blog.xml', 'w') as file:
    file.write(new_contents)
