'use strict';

angular.module('TrustNoOneApp')
  .controller('MessageController', [
    '$scope',
    'OTSecretService',
    'TNOCrypto',
    '$stateParams',
    '$q',
    '$log',
    '$timeout',
    function ($scope,
              OTSecretService,
              TNOCrypto,
              $stateParams,
              $q,
              $log,
              $timeout) {

      $scope.looking = true;
      $scope.decrypting = false;
      $scope.message = {
        'exists'  : null,
        'uuid'    : $stateParams.uuid,
        '$error'  : {},
        'password': undefined,
        'message' : undefined,
        'onetime' : undefined
      };

      // useful for debugging
      var delay = 0;

      $timeout(function () {
        OTSecretService
          .get({'uuid': $scope.message.uuid}).$promise
          .then(function (data) {
            $scope.message.onetime = data;
            $scope.message.exists = true;
          }, function () {
            $scope.message.exists = false;
          }).finally(function () {
            $scope.looking = false;
          });
      }, delay);

      $scope.are_we_there_yet = function () {
        return angular.isDefined($scope.message.password)
               && $scope.message.password !== ''
               && !$scope.decrypting;
      };

      var _decrypt_message = function () {
        return TNOCrypto.decrypt(
          TNOCrypto.decode({
            'salt'      : $scope.message.onetime.salt,
            'iv'        : $scope.message.onetime.iv,
            'adata'     : $scope.message.onetime.associated_data,
            'ciphertext': $scope.message.onetime.ciphertext,
            'tag'       : $scope.message.onetime.tag
          }),
          $scope.message.password
        );
      };

      $scope.view_message = function () {
        if (!$scope.are_we_there_yet()
            || $scope.message.message) {
          return;
        }

        var deferred = $q.defer();
        $scope.decrypting = true;

        $timeout(function () {
          var decrypted = _decrypt_message();
          $timeout(function () {
            if (decrypted === null) {
              deferred.reject();
            } else {
              deferred.resolve(decrypted);
            }
          }, delay)
        });

        return deferred.promise
          .then(function (plaintext) {
            $scope.message.message = plaintext;
            $scope.message.$error.password = undefined;
          }, function () {
            $scope.form.password.$error.invalid = true;
            $scope.message.password = undefined;
          })
          .finally(function () {
            $scope.decrypting = false;
          });
      };
    }
  ]);
