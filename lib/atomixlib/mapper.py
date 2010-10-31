#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
atomixlib is a Python package providing a simple interface to the Atom XML format.

The mapper module provides a set of classes to create a representation as pure
Python objects of Atom documents. The module offers a fairly tree oriented view
of an Atom document. Each elements becomes an attribute of the main document.

Usage:
======
# You should ALWAYS pass values as unicode objects to all your elements.

feed = Feed()
feed.id = ID(u'urn:uuid:af237fcf-5889-11db-b72d-0014a44de7e5')
feed.title = PlainTextTitle(u'My feed')
feed.updated = Updated()
author = Author(name=u'Jon Doe')
feed.authors.append(author)

entry = Entry()
entry.id = ID(u'urn:uuid:f3f3cf8c-5889-11db-bf47-0014a44de7e5')
entry.published = Published()
entry.content = PlainTextContent(u'Hello there')
feed.entries.append(entry)

entry = Entry()
entry.id = ID(u'urn:uuid:2206ff68-588a-11db-bab4-0014a44de7e5')
entry.published = Published()
# Text content should be a string in this case
entry.content = XHTMLContent(xhtml='<xh:b>Hello over there too</xh:b>',
                             xhtml_prefix=u'xh',
                             xhtml_namespace=u'http://www.w3.org/1999/xhtml')
feed.entries.append(entry)

>>> feed
<atom:feed xmlns:atom="http://www.w3.org/2005/Atom" element at -0x48383994 />
>>> feed.id
<atom:id xmlns:atom="http://www.w3.org/2005/Atom" element at -0x48383934 />
>>> unicode(feed.id)
u'urn:uuid:f3f3cf8c-5889-11db-bf47-0014a44de7e5'
>>> feed.id.value
u'urn:uuid:f3f3cf8c-5889-11db-bf47-0014a44de7e5'

Serialization and deserialization:
==================================
>>> import atomixlib
>>> atomixlib.default_engine_name = 'amara'
>>> f = atomixlib.s_feed(feed)
>>> print f
<?xml version="1.0" encoding="UTF-8"?>
<atom:feed xmlns:atom="http://www.w3.org/2005/Atom">
  <atom:id>urn:uuid:af237fcf-5889-11db-b72d-0014a44de7e5</atom:id>
  <atom:title type="text">My feed</atom:title>
  <atom:updated>2006-10-10T18:14:49.546096Z</atom:updated>
  <atom:author>
    <atom:name>Jon Doe</atom:name>
  </atom:author>
  <atom:entry>
    <atom:id>urn:uuid:f3f3cf8c-5889-11db-bf47-0014a44de7e5</atom:id>
    <atom:published>2006-10-10T18:14:49.551997Z</atom:published>
    <atom:content type="text">Hello there</atom:content>
  </atom:entry>
  <atom:entry>
    <atom:id>urn:uuid:2206ff68-588a-11db-bab4-0014a44de7e5</atom:id>
    <atom:published>2006-10-10T18:14:49.556267Z</atom:published>
    <atom:content type="xhtml">
      <div xmlns="http://www.w3.org/1999/xhtml">
        <xh:b xmlns:xh="http://www.w3.org/1999/xhtml">Hello over there too</xh:b>
      </div>
    </atom:content>
  </atom:entry>
</atom:feed>

>>> t = atomixlib.d_feed(f)
>>> t.id.value
u'urn:uuid:af237fcf-5889-11db-b72d-0014a44de7e5'

>>> e = atomixlib.s_entry(feed.entries[0])
>>> print e
<?xml version="1.0" encoding="UTF-8"?>
<atom:entry xmlns:atom="http://www.w3.org/2005/Atom">
  <atom:id>urn:uuid:f3f3cf8c-5889-11db-bf47-0014a44de7e5</atom:id>
  <atom:published>2006-10-10T18:18:27.998627Z</atom:published>
  <atom:content type="text">Hello there</atom:content>
</atom:entry>

>>> t.prefix = u'k'
>>> t.sync_children()
>>> f = atomixlib.s_feed(t)
>>> print f
<?xml version="1.0" encoding="UTF-8"?>
<k:feed xmlns:k="http://www.w3.org/2005/Atom">
  <k:id>urn:uuid:af237fcf-5889-11db-b72d-0014a44de7e5</k:id>
  <k:title type="text">My feed</k:title>
  <k:updated>2006-10-10T18:14:49.546096Z</k:updated>
  <k:entry>
    <k:id>urn:uuid:f3f3cf8c-5889-11db-bf47-0014a44de7e5</k:id>
    <k:published>2006-10-10T18:14:49.551997Z</k:published>
    <k:content type="text">Hello there</k:content>
  </k:entry>
  <k:entry>
    <k:id>urn:uuid:2206ff68-588a-11db-bab4-0014a44de7e5</k:id>
    <k:published>2006-10-10T18:14:49.556267Z</k:published>
    <k:content type="xhtml">
      <div xmlns="http://www.w3.org/1999/xhtml">
        <xh:b xmlns:xh="http://www.w3.org/1999/xhtml">Hello over there too</xh:b>
      </div>
    </k:content>
  </k:entry>
</k:feed>

# Move to the default namespace ''
>>> feed.prefix = None
>>> feed.sync_children(False)
>>> s = atomixlib.s_feed(feed)
"""

from atomixlib import ATOM10_PREFIX, ATOM10_NS, ATOMPUB_PREFIX, ATOMPUB_NS
from datetime import datetime

class XMLAttribute(object):
    """
    Maps the attribute of an XML element to a simple Python object.
    """
    def __init__(self, name=None, value=None, parent=None):
        """
        Maps the attribute of an XML element to a simple Python object.

        Keyword arguments:
        name -- Name of the attribute
        value -- content of the attribute
        parent -- element which this attribute belongs to
        """
        self.__parent = parent
        self.__name = name
        self.__value = value
        self.__prefix = u'xml'

        if parent:
            parent.attributes.append(self)
        
    def __unicode__(self):
        return self.__value
    
    def __str__(self):
        return self.__value

    def __repr__(self):
        value = self.__value or ''
        return '%s="%s" attribute at %s' % (self.__name, value, hex(id(self)))

    def getname(self):
        return self.__name
    
    def setname(self, value):
        self.__name = value
        
    name = property(getname, setname,
                    doc="Get and set the attribute name")
    
    def getprefix(self):
        return self.__prefix
    
    def setprefix(self, value):
        self.__prefix = value
        
    prefix = property(getprefix, setprefix,
                      doc="Get and set the attribute prefix")
    
    def getvalue(self):
        return self.__value
    
    def setvalue(self, value):
        self.__value = value
        
    value = property(getvalue, setvalue,
                     doc="Get and set the attribute value")
    
    def getparent(self):
        return self.__parent
    
    def setparent(self, value):
        self.__parent = value
        
    parent = property(getparent, setparent,
                      doc="Get and set the parent element for this element")
    
#############################################
# Atom elements
#############################################
class AtomAttribute(XMLAttribute):
    def __init__(self, name=None, value=None, parent=None):
        XMLAttribute.__init__(self, name, value, parent)
        if parent:
            self.prefix = parent.prefix
    
class AtomElement(object):
    """
    Maps an XML element to a Python object.
    """
    def __init__(self, name=None, value=None, prefix=None, namespace=None, parent=None):
        """
        Maps an XML element to a Python object.
        
        Keyword arguments:
        name -- Name of the XML element
        value -- Content of the element
        prefix -- QCName prefix
        namespace -- XML namespace attached to that element
        parent -- Parent element of this element
        """
        self.__parent = parent
        self.__prefix = prefix
        self.__xmlns = namespace
        self.__name = name
        self.__value = value
        self.__children = []
        self.__attributes = []

    def __repr__(self):
        prefix = self.prefix
        xmlns = self.xmlns
        if (prefix not in ('', None)) and xmlns:
            return '<%s:%s xmlns:%s="%s" element at %s />' % (prefix,
                                                              self.__name,
                                                              prefix,
                                                              xmlns,
                                                              hex(id(self)),)
        else:
            return "<%s element at %s />" % (self.__name, hex(id(self)))

    def __unicode__(self):
        return self.value
    
    def __str__(self):
        return self.value

    def sync_children(self, shallow=True):
        self.prefix = self.parent.prefix
        self.xmlns = self.parent.xmlns
        if shallow is False and hasattr(self, 'children'):
            for child in self.children:
                child.sync_children(shallow=shallow)
    
    def getvalue(self):
        return self.__value
    
    def setvalue(self, value):
        self.__value = value
        
    value = property(getvalue, setvalue,
                      doc="Get and set the text value for the element")
    
    def getchildren(self):
        return self.__children
    
    children = property(getchildren,
                        doc="Get direct children of this element")
    
    def getattributes(self):
        return self.__attributes
    
    attributes = property(getattributes,
                          doc="Get the element attributes")
    
    def getprefix(self):
        return self.__prefix
    
    def setprefix(self, value):
        self.__prefix = value
        
    prefix = property(getprefix, setprefix,
                      doc="Get and set the prefix for the element")
    
    def getnamespace(self):
        return self.__xmlns
    
    def setnamespace(self, value):
        self.__xmlns = value
        
    xmlns = property(getnamespace, setnamespace,
                     doc="Get and set the XML namespace for the element")

    def getparent(self):
        return self.__parent
    
    def setparent(self, value):
        self.__parent = value
        
    parent = property(getparent, setparent,
                      doc="Get and set the parent element for this element")

class ID(AtomElement):
    def __init__(self, value=None):
        """
        Maps to the atom:id element
    
        Keyword arguments:
        value -- Value of the element
        """
        AtomElement.__init__(self, name=u'id', value=value)

class PersonName(AtomElement):
    def __init__(self, value=None):
        """
        Maps to the atom:name element
    
        Keyword arguments:
        value -- Value of the element
        """
        AtomElement.__init__(self, name=u'name', value=value)
        
class PersonEmail(AtomElement):
    def __init__(self, value=None):
        """
        Maps to the atom:email element
    
        Keyword arguments:
        value -- Value of the element
        """
        AtomElement.__init__(self, name=u'email', value=value)
        
class PersonURI(AtomElement):
    def __init__(self, value=None):
        """
        Maps to the atom:uri element
    
        Keyword arguments:
        value -- Value of the element
        """
        AtomElement.__init__(self, name=u'uri', value=value)
    
class Author(AtomElement):
    def __init__(self, name=None, email=None, uri=None):
        """
        Maps to the atom:author element. Will automatically call
        PersonName, PersonEmail and PersonURI.
    
        Keyword arguments:
        name -- Name of the person
        email -- Email of the person
        uri -- URI associated to the person
        """
        AtomElement.__init__(self, name=u'author')
        self.name = PersonName(name)
        self.email = PersonEmail(email)
        self.uri = PersonURI(uri)
        self.__dict__['children'] = [self.name, self.email, self.uri]
          
class Contributor(AtomElement):
    def __init__(self, name=None, email=None, uri=None):
        """
        Maps to the atom:contributor element. Will automatically call
        PersonName, PersonEmail and PersonURI.
    
        Keyword arguments:
        name -- Name of the person
        email -- Email of the person
        uri -- URI associated to the person
        """
        AtomElement.__init__(self, name=u'author')
        self.name = PersonName(name)
        self.email = PersonEmail(email)
        self.uri = PersonURI(uri)
        self.__dict__['children'] = [self.name, self.email, self.uri]
        
class Category(AtomElement):
    def __init__(self, term=None, scheme=None, label=None):
        """
        Maps to the atom:category element. Will call AtomAttribute
        for the term, scheme and label attributes.

        Keyword arguments:
        term -- Value of term attribute
        scheme -- Value of the scheme attribute
        label -- value of the label attribute
        """
        AtomElement.__init__(self, name=u'category')
        self.term = AtomAttribute(name=u'term', value=term, parent=self)
        self.scheme = AtomAttribute(name=u'scheme', value=scheme, parent=self)
        self.label = AtomAttribute(name=u'label', value=label, parent=self)
        self.attributes.extend([self.term, self.scheme, self.label])

class Generator(AtomElement):
    def __init__(self, value=None, uri=None, version=None):
        """
        Maps to the atom:generator element. Will call AtomAttribute
        for the uri and version attributes.

        Keyword arguments:
        value -- Name of the generator
        uri -- URI associated to the generator
        version -- Version string of the generator
        """
        AtomElement.__init__(self, name=u'generator', value=value)
        self.uri = AtomAttribute(name=u'uri', value=uri, parent=self)
        self.version = AtomAttribute(name=u'version', value=version, parent=self)

class Icon(AtomElement):
    def __init__(self, uri=None):
        """
        Maps to the atom:icon element

        Keyword arguments:
        uri -- URI associated to the icon
        """
        AtomElement.__init__(self, name=u'icon', value=uri)
        
class Logo(AtomElement):
    def __init__(self, uri=None):
        """
        Maps to the atom:logo element

        Keyword arguments:
        uri -- URI associated to the logo
        """
        AtomElement.__init__(self, name=u'logo', value=uri)

class AtomDateElement(AtomElement):
    def __init__(self, name, dt=None):
        """
        Base class for date elements in Atom.

        Keyword arguments:
        name -- Name of the element
        dt -- DateTime instance. If None, dt will default to utcnow()
        """
        if dt is None:
            dt = datetime.utcnow()
        AtomElement.__init__(self, name=name, value=dt)

    def __unicode__(self):
        """
        Returns a unicode object of the datetime formated as an ISO date
        """
        return unicode(self.value.isoformat() + 'Z')

    def __str__(self):
        """
        Returns a string of the datetime formated as an ISO date
        """
        return str(self.value.isoformat() + 'Z')
        
class Published(AtomDateElement):
    def __init__(self, dt=None):
        """
        Maps to the atom:published element

        Keyword arguments:
        dt -- DateTime instance. If None, dt will default to utcnow()
        """
        AtomDateElement.__init__(self, name=u'published', dt=dt)
        
class Updated(AtomDateElement):
    def __init__(self, dt=None):
        """
        Maps to the atom:updated element

        Keyword arguments:
        dt -- DateTime instance.If None, dt will default to utcnow()
        """
        AtomDateElement.__init__(self, name=u'updated', dt=dt)

class PlainTextElement(AtomElement):
    def __init__(self, name=None, text=None):
        """
        Base class for any plain text construction.
        Automatically add a 'type' AtomAttribute of value 'text'.
        
        Keyword arguments:
        name -- Name of the element
        text -- Plain text value.
        """
        AtomElement.__init__(self, name=name, value=text)
        self.type = AtomAttribute(name=u'type', value=u'text', parent=self)
        
class HTMLElement(AtomElement):
    def __init__(self, name=None, escaped_html=None):
        """
        Base class for any HTML text construction.
        Automatically add a 'type' AtomAttribute of value 'html'.
        
        Keyword arguments:
        name -- Name of the element
        escaped_html -- Escaped HTML text.
        """
        AtomElement.__init__(self, name=name, value=escaped_html)
        self.type = AtomAttribute(name=u'type', value=u'html', parent=self)
         
class XHTMLElement(AtomElement):
    def __init__(self, name=None, xhtml=None, xhtml_prefix=None, xhtml_namespace=None):
        """
        Base class for any XHTML text construction.
        Automatically add a 'type' AtomAttribute of value 'xhtml' and
        a 'div' AtomElement with the prefix and namespace provided.
        The xhtml string will be attached to that div element.
        
        Keyword arguments:
        name -- Name of the element
        xhtml -- XHTML content as a Python string/unicode object
        xhtml_prefix -- prefix of the content
        xhtml_namespace -- namespace of the content 
        """
        AtomElement.__init__(self, name=name, value=None)
        self.type = AtomAttribute(name=u'type', value=u'xhtml', parent=self)
        self.div = AtomElement(name=u'div', value=xhtml, parent=self)
        self.div.prefix = xhtml_prefix
        self.div.xmlns = xhtml_namespace

    def __unicode__(self):
        return unicode(self.div)
    
    def __str__(self):
        return str(self.div)
        
class PlainTextContent(PlainTextElement):
    def __init__(self, text=None):
        """
        Plain text content construction.
        Automatically add a 'type' AtomAttribute of value 'text'.
        
        Keyword arguments:
        text -- Plain text content
        """
        PlainTextElement.__init__(self, name=u'content', text=text)
        
class HTMLContent(HTMLElement):
    def __init__(self, escaped_html=None):
        """
        HTML text construction.
        Automatically add a 'type' AtomAttribute of value 'html'.
        
        Keyword arguments:
        escaped_html -- Escaped HTML text.
        """
        HTMLElement.__init__(self, name=u'content', escaped_html=escaped_html)
        
class ExternalContent(AtomElement):
    def __init__(self, src=None, type=None):
        AtomElement.__init__(self, name=u'content', value=None)
        self.src = AtomAttribute(name=u'src', value=src, parent=self)
        self.type = AtomAttribute(name=u'type', value=type, parent=self)
        
class XHTMLContent(XHTMLElement):
    def __init__(self, xhtml=None, xhtml_prefix=None, xhtml_namespace=None):
        """
        XHTML content construction.
        Automatically add a 'type' AtomAttribute of value 'xhtml' and
        a 'div' AtomElement with the prefix and namespace provided.
        The xhtml string will be attached to that div element.
        
        Keyword arguments:
        xhtml -- XHTML content as a Python string/unicode object
        xhtml_prefix -- prefix of the content
        xhtml_namespace -- namespace of the content 
        """
        XHTMLElement.__init__(self, name=u'content', xhtml=xhtml,
                              xhtml_prefix=xhtml_prefix, xhtml_namespace=xhtml_namespace)

class PlainTextTitle(PlainTextElement):
    def __init__(self, text=None):
        """
        Plain text title construction.
        Automatically add a 'type' AtomAttribute of value 'text'.
        
        Keyword arguments:
        text -- Plain text content
        """
        PlainTextElement.__init__(self, name=u'title', text=text)
        
class HTMLTitle(HTMLElement):
    def __init__(self, escaped_html=None):
        """
        HTML title construction.
        Automatically add a 'type' AtomAttribute of value 'html'.
        
        Keyword arguments:
        escaped_html -- Escaped HTML text.
        """
        HTMLElement.__init__(self, name=u'title', escaped_html=escaped_html)
        
class XHTMLTitle(XHTMLElement):
    def __init__(self, xhtml=None, xhtml_prefix=None, xhtml_namespace=None):
        """
        XHTML title construction.
        Automatically add a 'type' AtomAttribute of value 'xhtml' and
        a 'div' AtomElement with the prefix and namespace provided.
        The xhtml string will be attached to that div element.
        
        Keyword arguments:
        xhtml -- XHTML content as a Python string/unicode object
        xhtml_prefix -- prefix of the content
        xhtml_namespace -- namespace of the content
        """
        XHTMLElement.__init__(self, name=u'title', xhtml=xhtml,
                              xhtml_prefix=xhtml_prefix, xhtml_namespace=xhtml_namespace)

class PlainTextSubtitle(PlainTextElement):
    def __init__(self, text=None):
        """
        Plain text subtitle construction.
        Automatically add a 'type' AtomAttribute of value 'text'.
        
        Keyword arguments:
        text -- Plain text content
        """
        PlainTextElement.__init__(self, name=u'subtitle', text=text)
        
class HTMLSubtitle(HTMLElement):
    def __init__(self, escaped_html=None):
        """
        HTML subtitle construction.
        Automatically add a 'type' AtomAttribute of value 'html'.
        
        Keyword arguments:
        escaped_html -- Escaped HTML text.
        """
        HTMLElement.__init__(self, name=u'subtitle', escaped_html=escaped_html)
        
class XHTMLSubtitle(XHTMLElement):
    def __init__(self, xhtml=None, xhtml_prefix=None, xhtml_namespace=None):
        """
        XHTML subtitle construction.
        Automatically add a 'type' AtomAttribute of value 'xhtml' and
        a 'div' AtomElement with the prefix and namespace provided.
        The xhtml string will be attached to that div element.
        
        Keyword arguments:
        xhtml -- XHTML content as a Python string/unicode object
        xhtml_prefix -- prefix of the content
        xhtml_namespace -- namespace of the content
        """
        XHTMLElement.__init__(self, name=u'subtitle', xhtml=xhtml,
                              xhtml_prefix=xhtml_prefix, xhtml_namespace=xhtml_namespace)

class PlainTextSummary(PlainTextElement):
    def __init__(self, text=None):
        """
        Plain text summary construction.
        Automatically add a 'type' AtomAttribute of value 'text'.
        
        Keyword arguments:
        text -- Plain text content
        """
        PlainTextElement.__init__(self, name=u'summary', text=text)
        
class HTMLSummary(HTMLElement):
    def __init__(self, escaped_html=None):
        """
        HTML summary construction.
        Automatically add a 'type' AtomAttribute of value 'html'.
        
        Keyword arguments:
        escaped_html -- Escaped HTML text.
        """
        HTMLElement.__init__(self, name=u'summary', escaped_html=escaped_html)
        
class XHTMLSummary(XHTMLElement):
    def __init__(self, xhtml=None, xhtml_prefix=None, xhtml_namespace=None):
        """
        XHTML summary construction.
        Automatically add a 'type' AtomAttribute of value 'xhtml' and
        a 'div' AtomElement with the prefix and namespace provided.
        The xhtml string will be attached to that div element.
        
        Keyword arguments:
        xhtml -- XHTML content as a Python string/unicode object
        xhtml_prefix -- prefix of the content
        xhtml_namespace -- namespace of the content
        """
        XHTMLElement.__init__(self, name=u'summary', xhtml=xhtml,
                              xhtml_prefix=xhtml_prefix, xhtml_namespace=xhtml_namespace)

class PlainTextRights(PlainTextElement):
    def __init__(self, text=None):
        """
        Plain text rights construction.
        Automatically add a 'type' AtomAttribute of value 'text'.
        
        Keyword arguments:
        text -- Plain text content
        """
        PlainTextElement.__init__(self, name=u'rights', text=text)
        
class HTMLRights(HTMLElement):
    def __init__(self, escaped_html=None):
        """
        HTML rights construction.
        Automatically add a 'type' AtomAttribute of value 'html'.
        
        Keyword arguments:
        escaped_html -- Escaped HTML text.
        """
        HTMLElement.__init__(self, name=u'rights', escaped_html=escaped_html)
        
class XHTMLRights(XHTMLElement):
    def __init__(self, xhtml=None, xhtml_prefix=None, xhtml_namespace=None):
        """
        XHTML rights construction.
        Automatically add a 'type' AtomAttribute of value 'xhtml' and
        a 'div' AtomElement with the prefix and namespace provided.
        The xhtml string will be attached to that div element.
        
        Keyword arguments:
        xhtml -- XHTML content as a Python string/unicode object
        xhtml_prefix -- prefix of the content
        xhtml_namespace -- namespace of the content
        """
        XHTMLElement.__init__(self, name=u'rights', xhtml=xhtml,
                              xhtml_prefix=xhtml_prefix, xhtml_namespace=xhtml_namespace)

class Link(AtomElement):
    def __init__(self, href=None, rel=None, type=None,
                 hreflang=None, title=None, length=None):
        """
        Maps to atom:link. Sets all the different link attributes.

        Keyword arguments:
        href -- IRI of this link
        rel -- Kind of link
        type -- Media type of the linked resource
        hreflang -- Language of the resource linked
        title -- Description of the linked resource
        length -- Size of the linked resource
        """
        AtomElement.__init__(self, name=u'link', value=None)
        self.href = AtomAttribute(name=u'href', value=href, parent=self)
        self.rel = AtomAttribute(name=u'rel', value=rel, parent=self)
        self.type = AtomAttribute(name=u'type', value=type, parent=self)
        self.hreflang = AtomAttribute(name=u'hreflang', value=hreflang, parent=self)
        self.title = AtomAttribute(name=u'title', value=title, parent=self)
        self.length = AtomAttribute(name=u'length', value=length, parent=self)
# Atom Publishing Protocol elements
class Workspace(AtomElement):
    def __init__(self):
        """
        Maps to app:workspace. Sets a list object named 'collections'
        containing Collection instances.
        """
        AtomElement.__init__(self, name=u'workspace', value=None)
        self.collections = []
        
class Collection(AtomElement):
    def __init__(self, href=None):
        """
        Maps to app:collection. Sets a list object named 'categories'
        containing Category instances.
        
        Keyword arguments:
        href -- IRI where to POST to the collection
        """
        AtomElement.__init__(self, name=u'collection', value=None)
        self.href = AtomAttribute(name=u'href', value=href, parent=self)
        self.categories = None # Categories instance or None
        
class Accept(AtomElement):
    def __init__(self, value=u'entry'):
        """
        Maps to app:accept
        
        Keyword arguments:
        value --
        """
        AtomElement.__init__(self, name=u'accept', value=value)
        
class Edited(AtomDateElement):
    def __init__(self, dt=None):
        """
        Maps to the app:edited element

        Keyword arguments:
        dt -- DateTime instance.If None, dt will default to utcnow()
        """
        AtomDateElement.__init__(self, name=u'edited', dt=dt)
      
class Categories(AtomElement):
    def __init__(self, fixed=None, scheme=None, href=None):
        """
        Maps to app:accept
        
        Keyword arguments:
        fixed -- True => 'yes', False => 'no', None => attribute not displayed.
        scheme -- Scheme associated with the categories
        href -- IRI
        """
        AtomElement.__init__(self, name=u'categories', value=None)
        self.categories = [] # will carry atom:category elements
        self.fixed = AtomAttribute(name=u'fixed', value=fixed, parent=self)
        self.scheme = AtomAttribute(name=u'scheme', value=scheme, parent=self)
        self.href = AtomAttribute(name=u'href', value=href, parent=self)
            
#############################################
# Atom document types
#############################################     
class AtomChildren(list):
    def __init__(self, parent=None):
        """
        List which will carry atom elements.

        Keyword arguments:
        parent -- Atom document parent of elements of this list
        """
        list.__init__(self)
        self.parent = parent
        
    def append(self, obj):
        """
        When adding a new Atom element to the list we
        propagate the prefix and namespace of the parent
        and then call sync_children on the element.
        """
        if obj.parent is None:
            obj.parent = self.parent
        if obj.prefix is None:
            obj.prefix = self.parent.prefix
        if obj.xmlns is None:
            obj.xmlns = self.parent.xmlns
        self.parent.children.append(obj)
        #obj.sync_children()
        list.append(self, obj)

    def remove(self, obj):
        """
        Remove the element from this list and from the
        parent.children list.
        """
        if obj in self.parent.children:
            self.parent.children.remove(obj)
        list.remove(self, obj)
        
class Atom(object):
    def __init__(self, name=None, prefix=None, namespace=None, parent=None):
        """
        Base class for Atom documents. Should not be instanciated
        directly. Creates a list names 'children' containing every
        AtomElements attached to the document. Also create a set
        of AtomChildren: entries, authors, categories, links and
        contributors where you can add AtomElement.
        
        Keyword arguments:
        name -- Name of the document
        prefix -- XML prefix of the element
        namespace -- XML namespace of the element
        """
        self.__dict__['parent'] = parent or self
        self.__dict__['name'] = name
        self.__dict__['prefix'] = prefix
        self.__dict__['xmlns'] = namespace
        self.__dict__['children'] = []
        self.__dict__['attributes'] = []
        for el_name in ('entries', 'authors', 'categories', 'links', 'contributors'):
            self.__dict__[el_name] = AtomChildren(self)
            
    def __setattr__(self, name, obj):
        if isinstance(obj, AtomElement):
            if obj.parent is None:
                obj.parent = self
            if obj.prefix is None:
                obj.prefix = self.prefix
            if obj.xmlns is None:
                obj.xmlns = self.xmlns
            obj.sync_children()
            self.children.append(obj)
        self.__dict__[name] = obj

    def __getattr__(self, name):
        try:
            return self.__dict__[name]
        except KeyError:
            raise AttributeError, name

    def __delattr__(self, name):
        try:
            del self.__dict__[name]
        except KeyError:
            raise AttributeError, name

    def __repr__(self):
        prefix = self.prefix
        xmlns = self.xmlns
        if (prefix not in ('', None)) and xmlns:
            return '<%s:%s xmlns:%s="%s" element at %s />' % (prefix,
                                                              self.name,
                                                              prefix,
                                                              xmlns,
                                                              hex(id(self)),)
        else:
            return "<%s element at %s />" % (self.name, hex(id(self)))

    def sync_children(self, shallow=True):
        for child in self.children:
            child.prefix = self.prefix
            child.xmlns = self.xmlns
            if not shallow:
                child.sync_children(shallow=shallow)
    
class Feed(Atom):
    def __init__(self, prefix=ATOM10_PREFIX, namespace=ATOM10_NS, parent=None):
        """
        Maps to the atom:feed element.
        
        Keyword arguments:
        prefix -- XML prefix of the element (defaults to u'atom')
        namespace -- XML namespace of the element 
        """
        Atom.__init__(self, u'feed', prefix=prefix, namespace=namespace, parent=parent)
    
class Entry(Atom):
    def __init__(self, prefix=ATOM10_PREFIX, namespace=ATOM10_NS, parent=None):
        """
        Maps to the atom:entry element.
        
        Keyword arguments:
        prefix -- XML prefix of the element (defaults to u'atom')
        namespace -- XML namespace of the element 
        """
        Atom.__init__(self, u'entry', prefix=prefix, namespace=namespace, parent=parent)
      
class Service(Atom):
    def __init__(self, prefix=ATOMPUB_PREFIX, namespace=ATOMPUB_NS, parent=None):
        """
        Maps to the app:service element.
        
        Keyword arguments:
        prefix -- XML prefix of the element (defaults to u'app')
        namespace -- XML namespace of the element 
        """
        Atom.__init__(self, u'service', prefix=prefix, namespace=namespace, parent=parent)
        for el_name in ('entries', 'authors', 'categories', 'links', 'contributors'):
            del self.__dict__[el_name]
        self.__dict__['workspaces'] = AtomChildren(self)
            
