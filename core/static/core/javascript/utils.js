var utilsApp = angular.module('utils', [])
    .controller('dropdownController', ['$rootScope', function($rootScope) {
        var dropdownController = this;
        dropdownController.active = null;
        dropdownController.options = [];

        dropdownController.add = function(option) {
            dropdownController.options.push(option);
        };

        dropdownController.toggle = function(option) {
            dropdownController.active = option;
            $rootScope.$emit('dropdownChanged', dropdownController.name, option);
        };

        dropdownController.init = function(name) {
            dropdownController.name = name;
            if(dropdownController.active == null)
                dropdownController.toggle(dropdownController.options[0]);
        };
    }])
    .directive('jsSelectDropdown', [function() {
        return {
            restrict: 'C',
            controller: 'dropdownController',
            controllerAs: 'dropdown',
            template: `
                <div class='btn-group text-center'>
                    <button type='button' class='btn btn-primary dropdown-toggle' data-toggle='dropdown' aria-haspopup='true' aria-expanded='false' style='background-color: #FFFFFF; border: 0; color: #000000; font-weight: bold; font-size: 14px; font-family: Verdana;'>
                        {{ dropdown.active.name }}
                        <span class='caret'></span>
                    </button>
                    <ul class='dropdown-menu'>
                        <li ng-repeat='option in dropdown.options'>
                            <a href='javascript:;' ng-click='dropdown.toggle(option)'>
                                {{ option.name }}<span class='glyphicons glyphicons-ok font-green-jungle' style='padding: 0 5px;' ng-show='dropdown.active == option'></span>
                            </a>
                        </li>
                    </ul>
                    <div class='hidden' ng-transclude></div>
                </div>
            `,
            replace: true,
            scope: {},
            transclude: true,
            link: function(scope, elem, attrs, controller) {
                controller.init(attrs['toggleName']);
            }
        };
    }])
        /* Directive for injecting an API source into ngTable. */
    .directive('option', function() {
        return {
            require: '^jsSelectDropdown',
            restrict: 'E',
            link: function(scope, element, attributes, dropdown) {
                // Merge all attributes over.
                var option = {
                    'name': element.text()
                };
                angular.merge(option, attributes);
                dropdown.add(option);
                if(attributes['selected'])
                    dropdown.toggle(option);
                element.remove();
            }
        };
    });
