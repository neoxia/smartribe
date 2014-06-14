'use strict';

app.controller('TribesShowCtrl', function($location, $rootScope, $routeParams, $scope, Tribe){
  $scope.auth.promise.then(function(){
    if (!$rootScope.logged) {
      $location.path('/');
    }
    $scope.page.title = 'Tribe';
    Tribe.get($routeParams.id).success(function(data){
      $scope.tribe = data;
    }).error(function(data){
      $scope.tribe = null;
      $scope.alertLaunch('error', data.detail);
    });
  });
});
