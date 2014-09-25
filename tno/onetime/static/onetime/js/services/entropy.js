'use strict';

angular.module('TrustNoOneApp')
  .factory('EntropyService', [
    '$resource',
    function ($resource) {
      return $resource('/api/v1/entropy/:bytes/');
    }
  ]);
