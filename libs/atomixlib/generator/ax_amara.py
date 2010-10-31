#!/usr/bin/env python
# -*- coding: utf-8 -*-

#############################################
# A big thanks to Uche Ogbuji
# (http://copia.ogbuji.net/blog/)
# for his help to improve atomixlib
# specially for the cursor idea :)
#############################################

##############################################################
# Get the excellent Amara toolkit at:
# http://uche.ogbuji.net/uche.ogbuji.net/tech/4suite/amara/
# This version of atomixlib requires Amara 1.1.9 or above
# It won't work with Amara 1.0
##############################################################
import amara
from atomixlib.lib.ax_exceptions import AtomixlibException
from atomixlib import ATOM10_NS_STR, ATOM10_NS, ATOMPUB_NS_STR, \
     ATOMPUB_NS, XHTML1_NS_STR, XHTML1_NS, THR_NS, \
     ENCODING, DUMMY_URI, COMMON_PREFIXES, __version__

GENERATOR_NAME = u'atomixlib [amara]'

#############################################
# Helper
#############################################
def _qname(ncname, prefix=None):
    if prefix:
        return "%s:%s" % (prefix, ncname)
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
    for p in COMMON_PREFIXES:
        if p != prefix:
            prefixes[p] = COMMON_PREFIXES[p]
    if prefix not in (None, ''):
        return Atomix(amara.parse('<%s:%s xmlns:%s="%s"/>' % (prefix, name, prefix, namespace),
                                  uri=uri,
                                  prefixes=prefixes),
                      encoding=ENCODING)

    
    return Atomix(amara.parse('<%s xmlns="%s"/>' % (name, namespace),
                              uri=uri,
                              prefixes=prefixes),
                  encoding=ENCODING)

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

def create_workspace(encoding=ENCODING, prefixes={}, uri=DUMMY_URI, prefix=None):
    """
    Create an empty app workspace document to be used through the
    Atom Publishing Protocol
    Return an instance of Atomix class.

    Keyword arguments:
    encoding -- encoding used throughout the XML document
    prefixes -- namespaces you might want to attach to the XML document
    uri -- base URI for the XML document created
    prefix -- the default prefix for this document
    """
    return create_empty_document('workspace', ATOMPUB_NS_STR, prefix, encoding, prefixes, uri)

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
    prefixes.update(COMMON_PREFIXES)
    # In the case where the source is a string, we need the uri as well
    if isinstance(source, basestring):
        return Atomix(amara.parse(source, uri=uri,
                                  prefixes=prefixes),
                      encoding=ENCODING)
    
    return Atomix(amara.parse(source,
                              prefixes=prefixes),
                  encoding=ENCODING)

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
        atom -- an amara bindery instance
        encoding -- the encoding used throughout the XML document
        """
        self.doc = atom
        self.encoding = encoding
        self.xhtmlprefix = ''
        self.cursor = self.doc.xml_children[0]

        self.default_prefix = self.cursor.prefix
        self.default_namespace = self.cursor.namespaceURI

    def __str__(self):
        """
        return an unindented version of the XML document as a string
        """
        return self.doc.xml(encoding=self.encoding)

    def xml(self, indent='no'):
        """
        return the atom document as a string

        Keyword arguments:
        indent -- specifies whether or not the result should be indented
        """
        return self.doc.xml(indent=indent, encoding=self.encoding)

    def _qname(self, ncname, prefix=None):
        if not prefix:
            prefix = self.default_prefix
            
        return _qname(ncname, prefix)
    
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
        self.doc.feed.xml_append(self.doc.xml_create_element(self._qname(u"entry", prefix=prefix),
                                                             ns=namespace))
        self.cursor = self.doc.feed.entry[-1]

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
        self.cursor.xml_append(self.doc.xml_create_element(self._qname(u"id", prefix=prefix),
                                                           ns=namespace))
        self.cursor.id = uri

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
        self.cursor.xml_append(self.doc.xml_create_element(self._qname(u"author", prefix=prefix), ns=namespace))
        construct_person(self.doc, self.cursor.author[-1], name, email, uri, prefix=prefix, namespace=namespace)
        
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
        self.cursor.xml_append(self.doc.xml_create_element(self._qname(u"category", prefix=prefix), ns=namespace))
        add_attribute(self.cursor.category[-1], u'term', term)
        add_attribute(self.cursor.category[-1], u'scheme', scheme)
        add_attribute(self.cursor.category[-1], u'label', label)

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
        self.cursor.xml_append(self.doc.xml_create_element(self._qname(u"contributor", prefix=prefix), ns=namespace))
        construct_person(self.doc, self.cursor.contributor[-1], name, email, uri, prefix=prefix, namespace=namespace)

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
        self.cursor.xml_append(self.doc.xml_create_element(self._qname(u"generator", prefix=prefix), ns=namespace))
        self.cursor.generator[-1] = value
        add_attribute(self.cursor.generator[-1], u'uri', uri)
        if value == GENERATOR_NAME and version == None:
            # automatically add this module's version
            add_attribute(self.cursor.generator[-1], u'version', unicode(__version__))
        else:
            add_attribute(self.cursor.generator[-1], u'version', version)

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
        self.cursor.xml_append(self.doc.xml_create_element(self._qname(u"icon", prefix=prefix),
                                                           ns=namespace))
        self.cursor.icon[-1] = uri

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
        self.cursor.xml_append(self.doc.xml_create_element(self._qname(u'title', prefix=prefix),
                                                           ns=namespace))
        _text_construct_mapper[mediaType](self.cursor.title[-1], title,
                                          self.encoding, self.xhtmlprefix,
                                          prefix=prefix, namespace=namespace)

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
        self.cursor.xml_append(self.doc.xml_create_element(self._qname(u"updated", prefix=prefix),
                                                           ns=namespace))
        construct_date(self.cursor.updated[-1], isoDate)

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
        self.cursor.xml_append(self.doc.xml_create_element(self._qname(u"published", prefix=prefix), ns=namespace))
        construct_date(self.cursor.published[-1], isoDate)
    
    def add_link(self, href, rel=None, mediaType=None,
                 hreflang=None, title=None, length=None, prefix=None, namespace=None):
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
        self.cursor.xml_append(self.doc.xml_create_element(self._qname(u"link", prefix=prefix), ns=namespace))
 
        add_attribute(self.cursor.link[-1], u'href', href)
        add_attribute(self.cursor.link[-1], u'rel', rel)
        add_attribute(self.cursor.link[-1], u'type', mediaType)
        add_attribute(self.cursor.link[-1], u'hreflang', hreflang)
        add_attribute(self.cursor.link[-1], u'title', title)
        add_attribute(self.cursor.link[-1], u'length', length)
        
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
        self.cursor.xml_append(self.doc.xml_create_element(self._qname(u'logo', prefix=prefix), ns=namespace))
        self.cursor.logo[-1] = uri

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
        self.cursor.xml_append(self.doc.xml_create_element(self._qname(u'rights', prefix=prefix), ns=namespace))
        _text_construct_mapper[mediaType](self.cursor.rights[-1], text,
                                          self.encoding, self.xhtmlprefix, prefix=prefix, namespace=namespace)
        
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
        self.cursor.xml_append(self.doc.xml_create_element(self._qname(u'subtitle', prefix=prefix), ns=namespace))
        _text_construct_mapper[mediaType](self.cursor.subtitle[-1], text,
                                          self.encoding, self.xhtmlprefix, prefix=prefix, namespace=namespace)

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
        self.cursor.xml_append(self.doc.xml_create_element(self._qname(u'summary', prefix=prefix), ns=namespace))
        _text_construct_mapper[mediaType](self.cursor.summary[-1], text,
                                          self.encoding, self.xhtmlprefix, prefix=prefix, namespace=namespace)

    def add_content(self, text='', target='inlineText',
                    src=None, mediaType=None, prefix=None, namespace=None):
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
        self.cursor.xml_append(self.doc.xml_create_element(self._qname(u'content', prefix=prefix), ns=namespace))
        if target in ['inlineText', 'inlineOther']:
            construct_plain_text(self.cursor.content[-1], text, self.encoding,
                                 prefix=prefix, namespace=namespace)
        elif target == 'inlineXHTML':
            construct_xhtml_text(self.cursor.content[-1], text, self.encoding, self.xhtmlprefix,
                                 prefix=prefix, namespace=namespace)
        elif target == 'inlineHTML':
            construct_html_text(self.cursor.content[-1], text, self.encoding,
                                prefix=prefix, namespace=namespace)
        elif target == 'outOfLine':
            construct_out_of_line_content(self.cursor.content[-1], mediaType, src,
                                          prefix=prefix, namespace=namespace)

    def copy_foreign_content(self, fragment, prefix=None, namespace=None):
        """
        insert an atom:content with a fragment child node.

        Keyword arguments:
        fragment -- Amara fragment instance
        """
        if not prefix:
            prefix = self.default_prefix
        if not namespace:
            namespace = self.default_namespace
        self.cursor.xml_append(self.doc.xml_create_element(self._qname(u'content', prefix=prefix), ns=namespace))
        self.cursor.content[-1].xml_append(fragment)

    ###########################################################
    # Support for Atom Feed Thread Extension (RFC 4685)
    ###########################################################
    def add_in_reply_to(self, ref, href=None,
                        mediaType=u'application/atom+xml', source=None, prefix=None, namespace=None):
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
        self.cursor.xml_append(self.doc.xml_create_element(self._qname(u'in-reply-to', prefix=prefix), ns=namespace))

        add_attribute(self.cursor.in_reply_to[-1], u'ref', ref)
        if href:
            add_attribute(self.cursor.in_reply_to[-1], u'type', mediaType)
            add_attribute(self.cursor.in_reply_to[-1], u'href', href)
        add_attribute(self.cursor.in_reply_to[-1], u'source', source)

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
        
        add_attribute(self.cursor.link[-1], self._qname(u'count', prefix=prefix), count)
        if not isoDate:
            isoDate = get_isodate()
        add_attribute(self.cursor.link[-1], self._qname(u'updated', prefix=prefix), isoDate)

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
        self.cursor.xml_append(self.doc.xml_create_element(self._qname(u'total', prefix=prefix),
                                                           ns=namespace))
        self.cursor.total[-1].xml_children.append(value)

    ###########################################################
    # Support for the Atom Publishing Protocol
    ###########################################################
    def add_workspace(self, prefix=None, namespace=None):
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
        self.doc.service.xml_append(self.doc.xml_create_element(self._qname(u'workspace', prefix=prefix),
                                                                ns=namespace))
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
        self.cursor.xml_append(self.doc.xml_create_element(self._qname(u"edited", prefix=prefix),
                                                           ns=namespace))
        construct_date(self.cursor.edited[-1], isoDate)

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

        collection.xml_append(self.doc.xml_create_element(self._qname(u'categories', prefix=prefix),
                                                          ns=namespace))
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
            
        workspace.xml_append(self.doc.xml_create_element(self._qname(u'collection', prefix=prefix),
                                                         ns=namespace))
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
            
        collection.xml_append(self.doc.xml_create_element(self._qname(u'accept', prefix=prefix),
                                                          ns=namespace))
        add_text(collection.accept[-1], value)
    

    def add_control(self, prefix=None, namespace=None):
        """
        insert an app:control element to an Atom entry
        set the cursor to the newly created element
        
        return the created element
        """
        if not prefix:
            prefix = self.default_prefix
        if not namespace:
            namespace = self.default_namespace
        self.cursor.xml_append(self.doc.xml_create_element(self._qname(u'control', prefix=prefix),
                                                           ns=namespace))
        self.cursor = self.cursor.contro[-1]
        
        return self.cursor
        
    def add_draft(self, value=u'no', prefix=None, namespace=None):
        """
        insert an app:draft element to a pub:control element

        Keyword arguments:
        value -- 'yes' to say the entry MAY not be publicly visible,'no' otherwise (default to 'no')
        """
        if not prefix:
            prefix = self.default_prefix
        if not namespace:
            namespace = self.default_namespace
        self.cursor.xml_append(self.doc.xml_create_element(self._qname(u'draft', prefix=prefix),
                                                           ns=namespace))
        self.cursor.draft[-1].xml_children.append(value)
        
#############################################
# Helper internal functions
# Private API
#############################################

def construct_person(doc, node, name, email=None, uri=None, prefix=None, namespace=None):
    node.xml_append(doc.xml_create_element(_qname(u"name", prefix), ns=namespace))
    node.name = name

    if email:
        node.xml_append(doc.xml_create_element(_qname(u"email", prefix), ns=namespace))
        node.email = email

    if uri:
        node.xml_append(doc.xml_create_element(_qname(u"uri", prefix), ns=namespace))
        node.uri = uri
        
def construct_plain_text(node, text, encoding, unused=None, prefix=None, namespace=None):
    node.xml_set_attribute(u'type', u'text')
    node.xml_children.append(text)

def construct_html_text(node, html, encoding, unused=None, prefix=None, namespace=None):
    node.xml_set_attribute(u'type', u'html')
    node.xml_children.append(html)

def construct_xhtml_text(node, xhtml, encoding, xhtmlprefix, prefix=None, namespace=None):
    node.xml_set_attribute(u'type', u'xhtml')
    if xhtmlprefix:
        node.xml_append_fragment('<%s:div xmlns:%s="%s">%s</%s:div>' %
                                 (xhtmlprefix, xhtmlprefix, XHTML1_NS_STR, xhtml, xhtmlprefix),
                                 encoding=encoding)
    else:
        node.xml_append_fragment('<div xmlns="%s">%s</div>' % (XHTML1_NS_STR, xhtml, ),
                                 encoding=encoding)

def construct_out_of_line_content(node, mediaType, src, prefix=None, namespace=None):
    node.xml_set_attribute(u'type', mediaType)
    node.xml_set_attribute(u'src', src)

def get_isodate(dt=None):
    """
    returns a date respecting ISO 8601 format
    """
    import datetime
    if not dt:
        dt = datetime.datetime.utcnow()
    return unicode(dt.isoformat() + 'Z')

def parse_isodate(dt):
    from amara import dateutil_standins
    return dateutil_standins.parse_isodate(dt)

def construct_date(node, isoDate=None):
    if not isoDate:
        isoDate = get_isodate()
    node.xml_children.append(isoDate)
    
def add_attribute(node, name, value):
    if value:
        node.xml_set_attribute(name, value)

def add_text(node, text, prefix=None):
    node.xml_children.append(text)

_text_construct_mapper = {
    u'text': construct_plain_text,
    u'html': construct_html_text,
    u'xhtml': construct_xhtml_text
    }
