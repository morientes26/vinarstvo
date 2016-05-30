var app = angular.module("app", ['ngRoute'])
.run(function($rootScope) {

    $rootScope.API_URL = "http://127.0.0.1:8000/api/";
})

// configure our routes
app.config(function($routeProvider) {
    
    $routeProvider

        // route for the product list in basic cart
        .when('/', {
            templateUrl : 'pages/list.html',
            controller  : 'list'
        })

        // route for the product list in event cart
        .when('/event', {
            templateUrl : 'pages/event.html',
            controller  : 'event'
        })

        // route for the detail of product 
        // if id then url is 'detail/?id='
        // if detailId then url is 'detail/id'
        .when('/detail/:detailId', {
            templateUrl : 'pages/detail.html',
            controller  : 'detail'
        })

        // route for the order
        .when('/order', {
            templateUrl : 'pages/order.html',
            controller  : 'order'
        });
});