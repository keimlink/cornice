import re


URL_PLACEHOLDER = re.compile(r'\{(.*)\}')


def generate_spore(services, name, base_url, version, **kwargs):
    """Utitlity to turn cornice web services into a SPORE-readable file.
    (Specifications to a Portable REST Environment)"""
    spore_doc = dict(
        name=name,
        base_url=base_url,
        version=version,
        expected_status=[200, ],
        methods={},
        **kwargs)

    for service in services:

        # the :foobar syntax should be removed.
        # see https://github.com/SPORE/specifications/issues/5
        service_path = re.sub(URL_PLACEHOLDER, ':\g<1>', service.path)

        service_params = None
        # get the list of placeholders
        results = URL_PLACEHOLDER.search(service.path)
        if results:
            service_params = results.groups()

        for method, view, args in service.definitions:
            view_info = {
                'path': service_path,
                'method': method,
                'format': args['renderer']
            }
            if service_params is not None:
                view_info['service_params'] = service_params

            if getattr(view, '__doc__'):
                view_info['description'] = view.__doc__

            # we have the values, but we need to merge this with
            # possible previous values for this method.
            if view.__name__ in spore_doc['methods']:
                # handle multiple decorators.
                pass
            else:
                spore_doc['methods'][view.__name__] = view_info

    return spore_doc
