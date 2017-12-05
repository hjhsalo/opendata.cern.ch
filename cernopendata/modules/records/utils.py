# -*- coding: utf-8 -*-
#
# This file is part of CERN Open Data Portal.
# Copyright (C) 2017 CERN.
#
# CERN Open Data Portal is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# CERN Open Data Portal is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with CERN Open Data Portal; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

"""Custom rendered for invenio-records-ui to prerender markdown content."""

from __future__ import absolute_import, print_function

from flask import current_app, render_template, render_template_string, Markup


def render_markdown_or_html(pid, record, template=None, **kwargs):
    r"""Renderer for markdown content containing Jinja directives.

    If record contains markdown content (type 'md') this renderer pre-renders
    markdown content with 1) Jinja renderer, 2) then with markdown renderer
    and then passes it to template rendering.

    Enables to use Jinja directives e.g. `url_for` in markdown content.
    (`<img src="{{ url_for('static', filename='img/demo.png') }}">`)

    :param pid: PID object.
    :param record: Record object.
    :param template: Template to render.
    :param \*\*kwargs: Additional view arguments based on URL rule.
    :return: The rendered template.
    """
    content = ""

    if record.get("body", {}).get("format", None) == "md":

        # Make sure that a Markdown parser is available
        parser = current_app.extensions.get('cod-markdown', None) or \
                 current_app.extensions.get('cod-mistune', None)
        if parser is None:
            # TODO: Write more meaningful error handling
            raise Exception("No Markdown parser available")

        md_content = record.get("body", {}).get("content", None)

        prerendered_content = render_template_string(md_content)

        content = Markup(parser.md(prerendered_content))

    elif record.get("body", {}).get("format", None) == "html":
        content = Markup(record.get("body", {}).get("content", None))

    else:
        # TODO: Write more meaningful error handling
        raise Exception("Unknown content type")

    return render_template(
        template,
        pid=pid,
        record=record,
        content=content
    )
