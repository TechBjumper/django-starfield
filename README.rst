Fork https://edugit.org/nik/django-starfield

Django stars widget
===================

Description
-----------

This is a simple widget rendering so-called rating stars as input for an
integer field. It is based solely on CSS 3, as laid out by `Martin Ivanov
<http://experiments.wemakesites.net/css3-rating-stars-with-selection.html>`_.

This is different from other star rating applications in that it provides
only a widget returning its selction to any IntegerField. It is not a
complete rating application, just a presentational widget for integer input.
It is also different in that it depends only on CSS3, without any
JavaScript.

In contrast to others (and to the original work credited above), this widget
also works on browsers that do not support CSS (like text-mode browsers). In
that case, it renders as basic radio buttons with numbers.

Usage
-----

Supports Django 5.2 and 6.0. Python 3.10 or newer is required; Django 6.0
requires Python 3.12 or newer. Older Django and Python versions are no longer
supported.

Add ``django_starfield`` to ``INSTALLED_APPS`` so Django can discover the
widget template and stylesheet. Use ``django.contrib.staticfiles`` and run
``collectstatic`` when deploying, as for other Django static assets.

Add the Stars widget to any IntegerField in a Django form.

.. code:: python

  from django import forms
  from django_starfield import Stars

  class StarsExampleForm(forms.Form):
      rating = forms.IntegerField(widget=Stars)

The following aspects are configurable, both in the Django settings and when
creating the widget (by passing an argument to Stars):

.. list-table:: Configuration
   :header-rows: 1

   * - Aspect
     - Default
     - Setting
     - Argument
   * - Number of stars
     - 5
     - ``STARFIELD_STARS``
     - ``stars``
   * - CSS content expression
     - ``"'\\2605'"``
     - ``STARFIELD_CONTENT``
     - ``content``
   * - Colour
     - ``#f5b301``
     - ``STARFIELD_COLOUR``
     - ``colour``
   * - Stylesheet path
     - ``django_starfield.css``
     - ``STARFIELD_CSS``
     - ``css_file``

The template can be configured with ``STARFIELD_TEMPLATE``. Custom templates
also receive ``unique_id``, which the default template uses in its HTML ids so
several widgets with the same field name can share a page. A random id is
generated on every render unless one is passed to the widget constructor.
CSS content and colour options are developer configuration, not user input.

Please note that some browsers render some Unicode characters, especially
emojis, as images, so changing the font colour will not work.


Upgrading from 1.x
------------------

Version 2.0 requires Django 5.2 or newer and replaces the ``codepoint``
option with ``content``, which takes a full CSS ``content`` value:

.. code:: python

    # 1.x
    Stars(codepoint='1f42c')
    STARFIELD_CODEPOINT = '1f42c'

    # 2.0
    Stars(content="'\\1f42c'")
    STARFIELD_CONTENT = "'\\1f42c'"

The HTML ids rendered by the default template now include ``unique_id``
(``<name>-<unique_id>-<n>`` instead of ``<name>-<n>``). Update any CSS or
JavaScript that targets the old ids, or pass a fixed ``unique_id``.


Django admin
------------

Attach a ModelForm to your ModelAdmin (replace Product with your own model):

.. code:: python

    from django import forms
    from django.contrib import admin
    from django_starfield import Stars
    from .models import Product

    class ProductAdminForm(forms.ModelForm):
        rating = forms.IntegerField(
            min_value=1, max_value=5, required=False, widget=Stars,
        )

        class Meta:
            model = Product
            fields = "__all__"

    @admin.register(Product)
    class ProductAdmin(admin.ModelAdmin):
        form = ProductAdminForm

The model field must allow empty values if ``required=False`` is used.
The widget controls presentation; the form field validates the rating range.
The radio widget does not provide a button to clear a selection.

Development
-----------

Install the package and run the tests from the repository root:

.. code:: console

    python -m pip install -e .
    python -Wd -m django test --settings=tests.settings
    python example/manage.py check

CI tests Django 5.2 on Python 3.10–3.14 and Django 6.0 on Python 3.12–3.14.
