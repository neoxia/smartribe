'use strict';

app.controller('IndexCtrl', function($http, $location, $rootScope, $scope/*, Geolocation*/, Token){
  $scope.auth.promise.then(function(){
    $scope.page = {};
    $scope.alert = {};
    $scope.loaded = true;
    $scope.alertLaunch = function(type, message){
      $scope.alert.type = type;
      $scope.alert.message = message;
      $scope.alert.display = true;
    };
    $scope.alertDismiss = function(){
      $scope.alert.display = false;
      $scope.alert.message = null;
      $scope.alert.type = null;
    };
    $scope.search = function(){
      // TODO :: execute search
    };
    $scope.logout = function(){
      $rootScope.logged = false;
      $http.defaults.headers.common.Authorization = null;
      Token.destroy();
      $rootScope.user = undefined;
      $scope.alertLaunch('success', 'Successfully logged out');
      $location.path('/');
    };
    // Location test
    /*Geolocation.get().then(function(geoposition){
      $scope.alertLaunch('success', 'Latitude: ' + geoposition.coords.latitude + ', longitude: ' + geoposition.coords.longitude + '.');
    }, function(error){
      $scope.alertLaunch('error', error);
    });*/
  });
});
