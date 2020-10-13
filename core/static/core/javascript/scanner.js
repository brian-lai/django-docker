/* AngularJS app definition */
var scannerApp = angular.module('scanner', [])
    /* Barcode servide which interacts with the API and processes data. */
    .service('scannerService', function() {
        var service = this;
        // Storage for scanner state
        service._is_active = false;

        /* Key intereceptor for preventing 'weird' behavior. */
        angular.element(window).on('keydown', function(ev) {
            // Only perform if the scanner is active
            if(service._is_active) {
                // Check for the special chars and prevent them from causing side-effects, ENTER or TAB
                if(ev.keyCode == 9 || ev.keyCode == 13) {
                    ev.preventDefault();
                }
            }
        });

        /* Initializes the barcode scanner environment. */
        service.init = function(callback) {
            $(document).scannerDetection({
                'endChar':[0, 3, 4, 13],
                'preventDefault': true,
                'stopPropagation': true
            }).bind('scannerDetectionComplete', function(e, data) { 
                service.clean(data.string, callback);
            });

            // Mark the scanner as active
            service._is_active = true;
        };

        /* Cancels the current scan session. */
        service.cancel = function() {
            if(service._is_active) {
                $(document).scannerDetection(false);
                service._is_active = false;
            }
        };

        /* Cleans the barcode and returns the new data. */
        service.clean = function(data, callback) {
            callback(data);
        };
    })
    /* Interacts with barcode scanning hardware to reduce errors and register the data with the webapp. */
    .controller('barcodeScannerController', ['$scope', 'scannerService', function($scope, scannerService) {
        var scanner = this;

        /* Binds the scanner to stop when the overlay is gone. */
        angular.element('#dynamic-modal')
            .on('hidden.bs.modal', function () {
                scanner.stop();
                scanner.element.focus();
            });

        /* Starts the scanner. */
        scanner.start = function() {
            scannerService.init(scanner.callback);
            $('#dynamic-modal').modal({
                remote: '/scan/modal/',
                show: true
            });
        };

        /* Stops the scanner. */
        scanner.stop = function() {
            scannerService.cancel()
            $('#dynamic-modal').modal('hide');
        };

        /* Performs the assignment of the barcode. */
        scanner.callback = function(barcode) {
            scanner.barcode = barcode;
            scanner.stop();
            $scope.$apply();
        };
    }])
    /* Custom directive for dynamically compiling HTML from processed directives. */
    .directive('barcodeField', ['$compile', function($compile) {
        return {
            restrict: 'A',
            controller: 'barcodeScannerController',
            controllerAs: 'scanner',
            template: '<input ng-click="scanner.start()" ng-model="scanner.barcode"/>',
            replace: true,
            link: function($scope, elem, attrs, controller) {
                controller.barcode = attrs.value;
                controller.element = elem;
            }
        };
    }]);