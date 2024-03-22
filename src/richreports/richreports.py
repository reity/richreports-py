"""
Library that supports the construction of human-readable, interactive static
analysis reports that consist of decorated concrete syntax representations of
programs.
"""
from __future__ import annotations
from typing import Union, Tuple
import doctest

class location(Tuple[int, int]):
    """
    Data structure for representing a location within a report as a tuple of
    two integers: the line number (where the first line in the report has a
    line number of ``1``) and the column on that line.
    """
    def __getattribute__(self, name):
        """
        Simulate named attributes for the two components of an instance.

        >>> l = location((13, 24))
        >>> l.line
        13
        >>> l.column
        24

        Other attributes should not be affected.

        >>> str(type(l.__hash__))
        "<class 'method-wrapper'>"
        """
        if name == 'line':
            return self[0]
        if name == 'column':
            return self[1]

        return object.__getattribute__(self, name)

class report:
    """
    Data structure that represents the raw concrete syntax string as a
    two-dimensional array of two-sided stacks. Each stack holds delimiters
    (left and right) that may appear before or after that character in
    the rendered version of the report.

    >>> r = report(
    ...    'def f(x, y):\\n' +
    ...    '    return x + y'
    ... )

    The individual lines in the supplied string can be retrieved via the
    ``lines`` attribute.

    >>> list(r.lines)
    ['def f(x, y):', '    return x + y']

    Delimiters can be added around a range within the report by specifying the
    locations corresponding to the endpoints (inclusive) of the range.

    >>> r.enrich((2, 11), (2, 15), '(', ')')
    >>> for line in r.render().split('\\n'):
    ...     print(line)
    def f(x, y):
        return (x + y)

    The optional ``enrich_intermediate_lines`` parameter can be used to delimit
    all complete lines that appear between the supplied endpoints.

    >>> r.enrich((1, 0), (2, 15), '<b>', '</b>', True)
    >>> for line in r.render().split('\\n'):
    ...     print(line)
    <b>def f(x, y):</b>
    <b>    return (x + y)</b>

    By default, the ``enrich_intermediate_lines`` parameter is set to ``False``.

    >>> r.enrich((1, 0), (2, 15), '<div>\\n', '\\n</div>')
    >>> for line in r.render().split('\\n'):
    ...     print(line)
    <div>
    <b>def f(x, y):</b>
    <b>    return (x + y)</b>
    </div>
    """
    def __init__(self: report, string: str):
        self.string = string
        self.lines = string.split('\n')
        self._stacks = (
            [[]] + # Allow line numbers to begin at index ``1``.
            [
                [([], c, []) for c in line] +
                [([], '', [])] # Allow enrichment of empty lines.
                for line in self.lines
            ]
        )

    def enrich( # pylint: disable=too-many-arguments
            self: report,
            start: Union[tuple, location], end: Union[tuple, location],
            left: str, right: str,
            enrich_intermediate_lines = False
        ):
        """
        Add a pair of left and right delimiters around a given range within this
        report instance.
        
        >>> r = report(
        ...    'def f(x, y):\\n' +
        ...    '    return x + y'
        ... )
        >>> r.enrich((1, 0), (2, 15), '<b>', '</b>', True)
        >>> for line in r.render().split('\\n'):
        ...     print(line)
        <b>def f(x, y):</b>
        <b>    return x + y</b>
        """
        # Tuples containing two integers are permitted.
        start = location(start)
        end = location(end)

        # Add the delimiters at the specified positions, and around any
        # intermediate lines.
        self._stacks[start.line][start.column][0].append(left)
        if enrich_intermediate_lines:
            for line in range(start.line, end.line):
                self._stacks[line][-1][2].append(right)
                self._stacks[line + 1][0][0].append(left)
        self._stacks[end.line][end.column][2].append(right)

    def render(self: report) -> str:
        """
        Return the report (including all delimiters) as a string.

        >>> r = report(
        ...    'def f(x, y):\\n' +
        ...    '    return x + y'
        ... )
        >>> for line in r.render().split('\\n'):
        ...     print(line)
        def f(x, y):
            return x + y
        """
        return '\n'.join([
            ''.join([
                ''.join(reversed(pres)) + c + ''.join(posts)
                for (pres, c, posts) in line
            ])
            for line in self._stacks[1:]
        ])

if __name__ == '__main__':
    doctest.testmod() # pragma: no cover
