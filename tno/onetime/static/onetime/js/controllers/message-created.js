'use strict';

angular.module('TrustNoOneApp')
  .controller('MessageCreatedController', [
    '$scope',
    '$location',
    'TNOState',
    '$log',
    '$timeout',
    function ($scope,
              $location,
              TNOState,
              $log,
              $timeout) {
      angular.extend($scope, TNOState.get());

      $scope.get_message_link = function () {
        if (angular.isDefined($scope.created)
            && angular.isDefined($scope.created.uuid)) {
          return INDEX_URL + 'read/' + $scope.created.uuid + '/';
        } else {
          return '';
        }
      };

      if (!angular.isDefined($scope.created)) {
        $location.path('/new/');
      }
    }
  ]);
