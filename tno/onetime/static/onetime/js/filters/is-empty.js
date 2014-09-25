'use strict';

Object.prototype.isEmpty = function () {
  var i;
  for (i in this) {
    if (this.hasOwnProperty(i)) {
      return false;
    }
  }
  return true;
};

angular.module('TrustNoOneApp')
  .filter('isEmpty', [
    '$rootScope',
    function ($rootScope) {
      $rootScope.isEmpty = function (obj) {
        return obj.isEmpty();
      };
      return $rootScope.isEmpty;
    }
  ]);
