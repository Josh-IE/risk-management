from io import StringIO

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.text import slugify

from django_s3_storage.storage import S3Storage


def tuple_to_dict(data):
    """Transforms a tuple into a list of dicts with 'text' & 'value' keys.

    Arguments:
        data {tulpe} -- Tuple to be transformed.
    Returns:
        {list} -- List of dicts [{'text': None, 'value': None}].
    """
    choice_ls = []
    for i, item in enumerate(data):
        value, choice = item
        choice_ls.append({"text": choice, "value": value})
    return choice_ls


def nested_field_parse(result):
    """Parses nested QueryDict in the form field[name]: value to python dict
    {field: {name: value}}.

    Arguments:
        result {QueryDict} -- QueryDict to be parsed.
    Returns:
        {dict} -- Nested dict.
    """

    data = {}
    # iterate the Query dict using .lists() to preserve all Multi values
    for key, value in result.lists():
        if "[" in key and "]" in key:
            # this is a nested key
            index_left_bracket = key.index("[")
            index_right_bracket = key.index("]")
            nested_dict_key = key[:index_left_bracket]
            nested_value_key = key[
                index_left_bracket + 1 : index_right_bracket
            ]
            if nested_dict_key not in data:
                data[nested_dict_key] = {}
            # check if nested key truly holds an array
            if key[-2:] == "[]":
                data[nested_dict_key][nested_value_key] = value
            else:
                # pull the first value in the array.
                data[nested_dict_key][nested_value_key] = value[0]
        else:
            data[key] = value[0]
    return data


def generate_unique_slug(klass, field):
    """Generates a unique slug from a string value.

    Arguments:
        klass {Model} -- Model class.
        field {string} -- Value to be slugified.
    Returns:
        {str} -- Unique slug.
    """
    slug_field = klass._meta.get_field("slug")
    max_slug_len = slug_field.max_length
    origin_slug = slugify(field)
    unique_slug = origin_slug
    count = 1
    while klass.objects.filter(slug=unique_slug).exists():
        suffix = "%s%s" % ("-", count)
        if len(origin_slug) + len(suffix) > max_slug_len:
            origin_slug = origin_slug[: max_slug_len - len(suffix)]
        unique_slug = "%s%s" % (origin_slug, suffix)
        count += 1
    return unique_slug


def store_file(file):
    """Stores File Object in file system.

    Arguments:
        file {FileObject} -- The file to be saved.
    Returns:
        {str} -- File path on file system.
    """
    if (
        settings.DEFAULT_FILE_STORAGE
        != "django.core.files.storage.FileSystemStorage"
    ):
        fs = S3Storage()
        return fs.save(file.name, file)
    else:
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        return fs.url(filename)


def generate_inmemory_text_file(file_name="foo.txt"):
    """Generates inmemory text file used for testing.

    Keyword Arguments:
        file_name {str} -- [Desired file name.] (default: {"foo.txt"})
    Returns:
        {InMemoryUploadedFile} -- In memory file object..
    """
    io = StringIO()
    length = io.write("foo")
    text_file = InMemoryUploadedFile(io, None, file_name, "text", length, None)
    text_file.seek(0)
    return text_file
