from datetime import date, timedelta
import datetime
from django.test import TestCase

from catalog.models import Author

class AuthorModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Author.objects.create(first_name='Big', last_name='Bob')

    def test_first_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_last_name_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')

    def test_date_of_birth_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_birth').verbose_name
        self.assertEqual(field_label, 'date of birth')

    def test_date_of_death_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('date_of_death').verbose_name
        self.assertEqual(field_label, 'Died')

    def test_first_name_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_last_name_comma_first_name(self):
        author = Author.objects.get(id=1)
        expected_object_name = f'{author.last_name}, {author.first_name}'
        self.assertEqual(str(author), expected_object_name)

    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(author.get_absolute_url(), '/catalog/author/1')


from django.test import TestCase
from django.utils import timezone
from catalog.models import Book, BookInstance
from django.contrib.auth.models import User
import uuid

class BookInstanceModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        book = Book.objects.create(
            title='Test Book',
            author=Author.objects.create(first_name='Test', last_name='Author'),
            summary='Test summary',
            isbn='1234567890',
        )
        cls.Id = uuid.uuid4()
        BookInstance.objects.create(
            id = cls.Id,
            book=book,
            imprint='Test Imprint',
            due_back = date.today() + timedelta(5),
            status='a'
        )
        
    def test_id_label(self):
        book_instance = BookInstance.objects.get(id=self.Id)
        field_label = book_instance._meta.get_field('id').verbose_name
        self.assertEqual(field_label, 'id')

    def test_book_label(self):
        book_instance = BookInstance.objects.get(id=self.Id)
        field_label = book_instance._meta.get_field('book').verbose_name
        self.assertEqual(field_label, 'book')

    def test_due_back_label(self):
        book_instance = BookInstance.objects.get(id=self.Id)
        field_label = book_instance._meta.get_field('due_back').verbose_name
        self.assertEqual(field_label, 'due back')

    def test_status_label(self):
        book_instance = BookInstance.objects.get(id=self.Id)
        field_label = book_instance._meta.get_field('status').verbose_name
        self.assertEqual(field_label, 'status')

    def test_borrower_label(self):
        book_instance = BookInstance.objects.get(id=self.Id)
        field_label = book_instance._meta.get_field('borrower').verbose_name
        self.assertEqual(field_label, 'borrower')

    def test_is_overdue_with_future_due_back(self):
        book_instance = BookInstance.objects.get(id=self.Id)
        self.assertFalse(book_instance.is_overdue)

    def test_is_overdue_with_past_due_back(self):
        past_due_back = date.today() - timedelta(days=5)
        book_instance = BookInstance.objects.create(
            book=Book.objects.first(),
            imprint='Test Imprint',
            due_back=past_due_back,
            status='a'
        )
        self.assertTrue(book_instance.is_overdue)

    def test_string_representation(self):
        book_instance = BookInstance.objects.get(id=self.Id)
        expected_object_name = f'{book_instance.id} ({book_instance.book.title})'
        self.assertEqual(str(book_instance), expected_object_name)

from catalog.models import Language

class LanguageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Language.objects.create(name='English')
        

    def test_name_label(self):
        language = Language.objects.get(id=1)
        field_label = language._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        language = Language.objects.get(id=1)
        max_length = language._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)

    def test_string_representation(self):
        language = Language.objects.get(id=1)
        self.assertEqual(str(language), 'English')

    


from catalog.models import Genre

class GenreModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Genre.objects.create(name='Science Fiction')

    def test_name_label(self):
        genre = Genre.objects.get(id=1)
        field_label = genre._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')

    def test_name_max_length(self):
        genre = Genre.objects.get(id=1)
        max_length = genre._meta.get_field('name').max_length
        self.assertEqual(max_length, 200)

    def test_string_representation(self):
        genre = Genre.objects.get(id=1)
        self.assertEqual(str(genre), 'Science Fiction')


from django.test import TestCase
from catalog.models import Book, Author, Genre

class BookModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        author = Author.objects.create(first_name='John', last_name='Doe')
        genre = Genre.objects.create(name='Science Fiction')
        cls.book = Book.objects.create(
            title='Test Book',
            author=author,
            summary='Test summary',
            isbn='1234567890123'
        )
        cls.book.genre.set([genre])  # Adding the genre to the ManyToManyField

    def test_title_label(self):
        book = Book.objects.get(id=self.book.id)
        field_label = book._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'title')

    def test_summary_label(self):
        book = Book.objects.get(id=self.book.id)
        field_label = book._meta.get_field('summary').verbose_name
        self.assertEqual(field_label, 'summary')

    def test_isbn_label(self):
        book = Book.objects.get(id=self.book.id)
        field_label = book._meta.get_field('isbn').verbose_name
        self.assertEqual(field_label, 'ISBN')

    def test_title_max_length(self):
        book = Book.objects.get(id=self.book.id)
        max_length = book._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)

    def test_summary_max_length(self):
        book = Book.objects.get(id=self.book.id)
        max_length = book._meta.get_field('summary').max_length
        self.assertEqual(max_length, 1000)

    def test_isbn_max_length(self):
        book = Book.objects.get(id=self.book.id)
        max_length = book._meta.get_field('isbn').max_length
        self.assertEqual(max_length, 13)

    def test_object_name_is_title(self):
        book = Book.objects.get(id=self.book.id)
        expected_object_name = book.title
        self.assertEqual(str(book), expected_object_name)

    def test_get_absolute_url(self):
        book = Book.objects.get(id=self.book.id)
        self.assertEqual(book.get_absolute_url(), f'/catalog/book/{self.book.id}')

