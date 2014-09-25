//'use strict';

foo = null;
angular.module('TrustNoOneApp')
  .factory('TNOState',
  function () {
    var state = {};
    function set(data) {
      state = data;
    }

    function get() {
      return state;
    }
    foo = get;

    return {
      state: state,
      set  : set,
      get  : get
    }

  });
