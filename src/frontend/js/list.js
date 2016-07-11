    app.controller("list", function($scope, $http, $rootScope, $cookies, $routeParams, shoppingcart, $translate) {
    
    $scope.title = $routeParams.type;
    $scope.isOrder = false;
    $scope.items = shoppingcart.getCustomer().items;
    $scope.image_background=getImageBackground($routeParams.type);

    getProducts($rootScope.API_URL, $routeParams.type);  

    $scope.backToList = function(){
        location.href = "#/";
    }

    $scope.showDetail = function(id){
    	location.href = "#/detail/"+id+'?back='+$routeParams.page+"/"+$routeParams.type;
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
        console.log('send form');

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

    function getProducts(base_url, group){

        var url = base_url + 'products/'
        $http.get(url,{
            params: { group: group }
        }).then(function (response) {
            $scope.products = response.data;
        });
    }

    function getImageBackground(type){

        switch(type){
            case 'white':
                return 'biele';
                break;
            case 'red':
                return 'cervene';
                break;
            case 'rose':
                return 'rose';
                break;
            case 'sweet':
                return 'sladke';
                break;
            case 'white_archive':
                return 'biele-arch';
                break;
            case 'red_archive':
                return 'cervene-arch';
                break; 
            case 'nealko':
                return 'nealko';
                break; 
            case 'sweets':
                return 'pochutiny';
                break;                      
            default:
                return 'biele';
        }

    }

});
