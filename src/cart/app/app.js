var app = angular.module("app", ['ngRoute', 'ngCookies','pascalprecht.translate'])
.run(function($rootScope, $cookies, shoppingcart, $translate) {

    $rootScope.API_URL = "http://127.0.0.1:8000/api/";
    shoppingcart.init('testovac_1');

    $rootScope.changeLanguage = function (key) {
    	$translate.use(key);
  	};
	
})

// configure our routes
app.config(function($routeProvider, $locationProvider) {
    
    $routeProvider

        // route for the product list in basic cart or event cart
        .when('/:page', {
            templateUrl : 'pages/list.html',
            controller  : 'list'
        })

        // route for the detail of product 
        // if id then url is 'detail/?id='
        // if detailId then url is 'detail/id'
        .when('/detail/:detailId', {
            templateUrl : 'pages/detail.html',
            controller  : 'detail'
        });

/*    $locationProvider.html5Mode({
                 enabled: true,
                 requireBase: false
          });*/

});

// get customer shopping cart
app.service('shoppingcart', function($cookies) {

	this.init = function (customerName) {
		// Setting a cookie
		if ($cookies.getObject('customer')==null){		
			var customer = {
								name: customerName,
								items: []
							}
			$cookies.putObject('customer', customer);
			console.log('init cookies');
		}
	}
    this.getCustomer = function () {
    	return $cookies.getObject('customer');
    }

    // pattern : //[ {"product": 28, "amount": 22},{"product": 26, "amount": 24} ]
    this.getJsonItems = function () {
    	var items = $cookies.getObject('customer').items;
    	var result = '['; 
    	for (i in items){
    		if (items[i]!=null && items[i][0]!=null && items[i][0]>0)
    			result += '{"product": '+i+', "amount": '+items[i][0]+', "name":"'+items[i][1]+'"},';
    	}
    	if (result.length>2)
    		result=result.substring(0, result.length-1);
    	result+=']';
    	return JSON.parse(result);
    }

    this.add = function(id, name){
    	var customer = this.getCustomer();
    	if (customer.items[id] == undefined)
    		customer.items[id] = [0,''];
    	customer.items[id][0] += 1;
    	customer.items[id][1] = name;
    	$cookies.putObject('customer', customer);
    }
    this.remove = function(id){
    	var customer = this.getCustomer();
    	if (customer.items[id] == undefined)
    		customer.items[id][0] = 1;
    	if (customer.items[id][0]>0)
    		customer.items[id][0] = customer.items[id][0] - 1;
    	$cookies.putObject('customer', customer);
    }
    this.clear = function(){
    	var customer = this.getCustomer();
    	for (i in customer.items)
    		customer.items[i]=[0,''];
    	$cookies.putObject('customer', customer);
    }
});

// default value of angular bind element. Example: {{ count | default:0 }}
app.filter('default', [function(){
  return function(value, def) {
    return value || def;
  };
}]);


app.config(function ($translateProvider) {
  
  $translateProvider.useSanitizeValueStrategy(null);
  $translateProvider.preferredLanguage('en');
  $translateProvider.translations('en', {
  	LOGO: 'Wine cart Karpatska perla',
    TITLE_CART: 'Wine cart',
    TITLE_EVENT: 'Wine cart of event',
    MESSAGE_ORDER_SEND_SUCCESS: 'Your order has been send succesfully',
    MESSAGE_ORDER_SEND_ERROR: 'Ups, order has NOT been send!',
    WINE_CART: 'Wine cart',
    EVENT_CART: 'Wine cart of event',
    TABLE_CODE: 'Code',
    TABLE_NAME: 'Name',
    TABLE_PRICE: 'Price',
    TABLE_AMOUNT: 'Amount',
    TABLE_DESCRIPTION: 'Description',
    CLEAN_BASKET: 'Clean shopping cart',
    ORDER_FORM: 'Order form',
    SUM_ALL: 'Sum all',
    SUM_PRICE: 'Price all',
    ORDER_FORM_FIRST_LAST_NAME_PLACEHOLDER: 'Name*',
    ORDER_FORM_CONTACT_PLACEHOLDER:'Contact detail*',
    ORDER_FORM_PHONE_PLACEHOLDER:'Phone*',
    ORDER_FORM_EMAIL_PLACEHOLDER:'Email',
    SEND_ORDER:'Send order',
    REQUIRED_ITEM: 'Required item',
    DETAIL_PRODUCT: 'Detail of product',
    BACK: 'Back',
  });
  $translateProvider.translations('sk', {
    LOGO: 'Vinná karta Karpatská perla',
    TITLE_CART: 'Vinná karta',
    TITLE_EVENT: 'Vinná karta ochutnávky',
    MESSAGE_ORDER_SEND_SUCCESS: 'Vaša objednávka bola úspešne odoslaná',
    MESSAGE_ORDER_SEND_ERROR: 'Ups, objednávku sa nepodarilo poslať!',
    WINE_CART: 'Vinná karta',
    EVENT_CART: 'Vinná karta ochutnávky',
    TABLE_CODE: 'Kód',
    TABLE_NAME: 'Názov',
    TABLE_PRICE: 'Cena',
    TABLE_AMOUNT: 'Množstvo',
    TABLE_DESCRIPTION: 'Popis',
    CLEAN_BASKET: 'Vymazať košík',
    ORDER_FORM: 'Poslať objednávku',
    SUM_ALL: 'Celkovo',
    SUM_PRICE: 'Výsledná cena',
    ORDER_FORM_FIRST_LAST_NAME_PLACEHOLDER: 'Meno a priezvisko*',
    ORDER_FORM_CONTACT_PLACEHOLDER:'Kontaktné informácie*',
    ORDER_FORM_PHONE_PLACEHOLDER:'Telefón*',
    ORDER_FORM_EMAIL_PLACEHOLDER:'Email',
    SEND_ORDER:'Poslať objednávku',
    REQUIRED_ITEM: 'Povinná položka',
    DETAIL_PRODUCT: 'Detail produktu',
    BACK: 'Naspäť',
  });
});