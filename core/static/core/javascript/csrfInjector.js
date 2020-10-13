angular.module('csrfInjector', ['ngCookies'])
    /* Handles subdomain cookie inclusion, since Angular won't. */
    .factory('csrfSubdomainInterceptor', ['$cookies', function($cookies) {
        // Factory object ot return
        var csrfInterceptor = {
            request: function(config) {
                if(isSameSubdomain(config.url)) {
                    config.headers['X-CSRFToken'] = $cookies.get('csrftoken');

                    // Additionally check if the method is POST/PATCH/DELETE to auto-include in the body
                    if(['POST', 'PATCH', 'DELETE'].indexOf(config.method) >= 0) {
                        if('data' in config && typeof(config.data) == 'object') {
                            config.data['csrfmiddlewaretoken'] = config.headers['X-CSRFToken'];
                        }
                    }
                    // Add API token from cookie
                    var jwt = $cookies.get(jwt_token_name);
                    if(jwt != undefined) {
                        config.headers['Authorization'] = 'JWT ' + jwt;
                    }
                }
                return config;
            }
        };
        function isSameSubdomain(url) {
            var subdomain = /^[^.]+\./;
            var urlParsingNode = document.createElement('a');
            urlParsingNode.setAttribute('href', url);

            return urlParsingNode.hostname.replace(subdomain, '') === window.location.hostname.replace(subdomain, '');
        }
        return csrfInterceptor;
    }])
    /* Sets global actions/attributes to the $http service. */
    .config(['$httpProvider', function($httpProvider) {
        // CSRF cookie is attached for Django form/request processing
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
        $httpProvider.defaults.withCredentials = true;

        // Attach interceptors which will act on each request/response cycle from $http service
        $httpProvider.interceptors.push('csrfSubdomainInterceptor');
    }]);
