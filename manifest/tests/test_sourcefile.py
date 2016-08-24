from ..sourcefile import SourceFile

def create(filename, contents=b""):
    assert isinstance(contents, bytes)
    return SourceFile("/", filename, "/", contents=contents)


def items(s):
    return [
        (item.item_type, item.url)
        for item in s.manifest_items()
    ]


def test_name_is_non_test():
    non_tests = [
        ".gitignore",
        ".travis.yml",
        "MANIFEST.json",
        "tools/test.html",
        "resources/test.html",
        "common/test.html",
        "conformance-checkers/test.html",
    ]

    for rel_path in non_tests:
        s = create(rel_path)
        assert s.name_is_non_test

        assert not s.content_is_testharness

        assert items(s) == []


def test_name_is_manual():
    manual_tests = [
        "html/test-manual.html",
        "html/test-manual.xhtml",
    ]

    for rel_path in manual_tests:
        s = create(rel_path)
        assert not s.name_is_non_test
        assert s.name_is_manual

        assert not s.content_is_testharness

        assert items(s) == [("manual", "/" + rel_path)]


def test_name_is_visual():
    visual_tests = [
        "html/test-visual.html",
        "html/test-visual.xhtml",
    ]

    for rel_path in visual_tests:
        s = create(rel_path)
        assert not s.name_is_non_test
        assert s.name_is_visual

        assert not s.content_is_testharness

        assert items(s) == [("visual", "/" + rel_path)]


def test_name_is_reference():
    references = [
        "css-namespaces-3/reftest/ref-lime-1.xml",
        "css21/reference/pass_if_box_ahem.html",
        "css21/csswg-issues/submitted/css2.1/reference/ref-green-box-100x100.xht",
        "selectors-3/selectors-empty-001-ref.xml",
        "css21/text/text-indent-wrap-001-notref-block-margin.xht",
        "css21/text/text-indent-wrap-001-notref-block-margin.xht",
        "css21/css-e-notation-ref-1.html",
        "css21/floats/floats-placement-vertical-004-ref2.xht",
        "css21/box/rtl-linebreak-notref1.xht",
        "css21/box/rtl-linebreak-notref2.xht"
    ]

    for rel_path in references:
        s = create(rel_path)
        assert not s.name_is_non_test
        assert s.name_is_reference

        assert not s.content_is_testharness

        assert items(s) == []


def test_worker():
    s = create("html/test.worker.js")
    assert not s.name_is_non_test
    assert not s.name_is_manual
    assert not s.name_is_visual
    assert not s.name_is_multi_global
    assert s.name_is_worker
    assert not s.name_is_reference

    assert not s.content_is_testharness

    assert items(s) == [("testharness", "/html/test.worker")]


def test_multi_global():
    s = create("html/test.any.js")
    assert not s.name_is_non_test
    assert not s.name_is_manual
    assert not s.name_is_visual
    assert s.name_is_multi_global
    assert not s.name_is_worker
    assert not s.name_is_reference

    assert not s.content_is_testharness

    assert items(s) == [
        ("testharness", "/html/test.any.html"),
        ("testharness", "/html/test.any.worker"),
    ]


def test_testharness():
    content = b"<script src=/resources/testharness.js></script>"

    for ext in ["htm", "html"]:
        filename = "html/test." + ext
        s = create(filename, content)

        assert not s.name_is_non_test
        assert not s.name_is_manual
        assert not s.name_is_visual
        assert not s.name_is_multi_global
        assert not s.name_is_worker
        assert not s.name_is_reference

        assert s.content_is_testharness

        assert items(s) == [("testharness", "/" + filename)]


def test_relative_testharness():
    content = b"<script src=../resources/testharness.js></script>"

    for ext in ["htm", "html"]:
        filename = "html/test." + ext
        s = create(filename, content)

        assert not s.name_is_non_test
        assert not s.name_is_manual
        assert not s.name_is_visual
        assert not s.name_is_multi_global
        assert not s.name_is_worker
        assert not s.name_is_reference

        assert not s.content_is_testharness

        assert items(s) == []


def test_testharness_xhtml():
    content = b"""
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<script src="/resources/testharness.js"></script>
<script src="/resources/testharnessreport.js"></script>
</head>
<body/>
</html>
"""

    for ext in ["xhtml", "xht", "xml"]:
        filename = "html/test." + ext
        s = create(filename, content)

        assert not s.name_is_non_test
        assert not s.name_is_manual
        assert not s.name_is_visual
        assert not s.name_is_multi_global
        assert not s.name_is_worker
        assert not s.name_is_reference

        assert s.content_is_testharness

        assert items(s) == [("testharness", "/" + filename)]


def test_relative_testharness_xhtml():
    content = b"""
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<script src="../resources/testharness.js"></script>
<script src="../resources/testharnessreport.js"></script>
</head>
<body/>
</html>
"""

    for ext in ["xhtml", "xht", "xml"]:
        filename = "html/test." + ext
        s = create(filename, content)

        assert not s.name_is_non_test
        assert not s.name_is_manual
        assert not s.name_is_visual
        assert not s.name_is_multi_global
        assert not s.name_is_worker
        assert not s.name_is_reference

        assert not s.content_is_testharness

        assert items(s) == []


def test_testharness_svg():
    content = b"""\
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:h="http://www.w3.org/1999/xhtml"
     version="1.1"
     width="100%" height="100%" viewBox="0 0 400 400">
<title>Null test</title>
<h:script src="/resources/testharness.js"/>
<h:script src="/resources/testharnessreport.js"/>
</svg>
"""

    filename = "html/test.svg"
    s = create(filename, content)

    assert not s.name_is_non_test
    assert not s.name_is_manual
    assert not s.name_is_visual
    assert not s.name_is_multi_global
    assert not s.name_is_worker
    assert not s.name_is_reference

    assert s.root
    assert s.content_is_testharness

    assert items(s) == [("testharness", "/" + filename)]


def test_relative_testharness_svg():
    content = b"""\
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     xmlns:h="http://www.w3.org/1999/xhtml"
     version="1.1"
     width="100%" height="100%" viewBox="0 0 400 400">
<title>Null test</title>
<h:script src="../resources/testharness.js"/>
<h:script src="../resources/testharnessreport.js"/>
</svg>
"""

    filename = "html/test.svg"
    s = create(filename, content)

    assert not s.name_is_non_test
    assert not s.name_is_manual
    assert not s.name_is_visual
    assert not s.name_is_multi_global
    assert not s.name_is_worker
    assert not s.name_is_reference

    assert s.root
    assert not s.content_is_testharness

    assert items(s) == []


def test_testharness_ext():
    content = b"<script src=/resources/testharness.js></script>"

    for filename in ["test", "test.test"]:
        s = create("html/" + filename, content)

        assert not s.name_is_non_test
        assert not s.name_is_manual
        assert not s.name_is_visual
        assert not s.name_is_multi_global
        assert not s.name_is_worker
        assert not s.name_is_reference

        assert not s.root
        assert not s.content_is_testharness

        assert items(s) == []


def test_css_visual():
    content = b"""
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<link rel="help" href="http://www.w3.org/TR/CSS21/box.html#bidi-box-model"/>
</head>
<body/>
</html>
"""

    for ext in ["xht", "html", "xhtml", "htm", "xml", "svg"]:
        filename = "html/test." + ext
        s = create(filename, content)

        assert not s.name_is_non_test
        assert not s.name_is_manual
        assert not s.name_is_visual
        assert not s.name_is_multi_global
        assert not s.name_is_worker
        assert not s.name_is_reference
        assert not s.content_is_testharness
        assert not s.content_is_ref_node

        assert s.content_is_css_visual

        assert items(s) == [("visual", "/" + filename)]


def test_xhtml_with_entity():
    content = b"""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
   "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
&nbsp;
</html>
"""

    for ext in ["xhtml", "xht", "xml"]:
        filename = "html/test." + ext
        s = create(filename, content)

        assert s.root is not None

        assert items(s) == []
