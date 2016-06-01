app.controller("list", function($scope, $http, $rootScope, $cookies, $routeParams, shoppingcart) {
    
    $scope.title = "Vinna karta";
    $scope.isOrder = false;
    $scope.items = shoppingcart.getCustomer().items;

    var url = $rootScope.API_URL + "product/list/";
    if ($routeParams.page=="event"){
    	url = $rootScope.API_URL +"product/event/list/";
    	$scope.title = "Vinna karta ochutnavky";
    }
    
    $http.get(url).then(function (response) {
        $scope.products = response.data;
    });

    $scope.showDetail = function(id){
    	location.href = "#/detail/"+id;
    }
    $scope.addToCart = function(id){
    	shoppingcart.add(id);
    	$scope.items = shoppingcart.getCustomer().items;
    }
    $scope.removeFromCart = function(id){
    	shoppingcart.remove(id);
    	$scope.items = shoppingcart.getCustomer().items;
    }
    $scope.cleanOrder = function(){
    	shoppingcart.clear();
    	$scope.isOrder = false;
    	$scope.items = shoppingcart.getCustomer().items;
    }
    $scope.showOrder = function(){
    	$scope.isOrder = true;
    }
    $scope.sendOrder = function(isValid) {
    	
    	if (isValid){
			window.alert('send order to server by form');
		}
	};
});