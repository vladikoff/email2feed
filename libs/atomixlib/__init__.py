#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = "0.6.1a"
__authors__ = ["Sylvain Hellegouarch (sh@defuze.org)"]
__contributors__ = ["Uche Ogbuji", "Andrew Ittner (andrew.ittner@usa.net)"]
__date__ = "2006/10/10"
__copyright__ = """
Copyright (c) 2005, 2006 Sylvain Hellegouarch
All rights reserved.
"""
__license__ = """
Redistribution and use in source and binary forms, with or without modification, 
are permitted provided that the following conditions are met:
 
     * Redistributions of source code must retain the above copyright notice, 
       this list of conditions and the following disclaimer.
     * Redistributions in binary form must reproduce the above copyright notice, 
       this list of conditions and the following disclaimer in the documentation 
       and/or other materials provided with the distribution.
     * Neither the name of Sylvain Hellegouarch & Andrew Ittner nor the names of their contributors 
       may be used to endorse or promote products derived from this software 
       without specific prior written permission.
 
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND 
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

__doc__ = """
atomixlib provides a simple API to generate:
 * Atom 1.0 documents respecting RFC 4287
 * Atom Feed Thread elements RFC 4685
 * Atom Publishing Protocol documents

atomixlib comes with:
 * A low level API to create those documents using
   underlying XML engines such as Amara or ElementTree.
 * Mapping classes which represent Atom documents and elements
   as pure Python object.
"""

# Change this variable to inform atomixlib of which
# underlying XML engine yo uwnat to use for further operations
# 'amara', 'elementtree'.
# For now we force the default to use Amara.
default_engine_name = 'amara'

# a set of default namespaces
ATOM10_NS_STR = 'http://www.w3.org/2005/Atom'
ATOM10_NS = u'http://www.w3.org/2005/Atom'
ATOMPUB_NS_STR = 'http://purl.org/atom/app#'
ATOMPUB_NS = u'http://purl.org/atom/app#'
XHTML1_NS_STR = 'http://www.w3.org/1999/xhtml'
XHTML1_NS = u'http://www.w3.org/1999/xhtml'
THR_NS = u'http://purl.org/syndication/thread/1.0'

# default prefixes
ATOM10_PREFIX = u'atom'
ATOMPUB_PREFIX = u'app'
THR_PREFIX = u'thr'

ENCODING = 'UTF-8'
DUMMY_URI = u'http://dummy.com'
COMMON_PREFIXES = { u'atom': ATOM10_NS, u'': ATOM10_NS,
                    u'app': ATOMPUB_NS, u'thr': THR_NS,
                    u'xhtml': XHTML1_NS, u'xh': XHTML1_NS}

__version__ = u'0.6.0a'

def get_generator(name=None):
    """returns the module object matching the requested engine name

    Keyword arguments:
    name -- requested engine name ('amara', 'elementtree')

    returns an engine module object
    """
    if not name:
        name = default_engine_name
    if name == 'amara':
        from generator import ax_amara as engine
    elif name == 'elementtree':
        from generator import ax_elementtree as engine
    else:
        raise ValueError, "'%s' is not a recognised engine" % name

    return engine

def get_serializer(name=None):
    """returns the module object matching the requested serializer name

    Keyword arguments:
    name -- requested serializer name ('amara', 'elementtree')

    returns a serializer module object
    """
    if not name:
        name = default_engine_name
    if name == 'amara':
        from serializer import ax_amara as serializer
    elif name == 'elementtree':
        raise NotImplementedError, 'ElementTree serialization not implemented'
    else:
        raise ValueError, "'%s' is not a recognised serializer" % name

    return serializer

def d_feed(source, strict=True):
    """
    Deserializes an XML string of an atom:feed document.
    Returns a atomixlib.mapper.Feed instance.
    
    Keyword arguments:
    strict -- if True the processing may stop if some
    conditions are not met.
    """
    g = get_generator()
    p = get_serializer()
    s = p.FeedSerializer(g)
    return s.deserialize(source, strict)

def d_entry(source, strict=True):
    """
    Deserializes an XML string of an atom:entry document.
    Returns a atomixlib.mapper.Entry instance.
    
    Keyword arguments:
    strict -- if True the processing may stop if some
    conditions are not met.
    """
    g = get_generator()
    p = get_serializer()
    s = p.EntrySerializer(g)
    return s.deserialize(source, strict)

def d_service(source, strict=True):
    """
    Deserializes an XML string of an app:service document.
    Returns a atomixlib.mapper.Service instance.
    
    Keyword arguments:
    strict -- if True the processing may stop if some
    conditions are not met.
    """
    g = get_generator()
    p = get_serializer()
    s = p.ServiceSerializer(g)
    return s.deserialize(source, strict)

def d_workspace(source, strict=True):
    """
    Deserializes an XML string of an app:workspace fragment.
    Returns a atomixlib.mapper.Workspace instance.
    
    Keyword arguments:
    strict -- if True the processing may stop if some
    conditions are not met.
    """
    g = get_generator()
    p = get_serializer()
    w = p.WorkspaceSerializer(g)
    return s.deserialize(source, strict)

def d_collection(source, strict=True):
    """
    Deserializes an XML string of an app:collection fragment.
    Returns a atomixlib.mapper.Collection instance.
    
    Keyword arguments:
    strict -- if True the processing may stop if some
    conditions are not met.
    """
    g = get_generator()
    p = get_serializer()
    c = p.CollectionSerializer(g)
    return c.deserialize(source, strict)

def s_feed(feed, atomix=None, indent=True):
    """
    Serializes a atomixlib.mapper.Feed instance into an XML string
    using the default XML engine.
    
    Keyword arguments:
    atomix -- You may provide an existing atomixlib.Atomix instance
    If not provided it will be created for the serialization purpose.
    indent -- Whether or not the document will be indented.
    """
    g = get_generator()
    p = get_serializer()
    s = p.FeedSerializer(g)
    return s.serialize(feed, atomix, indent)

def s_entry(entry, atomix=None, indent=True):
    """
    Serializes a atomixlib.mapper.Entry instance into an XML string
    using the default XML engine.
    
    Keyword arguments:
    atomix -- You may provide an existing atomixlib.Atomix instance
    If not provided it will be created for the serialization purpose.
    indent -- Whether or not the document will be indented.
    """
    g = get_generator()
    p = get_serializer()
    s = p.EntrySerializer(g)
    return s.serialize(entry, atomix, indent)

def s_service(service, atomix=None, indent=True):
    """
    Serializes a atomixlib.mapper.Service instance into an XML string
    using the default XML engine.
    
    Keyword arguments:
    atomix -- You may provide an existing atomixlib.Atomix instance
    If not provided it will be created for the serialization purpose.
    indent -- Whether or not the document will be indented.
    """
    g = get_generator()
    p = get_serializer()
    s = p.ServiceSerializer(g)
    return s.serialize(service, atomix, indent)

def s_workspace(workspace, atomix=None, indent=True):
    """
    Serializes a atomixlib.mapper.Workspace instance into an XML string
    using the default XML engine.
    
    Keyword arguments:
    atomix -- You may provide an existing atomixlib.Atomix instance
    If not provided it will be created for the serialization purpose.
    indent -- Whether or not the document will be indented.
    """
    g = get_generator()
    p = get_serializer()
    w = p.WorkspaceSerializer(g)
    return w.serialize(workspace, atomix, indent)

def s_collection(collection, atomix=None, indent=True):
    """
    Serializes a atomixlib.mapper.Collection instance into an XML string
    using the default XML engine.
    
    Keyword arguments:
    atomix -- You may provide an existing atomixlib.Atomix instance
    If not provided it will be created for the serialization purpose.
    indent -- Whether or not the document will be indented.
    """
    g = get_generator()
    p = get_serializer()
    c = p.CollectionSerializer(g)
    return c.serialize(collection, atomix, indent)
