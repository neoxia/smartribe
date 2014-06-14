'use strict';

app.controller('HomeCtrl', function($http, $rootScope, $scope, API_URL, Token, User){
  $scope.auth.promise.then(function(){
    $rootScope.$watch('logged', function(logged){
      if (logged) {
        $scope.page.title = 'Home';
      } else {
        $scope.page.title = 'Login';
        $scope.page.activeNav = 'login';
      }
    });
    $scope.login = function(){
      var credentials = {
        username: $scope.username,
        password: $scope.password
      };
      $http.post(API_URL + 'api-token-auth/', credentials).success(function(data){
        Token.set(data.token);
        $http.defaults.headers.common.Authorization = 'JWT ' + data.token;
        User.getCurrent().success(function(data){
          $rootScope.user = data;
          $rootScope.logged = true;
          $scope.alertLaunch('success', 'Successfully logged in');
        }).error(function(data){
          $rootScope.logged = false;
          $http.defaults.headers.common.Authorization = null;
          Token.destroy();
          $scope.alertLaunch('error', data.detail);
        });
      }).error(function(data){
        $scope.alertLaunch('error', data.detail);
      });
    };
  });
});
