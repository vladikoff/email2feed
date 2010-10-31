#!/usr/bin/env python
# -*- coding: utf-8 -*-

__doc__ = """
atomixlib handlers try to provide a higher level interface to
the atomixlib original generators.

This interface offers a way to manipulate Atom documents such as
feed and entry but also documents from the Atom Publishing Protocol.

Another goal of this interface is to provide a flexible way to
run validators and sortables on those Atom documents.

Typical usage would look like this:

  g = atomixlib.get_generator('amara')
  h = atomixlib.get_handler('amara')
  f = g.load('feed.xml')
  fh = h.Feed(f)
  udv = h.URNUUIDValidator()
  fh.validate(udv, xpath=u'//atom:id')
    # [<amara.bindery.id object at 0xb764476c>]
  fh.validate(udv, xpath=u'//atom:id', raise_error=True)
    # atomixlib.lib.ax_exceptions.AtomixlibValidatorError: \
      Wrong UUID format for element <amara.bindery.id object at 0xb764476c>

  # transform via XSLT 1.0
  fh.transform('/path/to/styleshet.xsl')

  # sort entries of feed per their published dates
  uds = h.PublishedSortable()
  fh.sort(uds)
"""

import re
from urlparse import urlparse

from Ft.Xml.Xvif import RelaxNgValidator
from Ft.Xml import InputSource
from Ft.Lib import Uri
from Ft.Xml.Xslt import Processor
from Ft.Lib.Uri import OsPathToUri

import amara
from amara import dateutil_standins
    
from atomixlib.generator import ax_amara as ax_engine
from atomixlib.lib.ax_exceptions import AtomixlibValidatorError as AVE

#############################################
# Built-In validators
#############################################
class Validator(object):
    """abstract base class for any validator"""
    def __init__(self):
        pass

class URIValidator(Validator):
    """abstract base class for any URI validator"""
    def __init__(self):
       Validator.__init__(self)

class URNValidator(URIValidator):
    """abstract base class for any URN validator"""
    def __init__(self):
       URIValidator.__init__(self)

class URNUUIDValidator(URNValidator):
    """validator for UUID URN"""
    _urn_uuid_regex = re.compile('(urn):(uuid):([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})')
    
    def __init__(self):
       URNValidator.__init__(self)

    def __call__(self, element, xpath, attr=None, raise_error=False):
        """iterates through the elements matching the XPath expression
           and validate the UUID URN

        Keyword arguments:
        element -- Amara element from which the XPath expression will be applied
        xpath -- XPath expression (must be unicode)
        attr -- the UUID URN is contained by this attribute of each element
        raise_error -- if True as soon as an element does not validate it
                       will raise a AtomixlibValidatorError error

        return a list of not validating elements when raise_error is False
        """
        els = element.xml_xpath(xpath)
        if not raise_error:
            els_in_error = []
            
        for el in els:
            if attr and hasattr(el, attr):
                uuid = unicode(getattr(el, attr))
            else:
                uuid = unicode(el)

            m = URNUUIDValidator._urn_uuid_regex.match(uuid)
            if not m or len(m.groups()) != 3:
                if raise_error:
                    raise AVE, "Wrong UUID format for element %s" % repr(el)
                else:
                    els_in_error.append(el)
                
        return els_in_error

                
class URLValidator(URIValidator):
    def __init__(self):
       URIValidator.__init__(self)

    def __call__(self, element, xpath, attr=u'href', raise_error=False):
        """iterates through the elements matching the XPath expression
           and validate the URL
           the validation is done by parsing the URL and checking if
           its scheme and host are set

        Keyword arguments:
        element -- Amara element from which the XPath expression will be applied
        xpath -- XPath expression (must be unicode)
        attr -- the UUID URN is contained by this attribute of each element
        raise_error -- if True as soon as an element does not validate it
                       will raise a AtomixlibValidatorError error

        return a list of not validating elements when raise_error is False
        """
        els = element.xml_xpath(xpath)
        if not raise_error:
            els_in_error = []
            
        for el in els:
            if attr and hasattr(el, attr):
                url = unicode(getattr(el, attr))
            else:
                url = unicode(el)
                
            scheme, netloc, path, parameters, query, fragment = urlparse(url)
            if not scheme or not netloc:
                if raise_error:
                    raise AVE, "Wrong URI for element %s" % repr(el)
                else:
                    els_in_error.append(el)

        return els_in_error
                
class DateTimeValidator(Validator):
    def __init__(self):
       Validator.__init__(self)
       
    def __call__(self, element, xpath, attr=None, raise_error=False):
        """iterates through the elements matching the XPath expression
           and validate the date
           validation is done by trying to parse it as an isodate

        Keyword arguments:
        element -- Amara element from which the XPath expression will be applied
        xpath -- XPath expression (must be unicode)
        attr -- the UUID URN is contained by this attribute of each element
        raise_error -- if True as soon as an element does not validate it
                       will raise a AtomixlibValidatorError error

        return a list of not validating elements when raise_error is False
        """
        els = element.xml_xpath(xpath)
        if not raise_error:
            els_in_error = []
            
        for el in els:
            if attr and hasattr(el, attr):
                dt = unicode(getattr(el, attr))
            else:
                dt = unicode(el)
                
            try:
                dateutil_standins.parse_isodate(dt)
            except StandardError, se:
                if raise_error:
                    raise AVE, "Wrong date format for element %s" % repr(el)
                else:
                    els_in_error.append(el)
                
        return els_in_error
    
class AuthorValidator(Validator):
    def __init__(self):
       Validator.__init__(self)
       
    def __call__(self, element, xpath, check_for=None, raise_error=False):
        """iterates through the elements matching the XPath expression
           and validate the author
           validation is done by verifying the existence of the elements
           passed to check_for: ['name', 'uri', 'email']
           
        Keyword arguments:
        element -- Amara element from which the XPath expression will be applied
        xpath -- XPath expression (must be unicode)
        check_for -- a list of elements to validate against
        raise_error -- if True as soon as an element does not validate it
                       will raise a AtomixlibValidatorError error

        return a list of not validating elements when raise_error is False
        """
        els = element.xml_xpath(xpath)
        if not raise_error:
            els_in_error = []

        if not check_for:
            check_for = ['name', 'uri', 'email']
            
        for el in els:
            for child in check_for:
                if not hasattr(el, child):
                   if raise_error:
                       raise AVE, "%s element is missing a '%s' child" % (repr(el), child)
                   else:
                       els_in_error.append(el)
                       # if the current element failed for one child
                       # there is no reason to check the others for that
                       # element
                       break
                   
        return els_in_error
                
class RelaxNGValidator(Validator):
    def __init__(self):
       Validator.__init__(self)

    def __call__(self, document, relaxng_filepath, raise_error=False):
        # TODO: Fix
        factory = InputSource.DefaultFactory
        rng_uri = Uri.OsPathToUri(relaxng_filepath, attemptAbsolute=1)
        rng_isrc = factory.fromUri(rng_uri)

        validator = RelaxNgValidator(rng_isrc)
        result = validator.isValid(document)
        if not result and raise_error:
            raise AVE, "Document is not valid"
        elif not result:
            return False

        return True

#############################################
# Built-In sortables
#############################################
class Sortable(object):
    """abstract base class for any sortable"""
    def __init__(self):
        pass

class DateSortable(Sortable):
    """abstract base class for date sortable"""
    def __init__(self):
        Sortable.__init__(self)

class PublishedSortable(DateSortable):
    def __init__(self):
        DateSortable.__init__(self)

    def __call__(self, root, latest_first=True):
        """sort entries within a feed based on their published date
       
        Keyword arguments:
        root -- the feed element
        latest_first -- if True then the most recent published entries will
                        be at the top of the feed.
                        entries which have a published date that can't be
                        parsed or none at all will be appended at the bottom

        returns a tuple of (sorted entries, found entries)
        """
        xpath = u'//atom:entry'
        els = root.xml_xpath(xpath)
        published = {}
        others = []
        for el in els:
            try:
                published[dateutil_standins.parse_isodate(unicode(el.published))] = el
            except StandardError, se:
                others.append(el)

        dts = published.keys()[:]
        dts.sort(reverse=latest_first)

        sorted_published = []
        for dt in dts:
            sorted_published.append(published[dt])

        sorted_published.extend(others)

        for el in els:
            root.xml_remove_child(el)
            
        for el in sorted_published:
            root.xml_append(el)

        return len(published), len(els)

#############################################
# Atom document types
#############################################
class AtomDocument(object):
    """base class for any XML document related to Atom and its relatives
       such as the Atom Publishing Protocol documents.
    """
    def __init__(self, atomix):
        """
        Keyword arguments:
        atomix -- Atomix instance
        """
        self.atomix = atomix

    def remove(self, xpath):
        """removes all elements matched by the XPath expression

        Keyword arguments:
        xpath -- XPath expression applied to the feed element
        """
        els = self.atomix.doc.xml_xpath(xpath)
        for el in els:
            el.xml_parent.xml_remove_child(el)
            
    def remove_attribute(self, xpath, attrs):
        """removes attributes from elements matched by the XPath expression

        Keyword arguments:
        xpath -- XPath expression applied to the feed element
        attrs -- a string or list of attribute names
                 that will be removed from each element
        """
        els = self.atomix.doc.xml_xpath(xpath)
        if isinstance(attr, basestring):
            attrs = [attrs]
        for el in els:
            for attr in attrs:
                if attr in el.xml_attributes:
                    del el.xml_attributes[attr]

    def copy(self, xpath_source, atomix_target, xpath_target):
        els_source = self.atomix.doc.xml_xpath(xpath)
        for el in els_source:
            el.xml_parent.xml_remove_child(el)
            
        els_target = atomix_target.xml_xpath(xpath_target)
        

    def transform(self, xslt_filepath):
        """transforms the document using the provided XSLT stylesheet

        Keyword arguments:
        xslt_filepath -- absolute path to the XSLT stylesheet

        returns the output of the transformation
        """
        processor = Processor.Processor()
        stylesheet_uri = OsPathToUri(xslt_filepath)
        transform = InputSource.DefaultFactory.fromUri(stylesheet_uri)
        document = InputSource.DefaultFactory.fromString(self.atomix.xml(),
                                                         ax_engine.DUMMY_URI)
        
        processor.appendStylesheet(transform)
        return processor.run(document)
        
class Feed(AtomDocument):
    def __init__(self, atomix):
        AtomDocument.__init__(self, atomix)

    def validate(self, validator, **kwargs):
        """validate the feed document against a validator
        
        Keyword arguments:
        validator -- a Validator or a subclass of Validator instance
        **kwargs -- any named parameters to pass to the validator

        returns the list of elements which don't validte or
        if you passed to raise_error to your validator parameters
        then it will raise an error as soon as the document does
        not validate
        """
        return validator(self.atomix.doc, **kwargs)

    def sort(self, sortable, **kwargs):
        return sortable(self.atomix.doc.feed, **kwargs)

class Entry(AtomDocument):
    def __init__(self, atomix):
        AtomDocument.__init__(self, atomix)

    def validate(self, validator, **kwargs):
        """validate the feed document against a validator
        
        Keyword arguments:
        validator -- a Validator or a subclass of Validator instance
        **kwargs -- any named parameters to pass to the validator

        returns the list of elements which don't validte or
        if you passed to raise_error to your validator parameters
        then it will raise an error as soon as the document does
        not validate
        """
        return validator(self.atomix.doc, **kwargs)

class Collection(AtomDocument):
    def __init__(self, atomix):
        AtomDocument.__init__(self, atomix)

    def validate(self, validator, **kwargs):
        """validate the feed document against a validator
        
        Keyword arguments:
        validator -- a Validator or a subclass of Validator instance
        **kwargs -- any named parameters to pass to the validator

        returns the list of elements which don't validte or
        if you passed to raise_error to your validator parameters
        then it will raise an error as soon as the document does
        not validate
        """
        return validator(self.atomix.doc, **kwargs)

    def sort(self, sortable):
        pass
    
class Member(AtomDocument):
    def __init__(self, atomix):
        AtomDocument.__init__(self, atomix)

    def validate(self, validator, **kwargs):
        """validate the feed document against a validator
        
        Keyword arguments:
        validator -- a Validator or a subclass of Validator instance
        **kwargs -- any named parameters to pass to the validator

        returns the list of elements which don't validte or
        if you passed to raise_error to your validator parameters
        then it will raise an error as soon as the document does
        not validate
        """
        return validator(self.atomix.doc, **kwargs)
