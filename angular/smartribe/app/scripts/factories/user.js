'use strict';

app.factory('User', function($http, API_URL){
  return {
    edit: function(id, user){
      return $http.put(API_URL + 'users/' + id + '/', user);
    },
    get: function(id){
      return $http.get(API_URL + 'users/' + id + '/');
    },
    getCurrent: function(){
      return $http.get(API_URL + 'users/');
    },
    push: function(user){
      return $http.post(API_URL + 'users/', user);
    },
  };
});
