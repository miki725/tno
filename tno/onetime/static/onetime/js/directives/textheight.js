'use strict';

angular.module('TrustNoOneApp')
  .directive('tnoTextHeight', function () {
    return {
      link: function (scope, elm, attrs, ctrl) {
        var adjust_height = function (newValue, oldValue) {
          if (newValue !== oldValue
              && Math.abs(newValue - oldValue) > 2) {
            elm[0].style.height = elm[0].scrollHeight + 1 + 'px';
          }
        };
        scope.$watch(
          function () {
            return elm[0].clientHeight;
          },
          adjust_height
        );
      }
    };
  });
