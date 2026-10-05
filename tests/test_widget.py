from html.parser import HTMLParser

from django import forms
from django.contrib import admin
from django.contrib.staticfiles import finders
from django.db import models
from django.test import RequestFactory, SimpleTestCase, override_settings

from django_starfield import Stars


class Inputs(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.inputs = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        if tag == 'input':
            self.inputs.append(dict(attrs))


class RatingForm(forms.Form):
    rating = forms.IntegerField(min_value=1, max_value=5, required=False, widget=Stars)


class Product(models.Model):
    rating = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        app_label = 'tests'


class ProductForm(forms.ModelForm):
    rating = forms.IntegerField(min_value=1, max_value=5, required=False, widget=Stars)

    class Meta:
        model = Product
        fields = ['rating']


class WidgetTests(SimpleTestCase):
    def test_render_selected_and_empty_values(self):
        for value in (None, 3, '3'):
            with self.subTest(value=value):
                inputs = Inputs(Stars().render('rating', value)).inputs
                self.assertEqual([i['value'] for i in inputs], ['5', '4', '3', '2', '1'])
                selected = [i['value'] for i in inputs if 'checked' in i]
                self.assertEqual(selected, [] if value is None else ['3'])

    def test_custom_star_count_and_settings(self):
        with override_settings(STARFIELD_STARS=7):
            self.assertEqual(len(Inputs(Stars().render('rating', None)).inputs), 7)
            self.assertEqual(len(Inputs(Stars(stars=3).render('rating', None)).inputs), 3)

    def test_form_submission_and_validation(self):
        for value, expected in [('4', 4), ('', None)]:
            form = RatingForm({'rating': value})
            self.assertTrue(form.is_valid(), form.errors)
            self.assertEqual(form.cleaned_data['rating'], expected)
        for value in ('0', '6', 'invalid'):
            self.assertFalse(RatingForm({'rating': value}).is_valid())

    def test_bound_form_preserves_selection(self):
        html = RatingForm({'rating': '4'})['rating'].as_widget()
        selected = [i['value'] for i in Inputs(html).inputs if 'checked' in i]
        self.assertEqual(selected, ['4'])

    def test_admin_model_form(self):
        model_admin = admin.ModelAdmin(Product, admin.AdminSite())
        model_admin.form = ProductForm
        form_class = model_admin.get_form(RequestFactory().get('/'))
        form = form_class(instance=Product(rating=2))
        selected = [i['value'] for i in Inputs(str(form['rating'])).inputs if 'checked' in i]
        self.assertEqual(selected, ['2'])
        bound = form_class({'rating': '5'})
        self.assertTrue(bound.is_valid(), bound.errors)
        self.assertEqual(bound.save(commit=False).rating, 5)

    def test_default_stylesheet_is_available(self):
        self.assertIsNotNone(finders.find('django_starfield.css'))

    def test_example_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'type="radio"', count=32)

    def test_custom_stylesheet_and_content(self):
        html = Stars(css_file='ratings/custom.css', content="'★'", colour='#ff1493').render('rating', 2)
        self.assertIn('/static/ratings/custom.css', html)
        self.assertIn('--starfield-content: &#x27;★&#x27;;', html)
        self.assertIn('color: #ff1493;', html)

    def test_same_form_twice_has_distinct_ids(self):
        first, second = (Inputs(str(RatingForm()['rating'])).inputs for _ in range(2))
        first_ids = {i['id'] for i in first}
        second_ids = {i['id'] for i in second}
        self.assertEqual(len(first_ids), 5)
        self.assertFalse(first_ids & second_ids)

    def test_explicit_unique_id(self):
        html = Stars(unique_id='fixed', colour='#ff1493').render('rating', None)
        self.assertIn('id="django-starfield-fixed"', html)
        self.assertIn('id="rating-fixed-0"', html)
        self.assertIn('for="rating-fixed-0"', html)
        self.assertIn('#django-starfield-fixed label', html)

    def test_not_clearable_by_default(self):
        inputs = Inputs(Stars().render('rating', 3)).inputs
        self.assertNotIn('', [i['value'] for i in inputs])

    def test_clearable_renders_empty_choice(self):
        for value, checked in [(None, True), (3, False)]:
            with self.subTest(value=value):
                inputs = Inputs(Stars(clearable=True, unique_id='fixed').render('rating', value)).inputs
                clear = inputs[-1]
                self.assertEqual(len(inputs), 6)
                self.assertEqual((clear['id'], clear['value']), ('rating-fixed-clear', ''))
                self.assertEqual('checked' in clear, checked)

    def test_clearable_from_settings(self):
        with override_settings(STARFIELD_CLEARABLE=True):
            self.assertEqual(len(Inputs(Stars().render('rating', None)).inputs), 6)
            self.assertEqual(len(Inputs(Stars(clearable=False).render('rating', None)).inputs), 5)

    def test_clearable_submission_clears_value(self):
        model_admin = admin.ModelAdmin(Product, admin.AdminSite())
        form_class = model_admin.get_form(RequestFactory().get('/'), widgets={'rating': Stars(clearable=True)})
        form = form_class({'rating': ''}, instance=Product(rating=2))
        self.assertTrue(form.is_valid(), form.errors)
        self.assertIsNone(form.save(commit=False).rating)
