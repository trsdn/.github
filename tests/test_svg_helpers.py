from datetime import UTC, datetime, timedelta
from xml.etree import ElementTree

from profile_stats.render.svg import esc, n, relative_time, svg_root, truncate


def test_escapes_xml_and_strips_control_characters():
    assert esc('A&B <tag> "quote" \x01') == 'A&amp;B &lt;tag&gt; &quot;quote&quot; '


def test_truncate_is_unicode_safe():
    assert truncate('abcdef', 4) == 'abc…'
    assert truncate('åß∂ƒ', 3) == 'åß…'


def test_number_formatting():
    assert n(999) == '999'
    assert n(1200) == '1.2k'
    assert n(12_500) == '12k'
    assert n(1_200_000) == '1.2m'


def test_relative_time():
    now = datetime(2026, 8, 24, tzinfo=UTC)
    assert relative_time(now - timedelta(days=3), now) == '3d ago'
    assert relative_time(now, now) == 'just now'


def test_svg_root_is_well_formed():
    ElementTree.fromstring(svg_root(10, 10, '<text>A&amp;B</text>'))
