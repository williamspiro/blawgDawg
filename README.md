# blawgDawg
Python tools for HubSpot blog objects

__blogDawg.py__ - Turn any external blog into a HubSpot importable XML file  
__blogFeaturedImageSoup.py__ - Soup featured images from an external blog, upload them to the File Manager, set them as featured for the posts respective HubSpot equivalent  

## externalBlogDawg.py
A Python python to turn any external blog into an XML file which you can import into HubSpot    
_REQUIRES_  
[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)  
[lxml](https://lxml.de/)  

_USAGE_  
This Python python requires manually setting a few variables to make sure we can scrub external content, and get all the content and data we need to import a blog into HubSpot. It will grab post titles, urls, meta descriptions, authors, tags and post bodies, and turn them all into importable `<items>`  

`blogRootUrl` - Root URL of the external blog    
`blogPosts`- Python list of blog urls to import  
`soup.` - There are 5 `soup.` statements which require a selector of the html elements(s) you are getting to grab content from. See the [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) docs to learn more about modifieing these selectors depending on your needs  

```
$ python3 externalBlogDawg.py
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