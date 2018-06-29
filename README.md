# blawgDawg
Python 3.6.5 tools for HubSpot blog objects 

__externalBlawgDawg.py__ - Turn any external blog into a HubSpot importable XML file  
__blogFeaturedImageSoup.py__ - Soup featured images from an external blog, upload them to the File Manager, set them as featured for the posts respective HubSpot equivalent  

## externalBlawgDawg.py
A Python python to turn any external blog into an XML file which you can import into HubSpot    
_REQUIRES_  
[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)  
[lxml](https://lxml.de/)  

_USAGE_  
This Python python requires manually setting a few variables to make sure we can scrub external content, and get all the content and data we need to import a blog into HubSpot. It will grab post titles, urls, meta descriptions, authors, tags and post bodies, and turn them all into importable `<items>`  

`blogRootUrl` - Root URL of the external blog    
`blogPosts`- Python list of blog urls to import  
`soup.` - There are 5 `soup.` statements which require a selector of the html elements(s) you are getting to grab content from. See the [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) docs to learn more about modifieing these selectors depending on your needs  
### __soups__  
`soup.find('title')` - you should not need to touch this soup. Finds and prints the `<item>` `<title>` to `blog.xml`
```
<title>This is the post title</title>
>>>>>
<title>This is the post title</title> 
```
`soup.find('meta', attrs={'name':'description'})` - you should not need to touch this soup. Finds and prints the `<item>` `<excerpt:encoded>` to `blog.xml`  

```
<meta name="description" content="This is the meta description"> 
>>>>>
<excerpt:encoded><![CDATA[This is the meta description]]<excerpt:encoded>
```
`soup.find('a', attrs={'rel':'author'})` - you likely need to change this soup. Finds the author and prints the `<item>` `<dc:creator>`, as well as creates top level `<wp:author>` tags in `blog.xml`
```
<a href="link" rel="author">Author</a>
>>>>>
<dc:creator>Author</dc:creator>
&
<wp:author>
    <wp:author_display_name><![CDATA[Author]]></wp:author_display_name>
    <wp:author_login><![CDATA[Author]]></wp:author_login>
</wp:author>
```
`soup.find_all('a', attrs={'rel':'category tag'})` - you likely need to change this soup. Finds the tags of a post and prints the `<item>` `<categories>` (sets `nicename`) to `blog.xml`
```
<a href="link" rel="category tag">Tag 1</a>
<a href="link" rel="category tag">Tag 2</a>
>>>>>
<category domain="category" nicename="tag-1"><![CDATA[cTag 1]]></category>
<category domain="category" nicename="tag-2"><![CDATA[Tag 2]]></category>
```
`soup.select('.entry-content')[0]` - you likely need to change this soup. Finds the content of a post and prints the `<item>` `<content:encoded>` to `blog.xml`
```
<div class="entry-content">This is the post body</div>
>>>>>
<content:encoded><![CDATA[This is the post body]]</content:encoded><
```

XML setup which happens on its own:
```
<?xml version='1.0' encoding='UTF-8'?>
<rss>
  <channel>
  <link>!!blog root url link from blogRootUrl variable!!</link>
  <
    !!<wp:author>s build here!!
  >
    <item>
        <link>!!post link from blogPosts library!!</link>
        <wp:post_id>!!set automatically!!</wp:post_id>
        <wp:status>publish</wp:status>
        <wp:post_type>post</wp:post_type>
        <
            !!The above soups fill in here!!
        >
    </item>
    ... !!for every post in blogPosts library, the above <item> is created!!
  </channel>
</rss>
```
```
$ python3 externalBlawgDawg.py
```

## blogFeaturedImageSoup.py
A Python python to find the featured image on an external blog, upload it to the HubSpot File Manager, and then set the HubSpot hosted version of the posts' `featuredImage` with the newly uploaded File Manager asset  
_REQUIRES_  
[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)  
[requests](http://docs.python-requests.org/en/master/)  

_USAGE_  
This Python python requires manually setting 4 variables: `accessToken`, `blogRootUrl`, `featuredImageSelector` & `postsToSoupScrubKitten`

`accessToken` - An access_token for the portal you want to blogFeaturedImageSoup  
`blogRootUrl`- The external blogs root url 
`featuredImageSelector` - The CSS selector which select the external blogs featured image (ex. `.featured-image img`)  
`postsToSoupScrubKitten` - A python list of the slugs of all of the external posts to soup (ex. `["slug/post/1", "slug/post/2", "slug/post/3"]`)  

It is important that the post slugs of the external and HubSpot posts are the same. `blogRootUrl` + `postsToSoupScrubKitten[slugs]` should equal the actual URL of the posts. `slug`s should not start with a `/`, rather, `blogRootUrl` should end with a `/`

```
$ python3 blogFeaturedImageSoup.py
```