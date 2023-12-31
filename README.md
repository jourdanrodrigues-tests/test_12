# Apollo Back-End Engineering Challenge

This challenge is designed to evaluate several things:
 - How well you know Python
 - How effectively you can work with the Django framework
 - How well you understand different data serialization formats, which is important for working with the diverse APIs Apollo integrates with
 - How well you handle data validation and exception handling
 - Your ability to work with connected Django pages
 - Your ability to work with Django Rest Framework

It is intended to take 2-4 hours. After you submit your solution (either by emailing us a .tar or .zip file, or uploading to GitHub), we will schedule a call to talk through your solution and how it could be extended to accomplish further goals.

## Setting Up

With Docker installed, run `docker-compose up` to start the server. The server should be running at `http://127.0.0.1:8000` once it's ready.

As for the tests, run `docker-compose run --rm server python manage.py test` (the `--rm` will destroy the container once it's shut down).

## Challenge Guidelines

This Django project consists of two parts:
1. A very simple HTML page at `/connected/`.
2. A stubbed out API endpoint at `/api/converter/convert/`

Your tasks are to:
1. Add a file input to the HTML page and modify the view so that, when a file is submitted, convert it to JSON and return that to the user
2. Add the same functionality to the API endpoint, returning the converted JSON as an `application/json` response.

To test your solution, you can run `python manage.py test`. This will execute 3 tests, which attempt to submit a file and check the response.

A good solution will not only pass the tests, but also work on any user-submitted XML file.
Furthermore, a good solution should never return a 500 error and should show an error message to the user if they upload an invalid XML file.

### JSON Conversion

For the purposes of this exercise, you may ignore any XML attributes. We are only interested in converting the XML node tags and any text values into JSON.

Leaf nodes should be converted into a JSON object with the node tag as the key and the node's text value as the value. For example, `<Foo>Bar</Foo>` should be converted to `{"Foo": "Bar"}`.

Non-leaf nodes should be converted into a JSON object with the node name as the key and an array of the node's children as the value. For example:
```xml
<Foo>
    <Bar>Baz</Bar>
</Foo>
```
should be converted to
```json
{
    "Foo": [
        {"Bar": "Baz"}
    ]
}
```

The tests provide additional examples of more complex conversions.
