'use strict';

angular.module('TrustNoOneApp')
  .service('TNOCrypto', [
    '$log',
    '$q',
    '$timeout',
    'EntropyService',
    function ($log,
              $q,
              $timeout,
              EntropyService) {
      this.iv_length = 32;
      this.salt_length = 32;
      this.adata_length = 16;
      this.key_length = 32;
      this.pbkdf2_iterations = 30000;

      this.get_server_entropy = function () {
        var self = this,
            randomness = null;

        return EntropyService
          .get({
            bytes: this.iv_length + this.salt_length + this.adata_length
          }).$promise
          .then(function (entropy) {
            randomness = forge.util.decode64(entropy.entropy);

            return {
              'iv'   : randomness.substring(0, self.iv_length),
              'salt' : randomness.substring(self.iv_length,
                self.iv_length + self.salt_length),
              'adata': randomness.substring(self.iv_length + self.salt_length)
            };
          },
          function () {
            return 'could not get server randomness sample';
          });
      };

      this.get_client_entropy = function () {
        var self = this,
            deferred = $q.defer();

        $timeout(function () {
          deferred.resolve({
            'iv'   : forge.random.getBytesSync(self.iv_length),
            'salt' : forge.random.getBytesSync(self.salt_length),
            'adata': forge.random.getBytesSync(self.adata_length)
          });
        });

        return deferred.promise;
      };

      this.get_entropy = function () {
        var self = this;

        return $q
          .all([this.get_client_entropy(), this.get_server_entropy()])
          .then(function (data) {
            var client = data[0],
                server = data[1];
            return {
              'iv'   : forge.util.xorBytes(client.iv, server.iv, self.iv_length),
              'salt' : forge.util.xorBytes(client.salt, server.salt, self.salt_length),
              'adata': forge.util.xorBytes(client.adata, server.adata, self.adata_length)
            };
          });
      };

      this.compute_key = function (password, salt) {
        return forge.pkcs5.pbkdf2(
          forge.util.encode64(password),
          salt,
          this.pbkdf2_iterations,
          this.key_length,
          forge.md.sha256.create()
        );
      };

      this.encrypt = function (variables, password, plaintext) {
        var key = this.compute_key(password, variables.salt),
            cipher = forge.cipher.createCipher('AES-GCM', key);

        cipher.start({
          iv            : variables.iv,
          additionalData: variables.adata,
          tagLength     : this.adata_length * 8
        });
        cipher.update(forge.util.createBuffer(plaintext));
        cipher.finish();

        var encrypted = cipher.output.data,
            tag = cipher.mode.tag.data;

        return {
          'ciphertext'     : encrypted,
          'tag'            : tag,
          'iv'             : variables.iv,
          'salt'           : variables.salt,
          'associated_data': variables.adata
        }
      };

      this.decrypt = function (variables, password) {
        var key = this.compute_key(password, variables.salt),
            decipher = forge.cipher.createDecipher('AES-GCM', key);
        //variables.tag[0] = 'a';
        decipher.start({
          iv            : variables.iv,
          additionalData: variables.adata,
          tagLength     : this.adata_length * 8,
          tag           : variables.tag
        });
        decipher.update(forge.util.createBuffer(variables.ciphertext));
        var pass = decipher.finish();
        // pass is false if there was a failure (eg: authentication tag didn't match)
        if (pass === false) {
          return null;
        }

        return decipher.output.toString();
      };

      this.encode = function (data) {
        var encoded = {};
        angular.forEach(data, function (value, key) {
          encoded[key] = forge.util.encode64(value);
        });
        return encoded;
      };

      this.decode = function (data) {
        var decoded = {};
        angular.forEach(data, function (value, key) {
          decoded[key] = forge.util.decode64(value);
        });
        return decoded;
      };

    }
  ]);
