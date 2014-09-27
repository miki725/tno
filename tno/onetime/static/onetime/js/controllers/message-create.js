'use strict';

angular.module('TrustNoOneApp')
  .controller('MessageCreateController', [
    '$scope',
    'OTSecretService',
    'TNOCrypto',
    'TNOState',
    '$log',
    '$state',
    '$timeout',
    function ($scope,
              OTSecretService,
              TNOCrypto,
              TNOState,
              $log,
              $state,
              $timeout) {

      $scope.encrypting = false;
      $scope.message = {
        'password': undefined,
        'message' : undefined
      };
      $scope.uuid = null;

      // useful for debugging
      var delay = 0;

      $scope.are_we_there_yet = function () {
        return angular.isDefined($scope.message.message)
               && $scope.message.message !== ''
               && angular.isDefined($scope.message.password)
               && $scope.message.password !== ''
               && !$scope.encrypting;
      };

      $scope.create_message = function () {
        if (!$scope.are_we_there_yet()) {
          return;
        }

        $scope.encrypting = true;
        TNOCrypto.get_entropy()
          .then(function (entropy) {
            var crypto = TNOCrypto.encode(TNOCrypto.encrypt(
              entropy,
              $scope.message.password,
              $scope.message.message
            ));
            return OTSecretService.save(crypto);
          })
          .then(function (data) {
            TNOState.state.created = data;
          })
          .finally(function () {
            $timeout(function () {
              $scope.message.message = undefined;
              $scope.message.password = undefined;
              $scope.encrypting = false;
              $state.go('created');
            }, delay);
          });
      };
    }
  ]);
