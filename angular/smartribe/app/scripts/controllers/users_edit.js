'use strict';

app.controller('UsersEditCtrl', function($location, $rootScope, $routeParams, $scope, User){
  $scope.auth.promise.then(function(){
    if (!$rootScope.logged) {
      $location.path('/');
    }
    $scope.page.title = 'Settings';
    var userId = $.grep($scope.user.url.split('/'), function(value){
      return value !== '';
    }).pop();
    $scope.usersEdit = function(){
      User.edit(userId, $scope.user).success(function(data){
        $rootScope.user = data;
        $scope.alertLaunch('success', 'Successfully edited user');
      }).error(function(data){
        $scope.alertLaunch('error', data.detail);
      });
    };
  });
});
