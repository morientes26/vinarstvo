var app = angular.module("app", ['ngRoute'])
.run(function($rootScope) {

    $rootScope.API_URL = "http://127.0.0.1:8000/api/";
})

// configure our routes
app.config(function($routeProvider) {
    
    $routeProvider

        // route for the product list
        .when('/', {
            templateUrl : 'pages/list.html',
            controller  : 'list'
        })

        // route for the detail of product
        .when('/detail', {
            templateUrl : 'pages/detail.html',
            controller  : 'detail'
        })

        // route for the order
        .when('/order', {
            templateUrl : 'pages/order.html',
            controller  : 'order'
        });
});