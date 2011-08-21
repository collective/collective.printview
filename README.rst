Introduction
============

Every now and then users ask if they could somehow get a view which displays 
all the documents from certain folder structure at one page *Collective.printview* 
is an answer to this request.

*Collective.printview* brings you @@printview view that you can call from every
folderish object in Plone. This view is drop dead simple having only one task - 
dig deep through folder structure and search for content based on settings specified
on *collective.printview* controlpanel. In controlpanel you can define which folderish content 
types *collective.printview* can use while it tries to dig deeper in folder structure.
You can also define content types which are used for getting the actual content.
Finally you can chooce workflow states which will be made available for this search
for content.

For each object we're going to pull content from, *collective.printview* expects
to find these three mehtods:

1) Title()
2) Description()
3) getText() OR text.raw

After @@printview has crawled through all the specified folders it returns plain
page containing title, description and body text from all the objects it encountered.
The resulting page contains some javascript magic which creates footnotes after
each links and moves the actual links to page footer.


Usage
=====

@@printview view can be used from folderish contents actions menu (where you
can find cut,copy,paste,rename and delete actions as well). You can also manually
type @@printview after the url.


Warning!
========

Usually we can get objects title and description from the catalog. This addon
would be pointless if we couldn't also get the actual bodytext. This is why 
*collective.printview* doesn't play with portal_catalog and instead of that goes
bravely with full objects. This is something that can have serious impact on
your sites performance - especially if there are lot's of folders and content
objects under the context you're using the @@printview. @@printview uses memoize
to cache results based on a key created from printview settings and timestamp of
a latest modification in the search context. This won't save you on a first run 
though - you can't say I didn't warn you :)

