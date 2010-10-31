#!/usr/bin/env python
# -*- coding: utf-8 -*-

#############################################
# Get the ElementTree source at:
# http://effbot.org/downloads/index.cgi#elementtree
# This version of atomixlib-et requires ElementTree 1.2.6 or above
#############################################

#try:
#    from cElementTree import Element, SubElement, parse
#    from cElementTree import ElementTree as ETX 
#except ImportError:
from elementtree.ElementTree import Element, SubElement, parse
from elementtree import ElementTree as ETX

from atomixlib import ATOM10_PREFIX, ATOM10_NS_STR, ATOM10_NS, ATOMPUB_NS_STR, \
     ATOMPUB_NS, XHTML1_NS_STR, XHTML1_NS, THR_NS, \
     ENCODING, DUMMY_URI, COMMON_PREFIXES, __version__

GENERATOR_NAME = u'atomixlib [elementtree]'

#############################################
# Helper
#############################################
def _qname(ncname, namespace=None):
    if namespace:
        return "{%s}%s" % (namespace, ncname)
    return ncname

#############################################
# Public API
#############################################
def create_empty_document(name, namespace, prefix=None, encoding=ENCODING, prefixes={}, uri=DUMMY_URI):
    """
    Create an empty document.
    Return an instance of Atomix class.

    Keyword arguments:
    name -- name of the root element
    namespace -- namespace for that element
    prefix -- default prefix attached to this document
    encoding -- encoding used throughout the XML document
    prefixes -- namespaces you might want to attach to the XML document
    uri -- base URI for the XML document created
    """
    # join any user-defined prefixes with default namespace and switch to key=URL, value=prefix
    for k, v in COMMON_PREFIXES.items():
        prefixes[v] = k
    prefixes[prefix] = namespace
    
    # update the ET namespace dict
    ETX._namespace_map.update(prefixes)
    # create root element
    return Atomix(Element(_qname(name, namespace)), encoding=ENCODING)

def create_feed(encoding=ENCODING, prefixes={}, uri=DUMMY_URI, prefix=None):
    """
    Create an empty atom feed document.
    Return an instance of Atomix class.

    Keyword arguments:
    encoding -- encoding used throughout the XML document
    prefixes -- namespaces you might want to attach to the XML document
    uri -- base URI for the XML document created
    prefix -- the default prefix for this document
    """
    return create_empty_document('feed', ATOM10_NS_STR, prefix, encoding, prefixes, uri)

def create_entry(encoding=ENCODING, prefixes={}, uri=DUMMY_URI, prefix=None):
    """
    Create an empty atom entry document.
    Return an instance of Atomix class.

    Keyword arguments:
    encoding -- encoding used throughout the XML document
    prefixes -- namespaces you might want to attach to the XML document
    uri -- base URI for the XML document created
    prefix -- the default prefix for this document
    """
    return create_empty_document('entry', ATOM10_NS_STR, prefix, encoding, prefixes, uri)
    
def create_service(encoding=ENCODING, prefixes={}, uri=DUMMY_URI, prefix=None):
    """
    Create an empty app service document to be used through the
    Atom Publishing Protocol
    Return an instance of Atomix class.

    Keyword arguments:
    encoding -- encoding used throughout the XML document
    prefixes -- namespaces you might want to attach to the XML document
    uri -- base URI for the XML document created
    prefix -- the default prefix for this document
    """
    return create_empty_document('service', ATOMPUB_NS_STR, prefix, encoding, prefixes, uri)

def create_collection(encoding=ENCODING, prefixes={}, uri=DUMMY_URI, prefix=None):
    """
    Create an empty app collection document to be used through the
    Atom Publishing Protocol
    Return an instance of Atomix class.

    Keyword arguments:
    encoding -- encoding used throughout the XML document
    prefixes -- namespaces you might want to attach to the XML document
    uri -- base URI for the XML document created
    prefix -- the default prefix for this document
    """
    return create_empty_document('collection', ATOMPUB_NS_STR, prefix, encoding, prefixes, uri)

def load(source, encoding=ENCODING, prefixes={}, uri=DUMMY_URI):
    """
    Load an Atom or Atom Publishing Protocol document and parse it.
    Returns an instance of Atomix class.

    Keyword arguments:
    source -- can be a string, a path, an URI or a file object
    encoding -- encoding used throughout the XML document
    prefixes -- namespaces you might want to attach to the XML document
    uri -- base URI for the XML document created (only required when source is a string)
    """
    
    for k, v in COMMON_PREFIXES.items():
        prefixes[v] = k
    # update the ET namespace dict
    ETX._namespace_map.update(prefixes)
    
    return Atomix(ETX.parse(source), encoding=ENCODING)

class Atomix:
    """
    Provides the API to generate Atom 1.0 documents and
    handle the Atom Publishing Protocol service document.
    The methods of this class follows the Atom specification closely.
    It supports all the atom elements except atom:source.

    Atomix holds an internal cursor to the current element under edition
    Each method adds an atom element to the element handled by the cursor.

    Only adding an entry will change the internal cursor to the newly created
    entry. Nontheless, if you need to come back to a specific atom element (feed or entry)
    you can set the cursor to the requested element.

    For example:

    atom : create_feed() # sets the cursor to atom.doc.feed
    atom.add_entry() # changes the cursor to atom.doc.feed.entry[-1]
    atom.cursor = atom.doc.feed # oops let's come back to the feed element for a while

    This should be rarely used as long as you create your atom document sequentially.

    Atomix also holds the namespace prefix used for XHTML input. By default it falls back
    to '' so that you do not need to specify the namespace prefix at all. But if you need
    to set a specific one simply do this:

    atom = create_feed()
    atom.xhtmlprefix = 'xhtml'
    atom.add_entry()
    atom.add_content('<xhtml:b>yeah</xhtml:b>', target='inlineXHTML')
    """
    def __init__(self, atom, encoding=ENCODING):
        """
        initialize an Atomix instance
        
        Keyword arguments:
        atom -- an ElementTree Element instance (the <atom:feed> root element)
        encoding -- the encoding used throughout the XML document
        """
        self.doc = atom
        self.encoding = encoding
        self.xhtmlprefix = ''
            
        # using ElementTree, the doc is already either 'atom:feed', 'atom:entry' or 'app:service' 
        # so no need to distinguish
        self.cursor = self.doc

        self.default_prefix = ATOM10_PREFIX
        self.default_namespace = ATOM10_NS
        
    def __str__(self):
        """
        return an unindented version of the XML document as a string
        """
        #TODO: indentation?
        # bah ET does not support indentation... too bad
        # return self.doc.xml(encoding=self.encoding)
        return ETX.tostring(self.doc, encoding=self.encoding)

    def xml(self, indent='no'):
        """
        return the atom document as a string

        Keyword arguments:
        indent -- specifies whether or not the result should be indented

        note that indentation is not yet supported with ElementTree
        """
        #TODO: indentation?
        # bah ET does not support indentation... too bad
        #return self.doc.xml(indent=indent, encoding=self.encoding)
        return ETX.tostring(self.doc, encoding=self.encoding)

    def _qname(self, ncname, namespace=None):
        if not namespace:
            namespace = self.default_namespace
        return _qname(ncname, namespace)

    ###########################################################
    # Support for Atom 1.0 a defined in RFC 4287
    ###########################################################
    def add_entry(self, prefix=None, namespace=None):
        """
        insert an atom:entry element into the Atom document
        it will set the internal cursor to the newly created entry.
        
        returns the newly created entry.
        """
        if not prefix:
            prefix = self.default_prefix
        if not namespace:
            namespace = self.default_namespace
        self.doc.append(Element(self._qname('entry', namespace)))
        self.cursor = self.doc[-1]

        return self.cursor

    def add_id(self, uri, prefix=None, namespace=None):
        """
        insert an atom:id element into the Atom document

        Keyword arguments:
        uri -- the id value as an URI
        """
        if not prefix:
            prefix = self.default_prefix
        if not namespace:
            namespace = self.default_namespace
        self.cursor.append(Element(self._qname('id', namespace)))
        self.cursor[-1].text = uri

    def add_author(self, name, email=None, uri=None, prefix=None, namespace=None):
        """
        insert an atom:author element into the Atom document

        Keyword arguments:
        name -- the name of the author
        email -- the email of the author, appended only if provided
        uri -- the uri of the author, appended only if provided
        """
        if not prefix:
            prefix = self.default_prefix
        if not namespace:
            namespace = self.default_namespace
        self.cursor.append(Element(self._qname('author', namespace)))
        construct_person(self.cursor[-1], name, email, uri, prefix=prefix, namespace=namespace)
        
    def add_category(self, term, scheme=None, label=None, prefix=None, namespace=None):
        """
        insert an atom:category element into the Atom document

        Keyword arguments:
        term -- the term defining the category
        scheme -- appended only if provided
        label -- a friendly user label of the category, appended only if provided
        """
        if not prefix:
            prefix = self.default_prefix
        if not namespace:
            namespace = self.default_namespace
        self.cursor.append(Element(self._qname('category', namespace)))
        add_attribute(self.cursor[-1], u'term', term)
        add_attribute(self.cursor[-1], u'scheme', scheme)
        add_attribute(self.cursor[-1], u'label', label)

    def add_contributor(self, name, email=None, uri=None, prefix=None, namespace=None):
        """
        insert an atom:contributor element into the Atom document

        Keyword arguments:
        name -- the name of the author
        email -- the email of the author, appended only if provided
        uri -- the uri of the author, appended only if provided
        """
        if not prefix:
            prefix = self.default_prefix
        if not namespace:
            namespace = self.default_namespace
        self.cursor.append(Element(self._qname('contributor', namespace)))
        construct_person(self.cursor[-1], name, email, uri, prefix=prefix, namespace=namespace)

    def add_generator(self, value=GENERATOR_NAME, uri=None, version=None, prefix=None, namespace=None):
        """
        insert an atom:generator element into the Atom document

        Keyword arguments:
        value -- the representation as a string of the generator
        uri -- the uri of the author, appended only if provided
        version -- the version of the generator
        """
        if not prefix:
            prefix = self.default_prefix
        if not namespace:
            namespace = self.default_namespace
        self.cursor.append(Element(self._qname('generator', namespace)))
        self.cursor[-1].text = value
        add_attribute(self.cursor[-1], u'uri', uri)
        if value == GENERATOR_NAME and version == None:
            # automatically add this module's version
            add_attribute(self.cursor[-1], u'version', __version__)
        else:
            add_attribute(self.cursor[-1], u'version', version)

    def add_icon(self, uri, prefix=None, namespace=None):
        """
        insert an atom:icon element into the Atom document

        Keyword arguments:
        uri -- the uri of the author, appended only if provided
        """
        if not prefix:
            prefix = self.default_prefix
        if not namespace:
            namespace = self.default_namespace
        self.cursor.append(Element(self._qname('icon', namespace)))
        self.cursor[-1].text = uri

    def add_title(self, title, mediaType='text', prefix=None, namespace=None):
        """
        insert an atom:title element into the Atom document

        Keyword arguments:
        title -- title value to be added
        mediaType -- media type used for the title (text, html or xhtml)
        """
        if not prefix:
            prefix = self.default_prefix
        if not namespace:
            namespace = self.default_namespace
        self.cursor.append(Element(self._qname('title', namespace)))
        _text_construct_mapper[mediaType](self.cursor[-1], title, self.encoding,
                                          self.xhtmlprefix, prefix=prefix, namespace=namespace)

    def add_updated(self, isoDate=None, prefix=None, namespace=None):
        """
        insert an atom:updated element into the Atom document

        Keyword arguments:
        isoDate -- value of the date respecting ISO 8601 format
        """
        if not prefix:
            prefix = self.default_prefix
        if not namespace:
            namespace = self.default_namespace
        self.cursor.append(Element(self._qname('updated', namespace)))
        construct_date(self.cursor[-1], isoDate)

    def add_published(self, isoDate=None, prefix=None, namespace=None):
        """
        insert an atom:published element into the Atom document

        Keyword arguments:
        isoDate -- value of the date respecting ISO 8601 format
        """
        if not prefix:
            prefix = self.default_prefix
        if not namespace:
            namespace = self.default_namespace
        self.cursor.append(Element(self._qname('published', namespace)))
        construct_date(self.cursor[-1], isoDate, prefix=prefix, namespace=namespace)
    
    def add_link(self, href, rel=None, mediaType=None, hreflang=None,
                 title=None, length=None, prefix=None, namespace=None):
        """
        insert an atom:link element into the Atom document

        Keyword arguments:
        href -- the URI of the link
        rel -- the type of the link
        mediaType -- the media type of the link
        hreflang -- the language of the link
        title -- a lable for the link
        length -- the length of the resource targeted by the URI
        """
        if not prefix:
            prefix = self.default_prefix
        if not namespace:
            namespace = self.default_namespace
        
        self.cursor.append(Element(self._qname('link', namespace)))
        add_attribute(self.cursor[-1], u'href', href)
        add_attribute(self.cursor[-1], u'rel', rel)
        add_attribute(self.cursor[-1], u'type', mediaType)
        add_attribute(self.cursor[-1], u'hreflang', hreflang)
        add_attribute(self.cursor[-1], u'title', title)
        add_attribute(self.cursor[-1], u'length', length)
        
    def add_logo(self, uri, prefix=None, namespace=None):
        """
        insert an atom:logo element into the Atom document

        Keyword arguments:
        uri -- the uri of the author, appended only if provided
        """
        if not prefix:
            prefix = self.default_prefix
        if not namespace:
            namespace = self.default_namespace
        self.cursor.append(Element(self._qname('logo', namespace)))
        self.cursor[-1].text = uri

    def add_rights(self, text, mediaType=u'text', prefix=None, namespace=None):
        """
        insert an atom:rights element into the Atom document

        Keyword arguments:
        text -- rights value to be added
        mediaType -- media type used for the rights (text, html or xhtml)
        """
        if not prefix:
            prefix = self.default_prefix
        if not namespace:
            namespace = self.default_namespace
        self.cursor.append(Element(self._qname('rights', namespace)))
        _text_construct_mapper[mediaType](self.cursor[-1], text, self.encoding,
                                          self.xhtmlprefix, prefix=prefix, namespace=namespace)
        
    def add_subtitle(self, text, mediaType=u'text', prefix=None, namespace=None):
        """
        insert an atom:subtitle element into the Atom document

        Keyword arguments:
        text -- subtitle value to be added
        mediaType -- media type used for the subtitle (text, html or xhtml)
        """
        if not prefix:
            prefix = self.default_prefix
        if not namespace:
            namespace = self.default_namespace
        self.cursor.append(Element(self._qname('subtitle', namespace)))
        _text_construct_mapper[mediaType](self.cursor[-1], text, self.encoding,
                                          self.xhtmlprefix, prefix=prefix, namespace=namespace)

    def add_summary(self, text, mediaType=u'text', prefix=None, namespace=None):
        """
        insert an atom:summary element into the Atom document

        Keyword arguments:
        text -- summary to be added
        mediaType -- media type used for the summary (text, html or xhtml)
        """
        if not prefix:
            prefix = self.default_prefix
        if not namespace:
            namespace = self.default_namespace
        self.cursor.append(Element(self._qname('summary', namespace)))
        _text_construct_mapper[mediaType](self.cursor[-1], text, self.encoding, self.xhtmlprefix)

    def add_content(self, text='', target='inlineText', src=None, mediaType=None, prefix=None, namespace=None):
        """
        insert an atom:content element into the Atom document

        Keyword arguments:
        text -- the actual content
        target -- the type of content 
        src -- the source of the actual content
        mediaType -- if src is provided, media-type of the source
        """
        if not prefix:
            prefix = self.default_prefix
        if not namespace:
            namespace = self.default_namespace
        self.cursor.append(Element(self._qname('content', namespace)))
        if target in ['inlineText', 'inlineOther']:
            construct_plain_text(self.cursor[-1], text, self.encoding,
                                 prefix=prefix, namespace=namespace)
        elif target == 'inlineXHTML':
            construct_xhtml_text(self.cursor[-1], text, self.encoding, self.xhtmlprefix,
                                 prefix=prefix, namespace=namespace)
        elif target == 'inlineHTML':
            construct_html_text(self.cursor[-1], text, self.encoding,
                                prefix=prefix, namespace=namespace)
        elif target == 'outOfLine':
            construct_out_of_line_content(self.cursor[-1], mediaType, src)

    def copy_foreign_content(self, fragment, prefix=None, namespace=None):
        """
        insert an atom:content with a fragment child node.

        Keyword arguments:
        fragment -- ElementTree fragment instance
        """
        if not prefix:
            prefix = self.default_prefix
        if not namespace:
            namespace = self.default_namespace
        self.cursor.append(Element(self._qname('content', namespace)))
        self.cursor[-1].append(fragment)

    ###########################################################
    # Support for Atom Feed Thread Extension (RFC 4685)
    ###########################################################
    def add_in_reply_to(self, ref, href=None, type=u'application/atom+xml',
                        source=None, prefix=None, namespace=None):
        """
        insert a thr:in-reply-to element to the Atom document

        Keyword arguments:
        ref -- identifier of the resource being responded to
        href -- IRI to retrieve the resource
        type -- media-type of the resource responded to
        source -- IRI of a feed or entry containing the resource responded to
        """
        if not prefix:
            prefix = self.default_prefix
        if not namespace:
            namespace = self.default_namespace
        self.cursor.append(Element(self._qname('in-reply-to', namespace)))

        add_attribute(self.cursor[-1], u'ref', ref)
        if href:
            add_attribute(self.cursor[-1], u'type', type)
            add_attribute(self.cursor[-1], u'href', href)
        add_attribute(self.cursor[-1], u'source', source)

    def add_replies_link(self, href, count, mediaType='application/atom+xml',
                         isoDate=None, prefix=None, namespace=None):
        """
        add an atom:link rel='replies' to the Atom document

        Keyword arguments:
        href -- IRI of the resource containing the replies
        count -- hint about the number of responses
        mediaType -- media-type of the resource holding the replies
        isoDate -- hint about the most updated reply
        """
        if not prefix:
            prefix = self.default_prefix
        if not namespace:
            namespace = self.default_namespace
        self.add_link(href, rel='replies', mediaType=mediaType)
        
        add_attribute(self.cursor.link[-1], u'count', count)
        if not isoDate:
            isoDate = get_isodate()
        add_attribute(self.cursor.link[-1], u'updated', isoDate)

    def add_total_replies(self, value, prefix=None, namespace=None):
        """
        add a thr:total element to the Atom document

        Keyword arguments:
        value -- total number of unique responses to an entry known to the publisher
        """
        if not prefix:
            prefix = self.default_prefix
        if not namespace:
            namespace = self.default_namespace
        self.cursor.xml_append(Element(self._qname('total', namespace)))
        self.cursor.total[-1].text = value

    ###########################################################
    # Support for the Atom Publishing Protocol
    ###########################################################
    def add_workspace(self, title, prefix=None, namespace=None):
        """
        insert an app:workspace element to the service document
        set the current cursor to that element

        Keyword arguments:
        title -- label of the workspace

        return the workspace created
        """
        if not prefix:
            prefix = self.default_prefix
        if not namespace:
            namespace = self.default_namespace
        self.doc.append(Element(self._qname('service', namespace)))
        add_attribute(self.cursor.workspace[-1], u'title', title)
        self.cursor = self.doc.service.workspace[-1]

        return self.cursor
    
    def add_edited(self, isoDate=None, prefix=None, namespace=None):
        """
        insert an app:edited element into the document

        Keyword arguments:
        isoDate -- value of the date respecting ISO 8601 format
        """
        if not prefix:
            prefix = self.default_prefix
        if not namespace:
            namespace = self.default_namespace
            self.doc.append(Element(self._qname('edited', namespace)))
        construct_date(self.cursor[-1], isoDate)

    def add_categories(self, fixed=False, scheme=None, href=None,
                       collection=None, prefix=None, namespace=None):
        """
        insert an app:categories element to an app:collection
        set the cursor to the categories

        Keyword arguments:
        fixed -- indicates whether or not the set of categories is fixed
                 True means 'yes', False means 'no'
                 and None means the attribute won't be output
        scheme -- IRI that identifies a categorization scheme
        href -- IRI reference identifying a Category Document
                if provided, fixed and scheme will be ignored

        return the categories created
        """
        if not prefix:
            prefix = self.default_prefix
        if not namespace:
            namespace = self.default_namespace
        if collection is None:
            collection = self.cursor

        collection.append(Element(self._qname('categories', namespace)))
        categories = collection.categories[-1]
        
        if href:
            add_attribute(categories, u'href', href)
        else:
            if fixed in (True, False):
                if fixed is True:
                    add_attribute(categories, u'fixed', u'yes')
                elif fixed is False:
                    add_attribute(categories, u'fixed', u'no')
            
                if scheme:
                    add_attribute(categories, u'scheme', scheme)
                    
        self.cursor = categories
        return categories
    
    def add_collection(self, href, workspace=None, prefix=None, namespace=None):
        """
        insert an app:collection element to an app:workspace element
        set the cursor to the collection
        
        Keyword arguments:
        href -- IRI of the feed representing the collection
        workspace -- if provided attach the collection to that element

        return the created collection
        """
        if not prefix:
            prefix = self.default_prefix
        if not namespace:
            namespace = self.default_namespace
        if workspace is None:
            workspace = self.cursor
            
        workspace.append(Element(self._qname('collection', namespace)))
        collection = workspace.collection[-1]
        add_attribute(collection, u'href', href)
        self.cursor = collection
        
        return collection

    def add_accept(self, value, collection=None, prefix=None, namespace=None):
        """
        insert an app:accept element to an app:collection element
        
        Keyword arguments:
        value -- comma seperated string of accepted media-types
        collection -- if provided attach the accept element to that collection
        """
        if not prefix:
            prefix = self.default_prefix
        if not namespace:
            namespace = self.default_namespace
        if collection is None:
            collection = self.cursor
            
        collection.append(Element(self._qname('accept', namespace)))
        add_text(collection.accept[-1], value)
    
    def add_control(self):
        """
        insert a app:control element to an Atom entry
        set the cursor to the newly created element
        
        return the created element
        """
        if not prefix:
            prefix = self.default_prefix
        if not namespace:
            namespace = self.default_namespace
        self.cursor.append(Element(self._qname('control', namespace)))
        self.cursor = self.cursor.control[-1]
        
        return self.cursor
        
    def add_draft(self, value=u'no', prefix=None, namespace=None):
        """
        insert a app:draft element to a pub:control element

        Keyword arguments:
        value -- 'yes' to say the entry MAY not be publicly visible,'no' otherwise (default to 'no')
        """
        if not prefix:
            prefix = self.default_prefix
        if not namespace:
            namespace = self.default_namespace
        self.cursor.append(Element(self._qname('draft', namespace)))
        self.cursor.draft[-1].text = value
        
#############################################
# Helper internal functions
# Private API
#############################################

def construct_person(node, name, email=None, uri=None, prefix=None, namespace=None):
    #TODO: remove doc parameter
    
    node.append(Element(_qname('name', namespace)))
    node[-1].text = name

    if email:
        node.append(Element(_qname('email', namespace)))
        node[-1].text = email

    if uri:
        node.append(Element(_qname('uri', namespace)))
        node[-1].text = uri
        
def construct_plain_text(node, text, encoding, unused=None, prefix=None, namespace=None):
    node.set(u'type', u'text')
    node.text = text

def construct_html_text(node, html, encoding, unused=None, prefix=None, namespace=None):
    node.set(u'type', u'html')
    node.text = html

def construct_xhtml_text(node, xhtml, encoding, xhtmlprefix):
    node.set(u'type', u'xhtml')
    try:
        if xhtmlprefix:
            nodediv = Element('{%s}div' % XHTML1_NS)
            nodediv.append(ETX.XML(xhtml))
            node.append(nodediv)
            #node.append(ETX.XML('<%s:div xmlns:%s="%s">%s</%s:div>' %
                        #(xhtmlprefix, xhtmlprefix, XHTML1_NS_STR, xhtml, xhtmlprefix))) #,
                        #encoding=encoding)
        else:
            nodediv = Element('div', {'xmlns': XHTML1_NS})
            nodediv.append(ETX.XML(xhtml))
            node.append(nodediv)
    except:
        # attempt to parse by wrapping xhtml in div
        nodediv = ETX.XML('<div xmlns="%s">%s</div>' % (XHTML1_NS, xhtml))
        node.append(nodediv)

def construct_out_of_line_content(node, text, mediaType, src, encoding):
    node.set(u'type', mediaType)
    node.set(u'src', src)
    node.text = text

def get_isodate():
    """
    returns a date respecting ISO 8601 format
    """
    import datetime
    return unicode(datetime.datetime.utcnow().isoformat() + 'Z')

def construct_date(node, isoDate=None):
    if not isoDate:
        isoDate = get_isodate()
    node.text = isoDate
    
def add_attribute(node, name, value):
    if value:
        node.set(name, value)

_text_construct_mapper = {
    u'text': construct_plain_text,
    u'html': construct_html_text,
    u'xhtml': construct_xhtml_text
    }
