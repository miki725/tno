'use strict';

var
  LOWERCASE_REGEX = /[a-z]/,
  UPPERCASE_REGEX = /[A-Z]/,
  DIGIT_REGEX = /[0-9]/;

angular.module('TrustNoOneApp')
  .directive('tnoPasswordLength', function () {
    return {
      require: 'ngModel',
      link   : function (scope, elm, attrs, ctrl) {
        ctrl.$parsers.unshift(function (viewValue) {
          if (viewValue.length < 10) {
            ctrl.$setValidity('length', false);
            return undefined;
          } else {
            ctrl.$setValidity('length', true);
            return viewValue;
          }
        });
      }
    };
  })
  .directive('tnoPasswordLowercase', function () {
    return {
      require: 'ngModel',
      link   : function (scope, elm, attrs, ctrl) {
        ctrl.$parsers.unshift(function (viewValue) {
          if (LOWERCASE_REGEX.test(viewValue)) {
            ctrl.$setValidity('lowercase', true);
            return viewValue;
          } else {
            ctrl.$setValidity('lowercase', false);
            return undefined;
          }
        });
      }
    };
  })
  .directive('tnoPasswordUppercase', function () {
    return {
      require: 'ngModel',
      link   : function (scope, elm, attrs, ctrl) {
        ctrl.$parsers.unshift(function (viewValue) {
          if (UPPERCASE_REGEX.test(viewValue)) {
            ctrl.$setValidity('uppercase', true);
            return viewValue;
          } else {
            ctrl.$setValidity('uppercase', false);
            return undefined;
          }
        });
      }
    };
  })
  .directive('tnoPasswordDigit', function () {
    return {
      require: 'ngModel',
      link   : function (scope, elm, attrs, ctrl) {
        ctrl.$parsers.push(function (viewValue) {
          if (DIGIT_REGEX.test(viewValue)) {
            ctrl.$setValidity('digit', true);
            return viewValue;
          } else {
            ctrl.$setValidity('digit', false);
            return undefined;
          }
        });
      }
    };
  });
