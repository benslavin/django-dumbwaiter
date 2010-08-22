=================
Django Dumbwaiter
=================

Optimizing expensive queries and calculations in web applications is a complex
and tedious problem. Dumbwaiter is designed to enable simple caching of data
while relieving the dogpile effect.

Numerous functions can be run in the background on a periodic basis, and will
persist the results of their evaluation to the database.


How to use dumbwaiter
=====================
The easiest way to get started with dumbwaiter is to add `dumbwaiter` to the
INSTALLED_APPS list in your `settings.py` and to add a setting called
`DUMBWAITER_FUNCTION_LIST` that conforms to the following standard:

::

	DUMBWAITER_FUNCTION_LIST = [
	    {
	        'function': 'time.time',
	        'name': 'time',
	        'frequency': 5,
	    },
	    {
	        'function': 'my_app.utils.function_name',
	        'name': 'count',
	        'frequency': 15,
	    },
	]

Each member of the function list can contain the following attributes:

function:
	An actual function or a string containing the path by which a function
	can be accessed.

name:
	The name by which the function will be referenced. This name must be unique.

frequency:
	The number of seconds between invocations of `function`. Defaults to
	`DUMBWAITER_DEFAULT_FREQUENCY`.

args:
	The arguments to be passed to `function`. Defaults to an empty list.

kwargs:
	The keyword arguments to be passed to `function`. Defaults to an empty dict.

max_saved:
	The depth of the history of cached data. This data is not accessible through
	the standard API, and currently only applied when using the database storage
	backend. Defaults to `DUMBWAITER_DEFAULT_SAVED`.

After the function list has been established the `run_dumbwaiter` management
command will run the specified functions at the specified intervals.

::

	./manage.py run_dumbwaiter

Once the run_dumbwaiter management command is started, it will begin to record
the values for each function. It is possible to retrieve the most recent value
through the use of `get_value`:

::

	import dumbwaiter
	my_value = dumbwaiter.get_value("count")

Additional settings
===================

There are several additional settings that may be customized.

DUMBWAITER_SERIALIZER:
	The name of a module containing the serializer to be used to store the
	value returned by functions in the function list. The serializer must be
	named `serializer` in the module specified. It must additionally support
	the `serialize` and `deserialize` methods. The default serializer lives
	in `dumbwaiter.serializers.pickler`.

DUMBWAITER_THREADED:
	The Dumbwaiter can run in threaded and non-threaded modes. The primary
	advantage of threaded operation is that functions do not block one another.
	The default is True.

DUMBWAITER_DEFAULT_SAVED:
 	The default depth of the history of cached data. Defaults to 10.

DUMBWAITER_DEFAULT_FREQUENCY:
	The default number of seconds between invocation of functions.
	Defaults to five minutes.

PICKLE_PROTOCOL:
	If using the `dumbwaiter.serializers.pickler` serializer, this specifies
	the version of the pickle protocol that will be used.
