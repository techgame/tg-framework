#!/usr/bin/env python
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##~ Copyright (C) 2002-2004  TechGame Networks, LLC.
##~ 
##~ This library is free software; you can redistribute it and/or
##~ modify it under the terms of the BSD style License as found in the 
##~ LICENSE file included with this distribution.
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import re

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class URIPathScheme(object):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    segments = ()
    attributes = None

    _pathsep = u'/'
    _pathattrsep = u';'

    _parentPathSegment = u'..'
    _currentPathSegment = u'.'

    _currentPathPart = u'' # empty string for joining
    _parentPathPart = u'..'

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Public Methods 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, pathOrSegments=u'', attributes=NotImplemented):
        if isinstance(pathOrSegments, basestring):
            if self._pathattrsep in pathOrSegments:
                pathOrSegments, self.attributes = pathOrSegments.split(self._pathattrsep, 1)
            self.setSegments(pathOrSegments.split(self._pathsep))
        elif isinstance(pathOrSegments, self.__class__):
            self.__dict__.update(pathOrSegments.__dict__)
        else:
            self.setSegments(pathOrSegments)

        if attributes is not NotImplemented:
            self.attributes = attributes

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def fromSegments(klass, segments, *args, **kw):
        return klass(segments, *args, **kw)
    fromSegments = classmethod(fromSegments)

    def fromPathString(klass, path, *args, **kw):
        return klass(path, *args, **kw)
    fromPathString = classmethod(fromPathString )

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __len__(self):
        return len(self.getSegments())

    def __getitem__(self, key):
        result = self.getSegments().__getitem__(key)
        if isinstance(key, slice):
            result = self.fromSegments(result)
        return result

    def __contains__(self, other):
        return self.contains(other)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def contains(self, other, proper=True):
        subpath = self.asSubpath(other, True)
        if proper: 
            return bool(subpath)
        else: 
            return subpath is not None

    def isSubpath(self, other, tolerant=True):
        subpath = self.asSubpath(other, tolerant)
        return subpath is not None

    def asSubpath(self, other, tolerant=False):
        other = self.fromPathString(other)
        otherSeg = other.getSegments(True) # filter out and 'curdirs'
        selfSeg = self.getSegments(True)
        valid = (selfSeg == otherSeg[:len(selfSeg)])
        if valid:
            return self.fromSegments(otherSeg[len(selfSeg):])
        elif tolerant:
            return None
        else:
            raise ValueError("%r is not a valid subpath of %r" % (other, self))

    def getSegments(self, simplify=False):
        if simplify:
            return filter(None, self.segments)
        else:
            return self.segments
    def setSegments(self, segments):
        self.segments = segments or []

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def asPathString(self, root=False):
        result = self._pathsep.join(self.getSegments()) or ''
        if self.attributes:
            result = self._pathattrsep.join((result, self.attributes))
        if root and not result.startswith(u'/'):
            result = self._pathsep.join((u'', result))
        return result
    def __unicode__(self):
        return unicode(self.asPathString())
    def __str__(self):
        return str(self.asPathString())
    def __repr__(self):
        return '<%s.%s "%s">' % (self.__class__.__module__, self.__class__.__name__, str(self))
    def __iter__(self):
        return iter(self.getSegments())

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def normalized(self):
        segments = self.getSegments()
        self.setSegments([])
        self.addPath(segments, andAttrs=False)
        return self

    def addPath(self, pathOrSegments, andAttrs=False):
        if isinstance(pathOrSegments, basestring):
            path = self.fromPathString(pathOrSegments)
        else: 
            path = pathOrSegments

        for each in iter(path):
            self.add(each)

        if andAttrs:
            self.attributes = path.attributes
        return self

    def add(self, segment):
        if segment == self._currentPathSegment:
            self.addCurrentSegment()
        elif segment == self._parentPathSegment:
            self.addParentSegment()
        else:
            self.addSegment(segment)
        return self

    def addParentSegment(self):
        tos = self.getTopSegment()
        if tos is None:
            # handles both empty, and tos is '' cases
            self.getSegments().append(self._parentPathPart)
        elif not tos:
            # pop 1 and recurse
            self.getSegments().pop()
            self.addParentSegment()
        elif tos == self._parentPathPart:
            # well, just go up another directory...
            self.getSegments().append(self._parentPathPart)
        else:
            # we have a vaild parent, so just remove it
            self.getSegments().pop()

        # this is implied
        self.addCurrentSegment()

    def addCurrentSegment(self):
        tos = self.getTopSegment()
        if tos:
            # path is "a/b" ==> make it "a/b/"
            # or path is "a/.." ==> make it "a/../"
            self.getSegments().append(self._currentPathPart)

    def addSegment(self, segment):
        tos = self.getTopSegment()
        if not tos:
            # handles both empty, and tos is '' cases
            self.getSegments()[-1:] = [segment]
        else:
            self.getSegments().append(segment)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def getTopSegment(self):
        if self.getSegments():
            return self.getSegments()[-1] 
        else:
            return None

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def splitCommon(*paths, **kw):
        """Returns (common, remaining) where all of the segments in common are
        shared among the otherPaths.  Remaining contains the "rest" of segments
        that not shared among the otherPaths."""
        import itertools
        common, remaining = [], []
        paths = map(iter, paths)
        pathColletion = itertools.imap(None, *paths)
        for pathSegments in pathColletion:
            # if all elements are equal (assumes transitivity)
            if pathSegments[:-1] == pathSegments[1:]:
                common.append(pathSegments[0])
                continue
            else:
                # oops... had one non-equal one... therefore, they are all
                # different from now on ;)
                for segment, restOfPath in map(None, pathSegments, paths):
                    remaining.append([segment] + list(restOfPath))
                break 
        else:
            for restOfPath in paths:
                remaining.append(list(restOfPath))

        return (common, remaining)

    def getRelative(self, other):
        """Returns the path necessary to get from `self` to `other` """
        common, (myPart, otherPart) = self.splitCommon(other)
        return self.fromSegments(['..',]*(len(myPart)-1) + otherPart)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class URI(object):
    """
    From RFC 2396 at <http://www.ietf.org/rfc/rfc2396.txt>
    ...
    B. Parsing a URI Reference with a Regular Expression

       As described in Section 4.3, the generic URI syntax is not sufficient
       to disambiguate the components of some forms of URI.  Since the
       "greedy algorithm" described in that section is identical to the
       disambiguation method used by POSIX regular expressions, it is
       natural and commonplace to use a regular expression for parsing the
       potential four components and fragment identifier of a URI reference.

       The following line is the regular expression for breaking-down a URI
       reference into its components.

          ^(([^:/?#]+):)?(//([^/?#]*))?([^?#]*)(\?([^#]*))?(#(.*))?
           12            3  4          5       6  7        8 9

       The numbers in the second line above are only to assist readability;
       they indicate the reference points for each subexpression (i.e., each
       paired parenthesis).  We refer to the value matched for subexpression
       <n> as $<n>.  For example, matching the above expression to

          http://www.ics.uci.edu/pub/ietf/uri/#Related

       results in the following subexpression matches:

          $1 = http:
          $2 = http
          $3 = //www.ics.uci.edu
          $4 = www.ics.uci.edu
          $5 = /pub/ietf/uri/
          $6 = <undefined>
          $7 = <undefined>
          $8 = #Related
          $9 = Related

       where <undefined> indicates that the component is not present, as is
       the case for the query component in the above example.  Therefore, we
       can determine the value of the four components and fragment as

          scheme    = $2
          authority = $4
          path      = $5
          query     = $7
          fragment  = $9

       and, going in the opposite direction, we can recreate a URI reference
       from its components using the algorithm in step 7 of Section 5.2.

    """

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _reURItype = r'^(?:(?P<scheme>[^:/?#@]+)(?P<_schemesep>:))?'
    _reURIauthority = r'(?:(?P<_authoritysep>//)(?P<authority>[^/?#]*))?'
    _reURIpath = r'(?P<path>(?P<_pathsep>/)?[^?#]+)?'
    _reURIquery = r'(?:(?P<_querysep>\?)(?P<query>[^#]*))?'
    _reURIfragment = r'(?:(?P<_fragmentsep>#)(?P<fragment>.*))?'

    _reURI = _reURItype + _reURIauthority + _reURIpath + _reURIquery + _reURIfragment
    _reURIPattern = re.compile(_reURI)

    # Default values
    _uriParts = {
        'scheme': None,
        'authority': None,
        'path': None,
        'query': None,
        'fragment': None,

        '_schemesep': u':',
        '_authoritysep': u'//',
        '_pathsep': u'/',
        '_pathattrsep': u';',
        '_querysep': u'?',
        '_fragmentsep': u'#',
        }
    locals().update(_uriParts)

    PathScheme = URIPathScheme

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Special 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __init__(self, uri=None, standardize=False, **kw):
        if uri is not None:
            self.setURI(uri, **kw)

        if standardize:
            self.standardize()

    def fromURI(klass, uriOther, copy=False):
        if not copy and isinstance(uriOther, klass):
            return uriOther
        else:
            return klass(uriOther)
    fromURI = classmethod(fromURI)

    def fromURIParts(klass, uriParts):
        r = klass()
        r.setURIParts(uriParts)
        return r
    fromURIParts = classmethod(fromURIParts)

    def copyFromURIParts(self, uriParts):
        return self.fromURIParts(uriParts)

    def copyFromURI(self, uriOther):
        return self.fromURI(uriOther, copy=True)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __getstate__(self):
        return dict(uri=self.getURIValue())
    def __setstate__(self, data):
        uri = data.pop('uri', '')
        self.setURI(uri)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def asURIStr(self, formatStr='<URI:%s>'):
        return formatStr % (self,)
    def __repr__(self):
        return self.asURIStr()
    def __len__(self):
        return len(self.getURIValue())
    def __unicode__(self):
        return unicode(self.getURIValue())
    def __str__(self):
        return str(self.getURIValue())
    def __cmp__(self, other):
        return cmp(str(self), str(other))
    def __hash__(self):
        return hash(str(self))

    def getURIParts(self):
        return {
            'scheme': self.scheme,
            'authority': self.authority,
            'path': self.path,
            'query': self.query,
            'fragment': self.fragment,
            }
    def setURIParts(self, kwparam={}, **kw):
        items = kwparam.items() + kw.items()
        for key, value in items:
            # but only if they are in known names
            if key in self._uriParts:
                setattr(self, key, value)
    def clearURIParts(self):
        for key in self._uriParts.keys():
            if key in self.__dict__:
                delattr(self, key)

    def standardize(self):
        self.standardizeSeperators()
        return self
    def standardizeSeperators(self):
        for key in self.__dict__.keys():
            if key.endswith('sep'):
                delattr(self, key)

    def getPathEx(self, *args, **kw):
        return self.PathScheme(self.path, *args, **kw)
    def setPathEx(self, path, *args, **kw):
        if args or kw:
            self.path = path.asPathString(*args, **kw)
        else:
            self.path = unicode(path)

    def normalizePath(self, path=None):
        if path is None:
            path = self.path
        self.setPathEx(self.PathScheme(path).normalized())
        return self.path

    def isAbsPath(self):
        if self.path:
            return self.path.startswith(self._pathsep)
        else:
            return False

    def getURI(self):
        return self
    def getURIValue(self):
        """
        Pseudocode from RFC 2396 at http://www.ietf.org/rfc/rfc2396.txt 
        Section 5.2, step 7 to recreate a URI reference from its components.
        """
        result = []
        if self.scheme is not None:
            result.append(self.scheme)
            if self._schemesep is not None:
                result.append(self._schemesep)
        if self.authority is not None:
            if self._authoritysep is not None:
                result.append(self._authoritysep)
            result.append(self.authority)
        if self.path is not None:
            result.append(self.path)
        if self.query is not None:
            if self._querysep is not None:
                result.append(self._querysep)
            result.append(self.query)
        if self.fragment is not None:
            if self._fragmentsep is not None:
                result.append(self._fragmentsep)
            result.append(self.fragment)
        result = map(unicode, result)
        return u''.join(result)
    def setURI(self, uri=None, **uriParts):
        self.clearURIParts()
        if isinstance(uri, URI):
            self.setURIParts(uri.getURIParts())
        elif uri is not None:
            uri = unicode(uri)
            match = self._reURIPattern.match(uri)
            if not match:
                raise ValueError("URI string is not parseable: %r" % uri)
            uriParts.update(match.groupdict())

        if uriParts: 
            self.setURIParts(uriParts)
    uri = property(getURIValue, setURI)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def join(self, uriRelative, append=False):
        """Resolve Relative URIs -- returns a new URI of the join

            from http://www.faqs.org/rfcs/rfc1808.html::

            4.  Resolving Relative URLs

        This section describes an example algorithm for resolving URLs within
        a context in which the URLs may be relative, such that the result is
        always a URL in absolute form.  Although this algorithm cannot
        guarantee that the resulting URL will equal that intended by the
        original author, it does guarantee that any valid URL (relative or
        absolute) can be consistently transformed to an absolute form given a
        valid base URL.

        The following steps are performed in order:

        Step 1: The base URL is established according to the rules of
                Section 3.  If the base URL is the empty string (unknown),
                the embedded URL is interpreted as an absolute URL and
                we are done.

        Step 2: Both the base and embedded URLs are parsed into their
                component parts as described in Section 2.4.

                a) If the embedded URL is entirely empty, it inherits the
                    entire base URL (i.e., is set equal to the base URL)
                    and we are done.

                b) If the embedded URL starts with a scheme name, it is
                    interpreted as an absolute URL and we are done.

                c) Otherwise, the embedded URL inherits the scheme of
                    the base URL.

        Step 3: If the embedded URL's <net_loc> is non-empty, we skip to
                Step 7.  Otherwise, the embedded URL inherits the <net_loc>
                (if any) of the base URL.

        Step 4: If the embedded URL path is preceded by a slash "/", the
                path is not relative and we skip to Step 7.

        Step 5: If the embedded URL path is empty (and not preceded by a
                slash), then the embedded URL inherits the base URL path,
                and

                a) if the embedded URL's <params> is non-empty, we skip to
                    step 7; otherwise, it inherits the <params> of the base
                    URL (if any) and

                b) if the embedded URL's <query> is non-empty, we skip to
                    step 7; otherwise, it inherits the <query> of the base
                    URL (if any) and we skip to step 7.

        Step 6: The last segment of the base URL's path (anything
                following the rightmost slash "/", or the entire path if no
                slash is present) is removed and the embedded URL's path is
                appended in its place.  The following operations are
                then applied, in order, to the new path:

                a) All occurrences of "./", where "." is a complete path
                    segment, are removed.

                b) If the path ends with "." as a complete path segment,
                    that "." is removed.

                c) All occurrences of "<segment>/../", where <segment> is a
                    complete path segment not equal to "..", are removed.
                    Removal of these path segments is performed iteratively,
                    removing the leftmost matching pattern on each iteration,
                    until no matching pattern remains.

                d) If the path ends with "<segment>/..", where <segment> is a
                    complete path segment not equal to "..", that
                    "<segment>/.." is removed.

        Step 7: The resulting URL components, including any inherited from
                the base URL, are recombined to give the absolute form of
                the embedded URL.

        Parameters, regardless of their purpose, do not form a part of the
        URL path and thus do not affect the resolving of relative paths.  In
        particular, the presence or absence of the ";type=d" parameter on an
        ftp URL does not affect the interpretation of paths relative to that
        URL.  Fragment identifiers are only inherited from the base URL when
        the entire embedded URL is empty.

        The above algorithm is intended to provide an example by which the
        output of implementations can be tested -- implementation of the
        algorithm itself is not required.  For example, some systems may find
        it more efficient to implement Step 6 as a pair of segment stacks
        being merged, rather than as a series of string pattern matches.
        """    
        uriBase = self.standardize()
        uriRelative = self.copyFromURI(uriRelative).standardize()

        # Step 1: Empty base URI
        if not uriBase:
            return uriRelative

        # Step 2a: Empty embedded URI
        if not uriRelative:
            return uriBase

        # Step 2b: Embedded specifices scheme
        if uriRelative.scheme:
            return uriRelative

        # Step 2c: Embedded inherits scheme
        uriRelative.scheme = uriBase.scheme

        # Step 3: Authority is specified... 
        if uriRelative.authority:
            return uriRelative
        else:
            uriRelative.authority = uriBase.authority

        # Step 4: Check for starting "/" in path
        if uriRelative.path and uriRelative.path.startswith(self._pathsep):
            return uriRelative

        # Step 5: Empty path
        if uriRelative.path and uriRelative.path.startswith(self._pathattrsep):
            # Step 5a: Empty path with params
            # Replace uriBase's path params with the uriRelative path params
            uriRelative.path = uriBase.path.split(self._pathattrsep, 1)[0] + uriRelative.path
            return uriRelative
        elif not uriRelative.path:
            # Step 5: (continued)
            uriRelative.path = uriBase.path

            # Step 5b: query inheritence
            if uriRelative.query:
                return uriRelative
            else:
                uriRelative.query = uriBase.query
                return uriRelative

        # Step 6: Path joining
        basePath = uriBase.getPathEx(attributes=None)
        if not append:
            basePath.segments.pop()
        basePath.addPath(uriRelative.path, andAttrs=True)
        uriRelative.setPathEx(basePath, root=True)

        # Step 7: Return result
        return uriRelative

    def append(self, uriRelative):
        return self.join(uriRelative, True)

    def isRelative(self, uriRelative, incEqual=False, incPath=True):
        uriBase = self.standardize()
        uriRelative = self.copyFromURI(uriRelative).standardize()

        # Step 2a: Empty embedded URI
        if not uriRelative:
            return False

        # Step 2b: Embedded specifices scheme
        if uriRelative.scheme:
            if not incEqual:
                return False
            else:
                # Note: According to http://www.ietf.org/rfc/rfc2396.txt, the
                # following is not correct; but it's useful for some comparisons
                if uriRelative.scheme != uriBase.scheme:
                    return False

        # Step 3: Authority is specified... 
        if uriRelative.authority:
            if not incEqual:
                return False
            else:
                # Note: According to http://www.ietf.org/rfc/rfc2396.txt, the
                # following is not correct, and indicates an absolute uri
                if uriRelative.authority != uriBase.authority:
                    return False

        if incPath and uriRelative.isAbsPath():
            return False

        # Tests conclude that this is a Relative URI
        return True

    def isAbsolute(self, uriRelative, incEqual=False, incPath=True):
        return not self.isRelative(uriRelative, incEqual, incPath)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Path utilites
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def __contains__(self, other):
        return self.contains(other)

    def contains(self, other, proper=True):
        subpath = self.asSubpath(other, True)
        if proper: 
            return bool(subpath)
        else: 
            return subpath is not None

    def isSubpath(self, other, tolerant=True):
        subpath = self.asSubpath(other, tolerant)
        return subpath is not None

    def asSubpath(self, uriRelative, tolerant=False):
        result = self.copyFromURI(uriRelative).standardize()
        path = self.getPathEx().asSubpath(result.getPathEx(), tolerant)
        if path is None:
            return None
        else:
            result.setPathEx(path)
            return result

    def asRelativeTo(self, other):
        pathEx = self.getPathEx().getRelative(other.getPathEx())
        parts = self.getURIParts()
        parts['path'] = pathEx.asPathString()
        result = self.copyFromURIParts(parts)
        return result

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class URIAuthorityDefault(URI):
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #~ Constants / Variables / Etc. 
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    _reURItype = URI._reURItype 
    _reURIauthority = r'(?:(?P<_authoritysep>//)?(?P<authority>[^/?#]*))'
    #_reURIpath = r'(?P<path>(?P<_pathsep>/)?[^?#]+)?'
    _reURIpath = URI._reURIpath
    _reURIquery = URI._reURIquery
    _reURIfragment = URI._reURIfragment

    _reURI = _reURItype + _reURIauthority + _reURIpath + _reURIquery + _reURIfragment
    _reURIPattern = re.compile(_reURI)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Class Aliases
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

RFC2396URI = URI
URIPathDefault = URI

URIAuthDefault = URIAuthorityDefault
URIAuthority = URIAuthorityDefault
URIAuth = URIAuthorityDefault
URIHost = URIAuthorityDefault

