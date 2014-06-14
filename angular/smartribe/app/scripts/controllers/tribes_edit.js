'use strict';

app.controller('TribesEditCtrl', function($location, $rootScope, $routeParams, $scope, Tribe){
  $scope.auth.promise.then(function(){
    if (!$rootScope.logged) {
      $location.path('/');
    }
    $scope.page.title = 'Edit tribe';
    Tribe.get($routeParams.id).success(function(data){
      $scope.tribe = data;
    }).error(function(data){
      $scope.tribe = null;
      $scope.alertLaunch('error', data.detail);
    });
    $scope.tribeEdit = function(){
      Tribe.put($routeParams.id, $scope.tribe).success(function(data){
        $scope.alertLaunch('success', 'Successfully edited tribe');
        $location.path('/tribes/' + data.tribeId);
      }).error(function(data){
        $scope.alertLaunch('error', data.detail);
      });
    };
  });
});
