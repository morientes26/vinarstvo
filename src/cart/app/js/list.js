app.controller("list", function($scope, $http, $rootScope, $cookies, $routeParams, shoppingcart, $translate) {
    
    $scope.title = 'TITLE_CART';
    $scope.isOrder = false;
    $scope.items = shoppingcart.getCustomer().items;

    var url = $rootScope.API_URL + "product/list/";
    var backUrl = "cart";
    $scope.event = 2; // FIXME: default event for product list
    if ($routeParams.page=="event"){
    	url = $rootScope.API_URL +"product/event/list/";
    	$scope.title = 'TITLE_EVENT';
        backUrl = "event";
    }	
    
    $http.get(url).then(function (response) {
        $scope.products = response.data;
    });

    $scope.showDetail = function(id){
    	location.href = "#/detail/"+id+'?back='+backUrl;
    }
    $scope.addToCart = function(id, name){
    	shoppingcart.add(id,name);
    	$scope.items = shoppingcart.getCustomer().items;
        renderOrder();
    }
    $scope.removeFromCart = function(id){
    	shoppingcart.remove(id);
    	$scope.items = shoppingcart.getCustomer().items;
        renderOrder();
    }
    $scope.cleanOrder = function(){
    	shoppingcart.clear();
    	$scope.isOrder = false;
    	$scope.items = shoppingcart.getCustomer().items;
    }
    $scope.showOrder = function(){
    	if (renderOrder())
    	   $scope.isOrder = true;
    }
    function renderOrder(){
        $scope.shoppinglist = shoppingcart.getJsonItems();
        $scope.sum_price = 0;

        if (Object.keys($scope.shoppinglist).length==0)
            return false;

        for ($item in $scope.shoppinglist){
            $scope.sum_price += $scope.shoppinglist[$item].amount;
        }  
        return true;     
    }
    $scope.sendOrder = function(form) {    	

    	if (form.$valid){
    		var url = $rootScope.API_URL + "order/create/";

			var dataObj = {
				customer_name : shoppingcart.getCustomer().name,  //form.customer_name.$viewValue
				contact_detail: form.contact_detail.$viewValue,
				email: form.email.$viewValue,
				phone: form.phone.$viewValue,
				event : form.event.$viewValue,
				items : shoppingcart.getJsonItems()
			};	
			console.log(dataObj);
			var res = $http.post(url, dataObj);
			res.success(function(data, status, headers, config) {
				$scope.message = 'MESSAGE_ORDER_SEND_SUCCESS';
				$scope.cleanOrder();
			});
			res.error(function(data, status, headers, config) {
				console.log( "failure message: " + JSON.stringify({data: data}));
				$scope.message = 'MESSAGE_ORDER_SEND_ERROR';
			});		
		} else {
			console.log('not valid form');
		}
	};
});
