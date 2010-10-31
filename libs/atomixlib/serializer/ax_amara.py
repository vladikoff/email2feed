#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
atomixlib is a Python package providing a simple interface to the Atom XML format.

This module defines AtomSerializer and AtomPubSerializer classes.
Those provide two methods:
 * serialize
 * deserialize

"""
from atomixlib.mapper import *

class AtomSerializer(object):
    def __init__(self, generator):
        self.generator = generator

    def _s_xml_attributes(self, atom, amara_inst):
        for attr in atom.attributes:
            if attr.prefix == u'xml':
                if attr.name in ['base', 'id', 'lang']:
                    amara_inst.xml_set_attribute((attr.name, u'http://www.w3.org/XML/1998/namespace'),
                                                 attr.value)
                        
    def _s_id(self, atom, atomix):
        if hasattr(atom, 'id'):
            atomix.add_id(atom.id.value, prefix=atom.id.prefix, namespace=atom.id.xmlns)
            
    def _s_title(self, atom, atomix):
        if hasattr(atom, 'title'):
            atomix.add_title(title=atom.title.value,
                             mediaType=atom.title.type.value,
                             prefix=atom.title.prefix, namespace=atom.title.xmlns)

    def _s_summary(self, atom, atomix):
        if hasattr(atom, 'summary'):
            atomix.add_summary(text=atom.summary.value,
                               mediaType=atom.summary.type.value,
                               prefix=atom.summary.prefix, namespace=atom.summary.xmlns)

    def _s_subtitle(self, atom, atomix):
        if hasattr(atom, 'subtitle'):
            atomix.add_subtitle(text=atom.subtitle.value,
                                mediaType=atom.subtitle.type.value,
                                prefix=atom.subtitle.prefix, namespace=atom.subtitle.xmlns)
    def _s_published(self, atom, atomix):
        if hasattr(atom, 'published'):
            atomix.add_published(unicode(atom.published),
                                 prefix=atom.published.prefix, namespace=atom.published.xmlns)
            
    def _s_updated(self, atom, atomix):
        if hasattr(atom, 'updated'):
            atomix.add_updated(unicode(atom.updated),
                               prefix=atom.updated.prefix, namespace=atom.updated.xmlns)

    def _s_edited(self, atom, atomix):
        if hasattr(atom, 'edited'):
            atomix.add_edited(unicode(atom.edited),
                              prefix=atom.edited.prefix, namespace=atom.edited.xmlns)

    def _s_collection(self, atom, atomix):
        if hasattr(atom, 'collection'):
            atomix.add_collection(href=atom.collection.href.value,
                                  prefix=atom.edited.prefix, namespace=atom.edited.xmlns)
                                  
    def _s_links(self, atom, atomix):
        for link in atom.links:
            atomix.add_link(href=link.href.value, rel=link.rel.value,
                            mediaType=link.type.value, hreflang=link.hreflang.value,
                            title=link.title.value, length=link.length.value,
                            prefix=link.prefix, namespace=link.xmlns)

    def _s_authors(self, atom, atomix):
        for author in atom.authors:
            atomix.add_author(name=author.name.value,
                              uri=author.uri.value,
                              email=author.email.value,
                              prefix=author.prefix, namespace=author.xmlns)

    def _s_categories(self, atom, atomix):
        for category in atom.categories:
            atomix.add_category(term=category.term.value,
                                scheme=category.scheme.value,
                                label=category.label.value,
                                prefix=category.prefix, namespace=category.xmlns)

    def _s_contributors(self, atom, atomix):
        for contributor in atom.contributors:
            atomix.add_contributor(name=contributor.name.value,
                                   uri=contributor.uri.value,
                                   email=contributor.email.value,
                                   prefix=contributor.prefix, namespace=contributor.xmlns)

    def _s_rights(self, atom, atomix):
        if hasattr(atom, 'rights'):
            atomix.add_rights(text=atom.rights.value,
                              mediaType=atom.rights.type.value,
                              prefix=atom.rights.prefix, namespace=atom.rights.xmlns)

    def _s_icon(self, atom, atomix):
        if hasattr(atom, 'icon'):
            atomix.add_icon(uri=atom.icon.value,
                            prefix=atom.icon.prefix, namespace=atom.icon.xmlns)

    def _s_logo(self, atom, atomix):
        if hasattr(atom, 'logo'):
            atomix.add_logo(uri=atom.logo.value,
                            prefix=atom.logo.prefix, namespace=atom.logo.xmlns)

    def _s_content(self, atom, atomix):
        if hasattr(atom, 'content'):
            if isinstance(atom.content, PlainTextContent):
                atomix.add_content(text=atom.content.value,
                                   prefix=atom.content.prefix, namespace=atom.content.xmlns)
            elif isinstance(atom.content, HTMLContent): 
                atomix.add_content(text=atom.content.value,
                                   target='inlineHTML',
                                   prefix=atom.content.prefix, namespace=atom.content.xmlns)
            elif isinstance(atom.content, XHTMLContent): 
                atomix.add_content(text=atom.content.div.value,
                                   target='inlineXHTML',
                                   prefix=atom.content.prefix, namespace=atom.content.xmlns)
            elif isinstance(atom.content, ExternalContent):
                atomix.add_content(src=atom.content.src.value,
                                   mediaType=atom.content.type.value,
                                   target='outOfLine',
                                   prefix=atom.content.prefix, namespace=atom.content.xmlns)

    #############################################################
    # Deserialization helpers
    #############################################################
    def _d_xml_attributes(self, atom, amara_inst):
        for attr in amara_inst.attributes:
            if attr[0] == u'http://www.w3.org/XML/1998/namespace':
                if attr[1] in [u'base', u'id', u'lang']:
                    XMLAttribute(name, unicode(amara_inst.attributes[attr]), parent=atom)
                     
    def _d_id(self, atom, amara_inst):
        if hasattr(amara_inst, 'id'):
            atom.id = ID(unicode(amara_inst.id))
            atom.id.prefix = amara_inst.id.prefix
            atom.id.xmlns = amara_inst.id.namespaceURI
        
    def _d_content(self, atom, amara_inst):
        if hasattr(amara_inst, 'content'):
            ttype = unicode(getattr(amara_inst.content, 'type', 'text'))

            if ttype == u'text':
                atom.content = PlainTextContent(text=unicode(amara_inst.content))
            elif ttype == u'html':
                atom.content = HTMLContent(escaped_html=unicode(amara_inst.content))
            elif ttype == u'xhtml':
                atom.content = XHTMLContent(xhtml=amara_inst.content.div.xml(),
                                            xhtml_prefix=amara_inst.content.div.prefix,
                                            xhtml_namespace=amara_inst.content.div.namespaceURI)
            elif hasattr(amara_inst.content, 'src'):
                atom.content = ExternalContent(src=unicode(amara_inst.content.src),
                                               type=ttype)
            
            atom.content.prefix = amara_inst.content.prefix
            atom.content.xmlns = amara_inst.content.namespaceURI
            
    def _d_title(self, atom, amara_inst, strict):
        if hasattr(amara_inst, 'title'):
            ttype = unicode(getattr(amara_inst.title, 'type', 'text'))

            if ttype == u'text':
                atom.title = PlainTextTitle(text=unicode(amara_inst.title))
            elif ttype == u'html':
                atom.title = HTMLTitle(escaped_html=unicode(amara_inst.title))
            elif ttype == u'xhtml':
                atom.title = XHTMLTitle(xhtml=unicode(amara_inst.title.div),
                                        xhtml_prefix=amara_inst.title.div.prefix,
                                        xhtml_namespace=amara_inst.title.div.namespaceURI)
            elif strict:
                raise ValueError, "Unknown title type '%s'" % ttype
        
            atom.title.prefix = amara_inst.title.prefix
            atom.title.xmlns = amara_inst.title.namespaceURI
            
    def _d_summary(self, atom, amara_inst, strict):
        if hasattr(amara_inst, 'summary'):
            ttype = unicode(getattr(amara_inst.summary, 'type', 'text'))

            if ttype == u'text':
                atom.summary = PlainTextSummary(text=unicode(amara_inst.summary))
            elif ttype == u'html':
                atom.summary = HTMLSummary(escaped_html=unicode(amara_inst.summary))
            elif ttype == u'xhtml':
                atom.summary = XHTMLSummary(xhtml=unicode(amara_inst.summary.div),
                                            xhtml_prefix=amara_inst.summary.div.prefix,
                                            xhtml_namespace=amara_inst.summary.div.namespaceURI)
            elif strict:
                raise ValueError, "Unknown summary type '%s'" % ttype
        
            atom.summary.prefix = amara_inst.summary.prefix
            atom.summary.xmlns = amara_inst.summary.namespaceURI
            
    def _d_subtitle(self, atom, amara_inst, strict):
        if hasattr(amara_inst, 'subtitle'):
            ttype = unicode(getattr(amara_inst.subtitle, 'type', 'text'))

            if ttype == u'text':
                atom.subtitle = PlainTextSubtitle(text=unicode(amara_inst.subtitle))
            elif ttype == u'html':
                atom.subtitle = HTMLSubtitle(escaped_html=unicode(amara_inst.subtitle))
            elif ttype == u'xhtml':
                atom.subtitle = XHTMLSubtitle(xhtml=unicode(amara_inst.subtitle.div),
                                              xhtml_prefix=amara_inst.title.div.prefix,
                                              xhtml_namespace=amara_inst.title.div.namespaceURI)
            elif strict:
                raise ValueError, "Unknown subtitle type '%s'" % ttype
        
            atom.subtitle.prefix = amara_inst.subtitle.prefix
            atom.subtitle.xmlns = amara_inst.subtitle.namespaceURI
            
    def _d_rights(self, atom, amara_inst, strict):
        if hasattr(amara_inst, 'rights'):
            ttype = unicode(getattr(amara_inst.rights, 'type', 'text'))

            if ttype == u'text':
                atom.rights = PlainTextRights(text=unicode(amara_inst.rights))
            elif ttype == u'html':
                atom.rights = HTMLRights(escaped_html=unicode(amara_inst.rights))
            elif ttype == u'xhtml':
                atom.rights = XHTMLRights(xhtml=unicode(amara_inst.rights.div),
                                          xhtml_prefix=amara_inst.title.div.prefix,
                                          xhtml_namespace=amara_inst.title.div.namespaceURI)
            elif strict:
                raise ValueError, "Unknown rights type '%s'" % ttype
        
            atom.rights.prefix = amara_inst.rights.prefix
            atom.rights.xmlns = amara_inst.rights.namespaceURI
            
    def _d_published(self, atom, amara_inst):
        if hasattr(amara_inst, 'published'):
            dt = self.generator.parse_isodate(unicode(amara_inst.published))
            atom.published = Published(dt=dt)
        
            atom.published.prefix = amara_inst.published.prefix
            atom.published.xmlns = amara_inst.published.namespaceURI
            
    def _d_updated(self, atom, amara_inst):
        if hasattr(amara_inst, 'updated'):
            dt = self.generator.parse_isodate(unicode(amara_inst.updated))
            atom.updated = Published(dt=dt)

            atom.updated.prefix = amara_inst.updated.prefix
            atom.updated.xmlns = amara_inst.updated.namespaceURI
            
    def _d_edited(self, atom, amara_inst):
        if hasattr(amara_inst, 'edited'):
            dt = self.generator.parse_isodate(unicode(amara_inst.edited))
            atom.edited = Edited(dt=dt)

            atom.edited.prefix = amara_inst.edited.prefix
            atom.edited.xmlns = amara_inst.edited.namespaceURI

    def _d_authors(self, atom, amara_inst):
        if hasattr(amara_inst, 'author'):
            for author in amara_inst.author:
                name = getattr(author, 'name', None) 
                if name: name = unicode(name)
                email = getattr(author, 'email', None)
                if email: email = unicode(email)
                uri = getattr(author, 'uri', None)
                if uri: uri = unicode(uri)
                a = Author(name=name, email=email, uri=uri)
                a.prefix = author.prefix
                a.xmlns = author.namespaceURI

                atom.authors.append(a)

    def _d_contributors(self, atom, amara_inst):
        if hasattr(amara_inst, 'contributor'):
            for contributor in amara_inst.contributor:
                name = getattr(contributor, 'name', None)
                if name: name = unicode(name)
                email = getattr(contributor, 'email', None)
                if email: email = unicode(email)
                uri = getattr(contributor, 'uri', None)
                if uri: uri = unicode(uri)
                c = Contributor(name=name, email=email, uri=uri)
                c.prefix = contributor.prefix
                c.xmlns = contributor.namespaceURI
                atom.contributors.append(c)

    def _d_categories(self, atom, amara_inst):
        if hasattr(amara_inst, 'category'):
            for category in amara_inst.category:
                term = getattr(category, 'term', None)
                if term: unicode(term)
                scheme = getattr(category, 'scheme', None)
                if scheme: unicode(scheme)
                label = getattr(category, 'label', None)
                if label: unicode(label)
                c = Category(term=term, scheme=scheme, label=label)
                c.prefix = category.prefix
                c.xmlns = category.namespaceURI
                atom.categories.append(c)

    def _d_links(self, atom, amara_inst):
        if hasattr(amara_inst, 'link'):
            for link in amara_inst.link:
                href = getattr(link, 'href', None) 
                if href: unicode(href)
                rel = getattr(link, 'rel', None) 
                if rel: unicode(rel)
                media_type = getattr(link, 'type', None) 
                if media_type: unicode(media_type)
                hreflang = getattr(link, 'hreflang', None) 
                if hreflang: unicode(hreflang)
                title = getattr(link, 'title', None) 
                if title: unicode(title)
                length = getattr(link, 'length', None) 
                if length: unicode(length)
                l = Link(href=href, rel=rel, type=media_type, 
                         hreflang=hreflang, length=length, title=title)
                l.prefix = link.prefix
                l.xmlns = link.namespaceURI
                atom.links.append(l)

    def _d_collection(self, atom, amara_inst):
        if hasattr(amara_inst, 'collection'):
            atom.collection = Collection(href=unicode(amara_inst.href))
            atom.collection.prefix = amara_inst.collection.prefix
            atom.collection.xmlns = amara_inst.collection.namespaceURI

    def _d_icon(self, atom, amara_inst):
        if hasattr(amara_inst, 'icon'):
            atom.icon = Icon(uri=unicode(amara_inst.icon))
            atom.icon.prefix = amara_inst.icon.prefix
            atom.icon.xmlns = amara_inst.icon.namespaceURI
            
    def _d_logo(self, atom, amara_inst):
        if hasattr(amara_inst, 'logo'):
            atom.logo = Logo(uri=unicode(amara_inst.logo))
            atom.logo.prefix = amara_inst.logo.prefix
            atom.logo.xmlns = amara_inst.logo.namespaceURI

    def _serialize(self, atom, atomix):
        self._s_id(atom, atomix)
        self._s_title(atom, atomix)
        self._s_subtitle(atom, atomix)
        self._s_updated(atom, atomix)
        self._s_published(atom, atomix)
        self._s_edited(atom, atomix)
        self._s_summary(atom, atomix)
        self._s_links(atom, atomix)
        self._s_collection(atom, atomix)
        self._s_rights(atom, atomix)
        self._s_authors(atom, atomix)
        self._s_contributors(atom, atomix)
        self._s_categories(atom, atomix)
        self._s_icon(atom, atomix)
        self._s_logo(atom, atomix)
        self._s_content(atom, atomix)

    def _deserialize(self, atom, amara_inst, strict=False):
        self._d_id(atom, amara_inst)
        self._d_title(atom, amara_inst, strict)
        self._d_subtitle(atom, amara_inst, strict)
        self._d_updated(atom, amara_inst)
        self._d_published(atom, amara_inst)
        self._d_edited(atom, amara_inst)
        self._d_summary(atom, amara_inst, strict)
        self._d_links(atom, amara_inst)
        self._d_rights(atom, amara_inst, strict)
        self._d_authors(atom, amara_inst)
        self._d_contributors(atom, amara_inst)
        self._d_collection(atom, amara_inst)
        self._d_categories(atom, amara_inst)
        self._d_icon(atom, amara_inst)
        self._d_logo(atom, amara_inst)
        self._d_content(atom, amara_inst)

class FeedSerializer(AtomSerializer):
    def __init__(self, generator):
        AtomSerializer.__init__(self, generator)

    def serialize(self, feed, atomix=None, indent=True):
        if not atomix:
            prefix = None
            prefixes = {}
            if feed.prefix is not None:
                prefixes = {feed.prefix: feed.xmlns}
                prefix = feed.prefix.encode()
            atomix = self.generator.create_feed(prefixes=prefixes, prefix=prefix)

        self._s_xml_attributes(feed, atomix.cursor)
        self._serialize(feed, atomix)

        es = EntrySerializer(self.generator)
        feed_cursor = atomix.cursor
        for entry in feed.entries:
            entrix = atomix.add_entry()
            es._serialize(entry, atomix)
            atomix.cursor = feed_cursor
        
        if indent: indent = 'yes'
        else: indent = 'no'

        return atomix.xml(indent=indent)

    def deserialize(self, source, strict=False):
        if isinstance(source, basestring):
            atomix = self.generator.load(source)
        elif hasattr(source, 'read'):
            atomix = self.generator.load(source.read())
        elif isinstance(source, self.generator.Atomix):
            atomix = source
        else:
            raise ValueError, "Cannot deserialize %s" % str(type(source))

        feed = Feed(prefix=atomix.default_prefix, namespace=atomix.default_namespace)
        atom = atomix.doc.feed

        self._d_xml_attributes(feed, atom)
        self._deserialize(feed, atom)
        
        es = EntrySerializer(self.generator)
        if hasattr(atom, 'entry'):
            for entrix in atom.entry:
                entry = Entry(prefix=atomix.default_prefix,
                              namespace=atomix.default_namespace)
                es._deserialize(entry, entrix)
                feed.entries.append(entry)
            
        return feed

class EntrySerializer(AtomSerializer):
    def __init__(self, generator):
        AtomSerializer.__init__(self, generator)

    def serialize(self, entry, atomix=None, indent=True):
        if not atomix:
            prefix = None
            prefixes = {}
            if entry.prefix is not None:
                prefixes = {entry.prefix: entry.xmlns}
                prefix = entry.prefix.encode()
            atomix = self.generator.create_entry(prefixes=prefixes, prefix=prefix)

        self._s_xml_attributes(entry, atomix.cursor)
        self._serialize(entry, atomix)

        if indent: indent = 'yes'
        else: indent = 'no'

        return atomix.xml(indent=indent)

    def deserialize(self, source, strict=False):
        if isinstance(source, basestring):
            atomix = self.generator.load(source)
        elif hasattr(source, 'read'):
            atomix = self.generator.load(source.read())
        elif isinstance(source, self.generator.Atomix):
            atomix = source
        else:
            raise ValueError, "Cannot deserialize %s" % str(type(source))

        entry = Entry(prefix=atomix.default_prefix,
                      namespace=atomix.default_namespace)
        atom = atomix.doc.entry

        self._d_xml_attributes(entry, atom)
        self._deserialize(entry, atom, strict)
        
        return entry

class AtomPubSerializer(AtomSerializer):
    def __init__(self, generator):
        AtomSerializer.__init__(self, generator)

class ServiceSerializer(AtomPubSerializer):
    def __init__(self, generator):
        AtomPubSerializer.__init__(self, generator)

    def _serialize(self, atom, atomix):
        ws = WorkspaceSerializer(self.generator)
        cursor = atomix.cursor
        for workspace in atom.workspaces:
            w = atomix.add_workspace()
            ws._serialize(workspace, atomix)
            atomix.cursor = cursor

    def _deserialize(self, atom, amara_inst, strict=False):
        if hasattr(amara_inst, 'workspace'):
            ws = WorkspaceSerializer(self.generator)
            for workspace in amara_inst.workspace:
                w = Workspace()
                w.prefix = amara_inst.prefix
                w.xmlns = amara_inst.namespaceURI
                ws._deserialize(w, workspace, strict)
                atom.workspaces.append(w)
            
    def serialize(self, service, atomix=None, indent=True):
        if not atomix:
            prefix = None
            prefixes = {}
            if service.prefix is not None:
                prefixes = {service.prefix: service.xmlns}
                prefix = service.prefix.encode()
            atomix = self.generator.create_service(prefixes=prefixes, prefix=prefix)

        self._s_xml_attributes(service, atomix.cursor)
        self._serialize(service, atomix)

        if indent: indent = 'yes'
        else: indent = 'no'

        return atomix.xml(indent=indent)

    def deserialize(self, source, strict=False):
        if isinstance(source, basestring):
            atomix = self.generator.load(source)
        elif hasattr(source, 'read'):
            atomix = self.generator.load(source.read())
        elif isinstance(source, self.generator.Atomix):
            atomix = source
        else:
            raise ValueError, "Cannot deserialize %s" % str(type(source))

        service = Service(prefix=atomix.default_prefix, namespace=atomix.default_namespace)
        atom = atomix.doc.service

        self._d_xml_attributes(service, atom)
        self._deserialize(service, atom, strict)
        
        return service

class WorkspaceSerializer(AtomPubSerializer):
    def __init__(self, generator):
        AtomPubSerializer.__init__(self, generator)

    def _serialize(self, atom, atomix):
        cs = CollectionSerializer(self.generator)
        self._s_title(atom, atomix)
        cursor = atomix.cursor
        for collection in atom.collections:
            c = atomix.add_collection(href=collection.href.value, workspace=cursor)
            cs._serialize(collection, atomix)
            atomix.cursor = cursor
            
    def _deserialize(self, atom, amara_inst, strict=False):
        self._d_title(atom, amara_inst, strict)
        if hasattr(amara_inst, 'collection'):
            cs = CollectionSerializer(self.generator)
            for collection in amara_inst.collection:
                c = Collection(href=unicode(collection.href))
                c.prefix = amara_inst.prefix
                c.xmlns = amara_inst.namespaceURI
                cs._deserialize(c, collection, strict)
                atom.collections.append(c)
                
    def serialize(self, workspace, atomix=None, indent=True):
        if not atomix:
            prefix = None
            prefixes = {}
            if workspace.prefix is not None:
                prefixes = {workspace.prefix: workspace.xmlns}
                prefix = workspace.prefix.encode()
            atomix = self.generator.create_workspace(prefixes=prefixes, prefix=prefix)

        self._s_xml_attributes(workspace, atomix.cursor)
        self._serialize(workspace, atomix)

        if indent: indent = 'yes'
        else: indent = 'no'

        return atomix.xml(indent=indent)

    def deserialize(self, source, strict=False):
        if isinstance(source, basestring):
            atomix = self.generator.load(source)
        elif hasattr(source, 'read'):
            atomix = self.generator.load(source.read())
        elif isinstance(source, self.generator.Atomix):
            atomix = source
        else:
            raise ValueError, "Cannot deserialize %s" % str(type(source))

        workspace = Workspace(prefix=atomix.default_prefix, namespace=atomix.default_namespace)
        atom = atomix.doc.workspace

        self._d_xml_attributes(workspace, atom)
        self._deserialize(workspace, atom, strict)
        
        return workspace
    
class CollectionSerializer(AtomPubSerializer):
    def __init__(self, generator):
        AtomPubSerializer.__init__(self, generator)

    def _serialize(self, atom, atomix):
        c = atomix.cursor
        self._s_title(atom, atomix)
        if atom.accept.value:
            atomix.add_accept(atom.accept.value)
                
        if atom.categories and atom.categories.categories:
            categories = atomix.add_categories(fixed=atom.categories.fixed.value,
                                               scheme=atom.categories.scheme.value,
                                               href=atom.categories.href.value,
                                               collection=c)
            for category in atom.categories.categories:
                atomix.add_category(term=category.term.value, scheme=category.scheme.value,
                                    label=category.label.value, prefix=category.prefix,
                                    namespace=category.xmlns)
    
    def _deserialize(self, atom, amara_inst, strict=False):
        self._d_title(atom, amara_inst, strict)
        if hasattr(amara_inst, 'accept'):
            atom.accept = Accept(value=unicode(amara_inst.accept))
            
        if hasattr(amara_inst, 'categories'):
            fixed = scheme = href = None
            if hasattr(amara_inst.categories, 'fixed'):
                fixed = unicode(amara_inst.categories.fixed)
                if fixed.lower() == u'yes':
                    fixed = True
                else:
                    fixed = False
            if hasattr(amara_inst.categories, 'scheme'):
                scheme = unicode(amara_inst.categories.scheme)
            if hasattr(amara_inst.categories, 'href'):
                href = unicode(amara_inst.categories.href)
            atom.categories = Categories(fixed=fixed, scheme=scheme, href=href)
            self._d_categories(atom.categories, amara_inst.categories)
                
    def serialize(self, collection, atomix=None, indent=True):
        if not atomix:
            prefix = None
            prefixes = {}
            if collection.prefix is not None:
                prefixes = {collection.prefix: collection.xmlns}
                prefix = collection.prefix.encode()
            atomix = self.generator.create_collection(prefixes=prefixes, prefix=prefix)

        self._s_xml_attributes(collection, atomix.cursor)
        self._serialize(collection, atomix)

        if indent: indent = 'yes'
        else: indent = 'no'

        return atomix.xml(indent=indent)

    def deserialize(self, source, strict=False):
        if isinstance(source, basestring):
            atomix = self.generator.load(source)
        elif hasattr(source, 'read'):
            atomix = self.generator.load(source.read())
        elif isinstance(source, self.generator.Atomix):
            atomix = source
        else:
            raise ValueError, "Cannot deserialize %s" % str(type(source))

        atom = atomix.doc.collection
        href = None
        if hasattr(atom, 'href'):
            href = unicode(atom.href)
        collection = Collection(href=href,
                                prefix=atomix.atom_prefix,
                                namespace=atomix.atom_namespace)

        self._d_xml_attributes(collection, atom)
        self._deserialize(collection, atom, strict)
        
        return collection
