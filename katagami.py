# -*- coding: utf-8 -*-
r"""katagami: a simple xml/html template library
============================================

This library is one of many `Python templating libraries
<http://wiki.python.org/moin/Templating>`_.


Features
--------
 * Based on XML's Processing instructions (`<?...?>`)
 * Simple features
 * Python script inside XML/HTML with any level indentation
 * `Inline Python expression`_
 * `Embed Python script`_
 * `Block structure`_
 * `Encoding detection`_
 * `Iteratable rendering`_
 * Supports both of Python 2 and Python 3
 * As fast as `mako <http://www.makotemplates.org/>`_


Example
-------

Make a HTML string with `inline Python expression`_ and Python's `for` (`Block
structure`_)::

    >>> from katagami import render_string, dprint as print
    >>> print(render_string('''<html>
    ... <body>
    ...     <? for name in names: {?>
    ...         <p>hello, <?=name?></p>
    ...     <?}?>
    ... </body>
    ... </html>''', {'names': ['world', 'python']}))
    <html>
    <body>
    <BLANKLINE>
            <p>hello, world</p>
    <BLANKLINE>
            <p>hello, python</p>
    <BLANKLINE>
    </body>
    </html>


Inline Python expression
------------------------

This feature evaluates your inline expression and output to result::

    >>> print(render_string('''<html><body>
    ...     <?='hello, world'?>
    ... </body></html>'''))
    <html><body>
        hello, world
    </body></html>

By the default, this example raises an exception, evaluated expression must be
`str` (`unicode` in Python 2)::

    >>> print(render_string('''<html><body>
    ...     <?=1?>
    ... </body></html>''')) #doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    ...
    TypeError: Can't convert 'int' object to str implicitly

Set the `cast_string` feature::

    >>> print(render_string('''<?py
    ...         from katagami import cast_string
    ...     ?><html><body>
    ...     <?=1?>
    ... </body></html>'''))
    <html><body>
        1
    </body></html>

Also set the `except_hook` feature::

    >>> print(render_string('''<?py
    ...         from katagami import except_hook
    ...     ?><html><body>
    ...     <?=1?>
    ... </body></html>'''))
    <html><body>
        Can't convert 'int' object to str implicitly
    </body></html>


Embed Python script
-------------------

All indentation will be arranged automatically::

    >>> print(render_string('''<html>
    ... <?py
    ...     # It is a top level here. This works fine.
    ...     if 1:
    ...         msg = 'message from indented script'
    ... ?>
    ... <body>
    ...     <p><?=msg?></p>
    ...     <?py msg = 'message from single line script' # This works fine too. ?>
    ...     <p><?=msg?></p>
    ...     <? if 1: {?>
    ... <?py
    ... # Is is nested here. This also works fine.
    ... msg = 'message from nested indented script'
    ... ?>
    ...     <p><?=msg?></p>
    ...     <?}?>
    ... </body>
    ... </html>'''))
    <html>
    <BLANKLINE>
    <body>
        <p>message from indented script</p>
    <BLANKLINE>
        <p>message from single line script</p>
    <BLANKLINE>
    <BLANKLINE>
        <p>message from nested indented script</p>
    <BLANKLINE>
    </body>
    </html>


Block structure
---------------

Indentation with C-style block structure::

    >>> print(render_string('''<html>
    ... <body>
    ...     <p>hello,&nbsp;
    ...     <? try: {?>
    ...         <?=name?>
    ...     <?} except NameError: {?>
    ...         NameError
    ...     <?} else: {?>
    ...         never output here
    ...     <?}?>
    ...     </p>
    ... </body>
    ... </html>'''))
    <html>
    <body>
        <p>hello,&nbsp;
    <BLANKLINE>
    <BLANKLINE>
            NameError
    <BLANKLINE>
        </p>
    </body>
    </html>

Note
~~~~

 * '<? }' and '{ ?>' are wrong. Don't insert space. '<?}' and '{?>' are correct.
 * Ending colon (':') is required.
 * Block closing '<?}?>' is required.


Iteratable rendering
--------------------

Render with iteration::

    >>> renderer = render_string('''<html><body>
    ...     <p>hello, <?= name ?></p>
    ...     </body></html>''', {'name': 'world'}, flags=returns_iter)
    >>> print(list(renderer))
    ['<html><body>\n    <p>hello, ', 'world', '</p>\n    </body></html>']


Encoding detection
------------------

Encoding will be detected automatically::

    >>> print(render_string(b'''<html>
    ... <head><meta charset="shift-jis"></head>
    ... <body>\x93\xfa\x96{\x8c\xea</body>
    ... </html>'''))
    <html>
    <head><meta charset="shift-jis"></head>
    <body>\u65e5\u672c\u8a9e</body>
    </html>

Supported formats:

 * <?xml encoding="ENCODING"?>
 * <meta charset="ENCODING">
 * <meta http-equiv="Content-Type" content="MIMETYPE; ENCODING">


Tips
----

Get the translated result::

    >>> renderer = render_string('''<html><body>
    ...     <p><?= name ?></p>
    ...     </body></html>''',
    ...     flags=returns_renderer)
    >>> print(renderer.script)
    __file__ = "<template-script#0>"
    __encoding__ = "utf-8"
    def __main__():
        yield "<html><body>\n    <p>"
        # -*- line 2, column 7 -*-
        yield name
        yield "</p>\n    </body></html>"

History
-------

 * 2.1.0 remove caching, remove i18n, fix bug, add `wheezy.web.templates` support
 * 2.0.2 fix empty template error, change behavior of feature flags import
 * 2.0.1 improve backward compatibility of the test
 * 2.0.0 change a lot and add some features
 * 1.1.0 change api, add except_handler, add shorthand of gettext (<?_message?>),
         some fixes
 * 1.0.3 fix ignoring `encoding` argument, fix indent bug, add `renderString`
 * 1.0.2 improve doctest compatibility, some fixes
 * 1.0.1 fix bugs, docs, speed
 * 1.0.0 remove backward compatibility
"""
from __future__ import print_function, unicode_literals, division

__version__ = '2.1.0'
__author__ = __author_email__ = 'chrono-meter@gmx.net'
__license__ = 'PSF'
__url__ = 'http://pypi.python.org/pypi/katagami'
# http://pypi.python.org/pypi?%3Aaction=list_classifiers
__classifiers__ = [i.strip() for i in '''\
    Development Status :: 4 - Beta
    Intended Audience :: Developers
    License :: OSI Approved :: Python Software Foundation License
    Operating System :: OS Independent
    Programming Language :: Python :: 2.7
    Programming Language :: Python :: 3
    Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries
    Topic :: Software Development :: Libraries :: Python Modules
    Topic :: Text Processing :: Markup :: HTML
    Topic :: Text Processing :: Markup :: XML
    '''.strip().splitlines()]
    #Development Status :: 5 - Production/Stable

import sys
import traceback
import os
import os.path
import re
import io
import tokenize
import pprint
import unicodedata
import logging; logger = logging.getLogger(__name__); del logging
import unittest


__all__ = (
    'render_file',
    'render_string',
    'render_resource',
    'returns_bytes',
    'returns_iter',
    'returns_renderer',
    )


#
# constants
#
features = (
    'cast_string',
    'except_hook',
    )
TAB = '    '
PREFIX, SUFFIX = '<?', '?>'
returns_bytes = 1
returns_iter = 2
returns_renderer = 4
cast_string = 10
except_hook = 20
notgiven = object()


#
# backward compatibility
#
# NOTE: PEP: 373, Extend Python 2.7 life till 2020.
if sys.version < '2.7':
    raise RuntimeError('not supported version: %s' % sys.version)
if sys.version < '3':
    # doctest compatibility with Python 2 and Python 3
    __doc__ = re.sub(
        "Can't convert '(.*?)' object to str implicitly",
        "Can't convert '\\1' object to unicode implicitly",
        __doc__)
    BytesType = str
    StringType = unicode
    def next(generator):
        return generator.next()
else:
    BytesType = bytes
    StringType = str


def Py_UNICODE_ISPRINTABLE(ch):
    """Returns 1 for Unicode characters to be hex-escaped when repr()ed,
    0 otherwise.
    All characters except those characters defined in the Unicode character
    database as following categories are considered printable.
       * Cc (Other, Control)
       * Cf (Other, Format)
       * Cs (Other, Surrogate)
       * Co (Other, Private Use)
       * Cn (Other, Not Assigned)
       * Zl Separator, Line ('\u2028', LINE SEPARATOR)
       * Zp Separator, Paragraph ('\u2029', PARAGRAPH SEPARATOR)
       * Zs (Separator, Space) other than ASCII space('\x20').

    http://hg.python.org/releasing/3.4.1/file/ea310ca42bb2/Objects/unicodectype.c#l147
    """
    return unicodedata.category(ch) not in ('Cc', 'Cf', 'Cs', 'Co', 'Cn', 'Zl',
                                            'Zp', 'Zs')


def py3_repr_str(string):
    """Python 3 str.__repr__
    http://hg.python.org/releasing/3.4.1/file/ea310ca42bb2/Objects/unicodeobject.c#l12289
    """
    if sys.version >= '3':
        return repr(string)

    quote = '\''
    if '\'' in string:
        if '"' in string:
            pass
        else:
            quote = '"'

    result = quote

    for c in string:
        if c in (quote, '\\'):
            result += '\\' + c
        elif c == '\t':
            result += '\\t'
        elif c == '\n':
            result += '\\n'
        elif c == '\r':
            result += '\\r'
        elif ord(c) < ord(' ') or ord(c) == 0x7f:
            result += '\\x%2.2x' % ord(c)
        elif ord(c) < 0x7f:
            result += c
        elif Py_UNICODE_ISPRINTABLE(c):
            result += c
        else:
            if ord(c) <= 0xff:
                result += '\\x%2.2x' % ord(c)
            elif ord(c) <= 0xffff:
                result += '\\u%4.4x' % ord(c)
            else:
                result += '\\U00%6.6x' % ord(c)

    result += quote

    return result


def py3_repr_bytes(bytes):
    """Python 3 bytes.__repr__
    http://hg.python.org/releasing/3.4.1/file/ea310ca42bb2/Objects/bytesobject.c#l593
    """
    if sys.version >= '3':
        return repr(bytes)

    # quote = '"' if '\'' in object else '\''
    quote = b'\''

    result = 'b' + quote

    for c in bytes:
        if c in (quote, b'\\'):
            result += '\\' + c
        elif c == b'\t':
            result += '\\t'
        elif c == b'\n':
            result += '\\n'
        elif c == b'\r':
            result += '\\r'
        elif ord(c) < ord(b' ') or ord(c) >= 0x7f:
            result += '\\x%2.2x' % ord(c)
        else:
            result += c

    result += quote

    return result


class PrettyPrinter(pprint.PrettyPrinter):

    def format(self, object, context, maxlevels, level):
        if isinstance(object, StringType):
            return py3_repr_str(object), True, False
        elif isinstance(object, BytesType):
            return py3_repr_bytes(object), True, False

        return pprint._safe_repr(object, context, maxlevels, level)


def dprint(object):
    """Print raw if object is string, else print repr-ed object with pprint.
    """
    if isinstance(object, StringType):
        print(object)
    else:
        PrettyPrinter().pprint(object)


#
# utility functions
#

def execcode(code, globals):
    """This function resolves this problem in Python 2::
        SyntaxError: unqualified exec is not allowed in function it is a nested function
    """
    exec(code, globals)


def literalize(s):
    # `unicode_escape` escapes '\'' and '\t' and '\n' and '\r' and '\\'.
    return '"%s"' % s.encode('unicode_escape').decode().replace('"', '\\"')


def decorate_attributes(**kwargs):
    """attributes decorator"""
    def result(function):
        for i in kwargs.items():
            setattr(function, *i)
        return function
    return result


class PythonTokens(list):

    @classmethod
    def tokenize(cls, readline):
        return cls(tokenize.generate_tokens(readline))

    def untokenize(self, ignore_position=True):
        tokens = self
        if sys.version < '3':
            # NOTE: Is this bug of tokenize.untokenize() ?
            # http://bugs.python.org/issue?%40columns=id%2Cactivity%2Ctitle%2Ccreator%2Cassignee%2Cstatus%2Ctype&%40sort=-activity&%40filter=status&%40action=searchid&ignore=file%3Acontent&%40search_text=untokenize+&submit=search&status=-1%2C1%2C2%2C3
            tokens = [(tokenize.NL, '\n', (1, 0), (1, 1), '\n')] + tokens
        if ignore_position:
            tokens = (token[:2] for token in tokens)
        return tokenize.untokenize(tokens)

    @classmethod
    def from_string(cls, string):
        assert isinstance(string, StringType)

        return cls.tokenize(io.StringIO(string).readline)

    @classmethod
    def from_file(cls, file):
        try:
            import pathlib
        except ImportError:
            Path = type(None)
        else:
            Path = pathlib.Path

        if isinstance(file, Path):
            with file.open() as fp:
                return cls.tokenize(fp.readline)
        else:
            with open(file) as fp:
                return cls.tokenize(fp.readline)

    @property
    def linetokens(self):
        chunk = []
        for token in self:
            chunk.append(token)
            if token[0] in (tokenize.NEWLINE, tokenize.NL):
                yield chunk
                chunk = []

        if chunk:
            yield chunk

    def strip_comments(self):
        for token in self[:]:
            if token[0] == tokenize.COMMENT:
                self.remove(token)

    def set_indent(self, indent=''):
        r"""Justify indentation.

        >>> tokens = PythonTokens.from_string('''
        ... # comment
        ...     a
        ...     if 1:
        ...         b
        ...     ''')
        >>> tokens.set_indent()
        >>> dprint(tokens.untokenize())
        <BLANKLINE>
        # comment
        a 
        if 1 :
            b 
        <BLANKLINE>

        >>> tokens = PythonTokens.from_string('''
        ... # comment
        ...     a
        ...     if 1:
        ...         b
        ...     ''')
        >>> tokens.set_indent(TAB * 2)
        >>> dprint(tokens.untokenize())
        <BLANKLINE>
        # comment
                a 
                if 1 :
                    b 
        <BLANKLINE>
        """
        TokenInfo = getattr(tokenize, 'TokenInfo', lambda *a: a)
        first_indent = None

        for i, token in enumerate(self):
            # found firstmost indent
            if first_indent is None:
                if token[0] == tokenize.INDENT:
                    first_indent = token[1]
                # NOTE: no tokenize.ENCODING in python2
                elif token[0] in (tokenize.NEWLINE, tokenize.NL, tokenize.COMMENT):
                    pass
                else:
                    first_indent = ''

            # string = indent string starts from beggining of the line
            if token[0] == tokenize.INDENT:
                if first_indent:
                    assert token[1].startswith(first_indent)
                    token = TokenInfo(token[0],
                                      indent + token[1][len(first_indent):],
                                      *token[2:])
                else:
                    token = TokenInfo(token[0], indent + token[1], *token[2:])

            self[i] = token

        if not first_indent:
            self.insert(0, (tokenize.INDENT, indent))

    def get_first_tokens(self):
        r"""Get the firstline tokens.

        >>> tokens = PythonTokens.from_string('''
        ...     # comment
        ...     "docstring"
        ...     some_statement
        ...     ''')
        >>> dprint(' '.join(token[1] for token in tokens.get_first_tokens()))
        some_statement
        """
        found = False
        for token in self:
            # skip comment and docstring
            if token[0] in (tokenize.NL, tokenize.INDENT, tokenize.COMMENT,
                            tokenize.STRING, ):
                pass
            elif token[0] == tokenize.NEWLINE:
                if found:
                    break
            else:
                found = True
                yield token

    def get_encoding(self):
        raise NotImplementedError()


def get_encodings_from_content(bytes):
    r"""Search xml/html encoding and return it.

    >>> dprint(get_encodings_from_content(
    ...     b'<?xml version="1.0" encoding="UTF-8"?>'))
    UTF-8
    >>> dprint(get_encodings_from_content(
    ...     b"<?xml version='1.0' encoding='UTF-8'?>"))
    UTF-8
    >>> dprint(get_encodings_from_content(
    ...     b'<?xml version=1.0 encoding=UTF-8?>'))
    UTF-8

    >>> dprint(get_encodings_from_content(b'<meta charset="UTF-8">'))
    UTF-8
    >>> dprint(get_encodings_from_content(b"<meta charset='UTF-8'>"))
    UTF-8
    >>> dprint(get_encodings_from_content(b'<meta charset=UTF-8>'))
    UTF-8

    >>> dprint(get_encodings_from_content(
    ...     b'<meta http-equiv="Content-Type" content="text/html; ' \
    ...     b'charset=UTF-8">'))
    UTF-8
    >>> dprint(get_encodings_from_content(
    ...     b"<meta http-equiv='Content-Type' content='text/html; " \
    ...     b"charset=UTF-8'>"))
    UTF-8
    """
    # TODO: see requests.utils.get_encodings_from_content
    encoding_patterns = (
        # <?xml encoding="utf-8"?>
        (b'<\?xml\\s+.*?encoding=["\']?([^\\s"\']+)["\']?.*?\?>', ),
        # <meta charset="UTF-8">
        # <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        (b'<meta\\s+.*?charset=["\']?([^\\s"\']+)["\']?.*?>', ),
        )

    if not isinstance(bytes, BytesType):
        bytes = bytes.encode('ascii', 'ignore')

    for pattern in encoding_patterns:
        s = bytes
        match = None
        for i in pattern:
            match = re.search(i, s, re.DOTALL | re.IGNORECASE)
            if not match:
                break
            s = match.group(0)
        if match and match.group(1):
            return match.group(1).decode()

    return 'utf-8'


#
# module functions
#

class Translator(object):
    # TODO: subclass or wrap or extend or inherit template...
    _name_counter = 0

    def __init__(self, file):
        self._makescript(file)

        try:
            self.code = compile(self.script, self.name, 'exec')
        except SyntaxError as e:
            lineno, offset = self._find_original_pos(e.lineno, e.offset)
            new_exception = SyntaxError(
                '%s near the line' % e.msg, (
                e.filename,
                lineno,
                offset,
                self._template_body.splitlines()[lineno - 1],
                ))
            new_exception.__cause__ = e
            raise new_exception

    def __call__(self, context, flags=0):
        """Execute the template script.

         * `context` -- dict. Execution namespace. Note that this argument is
                        changed on rendering.
         * `flags` -- Change output behavior. This value is combination of
                      returns_bytes or returns_iter.
         * `return` -- str or bytes or generator. See `flags`.
        """
        result = self._exectamplate(context, flags)
        if flags & returns_iter:
            return result
        elif flags & returns_bytes:
            return BytesType().join(result)
        else:
            return StringType().join(result)

    def _makescript(self, file):
        """make a script string from a template file
        
         * `file` -- file-like object
        """
        # check argument
        if sys.version < '3':
            if not hasattr(file, 'read'):
                raise TypeError('%r is not supported type' % file)
        else:
            if not isinstance(file, io.IOBase):
                raise TypeError('%r is not supported type' % file)
 
        # read all
        template_body = file.read()

        # detect encoding
        encoding = getattr(file, 'encoding', '')
        if not encoding:
            try:
                encoding = get_encodings_from_content(template_body)
            except Exception:
                logger.debug('encoding detection error', exc_info=True)
            # check encoding registered in Python
            try:
                b'test string'.decode(encoding)
            except LookupError:
                encoding = ''
        if not encoding:
            encoding = sys.getdefaultencoding()
            if encoding == 'ascii':
                encoding = 'utf-8'

        # cast string
        if isinstance(template_body, BytesType):
            template_body = template_body.decode(encoding)

        # save variables
        if hasattr(file, 'name'):
            self.name = file.name
        else:
            self.name = '<template-script#%d>' % self._name_counter
            self._name_counter += 1
        self.encoding = encoding
        self.features = 0
        self._template_body = template_body

        # loop vars
        self._lines = []
        self._indent = []
        self._current_position = (1, 0)
        self._firstmost_executable = True
        last = 0
        pattern = re.compile(
            re.escape(PREFIX) + '(?P<body>.*?)' + re.escape(SUFFIX), re.DOTALL)

        for match in pattern.finditer(template_body):
            start, end = match.span()

            # get pos
            _ = template_body[:start].splitlines()
            self._current_position = (len(_), len(_[-1])) if _ else (1, 0)
            del _

            # leading chunk
            chunk = template_body[last:start]
            if chunk:
                self._appendline('yield ' + literalize(chunk))
            last = end

            # insert marker
            self._appendline(
                '# -*- line %d, column %d -*-' % self._current_position)

            # process PI
            chunk = match.group('body')

            for i in sorted(i for i in dir(self) if i.startswith('_handle_')):
                handler = getattr(self, i)
                if re.match(handler.pattern, chunk):
                    handler(chunk)
                    if getattr(handler, 'executable', True):
                        self._firstmost_executable = False
                    break

            # not supported <?...?>
            else:
                chunk = PREFIX + chunk + SUFFIX
                self._appendline('yield ' + literalize(chunk))

        # trailing chunk
        chunk = template_body[last:]
        if chunk:
            self._appendline('yield ' + literalize(chunk))

        # check remaining indentation
        if self._indent:
            lineno, offset = self._indent[-1]
            raise IndentationError(
                'brace is not closed', (
                self.name,
                lineno,
                offset,
                self._template_body.splitlines()[lineno - 1],
                ))

        # make a script
        prefix = [
            '__file__ = %s' % literalize(self.name),
            # '__name__ = "__main__"',
            '__encoding__ = %s' % literalize(self.encoding),
            # make a code as function for `yield` and `return`
            'def __main__():',
            ]
        if not self._lines:
            self._lines.insert(0, 'pass')
        self.script = '\n'.join(prefix) + '\n' \
                    + '\n'.join(TAB + i for i in self._lines)

        # cleanup
        del self._lines
        assert not self._indent
        del self._indent
        del self._current_position
        del self._firstmost_executable

    def _exectamplate(self, context, flags=0):
        # see https://github.com/mitsuhiko/jinja2/blob/master/jinja2/debug.py
        # `Python 3.4.1 <http://hg.python.org/releasing/3.4/file/8671f89107c8/Python/traceback.c>`
        # _Py_DisplaySourceLine -> io.open
        # `Python 2.7.7 <http://hg.python.org/releasing/2.7.7/file/4b38a5a36536/Python/traceback.c>`
        # _Py_DisplaySourceLine -> fopen
        def _fix_error_pos(e):
            filename, lineno, funcname, _ \
                = traceback.extract_tb(sys.exc_info()[2])[-1]

            if filename == self.name and funcname == '__main__':
                lineno, offset = self._find_original_pos(lineno)
                new_exception = type(e)(*e.args)
                new_exception.__cause__ = e
                code = compile('\n' * (lineno - 1) + 'raise new_exception',
                               self.name, 'exec')
                execcode(code, locals())

        # python2 doesn't allow using return and yield in same function
        execcode(self.code, context)

        executor = context['__main__']()
        # TODO: module['__main__'](**context) ?
        if executor is None: # The template is empty or that has only scripts.
            raise StopIteration

        # run (iterate) template code and fetch string chunks
        try:
            value = notgiven
            while 1:
                if value is notgiven:
                    try:
                        value = next(executor)
                    except Exception as e:
                        _fix_error_pos(e)
                        raise

                    # TODO: handle generator type
                    if not isinstance(value, StringType):
                        if self.features & cast_string:
                            f = executor.gi_frame
                            if f and '__cast_string__' in f.f_locals:
                                value = f.f_locals['__cast_string__'](value)
                            elif f and '__cast_string__' in f.f_globals:
                                value = f.f_globals['__cast_string__'](value)
                            else:
                                value = StringType(value)
                        else:
                            continue
                else:
                    try:
                        value = executor.throw(
                            TypeError,
                            'Can\'t convert \'%s\' object to %s implicitly' % (
                                type(value).__name__, StringType.__name__))
                    except Exception as e:
                        _fix_error_pos(e)
                        raise

                if flags & returns_bytes:
                    value = value.encode(self.encoding)
                yield value

                value = notgiven

        except StopIteration:
            pass

        finally:
            executor.close()

    def _appendline(self, line):
        self._lines.append(TAB * len(self._indent) + line)

    def _embedscript(self, script, posmarker=True):
        tokens = PythonTokens.from_string(script)

        if posmarker:
            _tokens = tokens
            tokens = PythonTokens()

            for line in _tokens.linetokens:
                pos = line[0][2]
                if pos[0] == 1:
                    pos = self._current_position[0] + pos[0] - 1, \
                          self._current_position[1] + pos[1]
                else:
                    pos = self._current_position[0] + pos[0] - 1, pos[1]
                tokens.append((tokenize.COMMENT,
                               '# -*- line %d, column %d -*-' % pos))
                tokens.append((tokenize.NL, '\n'))
                tokens.extend(line)

        tokens.set_indent(TAB * len(self._indent))
        self._lines.extend(tokens.untokenize().splitlines())

    def _find_original_pos(self, lineno, column=0):
        # find markers
        pos = (lineno, 0)
        pattern = re.compile(
            '\s*# -\*- line (?P<line>\d+), column (?P<column>\d+) -\*-\s*')

        for currrent_lineno, line in enumerate(self.script.splitlines()):
            currrent_lineno += 1 # lineno starts from 1
            matched = pattern.match(line)
            if matched:
                pos = (int(matched.group('line')),
                       int(matched.group('column')))
            if currrent_lineno >= lineno:
                return pos

        raise ValueError()

    # <?=...?>
    @decorate_attributes(pattern='^=')
    def _handle_inline_expression(self, chunk):
        r"""Inline Python expression.

        >>> dprint(render_string('hello, <?=name?>', {'name': 'world'}))
        hello, world

        >>> dprint(render_string('hello, <?=name # hello ?>', {'name': 'world'}))
        hello, world

        >>> dprint(render_string('hello, <?= # comment\nname # hello ?>', {'name': 'world'}))
        hello, world


        Without cast_string, except_hook:
        >>> dprint(render_string('''
        ...     hello, <?=name?>
        ...     ''', {'name': 1}).strip()) #doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
            ...
        TypeError: ...

        With cast_string:
        >>> dprint(render_string('''<?py
        ...         from katagami import cast_string
        ...     ?>
        ...     hello, <?=name?>
        ...     ''', {'name': 1}).strip())
        hello, 1

        With except_hook:
        >>> dprint(render_string('''<?py
        ...         from katagami import except_hook
        ...     ?>
        ...     hello, <?=name?>
        ...     ''', {'name': 1}).strip()) # doctest:+ELLIPSIS
        hello, Can't convert 'int' object to ... implicitly


        Customize cast_string behavior:
        >>> dprint(render_string('''<?py
        ...         from katagami import cast_string
        ...         def __cast_string__(o):
        ...             "__cast_string__ must be return str (or unicode in Python 2)"
        ...             return '[%s]' % o
        ...     ?>
        ...     hello, <?=name?>
        ...     ''', {'name': 1}).strip())
        hello, [1]

        Give __cast_string__ via context:
        >>> dprint(render_string('''<?py
        ...         from katagami import cast_string
        ...     ?>
        ...     hello, <?=name?>
        ...     ''',
        ...     {'name': 1, '__cast_string__': lambda o: '<%s>' % o}).strip())
        hello, <1>

        Give __cast_string__ via default_context:
        >>> default_context['__cast_string__'] = lambda o: '(%s)' % o
        >>> dprint(render_string('''<?py
        ...         from katagami import cast_string
        ...     ?>
        ...     hello, <?=name?>
        ...     ''', {'name': 1}).strip())
        hello, (1)
        >>> del default_context['__cast_string__']


        Curtomize except_hook behavior:
        >>> dprint(render_string('''<?py
        ...         from katagami import except_hook
        ...         def __except_hook__(typ, val, tb):
        ...             "__except_hook__ must be return str (or unicode in Python 2)"
        ...             return '%s catched' % typ.__name__
        ...     ?>
        ...     hello, <?=name?>
        ...     ''', {'name': 1}).strip())
        hello, TypeError catched

        Give __except_hook__ via context:
        >>> dprint(render_string('''<?py
        ...         from katagami import except_hook
        ...     ?>
        ...     hello, <?=name?>
        ...     ''',
        ...     {'name': 1, '__except_hook__': lambda t, v, tb: str(v)}).strip()) # doctest:+ELLIPSIS
        hello, Can't convert 'int' object to ... implicitly

        Give __except_hook__ via default_context:
        >>> default_context['__except_hook__'] = lambda t, v, tb: str(v)
        >>> dprint(render_string('''<?py
        ...         from katagami import except_hook
        ...     ?>
        ...     hello, <?=name?>
        ...     ''', {'name': 1}).strip()) # doctest:+ELLIPSIS
        hello, Can't convert 'int' object to ... implicitly
        >>> del default_context['__except_hook__']
        """
        # sanitize expression
        tokens = PythonTokens.from_string(chunk[1:])
        tokens.strip_comments()
        expr = tokens.untokenize().strip()

        # except_hook is enabled
        if self.features & except_hook:
            self._embedscript('''
                try:
                    yield %s
                except:
                    if '__except_hook__' in locals():
                        yield locals()['__except_hook__'](
                            *__import__('sys').exc_info())
                    elif '__except_hook__' in globals():
                        yield globals()['__except_hook__'](
                            *__import__('sys').exc_info())
                    else:
                        yield %s(__import__('sys').exc_info()[1])
                ''' % (expr, StringType.__name__), posmarker=False)

        # normal mode, except_hook is disabled
        else:
            self._appendline('yield ' + expr)

    # <?py...?>
    @decorate_attributes(pattern='^py')
    def _handle_embed_script(self, chunk):
        r"""Embed Python script.

        Simple:
        >>> dprint(render_string('''
        ...     <?py
        ...         name = 'world'
        ...     ?>
        ...     hello, <?=name?>
        ...     ''').strip())
        hello, world

        Simple, different level indentation:
        >>> dprint(render_string('''
        ...     <?py
        ...         name = 'joe'
        ...     ?>
        ...     <?py
        ... name = 'world'
        ...     ?>
        ...     hello, <?=name?>
        ...     ''').strip())
        hello, world

        Nested with statement:
        >>> dprint(render_string('''
        ...     <? if 1: {?>
        ...         <?py
        ...             name = 'world'
        ...         ?>
        ...     <?}?>
        ...     hello, <?=name?>
        ...     ''').strip())
        hello, world

        Get feature flags from top of the embedded script:
        >>> render_string('''<?py
        ...     # comment
        ...     "docstring"
        ...     from katagami import cast_string, except_hook
        ...     ?>
        ...     ''', flags=returns_renderer).features
        30
        >>> render_string('''<html><?py
        ...     # comment
        ...     "docstring"
        ...     from katagami import cast_string, except_hook
        ...     ?></html>
        ...     ''', flags=returns_renderer).features
        30
        """
        # top of the template and first-line is `from katagami import ***`
        if self._firstmost_executable:
            firstline = list(
                PythonTokens.from_string(chunk[2:]).get_first_tokens())
            prefix = ' '.join(i[1] for i in firstline[:3])
            if prefix == 'from %s import' % __name__:
                for token in firstline[3:]:
                    if token[0] == tokenize.NAME and token[1] in self.features:
                        self.features |= globals()[token[1]]

        self._embedscript(chunk[2:])

    # <?}...{?>
    @decorate_attributes(pattern='(^}|.*{$)')
    def _handle_block(self, chunk):
        r"""Bridge Python and XML by brace.

        Simple, if-else:
        >>> dprint(render_string('''
        ...     <? if 1: {?>
        ...         hello, world
        ...     <?} else: {?>
        ...         hidden area
        ...     <?}?>
        ...     ''').strip())
        hello, world

        Nested:
        >>> dprint(render_string('''
        ...     <? if 1: {?>
        ...         <? if 1: {?>
        ...             hello, world
        ...         <?}?>
        ...     <?}?>''').strip())
        hello, world

        Simple, try-except-finally:
        >>> dprint(re.sub('\s+', ' ', render_string('''
        ...     hello,
        ...     <? try: {?>
        ...         <?=name?>
        ...     <?} except NameError: {?>
        ...         unknown
        ...     <?} finally: {?>
        ...         !
        ...     <?}?>
        ...     ''').strip()))
        hello, unknown !
        """
        if chunk.startswith('}'):
            chunk = chunk[1:]
            try:
                self._indent.pop()
            except LookupError:
                lineno, offset = self._current_position
                raise IndentationError(
                    'brace is not started', (
                    self.name,
                    lineno,
                    offset,
                    self._template_body.splitlines()[lineno - 1],
                    ))

        indent = None
        if chunk.endswith('{'):
            chunk = chunk[:-1]
            indent = self._current_position

        chunk = chunk.strip()
        if chunk:
            assert chunk.split()[0] not in ('def', 'class')
            self._appendline(chunk)

        if indent:
            self._indent.append(indent)

    # <?\...?>
    @decorate_attributes(pattern='^\\\\', executable=False)
    def _handle_escape(self, chunk):
        r"""Escape XML PIs.

        >>> dprint(render_string('<?\py "hello, world"?>'))
        <?py "hello, world"?>
        """
        self._appendline('yield ' + literalize(PREFIX + chunk[1:] + SUFFIX))


#
# module globals
#
default_translator = Translator
default_context = {
    # '__except_hook__': function(type, value, traceback) -> 'repr-ed error',
    # '__cast_string__': function(any_object) -> 'repr-ed object',
    # 'escape': xml.sax.saxutils.escape,
    # 'quoteattr': xml.sax.saxutils.quoteattr,
    }


def render_file(file_or_filename, context={}, flags=0):
    r"""Render a file-like object or a file.

     * `file_or_filename` -- file-like object or filename
     * `context` -- variables for template execution context
     * `flags` -- Combination of these values: returns_bytes, returns_iter,
                                               returns_renderer.
    """
    if isinstance(file_or_filename, StringType):
        with open(file_or_filename, 'rb') as fp:
            template = default_translator(fp)
    else:
        template = default_translator(file_or_filename)

    if flags & returns_renderer:
        assert not context
        return template

    return template(dict(default_context, **context), flags)


def render_string(string_or_bytes, context={}, flags=0):
    r"""Render a string or a bytes.


    >>> tmpl = '<?="\u3053\u3093\u306b\u3061\u306f"?>'

    String-in, string-out:
    >>> dprint(render_string(tmpl))
    \u3053\u3093\u306b\u3061\u306f

    Bytes-in, string-out:
    >>> dprint(render_string(tmpl.encode('utf-8')))
    \u3053\u3093\u306b\u3061\u306f


    String-in, Bytes-out:
    >>> dprint(render_string(tmpl, flags=returns_bytes))
    b'\xe3\x81\x93\xe3\x82\x93\xe3\x81\xab\xe3\x81\xa1\xe3\x81\xaf'

    Bytes-in, bytes-out:
    >>> dprint(render_string(tmpl.encode('utf-8'), flags=returns_bytes))
    b'\xe3\x81\x93\xe3\x82\x93\xe3\x81\xab\xe3\x81\xa1\xe3\x81\xaf'

    String-in, string-iterator-out:
    >>> dprint(list(render_string(tmpl, flags=returns_iter)))
    ['\u3053\u3093\u306b\u3061\u306f']

    String-in, bytes-iterator-out:
    >>> dprint(list(render_string(tmpl, flags=returns_bytes | returns_iter)))
    [b'\xe3\x81\x93\xe3\x82\x93\xe3\x81\xab\xe3\x81\xa1\xe3\x81\xaf']

    Bytes-in, string-iterator-out:
    >>> dprint(list(render_string(tmpl.encode('utf-8'), flags=returns_iter)))
    ['\u3053\u3093\u306b\u3061\u306f']

    Bytes-in, bytes-iterator-out:
    >>> dprint(list(render_string(tmpl.encode('utf-8'),
    ...                            flags=returns_bytes | returns_iter)))
    [b'\xe3\x81\x93\xe3\x82\x93\xe3\x81\xab\xe3\x81\xa1\xe3\x81\xaf']


    >>> renderer = render_string(tmpl, flags=returns_renderer)
    >>> isinstance(renderer, (StringType, BytesType))
    False
    >>> context = {}
    >>> bool(context)
    False
    >>> dprint(renderer(context))
    \u3053\u3093\u306b\u3061\u306f
    >>> bool(context)
    True
    """
    if isinstance(string_or_bytes, StringType):
        string_or_bytes = io.StringIO(string_or_bytes)
    elif isinstance(string_or_bytes, BytesType):
        string_or_bytes = io.BytesIO(string_or_bytes)
    else:
        raise TypeError(string_or_bytes)

    template = default_translator(string_or_bytes)

    if flags & returns_renderer:
        assert not context
        return template

    return template(dict(default_context, **context), flags)


def render_resource(package_or_requirement, resource_name, context={}, flags=0):
    r"""Render a package resource via `pkg_resources.resource_stream()`.
    """
    import pkg_resources

    template = default_translator(
        pkg_resources.resource_stream(package_or_requirement, resource_name))

    if flags & returns_renderer:
        assert not context
        return template

    return template(dict(default_context, **context), flags)


# TODO: webob.dec.wsgify(TemplateApp(filename, **response_kwargs))


class KatagamiTemplate(object):

    def __init__(self, path=None, suffix='.html', flags=0,
                 default_context=default_context, cache=None,
                 update_on_modified=True):
        assert not (flags & returns_renderer)
        self.path = path
        self.suffix = suffix
        self.flags = flags
        self.default_context = default_context
        self.cache = cache
        self.update_on_modified = update_on_modified

    def _get_template_filename(self, template_name):
        return os.path.join(self.path, template_name + self.suffix)

    def _create_template(self, template_name):
        import katagami

        filename = self._get_template_filename(template_name)
        mtime = os.stat(filename).st_mtime \
                if self.update_on_modified else -1

        if self.cache is not None and template_name in self.cache \
           and self.cache[template_name].mtime >= mtime:
            result = self.cache[template_name]

        else:
            with open(filename, 'rb') as fp:
                result = katagami.Translator(fp)

            if self.cache is not None:
                result.mtime = mtime
                self.cache[template_name] = result

        return result

    def __call__(self, template_name, kwargs):
        """Template contract is any callable of the following form:

            def render_template(self, template_name, **kwargs):
                return 'unicode string'

        https://pythonhosted.org/wheezy.web/userguide.html#contract
        """

        template = self._create_template(template_name)

        context = {}
        context.update(self.default_context)
        context.update(kwargs)

        # get wheezy.web.handlers.base.BaseHandler.render_template
        # if 'render_template' not in context:
        #     try:
        #         context['render_template'] \
        #             = context['path_for'].__self__.render_template
        #     except (LookupError, AttributeError):
        #         pass

        return template(context, self.flags)


# try:
#     import wheezy.web.templates
# except ImportError:
#     pass
# else:
#     wheezy.web.templates.KatagamiTemplate = KatagamiTemplate


class Test(unittest.TestCase):

    def render(self, chunk, lines=1, columns=0):
        return render_string(('\n' * (lines - 1)) + (' ' * columns) + chunk)

    def test_empty_template(self):
        self.assertEqual(render_string(''), '')

    def test_syntax_error_position_mod(self):
        with self.assertRaises(SyntaxError) as cx:
            self.render('<?py syntax error ?>', 10, 10)
        self.assertEqual(cx.exception.lineno, 10)
        self.assertEqual(cx.exception.offset, 10)

        # missing brace closing
        with self.assertRaises(IndentationError) as cx:
            self.render('<? if 1: {?>', 5, 9)
        self.assertEqual(cx.exception.lineno, 5)
        self.assertEqual(cx.exception.offset, 9)

        # brace closing without opening
        with self.assertRaises(IndentationError) as cx:
            self.render('<?} elif 1: {?>', 11, 3)
        self.assertEqual(cx.exception.lineno, 11)
        self.assertEqual(cx.exception.offset, 3)

    def test_error_position_mod(self):
        try:
            self.render('<?= 1 ?>', 3, 7)
        except TypeError:
            filename, lineno, funcname, _ \
                = traceback.extract_tb(sys.exc_info()[2])[-1]
            self.assertEqual(lineno, 3)


if __name__ == '__main__':
    # register: setup.py check sdist register upload
    # upload: setup.py check sdist upload
    import __main__
    import os.path
    import doctest
    import distutils.core

    __main__.__name__ = os.path.splitext(os.path.basename(__file__))[0]
    sys.modules[__main__.__name__] = __main__
    target = __main__

    if 'check' in sys.argv:
        unittest.main(argv=sys.argv[:1], exit=False)
        doctest.testmod()
        try:
            import docutils.core
        except ImportError:
            pass
        else:
            s = docutils.core.publish_string(target.__doc__, writer_name='html')
            with open(os.path.splitext(__file__)[0] + '.html', 'wb') as fp:
                fp.write(s)

    # http://docs.python.org/3/distutils/apiref.html?highlight=setup#distutils.core.setup
    distutils.core.setup(
        name=target.__name__,
        version=target.__version__,
        description=target.__doc__.splitlines()[0],
        long_description=target.__doc__,
        author=target.__author__,
        author_email=target.__author_email__,
        url=target.__url__,
        classifiers=target.__classifiers__,
        license=target.__license__,
        py_modules=[target.__name__, ],
        )


