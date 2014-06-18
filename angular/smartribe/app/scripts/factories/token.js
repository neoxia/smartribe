'use strict';

app.factory('Token', function($cookieStore){
  return {
    destroy: function(){
      $cookieStore.remove('smartribeToken');
    },
    get: function(){
      return $cookieStore.get('smartribeToken');
    },
    set: function(token){
      $cookieStore.put('smartribeToken', token);
    }
  };
});
