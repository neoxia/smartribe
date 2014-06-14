/* global app:true */
'use strict';

var app = angular.module('smartribeApp', [
  'ngCookies',
  'ngResource',
  'ngRoute',
  'ngSanitize'
]);

app.config(function($routeProvider){
  $routeProvider.when('/', {
    controller: 'HomeCtrl',
    templateUrl: 'views/home.html'
  }).when('/signup', {
    controller: 'UsersNewCtrl',
    templateUrl: 'views/users_new.html'
  }).when('/tribes', {
    controller: 'TribesCtrl',
    templateUrl: 'views/tribes.html'
  }).when('/tribes/new', {
    controller: 'TribesNewCtrl',
    templateUrl: 'views/tribes_new.html'
  }).when('/tribes/:id', {
    controller: 'TribesShowCtrl',
    templateUrl: 'views/tribes_show.html'
  }).when('/tribes/:id/edit', {
    controller: 'TribesEditCtrl',
    templateUrl: 'views/tribes_edit.html'
  }).otherwise({
    redirectTo: '/'
  });
});

app.constant('API_URL', 'http://localhost:8000/api/v1/');

app.run(function($http, $q, $rootScope, Token, User){
  $rootScope.auth = $q.defer();
  if (Token.get()) {
    $http.defaults.headers.common.Authorization = 'JWT ' + Token.get();
    User.getCurrent().success(function(data){
      $rootScope.user = data;
      $rootScope.logged = true;
      $rootScope.auth.resolve();
    }).error(function(){
      $rootScope.logged = false;
      $http.defaults.headers.common.Authorization = null;
      Token.destroy();
      $rootScope.auth.resolve();
    });
  } else {
    $rootScope.logged = false;
    $rootScope.auth.resolve();
  }
});
